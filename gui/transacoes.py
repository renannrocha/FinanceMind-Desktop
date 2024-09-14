import tkinter as tk
from tkinter import ttk, messagebox
from database import execute_query, search_query
from datetime import datetime

class AdicionarTransacao:
    def __init__(self, parent):
        self.parent = parent
        self.janela = tk.Frame(parent)
        self.janela.pack(fill=tk.BOTH, expand=True)
        self.criar_widgets()

    def criar_widgets(self):
        tk.Label(self.janela, text="Adicionar Transação", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.janela, text="Tipo:").pack(pady=5)
        self.tipo_var = tk.StringVar()
        tipo_combo = ttk.Combobox(self.janela, textvariable=self.tipo_var, values=['Receita', 'Despesa'], state='readonly')
        tipo_combo.pack(pady=5)
        tipo_combo.current(0)

        tk.Label(self.janela, text="Valor:").pack(pady=5)
        self.valor_entry = tk.Entry(self.janela)
        self.valor_entry.pack(pady=5)

        tk.Label(self.janela, text="Data (YYYY-MM-DD):").pack(pady=5)
        self.data_entry = tk.Entry(self.janela)
        self.data_entry.pack(pady=5)

        tk.Label(self.janela, text="Categoria:").pack(pady=5)
        self.categoria_var = tk.StringVar()
        categorias = search_query("SELECT nome FROM categorias WHERE tipo = ?", (self.tipo_var.get(),))
        categoria_combo = ttk.Combobox(self.janela, textvariable=self.categoria_var, values=[c[0] for c in categorias], state='readonly')
        categoria_combo.pack(pady=5)
        if categorias:
            categoria_combo.current(0)

        tk.Label(self.janela, text="Descrição:").pack(pady=5)
        self.descricao_entry = tk.Entry(self.janela)
        self.descricao_entry.pack(pady=5)

        salvar_btn = tk.Button(self.janela, text="Salvar", command=self.salvar)
        salvar_btn.pack(pady=10)

    def salvar(self):
        tipo = self.tipo_var.get()
        valor = self.valor_entry.get()
        data = self.data_entry.get()
        categoria = self.categoria_var.get()
        descricao = self.descricao_entry.get()

        if not valor or not data or not categoria:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        try:
            valor = float(valor)
            datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erro", "Valor ou data inválidos.")
            return

        categorias = search_query("SELECT id FROM categorias WHERE nome = ?", (categoria,))
        if categorias:
            categoria_id = categorias[0][0]
        else:
            messagebox.showerror("Erro", "Categoria não encontrada.")
            return

        execute_query('''
            INSERT INTO transacoes (tipo, valor, data, categoria_id, descricao)
            VALUES (?, ?, ?, ?, ?)
        ''', (tipo, valor, data, categoria_id, descricao))

        messagebox.showinfo("Sucesso", "Transação adicionada com sucesso.")
