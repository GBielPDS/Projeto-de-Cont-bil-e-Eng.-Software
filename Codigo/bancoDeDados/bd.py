import sqlite3
import os

class Banco_Dados():
    def __init__(self, arquivo="empresa.db"):
        self.arquivo = arquivo
        
    def criar_banco(self):    
        if os.path.exists(self.arquivo):
            print("Banco de dados já existe.")
        else:
            print("Banco de dados não existe. Criando...")
            conn = sqlite3.connect(self.arquivo)
            cursor = conn.cursor()

            # Cria todas as tabelas
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT,
                cpf TEXT NOT NULL UNIQUE,
                matricula TEXT,
                salario REAL,
                funcao TEXT
            )
            ''')


            cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                preco REAL NOT NULL,
                estoque INTEGER NOT NULL
            )
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS comprovante_vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                valor_total REAL NOT NULL,
                codigo INTEGER NOT NULL,
                data_venda TEXT NOT NULL,
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS historico_vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_venda TEXT NOT NULL,
                codigo_comprovante INTEGER NOT NULL,
                FOREIGN KEY (codigo_comprovante) REFERENCES comprovante_vendas(codigo)
            )
            ''')

            conn.commit()
            conn.close()
    
    def novo_produto(self, nome, descricao, preco, estoque):
        conn = sqlite3.connect(self.arquivo)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO produtos (nome, descricao, preco, estoque)
        VALUES (?, ?, ?, ?)
        ''', (nome, descricao, preco, estoque))
        conn.commit()
        conn.close()

    def buscar_produto(self, coluna, valor):
        conn = sqlite3.connect(self.arquivo)
        cursor = conn.cursor()
        if coluna == "nome":
            cursor.execute(f"SELECT * FROM produtos WHERE UPPER(nome) LIKE ?", (f"%{valor.upper()}%",))
        else:
            cursor.execute(f"SELECT * FROM produtos WHERE {coluna} = ?", (valor,))
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    
    def mostrar_todos(self, tabela):
        conn = sqlite3.connect(self.arquivo)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {tabela}')
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def atualizar_produto(self, id_produto, nome, descricao, preco, estoque):
        conn = sqlite3.connect(self.arquivo)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE produtos
            SET nome = ?, descricao = ?, preco = ?, estoque = ?
            WHERE id = ?
        ''', (nome, descricao, preco, estoque, id_produto))
        conn.commit()
        conn.close()

    def gerar_comprovante_venda(self, produto_id, quantidade, valor_total, codigo, data_venda):
        conn = sqlite3.connect(self.arquivo)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO comprovante_vendas (produto_id, quantidade, valor_total, codigo, data_venda)
            VALUES (?, ?, ?, ?, ?)
        ''', (produto_id, quantidade, valor_total, codigo, data_venda))
        conn.commit()
        conn.close()

    def gerar_codigo_comprovante(self):
        conn = sqlite3.connect(self.arquivo)
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(codigo) FROM comprovante_vendas')
        ultimo_codigo = cursor.fetchone()[0]
        if ultimo_codigo is None:
            novo_codigo = 1
        else:
            novo_codigo = ultimo_codigo + 1
        conn.close()
        return novo_codigo

    def registrar_historico_venda(self, data_venda, codigo_comprovante):
        conn = sqlite3.connect(self.arquivo)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO historico_vendas (data_venda, codigo_comprovante)
            VALUES (?, ?)
        ''', (data_venda, codigo_comprovante))
        conn.commit()
        conn.close()

    def cadastrar_funcionario(self, nome, telefone, email, cpf, matricula, salario, funcao):
        conn = sqlite3.connect(self.arquivo)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO funcionarios (nome, telefone, email, cpf, matricula, salario, funcao)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nome, telefone, email, cpf, matricula, salario, funcao))
        conn.commit()
        conn.close()

    def editar_funcionario(self, id, coluna, valor):
        conn = sqlite3.connect(self.arquivo)
        cursor = conn.cursor()
        cursor.execute(f'UPDATE funcionarios SET {coluna} = ? WHERE id = ?', (valor, id))
        conn.commit()
        conn.close()

    def buscar_funcionario(self, coluna, valor):
        conn = sqlite3.connect(self.arquivo)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM funcionarios WHERE {coluna} = ?', (valor,))
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    
    def conectar(self):
        return sqlite3.connect(self.arquivo)
