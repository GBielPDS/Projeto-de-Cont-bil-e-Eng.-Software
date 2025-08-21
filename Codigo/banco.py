import mysql.connector

DB_CONFIG = dict(
    host="localhost",
    user="root",
    password="",  #essa senha vc substitui pela sua do mysql, para ter permissão de acessar o banco#
    database="gestor360"
)

def conectar():
    return mysql.connector.connect(**DB_CONFIG)

def testar_conexao():
    con = conectar()
    con.close()
    return True
