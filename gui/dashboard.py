import tkinter as tk
from tkinter import ttk
from gui.transacoes import AdicionarTransacao
from gui.categorias import GerenciarCategorias
from gui.relatorios import Relatorios
from gui.orcamentos import Orcamentos
from utils.graficos import gerar_grafico_transacoes

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.criar_widgets()

    def criar_widgets(self):
        menu = tk.Frame(self.root)
        menu.pack(side=tk.LEFT, fill=tk.Y)

        tk.Button(menu, text="Dashboard", command=self.mostrar_dashboard).pack(pady=5)
        tk.Button(menu, text="Adicionar Transação", command=self.adicionar_transacao).pack(pady=5)
        tk.Button(menu, text="Gerenciar Categorias", command=self.gerenciar_categorias).pack(pady=5)
        tk.Button(menu, text="Relatórios", command=self.gerar_relatorios).pack(pady=5)
        tk.Button(menu, text="Orçamentos", command=self.gerenciar_orcamentos).pack(pady=5)

        self.conteudo = tk.Frame(self.root)
        self.conteudo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.mostrar_dashboard()

    def mostrar_dashboard(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

        tk.Label(self.conteudo, text="Visão Geral das Finanças", font=("Arial", 16)).pack(pady=10)

        frame_graficos = tk.Frame(self.conteudo)
        frame_graficos.pack(pady=10, fill=tk.BOTH, expand=True)

        gerar_grafico_transacoes(frame_graficos)

    def adicionar_transacao(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()
        AdicionarTransacao(self.conteudo)

    def gerenciar_categorias(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()
        GerenciarCategorias(self.conteudo)

    def gerar_relatorios(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()
        Relatorios(self.conteudo)

    def gerenciar_orcamentos(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()
        Orcamentos(self.conteudo)
