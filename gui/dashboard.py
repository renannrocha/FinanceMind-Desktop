import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.graficos import gerar_grafico_transacoes, gerar_grafico_despesas, gerar_grafico_receitas
from gui.transacoes import AdicionarTransacao
from gui.categorias import GerenciarCategorias
from gui.relatorios import Relatorios
from gui.orcamentos import Orcamentos

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("FinanceMind")
        self.centralizar_janela(1200, 800)  # Chamar a função para centralizar a janela
        self.root.resizable(False, False)
        self.conteudo_atual = None
        self.criar_widgets()

    def criar_widgets(self):
        menu = tk.Frame(self.root, bd=1, relief=tk.SUNKEN)
        menu.pack(side=tk.TOP, fill=tk.X)

        tk.Button(menu, text="Dashboard", command=self.mostrar_dashboard).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(menu, text="Adicionar Transação", command=self.adicionar_transacao).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(menu, text="Gerenciar Categorias", command=self.gerenciar_categorias).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(menu, text="Relatórios", command=self.gerar_relatorios).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(menu, text="Orçamentos", command=self.gerenciar_orcamentos).pack(side=tk.LEFT, padx=10, pady=5)

        separador = ttk.Separator(self.root, orient='horizontal')
        separador.pack(fill=tk.X, pady=5)

        self.conteudo = tk.Frame(self.root)
        self.conteudo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.mostrar_dashboard()

    def mostrar_dashboard(self):
        self.fechar_tela()
        self.trocar_tela(self.mostrar_dashboard)

        tk.Label(self.conteudo, text="Visão Geral das Finanças", font=("Arial", 16)).pack(pady=10)

        frame_graficos = tk.Frame(self.conteudo)
        frame_graficos.pack(pady=10, fill=tk.BOTH, expand=True)

        # Gerar e exibir gráficos
        fig_despesas = gerar_grafico_despesas()
        canvas_despesas = FigureCanvasTkAgg(fig_despesas, master=frame_graficos)
        canvas_despesas.draw()
        canvas_despesas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        fig_receitas = gerar_grafico_receitas()
        canvas_receitas = FigureCanvasTkAgg(fig_receitas, master=frame_graficos)
        canvas_receitas.draw()
        canvas_receitas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        fig_transacoes = gerar_grafico_transacoes()
        canvas_transacoes = FigureCanvasTkAgg(fig_transacoes, master=frame_graficos)
        canvas_transacoes.draw()
        canvas_transacoes.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

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
            for widget in self.conteudo.winfo_children():
                widget.destroy()
            self.conteudo_atual = nova_tela

    def fechar_tela(self):
        """Fecha a tela atual destruindo todos os widgets do conteúdo."""
        if self.conteudo_atual is not None:
            for widget in self.conteudo.winfo_children():
                widget.destroy()
            self.conteudo_atual = None

    def centralizar_janela(self, largura, altura):
        """Centraliza a janela no centro da tela"""
        largura_tela = self.root.winfo_screenwidth()  # Largura total da tela
        altura_tela = self.root.winfo_screenheight()  # Altura total da tela
        pos_x = (largura_tela // 2) - (largura // 2)  # Cálculo da posição X
        pos_y = (altura_tela // 2) - (altura // 2)  # Cálculo da posição Y
        self.root.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
