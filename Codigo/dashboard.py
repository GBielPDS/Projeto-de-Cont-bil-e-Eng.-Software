import tkinter as tk
from theme import *
from banco import conectar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from utils import fmt_moeda

class Dashboard:
    def __init__(self, app):
        self.app = app

    def render(self):
        self.app.clear()
        tk.Label(self.app.content, text="Painel Financeiro", font=FONT_TITLE, bg=BG, fg=DARK).pack(pady=10)

        cards = tk.Frame(self.app.content, bg=BG)
        cards.pack(pady=6)

        total_vendas, total_saidas, saldo = self._kpis()

        self._card(cards, "Faturamento", fmt_moeda(total_vendas), SUCCESS).grid(row=0, column=0, padx=8, pady=6)
        self._card(cards, "Despesas", fmt_moeda(total_saidas), DANGER).grid(row=0, column=1, padx=8, pady=6)
        self._card(cards, "Saldo", fmt_moeda(saldo), PRIMARY).grid(row=0, column=2, padx=8, pady=6)

        fig = Figure(figsize=(6.4, 3.2), dpi=100)
        ax = fig.add_subplot(111)
        dias, valores = self._vendas_ultimos_dias()
        ax.bar(dias, valores)  
        ax.set_title("Vendas – últimos 7 dias")
        ax.set_ylabel("R$")

        canvas = FigureCanvasTkAgg(fig, master=self.app.content)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    def _kpis(self):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT COALESCE(SUM(total),0) FROM vendas")
        vendas = float(cur.fetchone()[0] or 0)
        cur.execute("SELECT COALESCE(SUM(valor),0) FROM caixa WHERE tipo='saida'")
        saidas = float(cur.fetchone()[0] or 0)
        con.close()
        return vendas, saidas, vendas - saidas

    def _vendas_ultimos_dias(self):
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            SELECT DATE(data_venda) d, COALESCE(SUM(total),0) v
            FROM vendas
            GROUP BY DATE(data_venda)
            ORDER BY d DESC LIMIT 7
        """)
        rows = cur.fetchall()
        con.close()
        rows = rows[::-1]
        dias = [str(r[0]) for r in rows]
        valores = [float(r[1]) for r in rows]
        return dias, valores

    def _card(self, parent, titulo, valor, color):
        f = tk.Frame(parent, bg="white", padx=18, pady=14, bd=0, highlightthickness=0)
        tk.Label(f, text=titulo, font=FONT_SUB, bg="white", fg=color).pack(anchor="w")
        tk.Label(f, text=valor, font=("Arial", 16, "bold"), bg="white", fg=DARK).pack(anchor="w")
        return f
