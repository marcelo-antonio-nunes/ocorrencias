import tkinter as tk
from tkinter import messagebox
import subprocess
import os

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login App")
        self.root.geometry("300x200+500+200")

        # Variáveis para armazenar nome e senha
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Elementos da interface gráfica
        self.label_username = tk.Label(root, text="Nome de Usuário:")
        self.label_password = tk.Label(root, text="Senha:")

        self.entry_username = tk.Entry(root, textvariable=self.username_var)
        self.entry_password = tk.Entry(root, textvariable=self.password_var, show="*")

        self.button_login = tk.Button(root, text="Login", command=self.login, width=10, height=1)
        self.rounded_button(self.button_login)

        # Posicionamento centralizado dos elementos na tela
        self.label_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        self.label_password.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        self.button_login.grid(row=2, column=0, columnspan=2, pady=20, sticky=tk.NSEW)

        # Configuração do layout para centralizar
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        # Verificação de usuário e senha
        if username == "Marcelo" and password == "1975":
            messagebox.showinfo("Login", f"Bem-vindo, {username}!")
            # Abre a main.py 
            subprocess.Popen("py main.py")
            # Fecha a janela de login
            self.root.destroy()
        else:
            messagebox.showerror("Erro de Login", "Nome de usuário ou senha incorretos.")
            self.password_var.set("")
            self.username_var.set("")
            

    def rounded_button(self, button):
        button.config(relief=tk.GROOVE, bd=3, borderwidth=2, padx=5, pady=5, command=self.login)
        button.bind("<Enter>", lambda e: self.on_enter(button))
        button.bind("<Leave>", lambda e: self.on_leave(button))

    def on_enter(self, widget):
        widget.config(bg="lightgray")

    def on_leave(self, widget):
        widget.config(bg="white")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
