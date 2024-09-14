import tkinter as tk
from gui.login import Login

def main():
    root = tk.Tk()
    root.geometry("500x300")
    root.title("Login")
    Login(root)
    root.mainloop()

if __name__ == "__main__":
    main()
