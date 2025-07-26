import customtkinter as ctk
from tkinter import *

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

        self.button_estoque = ctk.CTkButton(self, text="Abrir Estoque", command=self.open_estoque)
        self.button_estoque.pack(pady=10)

        self.button_funcionarios = ctk.CTkButton(self, text="Gerenciar Funcionários", command=self.open_funcionarios)
        self.button_funcionarios.pack(pady=10)

    def open_funcionarios(self):
        print("Abrindo janela de funcionários...")

    def open_produtos(self):
        print("Abrindo janela de produtos...")

    def open_estoque(self):
        print("Abrindo janela de estoque...")
