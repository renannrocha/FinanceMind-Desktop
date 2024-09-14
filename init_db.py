from database import init_db

def main():
    """Função principal para inicializar o banco de dados."""
    init_db()
    print("Banco de dados e tabelas criados com sucesso.")

if __name__ == "__main__":
    main()
