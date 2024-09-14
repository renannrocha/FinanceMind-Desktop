import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import execute_query, search_query

class GerenciarCategorias:
    def __init__(self, parent):
        self.parent = parent
        self.janela = tk.Frame(parent)
        self.janela.pack(fill=tk.BOTH, expand=True)
        self.criar_widgets()

    def criar_widgets(self):
        tk.Label(self.janela, text="Gerenciar Categorias", font=("Arial", 16)).pack(pady=10)

        self.categorias_list = tk.Listbox(self.janela)
        self.categorias_list.pack(pady=10, fill=tk.BOTH, expand=True)
        self.carregar_categorias()

        adicionar_btn = tk.Button(self.janela, text="Adicionar Categoria", command=self.adicionar_categoria)
        adicionar_btn.pack(pady=5)

        editar_btn = tk.Button(self.janela, text="Editar Categoria", command=self.editar_categoria)
        editar_btn.pack(pady=5)

        excluir_btn = tk.Button(self.janela, text="Excluir Categoria", command=self.excluir_categoria)
        excluir_btn.pack(pady=5)

    def carregar_categorias(self):
        self.categorias_list.delete(0, tk.END)
        categorias = search_query("SELECT nome FROM categorias")
        for categoria in categorias:
            self.categorias_list.insert(tk.END, categoria[0])

    def adicionar_categoria(self):
        nome = self.ask_user_input("Adicionar Categoria", "Nome da Categoria:")
        if nome:
            tipo = self.ask_user_input("Adicionar Categoria", "Tipo (Receita/Despesa):")
            if tipo in ['Receita', 'Despesa']:
                execute_query("INSERT INTO categorias (nome, tipo) VALUES (?, ?)", (nome, tipo))
                self.carregar_categorias()
                messagebox.showinfo("Sucesso", "Categoria adicionada com sucesso.")
            else:
                messagebox.showerror("Erro", "Tipo inválido. Deve ser 'Receita' ou 'Despesa'.")

    def editar_categoria(self):
        selecionado = self.categorias_list.curselection()
        if selecionado:
            nome_antigo = self.categorias_list.get(selecionado)
            novo_nome = self.ask_user_input("Editar Categoria", "Novo Nome da Categoria:")
            if novo_nome:
                novo_tipo = self.ask_user_input("Editar Categoria", "Novo Tipo (Receita/Despesa):")
                if novo_tipo in ['Receita', 'Despesa']:
                    execute_query("UPDATE categorias SET nome = ?, tipo = ? WHERE nome = ?", (novo_nome, novo_tipo, nome_antigo))
                    self.carregar_categorias()
                    messagebox.showinfo("Sucesso", "Categoria atualizada com sucesso.")
                else:
                    messagebox.showerror("Erro", "Tipo inválido. Deve ser 'Receita' ou 'Despesa'.")
        else:
            messagebox.showwarning("Aviso", "Selecione uma categoria para editar.")

    def excluir_categoria(self):
        selecionado = self.categorias_list.curselection()
        if selecionado:
            nome = self.categorias_list.get(selecionado)
            execute_query("DELETE FROM categorias WHERE nome = ?", (nome,))
            self.carregar_categorias()
            messagebox.showinfo("Sucesso", "Categoria excluída com sucesso.")
        else:
            messagebox.showwarning("Aviso", "Selecione uma categoria para excluir.")

    def ask_user_input(self, title, prompt):
        user_input = simpledialog.askstring(title, prompt, parent=self.master)
        return user_input

    def destruir(self):
        """ Método que destrói o frame quando a aba é trocada """
        self.janela.destroy()
