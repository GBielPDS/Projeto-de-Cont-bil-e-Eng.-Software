import tkinter as tk
from tkinter import ttk, messagebox
from theme import *
from banco import conectar
from utils import registrar_historico, confirmar
from datetime import datetime

class EstoqueView:
    def __init__(self, app):
        self.app = app

    def render(self):
        self.app.clear()
        tk.Label(self.app.content, text="Estoque / Produtos", font=FONT_TITLE, bg=BG, fg=DARK).pack(pady=8)

        top = tk.Frame(self.app.content, bg=BG)
        top.pack(fill="x")

        self.busca = tk.Entry(top, font=FONT)
        self.busca.pack(side="left", padx=6, pady=6)
        tk.Button(top, text="Buscar", bg=PRIMARY, fg="white", command=self._buscar).pack(side="left", padx=4)
        tk.Button(top, text="Novo Produto", bg=SUCCESS, fg="white", command=self._novo).pack(side="left", padx=4)

        cols = ("ID","Nome","Cód. Barras","Categoria","Validade","Preço","Qtd")
        self.tree = ttk.Treeview(self.app.content, columns=cols, show="headings")
        for c in cols: self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

        btbar = tk.Frame(self.app.content, bg=BG)
        btbar.pack(fill="x")
        tk.Button(btbar, text="Entrada", bg=SUCCESS, fg="white", command=lambda: self._mov('entrada')).pack(side="left", padx=4, pady=4)
        tk.Button(btbar, text="Saída", bg=DANGER, fg="white", command=lambda: self._mov('saida')).pack(side="left", padx=4, pady=4)
        tk.Button(btbar, text="Editar", command=self._editar).pack(side="left", padx=4, pady=4)
        tk.Button(btbar, text="Remover", command=self._remover).pack(side="left", padx=4, pady=4)
        tk.Button(btbar, text="Histórico", command=self._historico).pack(side="left", padx=4, pady=4)

        self._carregar()

    def _carregar(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT id, nome, COALESCE(codigo_barras,''), COALESCE(categoria,''), COALESCE(validade,''), preco, quantidade FROM produtos ORDER BY id DESC")
        for row in cur.fetchall():
            self.tree.insert("", tk.END, values=row)
        con.close()

    def _buscar(self):
        termo = f"%{self.busca.get().strip()}%"
        for i in self.tree.get_children(): self.tree.delete(i)
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            SELECT id, nome, COALESCE(codigo_barras,''), COALESCE(categoria,''), COALESCE(validade,''), preco, quantidade
            FROM produtos
            WHERE nome LIKE %s OR categoria LIKE %s OR codigo_barras LIKE %s
            ORDER BY nome
        """, (termo, termo, termo))
        for row in cur.fetchall():
            self.tree.insert("", tk.END, values=row)
        con.close()

    def _novo(self):
        self._form_produto()

    def _editar(self):
        sel = self._selecionado()
        if not sel: return
        self._form_produto(sel)

    def _form_produto(self, dados=None):
        win = tk.Toplevel(self.app.root)
        win.title("Produto")
        labels = ["Nome","Cód. Barras","Categoria","Validade (YYYY-MM-DD)","Preço","Quantidade"]
        ents = []
        for i,l in enumerate(labels):
            tk.Label(win, text=l).grid(row=i, column=0, sticky="e", padx=6, pady=4)
            e = tk.Entry(win, width=30)
            e.grid(row=i, column=1, padx=6, pady=4)
            ents.append(e)

        if dados:
            pid, nome, cb, cat, val, preco, qtd = self.tree.item(dados, "values")
            vals = [nome, cb, cat, val, preco, qtd]
            for i,v in enumerate(vals): ents[i].insert(0, v)

        def salvar():
            nome, cb, cat, val, preco, qtd = [e.get().strip() for e in ents]
            try:
                preco = float(preco or 0)
                qtd = int(qtd or 0)
            except: 
                messagebox.showerror("Erro","Preço/Qtd inválidos."); return
            con = conectar()
            cur = con.cursor()
            if dados:
                pid = int(self.tree.item(dados,"values")[0])
                cur.execute("""
                    UPDATE produtos SET nome=%s, codigo_barras=%s, categoria=%s, validade=%s, preco=%s, quantidade=%s
                    WHERE id=%s
                """, (nome, cb or None, cat or None, val or None, preco, qtd, pid))
                registrar_historico(self.app.usuario["usuario"], f"Editou produto {pid}")
            else:
                cur.execute("""
                    INSERT INTO produtos (nome, codigo_barras, categoria, validade, preco, quantidade)
                    VALUES (%s,%s,%s,%s,%s,%s)
                """, (nome, cb or None, cat or None, val or None, preco, qtd))
                registrar_historico(self.app.usuario["usuario"], f"Cadastrou produto {nome}")
            con.commit()
            con.close()
            win.destroy()
            self._carregar()

        tk.Button(win, text="Salvar", bg=SUCCESS, fg="white", command=salvar).grid(row=len(labels), column=0, columnspan=2, pady=8)

    def _mov(self, tipo):
        sel = self._selecionado()
        if not sel: return
        pid = int(self.tree.item(sel, "values")[0])

        win = tk.Toplevel(self.app.root); win.title(f"{tipo.title()} de Estoque")
        tk.Label(win, text="Quantidade:").grid(row=0, column=0, padx=6, pady=6)
        e_q = tk.Entry(win, width=10); e_q.grid(row=0, column=1, padx=6, pady=6)
        tk.Label(win, text="Motivo:").grid(row=1, column=0, padx=6, pady=6)
        e_m = tk.Entry(win, width=30); e_m.grid(row=1, column=1, padx=6, pady=6)

        def salvar():
            try:
                q = int(e_q.get())
                if q <= 0: raise ValueError
            except: messagebox.showerror("Erro","Quantidade inválida."); return

            con = conectar()
            cur = con.cursor()
            if tipo == 'entrada':
                cur.execute("UPDATE produtos SET quantidade = quantidade + %s WHERE id=%s", (q, pid))
            else:
                
                cur.execute("SELECT quantidade FROM produtos WHERE id=%s", (pid,))
                atual = int(cur.fetchone()[0])
                if q > atual:
                    messagebox.showerror("Erro", "Estoque insuficiente."); con.close(); return
                cur.execute("UPDATE produtos SET quantidade = quantidade - %s WHERE id=%s", (q, pid))

            cur.execute("""
                INSERT INTO movimentacoes_estoque (id_produto, quantidade, tipo, motivo)
                VALUES (%s,%s,%s,%s)
            """, (pid, q, tipo, e_m.get().strip() or tipo))
            con.commit(); con.close()
            registrar_historico(self.app.usuario["usuario"], f"{tipo} de {q} un. no produto {pid}")
            win.destroy(); self._carregar()

        tk.Button(win, text="Confirmar", bg=PRIMARY, fg="white", command=salvar).grid(row=2, column=0, columnspan=2, pady=8)

    def _remover(self):
        sel = self._selecionado()
        if not sel: return
        pid = int(self.tree.item(sel, "values")[0])
        if not confirmar("Remover produto selecionado?"): return
        con = conectar(); cur = con.cursor()
        cur.execute("DELETE FROM produtos WHERE id=%s", (pid,))
        con.commit(); con.close()
        registrar_historico(self.app.usuario["usuario"], f"Removeu produto {pid}")
        self._carregar()

    def _historico(self):
        sel = self._selecionado()
        if not sel: return
        pid = int(self.tree.item(sel, "values")[0])
        win = tk.Toplevel(self.app.root); win.title("Histórico de Movimentações")
        cols = ("Data","Tipo","Qtd","Motivo")
        tree = ttk.Treeview(win, columns=cols, show="headings")
        for c in cols: tree.heading(c, text=c)
        tree.pack(fill="both", expand=True)
        con = conectar(); cur = con.cursor()
        cur.execute("""
            SELECT data_movimentacao, tipo, quantidade, COALESCE(motivo,'')
            FROM movimentacoes_estoque WHERE id_produto=%s ORDER BY id DESC
        """, (pid,))
        for r in cur.fetchall(): tree.insert("", tk.END, values=r)
        con.close()

    def _selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecione","Escolha um item da lista.")
            return None
        return sel[0]
