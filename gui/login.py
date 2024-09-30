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
        self.centralizar_janela(300, 200)  # Chamar a função para centralizar a janela
        self.root.resizable(False, False)
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
        if usuario and senha:
            self.root.withdraw()
            dashboard = tk.Toplevel(self.root)
            Dashboard(dashboard)
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def cadastrar(self):
        self.root.withdraw()
        mostrar_cadastro()
    
    def centralizar_janela(self, largura, altura):
        """Centraliza a janela no centro da tela"""
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura // 2) 
        pos_y = (altura_tela // 2) - (altura // 2) 
        self.root.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
