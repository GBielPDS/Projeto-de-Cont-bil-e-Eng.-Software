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


        # Frame para os botões de ação
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(pady=10, padx=10, fill="x")

        self.button_cadastrar = ctk.CTkButton(self.frame_botoes, text="Cadastrar Produtos", command=self.cadastrar_produtos)
        self.button_cadastrar.pack(side=LEFT, padx=5, pady=5, expand=True, fill="x")

        self.button_editar = ctk.CTkButton(self.frame_botoes, text="Editar Produtos", command=self.editar_produtos)
        self.button_editar.pack(side=LEFT, padx=5, pady=5, expand=True, fill="x")

        self.button_buscar = ctk.CTkButton(self.frame_botoes, text="Buscar Produtos", command=self.buscar_produtos)
        self.button_buscar.pack(side=LEFT, padx=5, pady=5, expand=True, fill="x")

        # ------ Frame para entrada de dados do produto ------
        self.frame_produto = ctk.CTkFrame(self)
        self.entry_nome = ctk.CTkEntry(self.frame_produto, placeholder_text="Nome do Produto: ")
        self.entry_preco = ctk.CTkEntry(self.frame_produto, placeholder_text="Preço do Produto: ")
        self.entry_descricao = ctk.CTkEntry(self.frame_produto, placeholder_text="Descrição do Produto: ")
        self.entry_estoque = ctk.CTkEntry(self.frame_produto, placeholder_text="Estoque do Produto: ")

        # Frame para botões Salvar e Fechar
        self.frame_salvar_fechar = ctk.CTkFrame(self.frame_produto)
        self.button_salvar = ctk.CTkButton(self.frame_salvar_fechar, text="Salvar Produto", command=self.salvar_produto)
        self.button_salvar.pack(side=LEFT, padx=5, pady=5, expand=True, fill="x")
        self.button_fechar = ctk.CTkButton(self.frame_salvar_fechar, text="Fechar", command=self.fechar_cadastro)
        self.button_fechar.pack(side=LEFT, padx=5, pady=5, expand=True, fill="x")
        self.label_alerta = ctk.CTkLabel(self, text="")

        # Frame para botões de busca
        self.frame_busca = ctk.CTkFrame(self)
        self.button_busca_id = ctk.CTkButton(self.frame_busca, text="Buscar por ID", command=self.buscar_por_id)
        self.button_busca_nome = ctk.CTkButton(self.frame_busca, text="Buscar por Nome", command=self.buscar_por_nome)
        self.button_busca_preco = ctk.CTkButton(self.frame_busca, text="Buscar por Preço", command=self.buscar_por_preco)
        self.button_mostrar_todos = ctk.CTkButton(self.frame_busca, text="Mostrar Todos", command=self.mostrar_todos)
        self.button_fechar_busca = ctk.CTkButton(self.frame_busca, text="Fechar", command=self.fechar_busca)
        
    def cadastrar_produtos(self):
        self.frame_produto.pack(pady=10, padx=10, fill="x")
        self.entry_nome.pack(pady=5, padx=10, fill="x")
        self.entry_preco.pack(pady=5, padx=10, fill="x")
        self.entry_descricao.pack(pady=5, padx=10, fill="x")
        self.entry_estoque.pack(pady=5, padx=10, fill="x")
        self.frame_salvar_fechar.pack(pady=10, padx=10, fill="x")
        self.label_alerta.pack(pady=10)

    def fechar_cadastro(self):
        self.label_alerta.configure(text="")
        self.frame_produto.pack_forget()
        self.label_alerta.pack_forget()

    def editar_produtos(self):
        pass

    def buscar_produtos(self):

        self.frame_busca.pack(pady=10, padx=10, fill="x")
        self.button_busca_id.pack(side=LEFT, padx=5, pady=5, expand=True, fill="x")
        self.button_busca_nome.pack(side=LEFT, padx=5, pady=5, expand=True, fill="x")
        self.button_busca_preco.pack(side=LEFT, padx=5, pady=5, expand=True, fill="x")
        self.button_mostrar_todos.pack(side=LEFT, padx=5, pady=5, expand=True, fill="x")
        self.button_fechar_busca.pack(padx=10, pady=10, expand=True, fill="x")
    
    def fechar_busca(self):
        self.frame_busca.pack_forget()
        self.label_alerta.configure(text="")
        self.label_alerta.pack_forget()
        try:
            self.entry_busca.pack_forget()
            self.button_executar_busca.pack_forget()
        except AttributeError:
            pass

    def buscar_por_id(self):
        self._mostrar_entry_busca('ID do Produto', self._executar_busca_id)

    def buscar_por_nome(self):
        self._mostrar_entry_busca('Nome do Produto', self._executar_busca_nome)

    def buscar_por_preco(self):
        self._mostrar_entry_busca('Preço do Produto', self._executar_busca_preco)

    def _mostrar_entry_busca(self, placeholder, comando_busca):
        # Remove entry e botão anteriores, se existirem
        if hasattr(self, 'entry_busca') and self.entry_busca:
            self.entry_busca.destroy()
        if hasattr(self, 'button_executar_busca') and self.button_executar_busca:
            self.button_executar_busca.destroy()
        # Adiciona entry e botão logo abaixo do frame_busca
        self.entry_busca = ctk.CTkEntry(self, placeholder_text=placeholder)
        self.entry_busca.pack(after=self.frame_busca, pady=5, padx=10, fill="x")
        self.button_executar_busca = ctk.CTkButton(self, text="Buscar", command=lambda: comando_busca(self.entry_busca.get()))
        self.button_executar_busca.pack(after=self.entry_busca, pady=5, padx=10)
        self.label_alerta.pack(pady=10)

    def _executar_busca_id(self, valor):
        if hasattr(self, 'frame_tabela') and self.frame_tabela:
            self.frame_tabela.destroy()
        if valor == "":
            self._mostrar_tabela([], ["ID não pode ser vazio."])
        elif not valor.isdigit():
            self._mostrar_tabela([], ["ID deve ser um número."])
        else:
            resultado = self.bd.buscar_produto('id', int(valor))
            if resultado:
                # Garante que o resultado seja uma lista de tuplas, igual às outras buscas
                if isinstance(resultado, tuple):
                    resultado = [resultado]
                self._mostrar_tabela(resultado, [])
            else:
                self._mostrar_tabela([], ["Nenhum produto encontrado com esse ID."])

    def _executar_busca_nome(self, valor):
        if hasattr(self, 'frame_tabela') and self.frame_tabela:
            self.frame_tabela.destroy()
        if not valor:
            self._mostrar_tabela([], ["Nome não pode ser vazio."])
            return
        resultados = self.bd.buscar_produto('nome', valor)
        if resultados:
            if isinstance(resultados, tuple):
                resultados = [resultados]
            self._mostrar_tabela(resultados, [])
        else:
            self._mostrar_tabela([], ["Nenhum produto encontrado com esse nome."])

    def _executar_busca_preco(self, valor):
        if hasattr(self, 'frame_tabela') and self.frame_tabela:
            self.frame_tabela.destroy()
        try:
            preco = float(valor.replace(',', '.'))
        except ValueError:
            self._mostrar_tabela([], ["Preço inválido."])
            return
        resultados = self.bd.buscar_produto('preco', preco)
        if resultados:
            if isinstance(resultados, tuple):
                resultados = [resultados]
            self._mostrar_tabela(resultados, [])
        else:
            self._mostrar_tabela([], ["Nenhum produto encontrado com esse preço."])
    def _mostrar_tabela(self, dados, mensagens):
        # Remove tabela anterior se existir
        if hasattr(self, 'frame_tabela') and self.frame_tabela:
            self.frame_tabela.destroy()
        self.frame_tabela = ctk.CTkFrame(self)
        self.frame_tabela.pack(pady=10, padx=10, fill="x")
        if not dados:
            # Mensagem de erro ou vazio
            for i, msg in enumerate(mensagens):
                label = ctk.CTkLabel(self.frame_tabela, text=msg, font=("Arial", 12, "bold"))
                label.grid(row=i, column=0, sticky="w", padx=5, pady=2)
        else:
            campos = ["id", "nome", "descricao", "preco", "estoque"]
            for idx, linha in enumerate(dados):
                for i, valor in enumerate(linha):
                    texto = f"{campos[i]}: {valor}"
                    label = ctk.CTkLabel(self.frame_tabela, text=texto)
                    label.grid(row=i + idx*len(campos), column=0, sticky="w", padx=5, pady=2)

    def mostrar_todos(self):
        if hasattr(self, 'frame_tabela') and self.frame_tabela:
            self.frame_tabela.destroy()
        try:
            resultados = self.bd.mostrar_todos = self.bd.mostrar_todos('produtos')
        except Exception as e:
            self._mostrar_tabela([], [f"Erro ao buscar produtos: {e}"])
            return
        if resultados:
            if isinstance(resultados, tuple):
                resultados = [resultados]
            self._mostrar_tabela(resultados, [])
        else:
            self._mostrar_tabela([], ["Nenhum produto cadastrado."])
        

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
