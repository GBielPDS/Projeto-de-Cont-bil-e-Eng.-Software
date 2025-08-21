import tkinter as tk
from tkinter import ttk, messagebox
from theme import *
from banco import conectar
from utils import registrar_historico

class FuncionariosView:
    def __init__(self, app):
        self.app = app

    def render(self):
        if self.app.usuario["perfil"] not in ("Administrador","Gerente"):
            messagebox.showwarning("Acesso negado","Somente Gerente/Administrador.")
            return

        self.app.clear()
        tk.Label(self.app.content, text="Funcionários / Acesso", font=FONT_TITLE, bg=BG, fg=DARK).pack(pady=8)

        top = tk.Frame(self.app.content, bg=BG); top.pack(fill="x")
        tk.Button(top, text="Novo", bg=SUCCESS, fg="white", command=self._novo).pack(side="left", padx=6, pady=6)
        tk.Button(top, text="Editar", command=self._editar).pack(side="left", padx=6)
        tk.Button(top, text="Desativar", bg=DANGER, fg="white", command=self._desativar).pack(side="left", padx=6)

        cols=("ID","Nome","Usuário","Perfil","Ativo")
        self.tree = ttk.Treeview(self.app.content, columns=cols, show="headings")
        for c in cols: self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

        self._carregar()

    def _carregar(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        con = conectar(); cur = con.cursor()
        cur.execute("SELECT id, nome, usuario, perfil, ativo FROM usuarios ORDER BY id DESC")
        for r in cur.fetchall(): self.tree.insert("", tk.END, values=r)
        con.close()

    def _novo(self):
        self._form()

    def _editar(self):
        sel = self._sel()
        if not sel: return
        self._form(self.tree.item(sel,"values"))

    def _form(self, dados=None):
        win = tk.Toplevel(self.app.root); win.title("Usuário")
        labs = ["Nome","Usuário","Senha","Perfil (Administrador/Gerente/Operador/Estoquista)"]
        ents=[]
        for i,l in enumerate(labs):
            tk.Label(win, text=l).grid(row=i, column=0, padx=6, pady=4, sticky="e")
            e = tk.Entry(win, width=30)
            e.grid(row=i, column=1, padx=6, pady=4)
            ents.append(e)

        if dados:
            _id, nome, usuario, perfil, ativo = dados
            vals = [nome, usuario, "", perfil]
            for i,v in enumerate(vals): ents[i].insert(0, v)

        def salvar():
            nome, usuario, senha, perfil = [e.get().strip() for e in ents]
            if not nome or not usuario or (not dados and not senha):
                messagebox.showerror("Erro","Preencha os campos."); return
            con = conectar(); cur = con.cursor()
            if dados:
                uid = int(dados[0])
                if senha:
                    cur.execute("UPDATE usuarios SET nome=%s, usuario=%s, senha=%s, perfil=%s WHERE id=%s",
                                (nome, usuario, senha, perfil, uid))
                else:
                    cur.execute("UPDATE usuarios SET nome=%s, usuario=%s, perfil=%s WHERE id=%s",
                                (nome, usuario, perfil, uid))
                registrar_historico(self.app.usuario["usuario"], f"Editou usuário {uid}")
            else:
                cur.execute("INSERT INTO usuarios (nome, usuario, senha, perfil) VALUES (%s,%s,%s,%s)",
                            (nome, usuario, senha, perfil or "Operador"))
                registrar_historico(self.app.usuario["usuario"], f"Cadastrou usuário {usuario}")
            con.commit(); con.close(); win.destroy(); self._carregar()

        tk.Button(win, text="Salvar", bg=PRIMARY, fg="white", command=salvar).grid(row=len(labs), column=0, columnspan=2, pady=8)

    def _desativar(self):
        sel = self._sel()
        if not sel: return
        uid = int(self.tree.item(sel,"values")[0])
        con = conectar(); cur = con.cursor()
        cur.execute("UPDATE usuarios SET ativo=0 WHERE id=%s", (uid,))
        con.commit(); con.close()
        registrar_historico(self.app.usuario["usuario"], f"Desativou usuário {uid}")
        self._carregar()

    def _sel(self):
        s = self.tree.selection()
        if not s:
            messagebox.showwarning("Selecione","Escolha um usuário.")
            return None
        return s[0]
