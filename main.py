import tkinter as tk
from gui.login import Login  # Certifique-se de que o caminho está correto

def main():
    root = tk.Tk()
    root.geometry("300x250")
    root.title("Login")
    Login(root)
    root.mainloop()

if __name__ == "__main__":
    main()
