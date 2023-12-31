import tkinter as tk
from tkinter import filedialog
import shutil
from datetime import datetime
import os

class BackupManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Backup")
        self.root.geometry("400x150+400+150")

        self.create_widgets()

    def create_widgets(self):
        # Botão para recuperar backup
        recover_button = tk.Button(self.root, text="Recuperar Backup", command=self.recover_backup)
        recover_button.pack(pady=10)

        # Botão para fazer backup
        backup_button = tk.Button(self.root, text="Fazer Backup", command=self.create_backup)
        backup_button.pack(pady=10)

    def recover_backup(self):
        file_path = filedialog.askopenfilename(title="Escolha o arquivo de backup", filetypes=[("Arquivos de Backup", "*.backup")])

        if file_path:
            try:
                # Renomeia o arquivo escolhido para ocorrencias.db
                shutil.copy(file_path, "ocorrencias.db")
                tk.messagebox.showinfo("Sucesso", "Backup recuperado com sucesso.")
            except Exception as e:
                tk.messagebox.showerror("Erro", f"Erro ao recuperar backup: {e}")

    def create_backup(self):
        # Escolhe o diretório de destino para o backup
        dest_directory = filedialog.askdirectory(title="Escolha o diretório para salvar o backup")

        if dest_directory:
            # Cria uma cópia do arquivo ocorrencias.db com o nome formatado com a data atual no diretório escolhido
            backup_name = os.path.join(dest_directory, f"ocorrencias_{datetime.now().strftime('%Y%m%d%H%M%S')}.backup")
            try:
                shutil.copy("ocorrencias.db", backup_name)
                tk.messagebox.showinfo("Sucesso", f"Backup criado com sucesso: {backup_name}")
            except Exception as e:
                tk.messagebox.showerror("Erro", f"Erro ao criar backup: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupManager(root)
    root.mainloop()
