import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database import execute_query, search_query
from datetime import datetime

class Orcamentos:
    def __init__(self, parent):
        self.master = parent
        self.criar_widgets()

    def criar_widgets(self):
        # Frame principal para o layout
        main_frame = tk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Adiciona a tabela de orçamentos
        self.criar_tabela(main_frame)

        # Adiciona o formulário de adição de orçamentos
        form_frame = tk.Frame(main_frame)
        form_frame.pack(pady=10, padx=10, fill=tk.X)

        # Título da tela
        tk.Label(form_frame, text="Adicionar Orçamento", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=10, sticky="w")

        # Categoria
        tk.Label(form_frame, text="Categoria:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.categoria_var = tk.StringVar()
        self.categoria_combo = ttk.Combobox(form_frame, textvariable=self.categoria_var, state='readonly')
        self.categoria_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.carregar_categorias()

        # Mês
        tk.Label(form_frame, text="Mês:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.mes_entry = tk.Entry(form_frame)
        self.mes_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Ano
        tk.Label(form_frame, text="Ano:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.ano_entry = tk.Entry(form_frame)
        self.ano_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Valor
        tk.Label(form_frame, text="Valor:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.valor_entry = tk.Entry(form_frame)
        self.valor_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Botão salvar
        salvar_btn = tk.Button(form_frame, text="Salvar", command=self.salvar)
        salvar_btn.grid(row=5, column=1, padx=5, pady=10, sticky="e")

        # Configurar as colunas para expandir
        form_frame.columnconfigure(1, weight=1)

    def criar_tabela(self, parent):
        # Frame da tabela
        table_frame = tk.Frame(parent)
        table_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Barra de rolagem
        self.scroll_y = tk.Scrollbar(table_frame, orient="vertical")
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Tabela
        self.table = ttk.Treeview(table_frame, yscrollcommand=self.scroll_y.set, columns=("Categoria", "Mês", "Ano", "Valor"), show="headings")
        self.table.pack(fill=tk.BOTH, expand=True)
        self.scroll_y.config(command=self.table.yview)

        # Definição das colunas
        self.table.heading("Categoria", text="Categoria")
        self.table.heading("Mês", text="Mês")
        self.table.heading("Ano", text="Ano")
        self.table.heading("Valor", text="Valor")
        
        self.table.column("Categoria", width=150)
        self.table.column("Mês", width=50)
        self.table.column("Ano", width=50)
        self.table.column("Valor", width=100)

        # Carregar orçamentos
        self.carregar_orcamentos()

    def carregar_categorias(self):
        categorias = search_query("SELECT nome FROM categorias")
        self.categoria_combo['values'] = [c[0] for c in categorias]
        if categorias:
            self.categoria_combo.current(0)

    def salvar(self):
        categoria = self.categoria_var.get()
        mes = self.mes_entry.get()
        ano = self.ano_entry.get()
        valor = self.valor_entry.get()

        if not categoria or not mes or not ano or not valor:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        try:
            mes = int(mes)
            ano = int(ano)
            valor = float(valor)
        except ValueError:
            messagebox.showerror("Erro", "Dados inválidos.")
            return

        categorias = search_query("SELECT id FROM categorias WHERE nome = ?", (categoria,))
        if categorias:
            categoria_id = categorias[0][0]
        else:
            messagebox.showerror("Erro", "Categoria não encontrada.")
            return

        execute_query('''INSERT INTO orcamentos (categoria_id, mes, ano, valor) VALUES (?, ?, ?, ?)''',
                      (categoria_id, mes, ano, valor))

        messagebox.showinfo("Sucesso", "Orçamento adicionado com sucesso.")
        self.carregar_orcamentos()

    def carregar_orcamentos(self):
        # Limpa as linhas existentes na tabela
        for row in self.table.get_children():
            self.table.delete(row)
        
        # Consulta SQL qualificada
        query = '''
        SELECT 
            categorias.nome AS categoria, 
            orcamentos.mes, 
            orcamentos.ano, 
            orcamentos.valor
        FROM 
            orcamentos 
        JOIN 
            categorias 
        ON 
            orcamentos.categoria_id = categorias.id
        '''
        
        orcamentos = search_query(query)
        
        for orcamento in orcamentos:
            self.table.insert("", tk.END, values=orcamento)
