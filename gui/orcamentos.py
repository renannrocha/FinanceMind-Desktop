import tkinter as tk
from tkinter import ttk, messagebox
from database import execute_query, search_query

class Orcamentos:
    def __init__(self, parent):
        self.parent = parent
        self.janela = tk.Frame(parent)
        self.janela.pack(fill=tk.BOTH, expand=True)
        self.criar_widgets()

    def criar_widgets(self):
        tk.Label(self.janela, text="Orçamentos", font=("Arial", 16)).pack(pady=10)

        # Adicionar widgets para gerenciamento de orçamentos
        tk.Label(self.janela, text="Categoria:").pack(pady=5)
        self.categoria_var = tk.StringVar()
        categorias = search_query("SELECT nome FROM categorias")
        categoria_combo = ttk.Combobox(self.janela, textvariable=self.categoria_var, values=[c[0] for c in categorias], state='readonly')
        categoria_combo.pack(pady=5)
        if categorias:
            categoria_combo.current(0)

        tk.Label(self.janela, text="Mês (1-12):").pack(pady=5)
        self.mes_entry = tk.Entry(self.janela)
        self.mes_entry.pack(pady=5)

        tk.Label(self.janela, text="Ano:").pack(pady=5)
        self.ano_entry = tk.Entry(self.janela)
        self.ano_entry.pack(pady=5)

        tk.Label(self.janela, text="Valor:").pack(pady=5)
        self.valor_entry = tk.Entry(self.janela)
        self.valor_entry.pack(pady=5)

        salvar_btn = tk.Button(self.janela, text="Salvar", command=self.salvar)
        salvar_btn.pack(pady=10)

    def salvar(self):
        categoria = self.categoria_var.get()
        mes = self.mes_entry.get()
        ano = self.ano_entry.get()
        valor = self.valor_entry.get()

        if not categoria or not mes or not ano or not valor:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        try:
            mes = int(mes)
            ano = int(ano)
            valor = float(valor)
            if mes < 1 or mes > 12:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Dados inválidos.")
            return

        categorias = search_query("SELECT id FROM categorias WHERE nome = ?", (categoria,))
        if categorias:
            categoria_id = categorias[0][0]
        else:
            messagebox.showerror("Erro", "Categoria não encontrada.")
            return

        execute_query('''
            INSERT INTO orcamentos (categoria_id, mes, ano, valor)
            VALUES (?, ?, ?, ?)
        ''', (categoria_id, mes, ano, valor))

        messagebox.showinfo("Sucesso", "Orçamento definido com sucesso.")
