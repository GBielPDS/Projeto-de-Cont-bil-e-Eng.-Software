import customtkinter as ctk
from tkinter import *
import sys
import os
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Codigo.bancoDeDados.bd import Banco_Dados

class Venda_janela(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento")
        ctk.set_appearance_mode("dark")
        self.geometry("720x600")
        self.create_widgets()
        self.bd = Banco_Dados("empresa.db")
        self.carrinho = {}

    def create_widgets(self):
        # Frame para os botões de ação
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(pady=20, padx=20, fill="x")

        self.button_venda = ctk.CTkButton(
            self.frame_botoes, text="Venda", command=self.vender_produto
        )
        self.button_venda.pack(side=LEFT, padx=10, pady=10, expand=True, fill="x")

    def vender_produto(self):
        # Remove frames antigos se existirem
        if hasattr(self, 'frame_venda_produtos') and self.frame_venda_produtos:
            self.frame_venda_produtos.destroy()
        if hasattr(self, 'frame_carrinho') and self.frame_carrinho:
            self.frame_carrinho.destroy()

        # Frame com todos os produtos como botões
        self.frame_venda_produtos = ctk.CTkFrame(self)
        self.frame_venda_produtos.pack(pady=10, padx=10, fill="x")

        produtos = self.bd.mostrar_todos('produtos')
        if not produtos:
            label = ctk.CTkLabel(self.frame_venda_produtos, text="Nenhum produto disponível.", font=("Arial", 12, "bold"))
            label.pack()
            return

        ctk.CTkLabel(self.frame_venda_produtos, text="Selecione um produto:").pack(anchor="w", padx=5)
        self.produto_selecionado = None

        def selecionar_produto(produto):
            self.produto_selecionado = produto
            self.entry_quantidade.delete(0, 'end')
            self.label_valor_total.configure(text="Valor total: R$ 0,00")

        for produto in produtos:
            texto = f"id: {produto[0]}  nome: {produto[1]}  preço: {produto[3]:.2f}  estoque: {produto[4]}"
            btn = ctk.CTkButton(
                self.frame_venda_produtos,
                text=texto,
                anchor="w",
                command=lambda p=produto: selecionar_produto(p)
            )
            btn.pack(fill="x", pady=3, padx=5)

        # Entry para quantidade
        self.entry_quantidade = ctk.CTkEntry(self.frame_venda_produtos, placeholder_text="Quantidade")
        self.entry_quantidade.pack(pady=5, padx=10, fill="x")

        # Label para valor total
        self.label_valor_total = ctk.CTkLabel(self.frame_venda_produtos, text="Valor total: R$ 0,00")
        self.label_valor_total.pack(pady=5, padx=10, anchor="w")

        # Botão para adicionar ao carrinho
        def adicionar_ao_carrinho():
            if not self.produto_selecionado:
                self.label_valor_total.configure(text="Selecione um produto.")
                return
            try:
                quantidade = int(self.entry_quantidade.get())
                if quantidade <= 0:
                    raise ValueError
            except ValueError:
                self.label_valor_total.configure(text="Quantidade inválida.")
                return

            estoque_disponivel = int(self.produto_selecionado[4])
            produto_id = self.produto_selecionado[0]
            # Soma o que já está no carrinho desse produto
            quantidade_no_carrinho = self.carrinho.get(produto_id, {}).get('quantidade', 0)
            if quantidade + quantidade_no_carrinho > estoque_disponivel:
                self.label_valor_total.configure(
                    text=f"Estoque insuficiente. Disponível: {estoque_disponivel - quantidade_no_carrinho}"
                )
                return

            preco = float(self.produto_selecionado[3])
            valor_total = quantidade * preco
            self._adicionar_ao_carrinho(self.produto_selecionado, quantidade, valor_total)

            # Atualiza o valor total do carrinho
            valor_total_carrinho = sum(item['valor_total'] for item in self.carrinho.values())
            self.label_valor_total.configure(text=f"Valor total: R$ {valor_total_carrinho:.2f}")

        btn_add_carrinho = ctk.CTkButton(
            self.frame_venda_produtos, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho
        )
        btn_add_carrinho.pack(side="left", pady=5, padx=10)

        # Botão para finalizar a venda
        btn_finalizar_venda = ctk.CTkButton(
            self.frame_venda_produtos, text="Finalizar Venda", command=self.finalizar_venda
        )
        btn_finalizar_venda.pack(side="left", pady=5, padx=10)

        # Botão para fechar o frame de venda de produtos e o carrinho
        def fechar_venda_e_carrinho():
            if hasattr(self, 'frame_venda_produtos') and self.frame_venda_produtos:
                self.frame_venda_produtos.destroy()
                self.frame_venda_produtos = None
            if hasattr(self, 'frame_carrinho') and self.frame_carrinho:
                self.frame_carrinho.destroy()
                self.frame_carrinho = None
            self.carrinho.clear()
            self.produto_selecionado = None

        btn_fechar_venda = ctk.CTkButton(
            self.frame_venda_produtos, text="Fechar", command=fechar_venda_e_carrinho
        )
        btn_fechar_venda.pack(side="left", pady=5, padx=10)

    def _adicionar_ao_carrinho(self, produto, quantidade, valor_total):
        # Cria ou atualiza o frame do carrinho
        if not hasattr(self, 'frame_carrinho') or not self.frame_carrinho:
            self.frame_carrinho = ctk.CTkFrame(self)
            self.frame_carrinho.pack(pady=10, padx=10, fill="x")
            ctk.CTkLabel(self.frame_carrinho, text="Carrinho:", font=("Arial", 12, "bold")).pack(anchor="w", padx=5)

        produto_id = produto[0]
        # Se já está no carrinho, atualiza quantidade e valor
        if produto_id in self.carrinho:
            self.carrinho[produto_id]['quantidade'] += quantidade
            self.carrinho[produto_id]['valor_total'] += valor_total
            # Atualiza o texto do label
            novo_texto = f"{produto[1]} (x{self.carrinho[produto_id]['quantidade']}) - R$ {self.carrinho[produto_id]['valor_total']:.2f}"
            self.carrinho[produto_id]['label'].configure(text=novo_texto)
        else:
            # Adiciona novo produto ao carrinho
            texto = f"{produto[1]} (x{quantidade}) - R$ {valor_total:.2f}"
            label = ctk.CTkLabel(self.frame_carrinho, text=texto, anchor="w")
            label.pack(fill="x", padx=5)
            self.carrinho[produto_id] = {
                'quantidade': quantidade,
                'valor_total': valor_total,
                'label': label
            }

    def finalizar_venda(self):
        # Atualiza o estoque de cada produto no carrinho
        for produto_id, item in self.carrinho.items():
            resultado = self.bd.buscar_produto('id', produto_id)
            print(f"Resultado da busca por id {produto_id}: {resultado}")
            print(f"Item no carrinho: {item}")
            if resultado:
                produto = resultado[0]
                estoque_atual = int(produto[4])
                nova_quantidade = estoque_atual - int(item['quantidade'])
                if nova_quantidade < 0:
                    nova_quantidade = 0  # Evita estoque negativo
                # Corrigido: passar todos os argumentos necessários
                self.bd.atualizar_produto(
                    id_produto=produto_id,
                    nome=produto[1],
                    descricao=produto[2],
                    preco=produto[3],
                    estoque=nova_quantidade
                )

        # Gera código do comprovante e data da venda
        codigo_comprovante = self.bd.gerar_codigo_comprovante()
        data_venda = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Gera comprovante para cada item do carrinho
        for produto_id, item in self.carrinho.items():
            self.bd.gerar_comprovante_venda(
                produto_id=produto_id,
                quantidade=item['quantidade'],
                valor_total=item['valor_total'],
                codigo=codigo_comprovante,     
                data_venda=data_venda           
            )
        
        self.bd.registrar_historico_venda(data_venda, codigo_comprovante)

        # Limpa o carrinho e fecha os frames
        if hasattr(self, 'frame_venda_produtos') and self.frame_venda_produtos:
            self.frame_venda_produtos.destroy()
            self.frame_venda_produtos = None
        if hasattr(self, 'frame_carrinho') and self.frame_carrinho:
            self.frame_carrinho.destroy()
            self.frame_carrinho = None
        self.carrinho.clear()
        self.produto_selecionado = None
