import tkinter as tk
from tkinter import messagebox
from theme import *
from banco import conectar
from datetime import date, timedelta
from utils import registrar_historico

class Notificacoes:
    def __init__(self, app):
        self.app = app

    def render(self):
        self.app.clear()
        tk.Label(self.app.content, text="Notificações", font=FONT_TITLE, bg=BG, fg=DARK).pack(pady=10)

        frame = tk.Frame(self.app.content, bg=BG)
        frame.pack(fill="both", expand=True)

        btn = tk.Button(frame, text="Verificar agora", bg=PRIMARY, fg="white",
                        command=self._verificar)
        btn.pack(anchor="w", padx=6, pady=6)

        self.lista = tk.Listbox(frame, height=16)
        self.lista.pack(fill="both", expand=True, padx=6, pady=6)

        self._carregar_registradas()

    def _carregar_registradas(self):
        self.lista.delete(0, tk.END)
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT criado_em, tipo, mensagem FROM notificacoes ORDER BY id DESC LIMIT 100")
        for dt, tipo, msg in cur.fetchall():
            self.lista.insert(tk.END, f"[{dt}] {tipo}: {msg}")
        con.close()

    def _verificar(self):
        hoje = date.today()
        alerta = hoje + timedelta(days=7)
        msgs = []

        con = conectar()
        cur = con.cursor()

        cur.execute("SELECT nome, quantidade FROM produtos WHERE quantidade <= 5")
        for nome, qtd in cur.fetchall():
            msgs.append(("baixa_estoque", f"{nome} com {qtd} un. em estoque"))

        cur.execute("SELECT nome, validade FROM produtos WHERE validade IS NOT NULL AND validade <= %s", (alerta,))
        for nome, val in cur.fetchall():
            msgs.append(("vencimento", f"{nome} vence em {val}"))

        for tipo, m in msgs:
            cur.execute("INSERT INTO notificacoes (tipo, mensagem) VALUES (%s,%s)", (tipo, m))
        con.commit()
        con.close()

        if msgs:
            messagebox.showwarning("Avisos do sistema", "\n".join([m for _, m in msgs]))
            registrar_historico(self.app.usuario["usuario"], f"Gerou {len(msgs)} notificações")
        else:
            messagebox.showinfo("Tudo certo", "Nenhuma notificação no momento.")

        self._carregar_registradas()
