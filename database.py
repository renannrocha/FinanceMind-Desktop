import sqlite3

DB_NAME = "financas_pessoais.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Criação da tabela de transações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria TEXT NOT NULL,
            tipo TEXT NOT NULL -- 'receita' ou 'despesa'
        )
    ''')
    
    # Criação da tabela de categorias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()