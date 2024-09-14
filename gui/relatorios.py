import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from utils.graficos import gerar_grafico_transacoes

class Relatorios:
    def __init__(self, parent):
        self.parent = parent
        self.janela = tk.Frame(parent)
        self.janela.pack(fill=tk.BOTH, expand=True)
        self.criar_widgets()

    def criar_widgets(self):
        # Título no canto esquerdo
        title_frame = tk.Frame(self.janela)
        title_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(title_frame, text="Relatórios", font=("Arial", 16)).pack(side=tk.LEFT)
        
        # Frame para as datas e seus textos
        periodo_frame = tk.Frame(self.janela)
        periodo_frame.pack(pady=5, padx=10, anchor='w')  # 'w' alinha à esquerda
        
        # Texto e campo de Data Início
        tk.Label(periodo_frame, text="Data Início:").pack(side=tk.LEFT, padx=(0, 5))
        self.inicio_entry = DateEntry(periodo_frame, width=12, date_pattern='yyyy-mm-dd')
        self.inicio_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        # Texto e campo de Data Fim
        tk.Label(periodo_frame, text="Data Fim:").pack(side=tk.LEFT, padx=(0, 5))
        self.fim_entry = DateEntry(periodo_frame, width=12, date_pattern='yyyy-mm-dd')
        self.fim_entry.pack(side=tk.LEFT)
        
        # Botão para gerar relatório
        gerar_btn = tk.Button(self.janela, text="Gerar Relatório", command=self.gerar_relatorio)
        gerar_btn.pack(pady=10)

    def gerar_relatorio(self):
        inicio = self.inicio_entry.get()
        fim = self.fim_entry.get()
        
        # Limpar widgets anteriores e exibir novo conteúdo
        for widget in self.janela.winfo_children():
            widget.destroy()
        
        tk.Label(self.janela, text=f"Relatório de {inicio} a {fim}", font=("Arial", 16)).pack(pady=10)
        gerar_grafico_transacoes(self.janela)

    # Funções de placeholder para o campo "Data Início"
    def on_entry_click_inicial(self, event):
        if self.inicio_entry.get() == self.inicio_placeholder:
            self.inicio_entry.delete(0, "end")
            self.inicio_entry.config(fg='black')

    def on_focusout_inicial(self, event):
        if self.inicio_entry.get() == "":
            self.inicio_entry.insert(0, self.inicio_placeholder)
            self.inicio_entry.config(fg='grey')

    # Funções de placeholder para o campo "Data Fim"
    def on_entry_click_fim(self, event):
        if self.fim_entry.get() == self.fim_placeholder:
            self.fim_entry.delete(0, "end")
            self.fim_entry.config(fg='black')

    def on_focusout_fim(self, event):
        if self.fim_entry.get() == "":
            self.fim_entry.insert(0, self.fim_placeholder)
            self.fim_entry.config(fg='grey')
