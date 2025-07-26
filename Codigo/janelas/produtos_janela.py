import customtkinter as ctk
from tkinter import *
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Codigo.bancoDeDados.bd import Banco_Dados

class Produto_janela(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento")
        ctk.set_appearance_mode("dark")
        self.geometry("720x600")
        self.create_widgets()
        self.bd = Banco_Dados("empresa.db")

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Bem-vindo ao sistema de gerenciamento!")
        self.label.pack(pady=20)

        self.button_cadastrar = ctk.CTkButton(self, text="Cadastrar Produtos", command=self.cadastrar_produtos)
        self.button_cadastrar.pack(pady=10)

        self.button_editar = ctk.CTkButton(self, text="Editar Produtos", command=self.editar_produtos)
        self.button_editar.pack(pady=10)

        self.button_buscar = ctk.CTkButton(self, text="Buscar Produtos", command=self.buscar_produtos)
        self.button_buscar.pack(pady=10)

        # ------ Frame para entrada de dados do produto ------
        self.frame_produto = ctk.CTkFrame(self)
        self.entry_nome = ctk.CTkEntry(self.frame_produto, placeholder_text="Nome do Produto: ")
        self.entry_preco = ctk.CTkEntry(self.frame_produto, placeholder_text="Preço do Produto: ")
        self.entry_descricao = ctk.CTkEntry(self.frame_produto, placeholder_text="Descrição do Produto: ")
        self.entry_estoque = ctk.CTkEntry(self.frame_produto, placeholder_text="Estoque do Produto: ")

        self.button_salvar = ctk.CTkButton(self.frame_produto, text="Salvar Produto", command=self.salvar_produto)
        self.label_alerta = ctk.CTkLabel(self, text="")
        
    def cadastrar_produtos(self):
        self.frame_produto.pack(pady=10, padx=10, fill="x")
        self.entry_nome.pack(pady=5, padx=10, fill="x")
        self.entry_preco.pack(pady=5, padx=10, fill="x")
        self.entry_descricao.pack(pady=5, padx=10, fill="x")
        self.entry_estoque.pack(pady=5, padx=10, fill="x")
        self.button_salvar.pack(pady=10)
        self.label_alerta.pack(pady=10)

    def editar_produtos(self):
        pass

    def buscar_produtos(self):
        pass

    def salvar_produto(self):

        nome = self.entry_nome.get()
        preco = self.entry_preco.get()
        descricao = self.entry_descricao.get()
        estoque = self.entry_estoque.get()
        print(f"Entrada, nome: {nome}, Preço: {preco}, Descrição: {descricao}, Estoque: {estoque}")

        if not nome or not preco:
            self.label_alerta.configure(text="Nome e preço são obrigatórios.")
        elif not preco.replace(',', '', 1).isdigit() and (not estoque.isdigit() or not estoque):
            self.label_alerta.configure(text="Preço e estoque devem ser numéricos.")
        elif len(preco) < 4 or preco[-3] != ',':
            self.label_alerta.configure(text="Formato de preço inválido. Use vírgula para separar os centavos.")   
        else:
            preco = float(preco.replace(',', '.'))
            if estoque == "":
                estoque = 0
            else:
                estoque = int(estoque)

            self.bd.novo_produto(nome, descricao, preco, estoque)
            print(f"Produto salvo: {nome}, Preço: {preco}, Descrição: {descricao}, Estoque: {estoque}")
            self.label_alerta.configure(text="Produto cadastrado com sucesso!")
            
            # limpar os campos de entrada
            self.entry_nome.delete(0, END)
            self.entry_preco.delete(0, END)
            self.entry_descricao.delete(0, END)
            self.entry_estoque.delete(0, END)
            self.entry_preco.focus()
            self.entry_estoque.focus()
            self.entry_descricao.focus()
            self.entry_nome.focus()


    
janela = Produto_janela()
janela.mainloop()
