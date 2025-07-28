import customtkinter as ctk
from tkinter import *
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Codigo.janelas.produtos_janela import Produto_janela  
from Codigo.janelas.funcionario_janela import Funcionario
from Codigo.janelas.vendas_janela import Venda_janela

class Home_janela(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento")
        ctk.set_appearance_mode("dark")
        self.geometry("720x600")
        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Bem-vindo ao sistema de gerenciamento!")
        self.label.pack(pady=20)

        self.button_produtos = ctk.CTkButton(self, text="Gerenciar Produtos", command=self.open_produtos)
        self.button_produtos.pack(pady=10)

        self.button_vendas = ctk.CTkButton(self, text="Realizar Venda", command=self.open_vendas)
        self.button_vendas.pack(pady=10)

        self.button_funcionarios = ctk.CTkButton(self, text="Gerenciar Funcionários", command=self.open_funcionarios)
        self.button_funcionarios.pack(pady=10)

    def open_funcionarios(self):
        global app
        self.after(100, self.destroy)
        app = Funcionario()
        app.mainloop()

    def open_produtos(self):
        global app
        self.after(100, self.destroy)
        app = Produto_janela()
        app.mainloop()

    def open_vendas(self):
        global app
        self.after(100, self.destroy)
        app = Venda_janela()
        app.mainloop()
