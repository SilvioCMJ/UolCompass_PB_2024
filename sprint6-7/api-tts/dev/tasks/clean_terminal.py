import os

def clean_terminal():
    """Limpa o terminal: Windows/Linux."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

if __name__ == "__main__":
    clean_terminal()