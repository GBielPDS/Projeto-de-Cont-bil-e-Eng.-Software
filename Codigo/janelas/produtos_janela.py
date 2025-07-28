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

        # Botão Home
        self.button_home = ctk.CTkButton(self.frame_botoes, text="Home", command=self.open_home)
        self.button_home.pack(side=LEFT, padx=5, pady=5, expand=True, fill="x")

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
        # Remove frames antigos se existirem
        if hasattr(self, 'frame_editar') and self.frame_editar:
            self.frame_editar.destroy()
        if hasattr(self, 'frame_tabela_editar') and self.frame_tabela_editar:
            self.frame_tabela_editar.destroy()
        if hasattr(self, 'frame_editar_form') and self.frame_editar_form:
            self.frame_editar_form.destroy()

        # Frame para buscar produto por ID ou Nome
        self.frame_editar = ctk.CTkFrame(self)
        self.frame_editar.pack(pady=10, padx=10, fill="x")

        self.entry_editar_id = ctk.CTkEntry(self.frame_editar, placeholder_text="ID do Produto")
        self.entry_editar_id.pack(side=LEFT, padx=5, pady=5, expand=True, fill="x")
        self.entry_editar_nome = ctk.CTkEntry(self.frame_editar, placeholder_text="Nome do Produto")
        self.entry_editar_nome.pack(side=LEFT, padx=5, pady=5, expand=True, fill="x")

        self.button_buscar_editar = ctk.CTkButton(
            self.frame_editar, text="Buscar", 
            command=self._buscar_produtos_para_editar
        )
        self.button_buscar_editar.pack(side=LEFT, padx=5, pady=5, expand=True, fill="x")

        # Botão fechar para toda a área de edição
        self.button_fechar_editar = ctk.CTkButton(
            self.frame_editar, text="Fechar", command=self.fechar_editar_produto
        )
        self.button_fechar_editar.pack(side=LEFT, padx=5, pady=5, expand=True, fill="x")

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
            if hasattr(self, 'entry_busca') and self.entry_busca:
                self.entry_busca.pack_forget()
            if hasattr(self, 'button_executar_busca') and self.button_executar_busca:
                self.button_executar_busca.pack_forget()
            if hasattr(self, 'frame_tabela') and self.frame_tabela:
                self.frame_tabela.destroy()
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
        valor = valor.upper()
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
            resultados = self.bd.mostrar_todos('produtos')
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
        nome = self.entry_nome.get().upper()
        preco = self.entry_preco.get()
        descricao = self.entry_descricao.get().upper()
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

    def _buscar_produtos_para_editar(self):
        # Remove tabela anterior se existir
        if hasattr(self, 'frame_tabela_editar') and self.frame_tabela_editar:
            self.frame_tabela_editar.destroy()
        if hasattr(self, 'frame_editar_form') and self.frame_editar_form:
            self.frame_editar_form.destroy()

        id_valor = self.entry_editar_id.get().strip()
        nome_valor = self.entry_editar_nome.get().strip().upper()

        if id_valor:
            resultados = self.bd.buscar_produto('id', int(id_valor)) if id_valor.isdigit() else []
        elif nome_valor:
            resultados = self.bd.buscar_produto('nome', nome_valor)
        else:
            resultados = []

        self.frame_tabela_editar = ctk.CTkFrame(self)
        self.frame_tabela_editar.pack(pady=10, padx=10, fill="x")

        if not resultados:
            label = ctk.CTkLabel(self.frame_tabela_editar, text="Nenhum produto encontrado.", font=("Arial", 12, "bold"))
            label.pack()
            return

        campos = ["id", "nome", "descricao", "preco", "estoque"]
        for idx, linha in enumerate(resultados):
            texto = "\n".join([f"{campos[i]}: {linha[i]}" for i in range(len(campos))])
            btn = ctk.CTkButton(
                self.frame_tabela_editar, 
                text=texto, 
                anchor="w",
                command=lambda l=linha: self._mostrar_form_editar_produto(l)
            )
            btn.pack(fill="x", pady=3, padx=5)

    def _mostrar_form_editar_produto(self, produto):
        # Remove tabela e form anterior se existirem
        if hasattr(self, 'frame_tabela_editar') and self.frame_tabela_editar:
            self.frame_tabela_editar.destroy()
        if hasattr(self, 'frame_editar_form') and self.frame_editar_form:
            self.frame_editar_form.destroy()

        self.frame_editar_form = ctk.CTkFrame(self)
        self.frame_editar_form.pack(pady=10, padx=10, fill="x")

        campos = ["id", "nome", "descricao", "preco", "estoque"]
        self.editar_entries = {}

        for i, campo in enumerate(campos):
            label = ctk.CTkLabel(self.frame_editar_form, text=f"{campo.capitalize()}:")
            label.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            entry = ctk.CTkEntry(self.frame_editar_form)
            entry.insert(0, str(produto[i]))
            if campo == "id":
                entry.configure(state="disabled")
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            self.editar_entries[campo] = entry

        button_salvar = ctk.CTkButton(
            self.frame_editar_form, text="Salvar Alterações",
            command=self._salvar_edicao_produto
        )
        button_salvar.grid(row=len(campos), column=0, columnspan=2, pady=10)

    def _salvar_edicao_produto(self):
        # Recupera os valores editados
        id_produto = self.editar_entries["id"].get()
        nome = self.editar_entries["nome"].get().upper()
        descricao = self.editar_entries["descricao"].get().upper()
        preco = self.editar_entries["preco"].get()
        estoque = self.editar_entries["estoque"].get()

        # Aqui você pode adicionar validações se quiser

        self.bd.atualizar_produto(id_produto, nome, descricao, preco, estoque)
        self.label_alerta.configure(text="Produto atualizado com sucesso!")
        if hasattr(self, 'frame_editar_form') and self.frame_editar_form:
            self.frame_editar_form.destroy()

        # Buscar o produto atualizado e mostrar na tela
        produto_atualizado = self.bd.buscar_produto('id', int(id_produto))
        if produto_atualizado:
            self.frame_tabela_editar = ctk.CTkFrame(self)
            self.frame_tabela_editar.pack(pady=10, padx=10, fill="x")
            campos = ["id", "nome", "descricao", "preco", "estoque"]
            for idx, linha in enumerate(produto_atualizado):
                texto = "\n".join([f"{campos[i]}: {linha[i]}" for i in range(len(campos))])
                label = ctk.CTkLabel(self.frame_tabela_editar, text=texto, anchor="w", justify="left")
                label.pack(fill="x", pady=3, padx=5)

    def fechar_editar_produto(self):
        if hasattr(self, 'frame_editar') and self.frame_editar:
            self.frame_editar.destroy()
        if hasattr(self, 'frame_tabela_editar') and self.frame_tabela_editar:
            self.frame_tabela_editar.destroy()
        if hasattr(self, 'frame_editar_form') and self.frame_editar_form:
            self.frame_editar_form.destroy()
        self.label_alerta.configure(text="")

    def open_home(self):
        global app
        from Codigo.janelas.home import Home_janela
        self.after(100, self.destroy)
        app = Home_janela()
        app.mainloop()
