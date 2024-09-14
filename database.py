import sqlite3

DB_NAME = "financas_pessoais.db"

def get_db_connection():
    """Obtém uma conexão com o banco de dados."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def execute_query(query, params=()):
    """Executa uma query no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def search_query(query, params=()):
    """Busca dados no banco de dados e retorna os resultados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def init_db():
    """Inicializa o banco de dados criando as tabelas necessárias."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL CHECK(tipo IN ('Receita', 'Despesa'))
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL CHECK(tipo IN ('Receita', 'Despesa')),
            valor REAL NOT NULL,
            data DATE NOT NULL,
            categoria_id INTEGER,
            descricao TEXT,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orcamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER NOT NULL,
            mes INTEGER NOT NULL CHECK(mes BETWEEN 1 AND 12),
            ano INTEGER NOT NULL,
            valor REAL NOT NULL,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Banco de dados e tabelas criados com sucesso.")
