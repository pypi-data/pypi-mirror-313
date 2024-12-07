import os

def clear_console():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')  # Use 'cls' for Windows, 'clear' for Unix