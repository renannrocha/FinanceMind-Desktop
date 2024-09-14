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
        self.root.title("FinanceMind")
        self.conteudo_atual = None  # Variável para rastrear a tela atual
        self.criar_widgets()

    def criar_widgets(self):
        # Criar um frame para o menu superior
        menu = tk.Frame(self.root, bd=1, relief=tk.SUNKEN)  # Borda para separar o menu
        menu.pack(side=tk.TOP, fill=tk.X)

        # Botões no menu superior
        tk.Button(menu, text="Dashboard", command=self.mostrar_dashboard).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(menu, text="Adicionar Transação", command=self.adicionar_transacao).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(menu, text="Gerenciar Categorias", command=self.gerenciar_categorias).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(menu, text="Relatórios", command=self.gerar_relatorios).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(menu, text="Orçamentos", command=self.gerenciar_orcamentos).pack(side=tk.LEFT, padx=10, pady=5)

        # Criar uma linha divisória abaixo do menu
        separador = ttk.Separator(self.root, orient='horizontal')
        separador.pack(fill=tk.X, pady=5)

        # Frame para o conteúdo principal
        self.conteudo = tk.Frame(self.root)
        self.conteudo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.mostrar_dashboard()

    def mostrar_dashboard(self):
        self.fechar_tela()
        self.trocar_tela(self.mostrar_dashboard)
        
        tk.Label(self.conteudo, text="Visão Geral das Finanças", font=("Arial", 16)).pack(pady=10)

        frame_graficos = tk.Frame(self.conteudo)
        frame_graficos.pack(pady=10, fill=tk.BOTH, expand=True)

        gerar_grafico_transacoes(frame_graficos)

    def adicionar_transacao(self):
        self.fechar_tela()
        self.trocar_tela(self.adicionar_transacao)
        AdicionarTransacao(self.conteudo)

    def gerenciar_categorias(self):
        self.fechar_tela()
        self.trocar_tela(self.gerenciar_categorias)
        GerenciarCategorias(self.conteudo)

    def gerar_relatorios(self):
        self.fechar_tela()
        self.trocar_tela(self.gerar_relatorios)
        Relatorios(self.conteudo)

    def gerenciar_orcamentos(self):
        self.fechar_tela()
        self.trocar_tela(self.gerenciar_orcamentos)
        Orcamentos(self.conteudo)

    def trocar_tela(self, nova_tela):
        """Remove os widgets da tela atual e carrega a nova tela."""
        if self.conteudo_atual != nova_tela:
            # Destrói o conteúdo da tela atual
            for widget in self.conteudo.winfo_children():
                widget.destroy()
            self.conteudo_atual = nova_tela

    def fechar_tela(self):
        """Fecha a tela atual destruindo todos os widgets do conteúdo."""
        if self.conteudo_atual is not None:
            for widget in self.conteudo.winfo_children():
                widget.destroy()  # Remove todos os widgets da tela
            self.conteudo_atual = None  # Reseta a variável de conteúdo atual
