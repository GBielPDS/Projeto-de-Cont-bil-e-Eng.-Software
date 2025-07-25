import sqlite3
import os

class Banco_Dados():
    def __init__(self, arquivo):
        self.arquivo = arquivo
        if os.path.exists(arquivo):
            print("Banco de dados já existe.")
        else:
            print("Banco de dados não existe. Criando...")
            conn = sqlite3.connect(arquivo)
            cursor = conn.cursor()

            # Criar todas tabelas
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
            CREATE TABLE IF NOT EXISTS historico_vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_venda TEXT NOT NULL,
                funcionario_id INTEGER,
                produto_id INTEGER,
                quantidade INTEGER NOT NULL,
                valor_total REAL NOT NULL,
                FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id),
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
            ''')

            conn.commit()
            conn.close()

