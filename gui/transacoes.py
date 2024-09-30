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
        self.transacao_id = None  # Variável para armazenar o ID da transação a ser atualizada
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

        # Botões Salvar, Limpar e Atualizar
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=6, column=1, padx=5, pady=10, sticky="e")

        salvar_btn = tk.Button(btn_frame, text="Salvar", command=self.salvar)
        salvar_btn.pack(side=tk.LEFT, padx=5)

        limpar_btn = tk.Button(btn_frame, text="Limpar", command=self.limpar_campos)
        limpar_btn.pack(side=tk.LEFT, padx=5)

        atualizar_btn = tk.Button(btn_frame, text="Atualizar", command=self.atualizar, state=tk.DISABLED)
        atualizar_btn.pack(side=tk.LEFT, padx=5)
        self.atualizar_btn = atualizar_btn  # Guardar referência do botão para habilitar/desabilitar

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

        # Evento de seleção na tabela
        self.table.bind("<<TreeviewSelect>>", self.preencher_campos)

    def carregar_categorias(self):
        tipo = self.tipo_var.get()
        try:
            categorias = search_query("SELECT nome FROM categorias WHERE tipo = ?", (tipo,))
            self.categoria_combo['values'] = [c[0] for c in categorias]
            if categorias:
                self.categoria_combo.current(0)
        except Exception as e:
            messagebox.showerror("Erro ao carregar categorias", str(e))

    def atualizar_categorias(self, *args):
        self.carregar_categorias()

    def preencher_campos(self, event):
        """Preenche os campos com os dados da transação selecionada."""
        selected_item = self.table.selection()
        if selected_item:
            item_data = self.table.item(selected_item, 'values')
            tipo, valor, data, categoria, descricao = item_data

            # Preencher os campos
            self.tipo_var.set(tipo)
            self.valor_entry.delete(0, tk.END)
            self.valor_entry.insert(0, valor)
            self.data_entry.set_date(datetime.strptime(data, "%Y-%m-%d"))
            self.categoria_var.set(categoria)
            self.descricao_entry.delete(0, tk.END)
            self.descricao_entry.insert(0, descricao)

            # Ativar o botão de atualizar
            self.atualizar_btn.config(state=tk.NORMAL)

            # Definir a transação atual para atualizar
            transacao_info = search_query('''SELECT id FROM transacoes WHERE tipo = ? AND valor = ? AND data = ? AND descricao = ?''',
                                          (tipo, valor, data, descricao))
            if transacao_info:
                self.transacao_id = transacao_info[0][0]

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
            execute_query(
                "INSERT INTO transacoes (tipo, valor, data, categoria_id, descricao) VALUES (?, ?, ?, (SELECT id FROM categorias WHERE nome = ?), ?)",
                (tipo, valor, data, categoria, descricao)
            )
            messagebox.showinfo("Sucesso", "Transação salva com sucesso.")
            self.limpar_campos()
            self.carregar_transacoes()
        except Exception as e:
            messagebox.showerror("Erro ao salvar transação", str(e))

    def atualizar(self):
        """Atualiza a transação selecionada com os dados inseridos no formulário."""
        if self.transacao_id is None:
            messagebox.showerror("Erro", "Nenhuma transação selecionada para atualização.")
            return

        tipo = self.tipo_var.get()
        valor = self.valor_entry.get()
        data = self.data_entry.get_date()  # Usar a data selecionada
        categoria = self.categoria_var.get()
        descricao = self.descricao_entry.get()

        if not valor or not data or not categoria:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        try:
            execute_query(
                "UPDATE transacoes SET tipo = ?, valor = ?, data = ?, categoria_id = (SELECT id FROM categorias WHERE nome = ?), descricao = ? WHERE id = ?",
                (tipo, valor, data, categoria, descricao, self.transacao_id)
            )
            messagebox.showinfo("Sucesso", "Transação atualizada com sucesso.")
            self.limpar_campos()
            self.carregar_transacoes()
        except Exception as e:
            messagebox.showerror("Erro ao atualizar transação", str(e))

    def carregar_transacoes(self):
        """Carrega as transações da base de dados e exibe na tabela."""
        try:
            transacoes = search_query('''
                SELECT t.tipo, t.valor, t.data, c.nome AS categoria, t.descricao
                FROM transacoes t
                JOIN categorias c ON t.categoria_id = c.id
            ''')
            self.table.delete(*self.table.get_children())
            for transacao in transacoes:
                self.table.insert("", tk.END, values=transacao)
        except Exception as e:
            messagebox.showerror("Erro ao carregar transações", str(e))

    def limpar_campos(self):
        """Limpa os campos do formulário."""
        self.tipo_var.set("Receita")
        self.valor_entry.delete(0, tk.END)
        self.data_entry.set_date(datetime.today())
        self.categoria_var.set('')
        self.descricao_entry.delete(0, tk.END)

        # Desabilitar botão de atualizar
        self.atualizar_btn.config(state=tk.DISABLED)

        # Resetar a transação ID
        self.transacao_id = None

    def exportar_para_csv(self):
        filtro = self.filtro_var.get()

        try:
            if filtro == "Todos":
                transacoes = search_query('''
                    SELECT t.tipo, t.valor, t.data, c.nome AS categoria, t.descricao
                    FROM transacoes t
                    JOIN categorias c ON t.categoria_id = c.id
                ''')
            else:
                transacoes = search_query('''
                    SELECT t.tipo, t.valor, t.data, c.nome AS categoria, t.descricao
                    FROM transacoes t
                    JOIN categorias c ON t.categoria_id = c.id
                    WHERE t.tipo = ?
                ''', (filtro,))

            if not transacoes:
                messagebox.showinfo("Sem dados", "Não há transações para exportar.")
                return

            # Abrir diálogo para salvar o arquivo CSV
            file_path = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if not file_path:
                return

            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Tipo", "Valor", "Data", "Categoria", "Descrição"])
                writer.writerows(transacoes)

            messagebox.showinfo("Sucesso", f"Transações exportadas com sucesso para {file_path}")
        except Exception as e:
            messagebox.showerror("Erro ao exportar", str(e))
