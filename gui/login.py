import tkinter as tk
from tkinter import messagebox
from gui.dashboard import Dashboard  # Certifique-se de que o caminho está correto

def mostrar_cadastro():
    root = tk.Tk()
    from gui.cadastro import Cadastro
    Cadastro(root)
    root.mainloop()

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.criar_widgets()

    def criar_widgets(self):
        tk.Label(self.root, text="Usuário:").pack(pady=5)
        self.usuario_entry = tk.Entry(self.root)
        self.usuario_entry.pack(pady=5)

        tk.Label(self.root, text="Senha:").pack(pady=5)
        self.senha_entry = tk.Entry(self.root, show='*')
        self.senha_entry.pack(pady=5)

        login_btn = tk.Button(self.root, text="Login", command=self.login)
        login_btn.pack(pady=10)

        cadastro_btn = tk.Button(self.root, text="Cadastrar", command=self.cadastrar)
        cadastro_btn.pack(pady=5)

    def login(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()
        # Implementar lógica de autenticação
        if usuario and senha:
            # Exemplo de navegação para o Dashboard
            self.root.withdraw()
            dashboard = tk.Toplevel(self.root)
            Dashboard(dashboard)
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def cadastrar(self):
        self.root.withdraw()  # Oculta a tela de login
        mostrar_cadastro()  # Abre a tela de cadastro
