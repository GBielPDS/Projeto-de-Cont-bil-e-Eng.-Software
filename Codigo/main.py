from bancoDeDados.bd import Banco_Dados
from janelas.home import Home_janela

bd = Banco_Dados("empresa.db")

home = Home_janela()
home.mainloop()
