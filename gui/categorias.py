import tkinter as tk
from tkinter import ttk
from database import get_db_connection

class Categorias:
    def __init__(self, master):
        self.master = master
        self.master.title("Categorias")
        
        # Campos para adicionar categorias
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Nome da Categoria:").pack()
        self.nome_entry = ttk.Entry(self.master)
        self.nome_entry.pack()

        ttk.Button(self.master, text="Adicionar Categoria", command=self.adicionar_categoria).pack(pady=10)
        ttk.Button(self.master, text="Ver Categorias", command=self.ver_categorias).pack(pady=10)

    def adicionar_categoria(self):
        nome = self.nome_entry.get()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO categorias (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()

    def ver_categorias(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM categorias')
        categorias = cursor.fetchall()
        for categoria in categorias:
            print(categoria)
        conn.close()