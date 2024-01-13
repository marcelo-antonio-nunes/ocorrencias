import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import time
import webbrowser

def execute_commands():
    # # Atualiza o pip
    subprocess.run(["python.exe", "-m", "pip", "install", "--upgrade", "pip"])
    url = "http://127.0.0.1:5000/"
    webbrowser.open(url)
    # Instala as dependências do arquivo requirements.txt
    subprocess.run(["pip", "install", "-r", "requirements.txt"])
    subprocess.run(["python", "main.py"])

    
execute_commands()
