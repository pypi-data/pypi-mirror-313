import colorama
from colorama import Fore, Style

# Inizializza colorama
colorama.init()

def log(message, log_type="info"):
    if log_type == "info":
        print(Fore.GREEN + "" + message + Style.RESET_ALL)
    elif log_type == "warning":
        print(Fore.YELLOW + "[WARNING] " + message + Style.RESET_ALL)
    elif log_type == "error":
        print(Fore.RED + "[ERROR] " + message + Style.RESET_ALL)
    else:
        print(Fore.WHITE + "[LOG] " + message + Style.RESET_ALL)
