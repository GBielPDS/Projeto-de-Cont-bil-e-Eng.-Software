
import tkinter as tk
from tkinter import ttk, messagebox
from theme import *
from banco import conectar

class ClientesView:
    def __init__(self, app):
        self.app = app

    def render(self):
        self.app.clear()
        tk.Label(self.app.content, text="Clientes / Contas a Receber", font=FONT_TITLE, bg=BG, fg=DARK).pack(pady=8)

        tabs = ttk.Notebook(self.app.content)
        tabs.pack(fill="both", expand=True, padx=6, pady=6)

        f1 = tk.Frame(tabs, bg=BG); tabs.add(f1, text="Clientes")
        f2 = tk.Frame(tabs, bg=BG); tabs.add(f2, text="Contas a Receber")

        tk.Button(f1, text="Novo Cliente", bg=SUCCESS, fg="white", command=self._novo_cliente).pack(anchor="w", padx=6, pady=6)
        cols=("ID","Nome","CPF/CNPJ","Telefone","Email")
        self.tree_cli = ttk.Treeview(f1, columns=cols, show="headings")
        for c in cols: self.tree_cli.heading(c, text=c)
        self.tree_cli.pack(fill="both", expand=True, padx=6, pady=6)
        self._load_cli()

        top = tk.Frame(f2, bg=BG); top.pack(fill="x")
        tk.Button(top, text="Marcar como Pago", bg=PRIMARY, fg="white", command=self._pagar).pack(side="left", padx=6, pady=6)

        cols2=("ID","Cliente","Venda","Valor","Vencimento","Status")
        self.tree_cr = ttk.Treeview(f2, columns=cols2, show="headings")
        for c in cols2: self.tree_cr.heading(c, text=c)
        self.tree_cr.pack(fill="both", expand=True, padx=6, pady=6)
        self._load_cr()

    def _novo_cliente(self):
        win = tk.Toplevel(self.app.root); win.title("Cliente")
        labs=["Nome","CPF/CNPJ","Telefone","Email"]; ents=[]
        for i,l in enumerate(labs):
            tk.Label(win, text=l).grid(row=i, column=0, padx=6, pady=4, sticky="e")
            e=tk.Entry(win, width=32); e.grid(row=i, column=1, padx=6, pady=4); ents.append(e)

        def salvar():
            vals=[e.get().strip() for e in ents]
            con=conectar(); cur=con.cursor()
            cur.execute("INSERT INTO clientes (nome, cpf_cnpj, telefone, email) VALUES (%s,%s,%s,%s)", tuple(vals))
            con.commit(); con.close(); win.destroy(); self._load_cli()

        tk.Button(win, text="Salvar", bg=SUCCESS, fg="white", command=salvar).grid(row=len(labs), column=0, columnspan=2, pady=8)

    def _load_cli(self):
        for i in self.tree_cli.get_children(): self.tree_cli.delete(i)
        con=conectar(); cur=con.cursor()
        cur.execute("SELECT id, nome, COALESCE(cpf_cnpj,''), COALESCE(telefone,''), COALESCE(email,'') FROM clientes ORDER BY id DESC")
        for r in cur.fetchall(): self.tree_cli.insert("", tk.END, values=r)
        con.close()

    def _load_cr(self):
        for i in self.tree_cr.get_children(): self.tree_cr.delete(i)
        con=conectar(); cur=con.cursor()
        cur.execute("""
            SELECT cr.id, c.nome, COALESCE(cr.id_venda,''), cr.valor_total, cr.data_vencimento, cr.status
            FROM contas_receber cr JOIN clientes c ON c.id=cr.cliente_id
            ORDER BY cr.data_vencimento
        """)
        for r in cur.fetchall(): self.tree_cr.insert("", tk.END, values=r)
        con.close()

    def _pagar(self):
        sel = self.tree_cr.selection()
        if not sel: return
        cid = int(self.tree_cr.item(sel[0], "values")[0])
        con=conectar(); cur=con.cursor()
        cur.execute("UPDATE contas_receber SET status='Pago', recebido_em=NOW() WHERE id=%s", (cid,))
        con.commit(); con.close()
        self._load_cr()
        messagebox.showinfo("OK","Conta marcada como paga.")
