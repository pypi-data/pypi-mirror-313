import colorama
from colorama import Fore, Style

# Inizializza colorama
colorama.init()

def color(message, text_color="white"):
    colors = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
        "black": Fore.BLACK
    }

    # Imposta il colore predefinito se non è valido
    color_code = colors.get(text_color.lower(), Fore.WHITE)

    # Stampa il messaggio colorato
    print(color_code + message + Style.RESET_ALL)
