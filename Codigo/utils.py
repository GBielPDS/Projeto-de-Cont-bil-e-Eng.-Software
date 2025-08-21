from datetime import datetime
from tkinter import messagebox
from banco import conectar

def registrar_historico(usuario, acao):
    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO historico (usuario, acao) VALUES (%s,%s)", (usuario, acao))
    con.commit()
    con.close()

def fmt_moeda(v):
    return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X",".")

def confirmar(msg):
    return messagebox.askyesno("Confirmação", msg)

def now():
    return datetime.now()
