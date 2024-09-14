import tkinter as tk
from tkinter import ttk
from database import get_db_connection

class Transacoes:
    def __init__(self, master):
        self.master = master
        self.master.title("Transações")
        
        # Criação dos campos de entrada
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Descrição:").pack()
        self.descricao_entry = ttk.Entry(self.master)
        self.descricao_entry.pack()

        tk.Label(self.master, text="Valor:").pack()
        self.valor_entry = ttk.Entry(self.master)
        self.valor_entry.pack()

        tk.Label(self.master, text="Categoria:").pack()
        self.categoria_entry = ttk.Entry(self.master)
        self.categoria_entry.pack()

        tk.Label(self.master, text="Tipo (receita/despesa):").pack()
        self.tipo_entry = ttk.Entry(self.master)
        self.tipo_entry.pack()

        ttk.Button(self.master, text="Adicionar Transação", command=self.adicionar_transacao).pack(pady=10)
        ttk.Button(self.master, text="Ver Transações", command=self.ver_transacoes).pack(pady=10)

    def adicionar_transacao(self):
        descricao = self.descricao_entry.get()
        valor = float(self.valor_entry.get())
        categoria = self.categoria_entry.get()
        tipo = self.tipo_entry.get()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transacoes (data, descricao, valor, categoria, tipo)
            VALUES (DATE('now'), ?, ?, ?, ?)
        ''', (descricao, valor, categoria, tipo))
        conn.commit()
        conn.close()

    def ver_transacoes(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transacoes')
        transacoes = cursor.fetchall()
        for transacao in transacoes:
            print(transacao)
        conn.close()