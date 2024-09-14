import tkinter as tk
from tkinter import ttk, messagebox
from database import execute_query, search_query
from datetime import datetime

class AdicionarTransacao:
    def __init__(self, parent):
        self.master = parent
        self.criar_widgets()

    def criar_widgets(self):
        tk.Label(self.master, text="Adicionar Transação", font=("Arial", 16)).pack(pady=10)

        self.tipo_var = tk.StringVar(value="Receita")
        tk.Label(self.master, text="Tipo (Receita/Despesa):").pack(pady=5)
        tipo_frame = tk.Frame(self.master)
        tipo_frame.pack(pady=5)
        tk.Radiobutton(tipo_frame, text="Receita", variable=self.tipo_var, value="Receita").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(tipo_frame, text="Despesa", variable=self.tipo_var, value="Despesa").pack(side=tk.LEFT, padx=5)

        tk.Label(self.master, text="Valor:").pack(pady=5)
        self.valor_entry = tk.Entry(self.master)
        self.valor_entry.pack(pady=5)

        tk.Label(self.master, text="Data (YYYY-MM-DD):").pack(pady=5)
        self.data_entry = tk.Entry(self.master)
        self.data_entry.pack(pady=5)

        tk.Label(self.master, text="Categoria:").pack(pady=5)
        self.categoria_var = tk.StringVar()
        self.categoria_combo = ttk.Combobox(self.master, textvariable=self.categoria_var, state='readonly')
        self.categoria_combo.pack(pady=5)
        self.carregar_categorias()

        tk.Label(self.master, text="Descrição:").pack(pady=5)
        self.descricao_entry = tk.Entry(self.master)
        self.descricao_entry.pack(pady=5)

        salvar_btn = tk.Button(self.master, text="Salvar", command=self.salvar)
        salvar_btn.pack(pady=10)

        # Garantir que o trace_add funcione corretamente
        self.tipo_var.trace_add("write", self.atualizar_categorias)

    def carregar_categorias(self):
        tipo = self.tipo_var.get()
        categorias = search_query("SELECT nome FROM categorias WHERE tipo = ?", (tipo,))
        self.categoria_combo['values'] = [c[0] for c in categorias]
        if categorias:
            self.categoria_combo.current(0)

    def atualizar_categorias(self, *args):
        self.carregar_categorias()

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
