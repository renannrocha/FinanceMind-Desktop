import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database import execute_query, search_query
from datetime import datetime
import csv
from tkinter.filedialog import asksaveasfilename

class AdicionarTransacao:
    def __init__(self, parent):
        self.master = parent
        self.criar_widgets()

    def criar_widgets(self):
        # Frame principal para o layout
        main_frame = tk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Adiciona a tabela de transações
        self.criar_tabela(main_frame)

        # Adiciona o formulário de adição de transações
        form_frame = tk.Frame(main_frame)
        form_frame.pack(pady=10, padx=10, fill=tk.X)

        # Título da tela
        tk.Label(form_frame, text="Adicionar Transação", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=10, sticky="w")

        # Tipo
        tk.Label(form_frame, text="Tipo:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tipo_frame = tk.Frame(form_frame)
        tipo_frame.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.tipo_var = tk.StringVar(value="Receita")
        tk.Radiobutton(tipo_frame, text="Receita", variable=self.tipo_var, value="Receita").pack(side=tk.LEFT)
        tk.Radiobutton(tipo_frame, text="Despesa", variable=self.tipo_var, value="Despesa").pack(side=tk.LEFT)

        # Valor
        tk.Label(form_frame, text="Valor:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.valor_entry = tk.Entry(form_frame)
        self.valor_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Data
        tk.Label(form_frame, text="Data:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.data_entry = DateEntry(form_frame, width=15, background='darkblue', foreground='white', borderwidth=2)
        self.data_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Categoria
        tk.Label(form_frame, text="Categoria:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.categoria_var = tk.StringVar()
        self.categoria_combo = ttk.Combobox(form_frame, textvariable=self.categoria_var, state='readonly')
        self.categoria_combo.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.carregar_categorias()

        # Descrição
        tk.Label(form_frame, text="Descrição:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.descricao_entry = tk.Entry(form_frame)
        self.descricao_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        # Botão salvar
        salvar_btn = tk.Button(form_frame, text="Salvar", command=self.salvar)
        salvar_btn.grid(row=6, column=1, padx=5, pady=10, sticky="e")

        # Botão limpar
        limpar_btn = tk.Button(form_frame, text="Limpar", command=self.limpar_campos)
        limpar_btn.grid(row=6, column=0, padx=5, pady=10, sticky="w")

        # Filtro de exportação
        tk.Label(form_frame, text="Filtrar exportação:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.filtro_var = tk.StringVar(value="Todos")
        filtro_frame = tk.Frame(form_frame)
        filtro_frame.grid(row=7, column=1, padx=5, pady=5, sticky="w")
        tk.Radiobutton(filtro_frame, text="Todos", variable=self.filtro_var, value="Todos").pack(side=tk.LEFT)
        tk.Radiobutton(filtro_frame, text="Receita", variable=self.filtro_var, value="Receita").pack(side=tk.LEFT)
        tk.Radiobutton(filtro_frame, text="Despesa", variable=self.filtro_var, value="Despesa").pack(side=tk.LEFT)

        # Botão exportar para CSV
        exportar_btn = tk.Button(form_frame, text="Exportar para CSV", command=self.exportar_para_csv)
        exportar_btn.grid(row=7, column=2, padx=5, pady=10, sticky="e")

        # Configurar as colunas para expandir
        form_frame.columnconfigure(1, weight=1)

        # Atualiza categorias
        self.tipo_var.trace_add("write", self.atualizar_categorias)

    def criar_tabela(self, parent):
        # Frame da tabela
        table_frame = tk.Frame(parent)
        table_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Barra de rolagem
        self.scroll_y = tk.Scrollbar(table_frame, orient="vertical")
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Tabela
        self.table = ttk.Treeview(table_frame, yscrollcommand=self.scroll_y.set, columns=("Tipo", "Valor", "Data", "Categoria", "Descrição"), show="headings")
        self.table.pack(fill=tk.BOTH, expand=True)
        self.scroll_y.config(command=self.table.yview)

        # Definição das colunas
        self.table.heading("Tipo", text="Tipo")
        self.table.heading("Valor", text="Valor")
        self.table.heading("Data", text="Data")
        self.table.heading("Categoria", text="Categoria")
        self.table.heading("Descrição", text="Descrição")
        
        self.table.column("Tipo", width=100)
        self.table.column("Valor", width=100)
        self.table.column("Data", width=100)
        self.table.column("Categoria", width=150)
        self.table.column("Descrição", width=200)

        # Carregar transações
        self.carregar_transacoes()

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
        data = self.data_entry.get_date()  # Usar a data selecionada
        categoria = self.categoria_var.get()
        descricao = self.descricao_entry.get()

        if not valor or not data or not categoria:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        try:
            valor = float(valor)
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")
            return

        categorias = search_query("SELECT id FROM categorias WHERE nome = ?", (categoria,)) 
        if categorias:
            categoria_id = categorias[0][0]
        else:
            messagebox.showerror("Erro", "Categoria não encontrada.")
            return

        execute_query('''INSERT INTO transacoes (tipo, valor, data, categoria_id, descricao) VALUES (?, ?, ?, ?, ?)''',
                      (tipo, valor, data, categoria_id, descricao))

        messagebox.showinfo("Sucesso", "Transação adicionada com sucesso.")
        self.carregar_transacoes()

    def carregar_transacoes(self):
        # Limpa as linhas existentes na tabela
        for row in self.table.get_children():
            self.table.delete(row)
        
        # Consulta SQL qualificada
        query = '''
        SELECT 
            transacoes.tipo, 
            transacoes.valor, 
            transacoes.data, 
            categorias.nome AS categoria, 
            transacoes.descricao 
        FROM 
            transacoes 
        JOIN 
            categorias 
        ON 
            transacoes.categoria_id = categorias.id
        '''
        
        transacoes = search_query(query)
        
        for transacao in transacoes:
            self.table.insert("", tk.END, values=transacao)

    def limpar_campos(self):
        """Limpa todos os campos do formulário."""
        self.tipo_var.set("Receita")
        self.valor_entry.delete(0, tk.END)
        self.data_entry.set_date(datetime.now())
        self.categoria_var.set("")
        self.descricao_entry.delete(0, tk.END)

    def exportar_para_csv(self):
        """Exporta os dados da tabela para um arquivo CSV com base no filtro selecionado."""
        filtro = self.filtro_var.get()

        # Selecionar o arquivo de destino
        file_path = asksaveasfilename(defaultextension=".csv",
                                      filetypes=[("CSV files", "*.csv")],
                                      title="Salvar arquivo como")
        if not file_path:
            return

        # Consulta SQL com filtro
        if filtro == "Todos":
            query = '''
            SELECT 
                transacoes.tipo, 
                transacoes.valor, 
                transacoes.data, 
                categorias.nome AS categoria, 
                transacoes.descricao 
            FROM 
                transacoes 
            JOIN 
                categorias 
            ON 
                transacoes.categoria_id = categorias.id
            '''
        else:
            query = '''
            SELECT 
                transacoes.tipo, 
                transacoes.valor, 
                transacoes.data, 
                categorias.nome AS categoria, 
                transacoes.descricao 
            FROM 
                transacoes 
            JOIN 
                categorias 
            ON 
                transacoes.categoria_id = categorias.id
            WHERE 
                transacoes.tipo = ?
            '''
        
        transacoes = search_query(query, (filtro,) if filtro != "Todos" else ())

        # Salvar em CSV
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Tipo", "Valor", "Data", "Categoria", "Descrição"])
            for transacao in transacoes:
                writer.writerow(transacao)

        messagebox.showinfo("Sucesso", "Dados exportados para CSV com sucesso.")
