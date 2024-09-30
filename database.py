import sqlite3

DB_NAME = "financas_pessoais.db"

def get_db_connection():
    """Obtém uma conexão com o banco de dados."""
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def execute_query(query, params=()):
    """Executa uma query no banco de dados."""
    conn = get_db_connection()
    if conn is None:
        print("Conexão não estabelecida. Query não executada.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao executar a query: {e}")
    finally:
        conn.close()

def search_query(query, params=()):
    """Busca dados no banco de dados e retorna os resultados."""
    conn = get_db_connection()
    if conn is None:
        print("Conexão não estabelecida. Busca não realizada.")
        return []

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as e:
        print(f"Erro ao buscar dados: {e}")
        return []
    finally:
        conn.close()

def init_db():
    """Inicializa o banco de dados criando as tabelas necessárias."""
    conn = get_db_connection()
    if conn is None:
        print("Conexão não estabelecida. Banco de dados não inicializado.")
        return

    try:
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
        print("Banco de dados e tabelas criados com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()

