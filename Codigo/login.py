import tkinter as tk
from tkinter import messagebox
from banco import conectar
from theme import *
from dashboard import Dashboard
from notificacoes import Notificacoes
from estoque import EstoqueView
from caixa import CaixaView
from devolucoes import DevolucaoTrocaView
from relatorios import RelatoriosView
from funcionarios import FuncionariosView
from backups import BackupView
from clientes import ClientesView

class AppShell:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario  
        self.root.title("Gestor360")
        self.root.config(bg=BG)
        self._montar_layout()
        self._carregar_boas_vindas()

    def _montar_layout(self):
        self.sidebar = tk.Frame(self.root, bg=DARK, width=230)
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self.root, bg=BG)
        self.content.pack(side="right", fill="both", expand=True)

        tk.Label(self.sidebar, text=f"Gestor360\n{self.usuario['perfil']}",
                 bg=DARK, fg="white", font=FONT_SUB, pady=16).pack(fill="x")

        self._btn("Painel", lambda: Dashboard(self).render())
        self._btn("Notificações", lambda: Notificacoes(self).render())
        self._btn("Estoque", lambda: EstoqueView(self).render())
        self._btn("Caixa / Vendas", lambda: CaixaView(self).render())
        self._btn("Devoluções / Trocas", lambda: DevolucaoTrocaView(self).render())
        self._btn("Relatórios", lambda: RelatoriosView(self).render())
        self._btn("Clientes / Contas", lambda: ClientesView(self).render())

        if self.usuario["perfil"] in ("Administrador","Gerente"):
            self._btn("Funcionários", lambda: FuncionariosView(self).render())
        if self.usuario["perfil"] == "Administrador":
            self._btn("Backups", lambda: BackupView(self).render())

        tk.Button(self.sidebar, text="Sair", bg=DANGER, fg="white",
                  command=self.root.destroy, relief="flat").pack(side="bottom", fill="x", pady=8, padx=8)

    def _btn(self, text, cmd):
        tk.Button(self.sidebar, text=text, bg=PRIMARY, fg="white",
                  relief="flat", font=FONT, command=cmd).pack(fill="x", padx=8, pady=4)

    def clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _carregar_boas_vindas(self):
        self.clear()
        tk.Label(self.content, text="🛍️ Bem-vindo ao Gestor360",
                 bg=BG, fg=DARK, font=FONT_TITLE).pack(pady=16)
        frase = "Controle total do seu estoque e caixa em um só lugar.\nOrganize, analise e cresça com inteligência!"
        tk.Label(self.content, text=frase, bg=BG, fg=TEXT, font=FONT).pack(pady=6)

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1080x680")
        self.root.config(bg=BG)
        self._build()

    def _build(self):
        card = tk.Frame(self.root, bg="white", padx=24, pady=24)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="Gestor360", font=FONT_TITLE, bg="white", fg=DARK).grid(row=0, column=0, columnspan=2, pady=(0,12))
        tk.Label(card, text="Usuário:", bg="white", font=FONT).grid(row=1, column=0, sticky="e", pady=4, padx=6)
        tk.Label(card, text="Senha:", bg="white", font=FONT).grid(row=2, column=0, sticky="e", pady=4, padx=6)

        self.e_user = tk.Entry(card, font=FONT)
        self.e_pass = tk.Entry(card, font=FONT, show="*")
        self.e_user.grid(row=1, column=1, pady=4)
        self.e_pass.grid(row=2, column=1, pady=4)

        tk.Button(card, text="Entrar", bg=SUCCESS, fg="white", font=FONT,
                  command=self._login).grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

    def _login(self):
        u = self.e_user.get().strip()
        s = self.e_pass.get().strip()
        if not u or not s:
            messagebox.showerror("Erro", "Informe usuário e senha.")
            return
        con = conectar()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuarios WHERE usuario=%s AND senha=%s AND ativo=1", (u, s))
        row = cur.fetchone()
        con.close()
        if row:
            AppShell(self.root, {"id":row["id"],"nome":row["nome"],"usuario":row["usuario"],"perfil":row["perfil"]})
        else:
            messagebox.showerror("Falha", "Credenciais inválidas.")
