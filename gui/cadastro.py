import tkinter as tk
from tkinter import messagebox
from database import execute_query

def mostrar_login():
    try:
        root = tk.Tk()
        from gui.login import Login
        Login(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir a janela de login: {e}")

class Cadastro:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro")
        try:
            self.centralizar_janela(300, 300)  # Chamar a função para centralizar a janela
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao centralizar a janela: {e}")
        self.root.resizable(False, False)
        self.criar_widgets()

    def criar_widgets(self):
        tk.Label(self.root, text="Usuário:").pack(pady=5)
        self.usuario_entry = tk.Entry(self.root)
        self.usuario_entry.pack(pady=5)

        tk.Label(self.root, text="Senha:").pack(pady=5)
        self.senha_entry = tk.Entry(self.root, show='*')
        self.senha_entry.pack(pady=5)

        tk.Label(self.root, text="Confirmar Senha:").pack(pady=5)
        self.confirmar_senha_entry = tk.Entry(self.root, show='*')
        self.confirmar_senha_entry.pack(pady=5)

        cadastro_btn = tk.Button(self.root, text="Cadastrar", command=self.cadastrar)
        cadastro_btn.pack(pady=10)

        voltar_btn = tk.Button(self.root, text="Voltar", command=self.voltar)
        voltar_btn.pack(pady=5)

    def cadastrar(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()
        confirmar_senha = self.confirmar_senha_entry.get()

        if not usuario or not senha or not confirmar_senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        if senha != confirmar_senha:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return

        try:
            execute_query("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            self.root.destroy()
            mostrar_login()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {e}")

    def voltar(self):
        try:
            self.root.destroy()
            mostrar_login()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao voltar para a tela de login: {e}")

    def centralizar_janela(self, largura, altura):
        """Centraliza a janela no centro da tela"""
        try:
            largura_tela = self.root.winfo_screenwidth()
            altura_tela = self.root.winfo_screenheight()
            pos_x = (largura_tela // 2) - (largura // 2)
            pos_y = (altura_tela // 2) - (altura // 2)
            self.root.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
        except Exception as e:
            raise RuntimeError(f"Erro ao calcular a posição da janela: {e}")
