import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Codigo.bancoDeDados.bd import Banco_Dados

class Gerente():
    def __init__(self, matricula="0000"):
        self.matricula = matricula

    def cadastrar_produto(nome, descricao, preco, estoque=0):
        banco = Banco_Dados()
        banco.novo_produto(nome, descricao, preco, estoque)

    def buscar_produto():
        pass

    def editar_produto():
        pass

    def cadastrar_funcionario():
        pass

    def buscar_funcionario():
        pass

    def editar_funionario():
        pass

    def gerar_relatorio():
        pass
    