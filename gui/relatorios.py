import tkinter as tk
from database import get_db_connection

class Relatorios:
    def __init__(self, master):
        self.master = master
        self.master.title("Relatórios")

        # Exibir resumo de receitas e despesas
        self.exibir_relatorio()

    def exibir_relatorio(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT SUM(valor) FROM transacoes WHERE tipo = "receita"')
        total_receitas = cursor.fetchone()[0] or 0

        cursor.execute('SELECT SUM(valor) FROM transacoes WHERE tipo = "despesa"')
        total_despesas = cursor.fetchone()[0] or 0

        saldo = total_receitas - total_despesas

        tk.Label(self.master, text=f"Receitas Totais: {total_receitas}").pack()
        tk.Label(self.master, text=f"Despesas Totais: {total_despesas}").pack()
        tk.Label(self.master, text=f"Saldo Atual: {saldo}").pack()

        conn.close()
