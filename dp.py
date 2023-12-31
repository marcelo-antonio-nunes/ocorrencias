# install_dependencies.py
import subprocess

def install_requirements():
    try:
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
        print("Dependências instaladas com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar as dependências: {e}")
        
if __name__ == "__main__":
    install_requirements()
