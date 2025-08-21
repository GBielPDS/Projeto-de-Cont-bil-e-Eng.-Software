import tkinter as tk
from tkinter import filedialog, messagebox
from theme import *
from utils import registrar_historico
import os

class BackupView:
    def __init__(self, app):
        self.app = app

    def render(self):
        if self.app.usuario["perfil"] != "Administrador":
            messagebox.showwarning("Acesso negado","Somente Administrador.")
            return
        self.app.clear()
        tk.Label(self.app.content, text="Backups do Banco", font=FONT_TITLE, bg=BG, fg=DARK).pack(pady=8)
        tk.Button(self.app.content, text="Gerar Backup (mysqldump)", bg=PRIMARY, fg="white",
                  command=self._backup).pack(pady=10)

    def _backup(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".sql", initialfile="backup_gestor360.sql")
        if not caminho: return
        
        cmd = f'mysqldump -u root -p{os.environ.get("MYSQL_PWD","sua_senha_mysql")} gestor360 > "{caminho}"'
        ret = os.system(cmd)
        if ret == 0:
            registrar_historico(self.app.usuario["usuario"], "Backup gerado")
            messagebox.showinfo("OK","Backup criado com sucesso.")
        else:
            messagebox.showerror("Erro","Falha ao executar mysqldump. Verifique PATH e senha.")
