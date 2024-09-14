import tkinter as tk
from gui.dashboard import Dashboard
from database import init_db

def main():
    # Inicializa o banco de dados
    init_db()

    # Cria a janela principal
    root = tk.Tk()
    root.title("FinanceMind - Controle Financeiro Pessoal")
    root.geometry("800x600")

    # Inicializa o dashboard
    app = Dashboard(root)
    
    # Inicia o loop da GUI
    root.mainloop()

if __name__ == '__main__':
    main()
