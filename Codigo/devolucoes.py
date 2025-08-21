import tkinter as tk
from tkinter import ttk, messagebox
from theme import *
from banco import conectar
from utils import registrar_historico

class DevolucaoTrocaView:
    def __init__(self, app):
        self.app = app

    def render(self):
        self.app.clear()
        tk.Label(self.app.content, text="Devoluções e Trocas", font=FONT_TITLE, bg=BG, fg=DARK).pack(pady=8)

        top = tk.Frame(self.app.content, bg=BG); top.pack(fill="x")
        tk.Label(top, text="ID da Venda:", bg=BG).pack(side="left", padx=4)
        self.e_venda = tk.Entry(top, width=10); self.e_venda.pack(side="left", padx=4)
        tk.Button(top, text="Buscar", bg=PRIMARY, fg="white", command=self._buscar).pack(side="left", padx=4)

        cols = ("ItemID","Produto","Qtd","Preço","ProdutoID")
        self.tree = ttk.Treeview(self.app.content, columns=cols, show="headings")
        for c in cols[:-1]: self.tree.heading(c, text=c)
        self.tree.column("ProdutoID", width=0, stretch=False)
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

        bar = tk.Frame(self.app.content, bg=BG); bar.pack(fill="x")
        tk.Button(bar, text="Registrar Devolução", bg=DANGER, fg="white", command=self._devolver).pack(side="left", padx=4, pady=4)
        tk.Button(bar, text="Efetuar Troca", bg=SUCCESS, fg="white", command=self._trocar).pack(side="left", padx=4, pady=4)

    def _buscar(self):
        vid = self.e_venda.get().strip()
        if not vid: return
        for i in self.tree.get_children(): self.tree.delete(i)
        con = conectar(); cur = con.cursor()
        cur.execute("""
            SELECT iv.id, p.nome, iv.quantidade, iv.preco_unitario, p.id
            FROM itens_venda iv
            JOIN produtos p ON p.id = iv.id_produto
            WHERE iv.id_venda = %s
        """, (vid,))
        for r in cur.fetchall():
            self.tree.insert("", tk.END, values=r)
        con.close()

    def _devolver(self):
        sel = self.tree.selection()
        if not sel: return
        item_id, nome, qtd, preco, pid = self.tree.item(sel[0],"values")
        win = tk.Toplevel(self.app.root); win.title("Devolução")
        tk.Label(win, text=f"Devolver '{nome}' Qtd (máx {qtd}):").grid(row=0, column=0, padx=6, pady=6)
        e_q = tk.Entry(win); e_q.insert(0, str(qtd)); e_q.grid(row=0, column=1, padx=6, pady=6)
        tk.Label(win, text="Motivo:").grid(row=1, column=0, padx=6, pady=6)
        e_m = tk.Entry(win, width=28); e_m.grid(row=1, column=1, padx=6, pady=6)

        def salvar():
            try:
                q = int(e_q.get()); 
                if q<=0 or q>int(qtd): raise ValueError
            except: messagebox.showerror("Erro","Qtd inválida."); return
            con = conectar(); cur = con.cursor()
            
            cur.execute("UPDATE produtos SET quantidade=quantidade+%s WHERE id=%s", (q, pid))
          
            cur.execute("""
                INSERT INTO devolucoes (id_venda, id_item_venda, id_produto, quantidade, motivo)
                VALUES (%s,%s,%s,%s,%s)
            """, (self.e_venda.get(), item_id, pid, q, e_m.get() or 'Devolução'))
      
            cur.execute("""
                INSERT INTO movimentacoes_estoque (id_produto, quantidade, tipo, motivo)
                VALUES (%s,%s,'devolucao',%s)
            """, (pid, q, 'Devolução'))
            con.commit(); con.close()
            registrar_historico(self.app.usuario["usuario"], f"Devolveu {q} do item {item_id} venda {self.e_venda.get()}")
            win.destroy(); self._buscar()

        tk.Button(win, text="Confirmar", bg=PRIMARY, fg="white", command=salvar).grid(row=2, column=0, columnspan=2, pady=8)

    def _trocar(self):
        sel = self.tree.selection()
        if not sel: return
        item_id, nome, qtd, preco, pid_dev = self.tree.item(sel[0],"values")
        win = tk.Toplevel(self.app.root); win.title("Troca")
        tk.Label(win, text=f"Devolver '{nome}' qtd (máx {qtd}):").grid(row=0, column=0, padx=6, pady=6)
        e_qd = tk.Entry(win); e_qd.insert(0, str(qtd)); e_qd.grid(row=0, column=1, padx=6, pady=6)

        tk.Label(win, text="Produto novo (ID):").grid(row=1, column=0, padx=6, pady=6)
        e_pidn = tk.Entry(win); e_pidn.grid(row=1, column=1, padx=6, pady=6)
        tk.Label(win, text="Qtd nova:").grid(row=2, column=0, padx=6, pady=6)
        e_qn = tk.Entry(win); e_qn.insert(0,"1"); e_qn.grid(row=2, column=1, padx=6, pady=6)

        tk.Label(win, text="Motivo:").grid(row=3, column=0, padx=6, pady=6)
        e_m = tk.Entry(win, width=28); e_m.grid(row=3, column=1, padx=6, pady=6)

        def salvar():
            try:
                qd = int(e_qd.get()); qn = int(e_qn.get()); pid_n = int(e_pidn.get())
                if qd<=0 or qd>int(qtd) or qn<=0: raise ValueError
            except: messagebox.showerror("Erro","Dados inválidos."); return

            con = conectar(); cur = con.cursor()
            
            cur.execute("UPDATE produtos SET quantidade=quantidade+%s WHERE id=%s", (qd, pid_dev))
            cur.execute("""
                INSERT INTO movimentacoes_estoque (id_produto, quantidade, tipo, motivo)
                VALUES (%s,%s,'troca_entrada',%s)
            """, (pid_dev, qd, e_m.get() or 'Troca'))
           
            cur.execute("SELECT quantidade FROM produtos WHERE id=%s", (pid_n,))
            q_atual = cur.fetchone()
            if not q_atual or q_atual[0] < qn:
                con.rollback(); con.close()
                messagebox.showerror("Erro","Estoque insuficiente do produto novo.")
                return
            cur.execute("UPDATE produtos SET quantidade=quantidade-%s WHERE id=%s", (qn, pid_n))
            cur.execute("""
                INSERT INTO movimentacoes_estoque (id_produto, quantidade, tipo, motivo)
                VALUES (%s,%s,'troca_saida',%s)
            """, (pid_n, qn, e_m.get() or 'Troca'))
           
            cur.execute("""
                INSERT INTO trocas (id_venda_original, id_produto_devolvido, qtd_devolvida, id_produto_entregue, qtd_entregue, motivo)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (self.e_venda.get(), pid_dev, qd, pid_n, qn, e_m.get() or 'Troca'))
            con.commit(); con.close()
            registrar_historico(self.app.usuario["usuario"], f"Troca venda {self.e_venda.get()} dev {qd} -> novo {pid_n} x{qn}")
            win.destroy(); self._buscar()

        tk.Button(win, text="Confirmar", bg=PRIMARY, fg="white", command=salvar).grid(row=4, column=0, columnspan=2, pady=8)
