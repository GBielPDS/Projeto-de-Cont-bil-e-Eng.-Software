from bancoDeDados.bd import Banco_Dados
from janelas.home import Home_janela

bd = Banco_Dados("empresa.db")
bd.criar_banco()

global app
app = Home_janela()
app.mainloop()
