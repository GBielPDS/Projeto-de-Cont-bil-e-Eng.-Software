import tkinter as tk
from tkinter import ttk, messagebox
from theme import *
from banco import conectar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime

class RelatoriosView:
    def __init__(self, app):
        self.app = app

    def render(self):
        self.app.clear()
        tk.Label(self.app.content, text="Relatórios e Gráficos", font=FONT_TITLE, bg=BG, fg=DARK).pack(pady=8)

        filtros = tk.Frame(self.app.content, bg=BG); filtros.pack()
        tk.Label(filtros, text="Início (YYYY-MM-DD):", bg=BG).grid(row=0, column=0, padx=4, pady=4, sticky="e")
        tk.Label(filtros, text="Fim (YYYY-MM-DD):", bg=BG).grid(row=0, column=2, padx=4, pady=4, sticky="e")
        self.e_ini = tk.Entry(filtros); self.e_ini.grid(row=0, column=1, padx=4)
        self.e_fim = tk.Entry(filtros); self.e_fim.grid(row=0, column=3, padx=4)
        tk.Button(filtros, text="Gerar", bg=PRIMARY, fg="white", command=self._gerar).grid(row=0, column=4, padx=6)

        self.frame_graf = tk.Frame(self.app.content, bg=BG); self.frame_graf.pack(fill="both", expand=True, padx=8, pady=8)

    def _gerar(self):
        ini, fim = self.e_ini.get().strip(), self.e_fim.get().strip()
        try:
            di = datetime.strptime(ini, "%Y-%m-%d")
            df = datetime.strptime(fim, "%Y-%m-%d")
            if di>df: raise ValueError
        except:
            messagebox.showerror("Erro", "Datas inválidas."); return

        for w in self.frame_graf.winfo_children(): w.destroy()

        con = conectar(); cur = con.cursor()
        cur.execute("""
            SELECT p.nome, SUM(iv.quantidade) qtd, SUM(iv.quantidade*iv.preco_unitario) fat
            FROM itens_venda iv
            JOIN vendas v ON v.id=iv.id_venda
            JOIN produtos p ON p.id=iv.id_produto
            WHERE v.data_venda BETWEEN %s AND %s
            GROUP BY p.nome
            ORDER BY qtd DESC
        """, (ini+" 00:00:00", fim+" 23:59:59"))
        rows = cur.fetchall()

        nomes = [r[0] for r in rows]
        qts = [int(r[1]) for r in rows]
        fats = [float(r[2]) for r in rows]

        fig = Figure(figsize=(6.4, 3.2), dpi=100); ax = fig.add_subplot(111)
        if nomes: ax.bar(nomes, qts)
        ax.set_title("Produtos mais vendidos (Qtd)")
        ax.tick_params(axis='x', labelrotation=45)
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graf); canvas.draw(); canvas.get_tk_widget().pack(pady=6)

        fig2 = Figure(figsize=(6.4, 3.2), dpi=100); ax2 = fig2.add_subplot(111)
        if nomes: ax2.bar(nomes, fats)
        ax2.set_title("Faturamento por produto (R$)")
        ax2.tick_params(axis='x', labelrotation=45)
        canvas2 = FigureCanvasTkAgg(fig2, master=self.frame_graf); canvas2.draw(); canvas2.get_tk_widget().pack(pady=6)

        con.close()

        self._dre(ini, fim)

    def _dre(self, ini, fim):
        con = conectar(); cur = con.cursor()
        cur.execute("SELECT COALESCE(SUM(total),0) FROM vendas WHERE data_venda BETWEEN %s AND %s", (ini+" 00:00:00", fim+" 23:59:59"))
        receitas = float(cur.fetchone()[0] or 0)
        cur.execute("SELECT COALESCE(SUM(valor),0) FROM caixa WHERE tipo='saida' AND data_lcto BETWEEN %s AND %s", (ini+" 00:00:00", fim+" 23:59:59"))
        despesas = float(cur.fetchone()[0] or 0)
        con.close()
        lucro = receitas - despesas

        card = tk.Frame(self.frame_graf, bg="white", padx=14, pady=10)
        card.pack(fill="x", pady=8)
        tk.Label(card, text="DRE (Período)", font=FONT_SUB, bg="white", fg=DARK).pack(anchor="w")
        tk.Label(card, text=f"Receitas: R$ {receitas:,.2f}".replace(",", "X").replace(".", ",").replace("X","."), bg="white").pack(anchor="w")
        tk.Label(card, text=f"Despesas: R$ {despesas:,.2f}".replace(",", "X").replace(".", ",").replace("X","."), bg="white").pack(anchor="w")
        tk.Label(card, text=f"Resultado: R$ {lucro:,.2f}".replace(",", "X").replace(".", ",").replace("X","."), bg="white", fg=(SUCCESS if lucro>=0 else DANGER)).pack(anchor="w")
