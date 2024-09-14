import tkinter as tk
from tkinter import ttk
from gui.transacoes import Transacoes
from gui.categorias import Categorias
from gui.relatorios import Relatorios
from gui.orcamentos import Orcamentos

class Dashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Dashboard")

        # Cria os botões para acessar outras telas
        self.create_widgets()

    def create_widgets(self):
        ttk.Button(self.master, text="Transações", command=self.abrir_transacoes).pack(pady=10)
        ttk.Button(self.master, text="Categorias", command=self.abrir_categorias).pack(pady=10)
        ttk.Button(self.master, text="Relatórios", command=self.abrir_relatorios).pack(pady=10)
        ttk.Button(self.master, text="Orçamentos", command=self.abrir_orcamentos).pack(pady=10)

    def abrir_transacoes(self):
        transacoes_window = tk.Toplevel(self.master)
        Transacoes(transacoes_window)

    def abrir_categorias(self):
        categorias_window = tk.Toplevel(self.master)
        Categorias(categorias_window)

    def abrir_relatorios(self):
        relatorios_window = tk.Toplevel(self.master)
        Relatorios(relatorios_window)

    def abrir_orcamentos(self):
        orcamentos_window = tk.Toplevel(self.master)
        Orcamentos(orcamentos_window)
