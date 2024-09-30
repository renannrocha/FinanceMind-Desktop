import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from utils.graficos import gerar_grafico_despesas, gerar_grafico_receitas
from utils.exportar import exportar_para_pdf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Relatorios:
    def __init__(self, parent):
        self.parent = parent
        self.janela = tk.Frame(parent)
        self.janela.pack(fill=tk.BOTH, expand=True)
        self.criar_widgets()

    def criar_widgets(self):
        title_frame = tk.Frame(self.janela)
        title_frame.pack(fill=tk.X, pady=10)

        tk.Label(title_frame, text="Relatórios", font=("Arial", 16)).pack(side=tk.TOP, anchor='center')

        periodo_frame = tk.Frame(self.janela)
        periodo_frame.pack(pady=5, padx=10, anchor='center')

        tk.Label(periodo_frame, text="Data Início:").grid(row=0, column=0, padx=(0, 5), pady=5, sticky='e')
        self.inicio_entry = DateEntry(periodo_frame, width=12, date_pattern='yyyy-mm-dd')
        self.inicio_entry.grid(row=0, column=1, padx=(0, 20), pady=5, sticky='w')

        tk.Label(periodo_frame, text="Data Fim:").grid(row=0, column=2, padx=(0, 5), pady=5, sticky='e')
        self.fim_entry = DateEntry(periodo_frame, width=12, date_pattern='yyyy-mm-dd')
        self.fim_entry.grid(row=0, column=3, padx=(0, 20), pady=5, sticky='w')

        # Configurar as colunas para centralizar
        periodo_frame.columnconfigure(0, weight=1)
        periodo_frame.columnconfigure(1, weight=1)
        periodo_frame.columnconfigure(2, weight=1)
        periodo_frame.columnconfigure(3, weight=1)

        # Botão para gerar relatório
        gerar_btn = tk.Button(self.janela, text="Gerar Relatório", command=self.gerar_relatorio)
        gerar_btn.pack(pady=10)

        # Frame para os gráficos com scrollbar
        self.frame_graficos = tk.Frame(self.janela)
        self.frame_graficos.pack(fill=tk.BOTH, expand=True)

        self.canvas_scroll = tk.Canvas(self.frame_graficos)
        self.canvas_scroll.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.frame_graficos, orient="vertical", command=self.canvas_scroll.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_scroll.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_scroll.bind('<Configure>', lambda e: self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all")))

        self.scrollable_frame = tk.Frame(self.canvas_scroll)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all")))
        self.canvas_scroll.create_window((0, 0), window=self.scrollable_frame, anchor="n")

    def gerar_relatorio(self):
        inicio = self.inicio_entry.get()
        fim = self.fim_entry.get()

        # Limpar os gráficos antigos, mas manter os campos de entrada e botões
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Título do Relatório
        tk.Label(self.scrollable_frame, text=f"Relatório de {inicio} a {fim}", font=("Arial", 16)).pack(pady=10, anchor='center')

        # Gerar e exibir gráficos com título e descrição
        self.adicionar_grafico("Despesas", gerar_grafico_despesas, f"Despesas de {inicio} a {fim}")
        self.adicionar_grafico("Receitas", gerar_grafico_receitas, f"Receitas de {inicio} a {fim}")

        # Botão para exportar PDF
        exportar_btn = tk.Button(self.scrollable_frame, text="Exportar para PDF", command=lambda: exportar_para_pdf(inicio, fim))
        exportar_btn.pack(pady=10, anchor='center')

    def adicionar_grafico(self, titulo, funcao_gerar_grafico, descricao):
        """Função auxiliar para adicionar gráficos com títulos e descrições."""
        # Frame para centralizar conteúdo, com preenchimento horizontal
        grafico_frame = tk.Frame(self.scrollable_frame)
        grafico_frame.pack(fill=tk.X, expand=True, pady=10)  # fill=tk.X para usar toda a largura

        # Título do gráfico
        tk.Label(grafico_frame, text=titulo, font=("Arial", 14)).pack(pady=5, anchor='center')

        # Descrição do gráfico
        tk.Label(grafico_frame, text=descricao, font=("Arial", 10)).pack(pady=5, anchor='center')

        # Gerar gráfico
        fig = funcao_gerar_grafico()
        canvas = FigureCanvasTkAgg(fig, master=grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Preencher horizontal e verticalmente
