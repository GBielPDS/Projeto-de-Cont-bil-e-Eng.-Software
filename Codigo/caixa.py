import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from theme import *
from banco import conectar
from utils import registrar_historico, fmt_moeda
from datetime import datetime

class CaixaView:
    def __init__(self, app):
        self.app = app
        self.itens = []
        self.total = 0.0

    def render(self):
        self.app.clear()
        tk.Label(self.app.content, text="Caixa / Registrar Vendas", font=FONT_TITLE, bg=BG, fg=DARK).pack(pady=8)

        top = tk.Frame(self.app.content, bg=BG); top.pack(fill="x")
        tk.Label(top, text="Cód. barras:", bg=BG, font=FONT).pack(side="left", padx=4)
        self.e_cod = tk.Entry(top, font=FONT, width=18); self.e_cod.pack(side="left", padx=4)
        tk.Label(top, text="Qtd:", bg=BG, font=FONT).pack(side="left", padx=4)
        self.e_qtd = tk.Entry(top, font=FONT, width=5); self.e_qtd.insert(0,"1"); self.e_qtd.pack(side="left", padx=4)
        tk.Button(top, text="Adicionar", bg=PRIMARY, fg="white", command=self._add_item).pack(side="left", padx=6)

        cols = ("Produto","Qtd","Preço","Subtotal","id_produto")
        self.tree = ttk.Treeview(self.app.content, columns=cols, show="headings")
        for c in cols[:-1]: self.tree.heading(c, text=c)
        self.tree.column("id_produto", width=0, stretch=False)
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

        bottom = tk.Frame(self.app.content, bg=BG); bottom.pack(fill="x")
        tk.Label(bottom, text="Forma:", bg=BG).pack(side="left", padx=4)
        self.cb_forma = ttk.Combobox(bottom, values=["dinheiro","cartao","pix","fiado"], state="readonly", width=12)
        self.cb_forma.set("dinheiro"); self.cb_forma.pack(side="left")
        tk.Label(bottom, text="Desconto:", bg=BG).pack(side="left", padx=6)
        self.e_desc = tk.Entry(bottom, width=8); self.e_desc.insert(0,"0"); self.e_desc.pack(side="left")
        tk.Button(bottom, text="Remover item", command=self._remover_item).pack(side="left", padx=6)
        tk.Button(bottom, text="Finalizar", bg=SUCCESS, fg="white", command=self._finalizar).pack(side="right", padx=6)

        self.lbl_total = tk.Label(self.app.content, text="Total: R$ 0,00", font=FONT_SUB, bg=BG, fg=DARK)
        self.lbl_total.pack(anchor="e", padx=12)

    def _add_item(self):
        cod = self.e_cod.get().strip()
        try: qtd = int(self.e_qtd.get().strip() or "1")
        except: messagebox.showerror("Erro","Qtd inválida."); return
        if not cod or qtd<=0: messagebox.showerror("Erro","Dados inválidos."); return

        con = conectar(); cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM produtos WHERE codigo_barras=%s", (cod,))
        p = cur.fetchone(); con.close()
        if not p:
            messagebox.showerror("Erro","Produto não encontrado."); return
        if p["quantidade"] < qtd:
            messagebox.showerror("Erro","Estoque insuficiente."); return

        subtotal = float(p["preco"]) * qtd
        self.tree.insert("", tk.END, values=(p["nome"], qtd, fmt_moeda(p["preco"]), fmt_moeda(subtotal), p["id"]))
        self.total += subtotal
        self._atualiza_total()
        self.e_cod.delete(0, tk.END)

    def _remover_item(self):
        sel = self.tree.selection()
        if not sel: return
        subtotal_txt = self.tree.item(sel[0],"values")[3]
        subtotal = float(subtotal_txt.replace("R$ ","").replace(".","").replace(",","."))
        self.total -= subtotal
        self.tree.delete(sel[0])
        self._atualiza_total()

    def _atualiza_total(self):
        self.lbl_total.config(text=f"Total: {fmt_moeda(self.total)}")

    def _finalizar(self):
        itens = [self.tree.item(i,"values") for i in self.tree.get_children()]
        if not itens:
            messagebox.showerror("Erro","Nenhum item."); return
        try:
            desconto = float(self.e_desc.get().replace(",", ".") or 0)
        except: desconto = 0.0

        total = max(0.0, self.total - desconto)
        forma = self.cb_forma.get()

        con = conectar(); cur = con.cursor()
        
        cur.execute("""
            INSERT INTO vendas (id_funcionario, total, forma_pagamento, desconto)
            VALUES (%s,%s,%s,%s)
        """, (self.app.usuario["id"], total, forma, desconto))
        id_venda = cur.lastrowid

        
        for nome, qtd, preco_txt, sub_txt, id_prod in itens:
            qtd = int(qtd)
            cur.execute("SELECT quantidade, preco FROM produtos WHERE id=%s", (id_prod,))
            q_atual, preco = cur.fetchone()
            if qtd>q_atual:
                con.rollback(); con.close()
                messagebox.showerror("Erro","Estoque insuficiente durante a finalização.")
                return
            cur.execute("""
                INSERT INTO itens_venda (id_venda, id_produto, quantidade, preco_unitario)
                VALUES (%s,%s,%s,%s)
            """, (id_venda, id_prod, qtd, preco))
            cur.execute("UPDATE produtos SET quantidade=quantidade-%s WHERE id=%s", (qtd, id_prod))
            cur.execute("""
                INSERT INTO movimentacoes_estoque (id_produto, quantidade, tipo, motivo)
                VALUES (%s,%s,'saida','Venda')
            """, (id_prod, qtd))

        con.commit(); con.close()

        if forma == "fiado":
            self._criar_conta_a_receber(id_venda, total)

        registrar_historico(self.app.usuario["usuario"], f"Venda {id_venda} total {total}")
        self._gerar_comprovante(id_venda, itens, total, desconto, forma)
        messagebox.showinfo("Sucesso", f"Venda {id_venda} registrada.")
        self.render()

    def _criar_conta_a_receber(self, id_venda, total):
        win = tk.Toplevel(self.app.root); win.title("Conta a receber")
        tk.Label(win, text="Cliente (ID):").grid(row=0, column=0, padx=6, pady=6)
        e_cli = tk.Entry(win); e_cli.grid(row=0, column=1, padx=6, pady=6)
        tk.Label(win, text="Vencimento (YYYY-MM-DD):").grid(row=1, column=0, padx=6, pady=6)
        e_venc = tk.Entry(win); e_venc.insert(0, datetime.now().date().isoformat()); e_venc.grid(row=1, column=1, padx=6, pady=6)

        def salvar():
            con = conectar(); cur = con.cursor()
            cur.execute("""
                INSERT INTO contas_receber (cliente_id, id_venda, valor_total, data_vencimento)
                VALUES (%s,%s,%s,%s)
            """, (int(e_cli.get()), id_venda, total, e_venc.get()))
            con.commit(); con.close(); win.destroy()
            messagebox.showinfo("OK","Conta a receber gerada.")

        tk.Button(win, text="Salvar", bg=PRIMARY, fg="white", command=salvar).grid(row=2, column=0, columnspan=2, pady=8)

    def _gerar_comprovante(self, id_venda, itens, total, desconto, forma):
        # comprovante .txt simples (offline)
        arq = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=f"comprovante_{id_venda}.txt")
        if not arq: return
        linhas = []
        linhas.append("GESTOR360 - COMPROVANTE DE VENDA\n")
        linhas.append(f"Venda: {id_venda}  Data: {datetime.now()}\n")
        linhas.append("=====================================\n")
        for nome, qtd, preco_txt, sub_txt, _ in itens:
            linhas.append(f"{nome}  x{qtd}  {preco_txt}  Sub: {sub_txt}\n")
        linhas.append("-------------------------------------\n")
        linhas.append(f"Desconto: {fmt_moeda(desconto)}\n")
        linhas.append(f"Total: {fmt_moeda(total)}\n")
        linhas.append(f"Pagamento: {forma}\n")
        with open(arq, "w", encoding="utf-8") as f:
            f.writelines(linhas)
