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
        
        tk.Label(title_frame, text="Relatórios", font=("Arial", 16)).pack(side=tk.LEFT)
        
        periodo_frame = tk.Frame(self.janela)
        periodo_frame.pack(pady=5, padx=10, anchor='w')
        
        tk.Label(periodo_frame, text="Data Início:").pack(side=tk.LEFT, padx=(0, 5))
        self.inicio_entry = DateEntry(periodo_frame, width=12, date_pattern='yyyy-mm-dd')
        self.inicio_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(periodo_frame, text="Data Fim:").pack(side=tk.LEFT, padx=(0, 5))
        self.fim_entry = DateEntry(periodo_frame, width=12, date_pattern='yyyy-mm-dd')
        self.fim_entry.pack(side=tk.LEFT)
        
        gerar_btn = tk.Button(self.janela, text="Gerar Relatório", command=self.gerar_relatorio)
        gerar_btn.pack(pady=10)

    def gerar_relatorio(self):
        inicio = self.inicio_entry.get()
        fim = self.fim_entry.get()
        
        # Limpar widgets anteriores e exibir novo conteúdo
        for widget in self.janela.winfo_children():
            widget.destroy()
        
        tk.Label(self.janela, text=f"Relatório de {inicio} a {fim}", font=("Arial", 16)).pack(pady=10)

        # Gerar e exibir gráficos
        frame_graficos = tk.Frame(self.janela)
        frame_graficos.pack(pady=10, fill=tk.BOTH, expand=True)
        
        fig_despesas = gerar_grafico_despesas()
        canvas_despesas = FigureCanvasTkAgg(fig_despesas, master=frame_graficos)
        canvas_despesas.draw()
        canvas_despesas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        fig_receitas = gerar_grafico_receitas()
        canvas_receitas = FigureCanvasTkAgg(fig_receitas, master=frame_graficos)
        canvas_receitas.draw()
        canvas_receitas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adicionar botão para exportar PDF
        exportar_btn = tk.Button(self.janela, text="Exportar para PDF", command=lambda: exportar_para_pdf(inicio, fim))
        exportar_btn.pack(pady=10)
