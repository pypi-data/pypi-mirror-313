from datetime import datetime

def date():
    """Restituisce la data corrente in formato 'YYYY-MM-DD'."""
    return datetime.now().strftime("%Y-%m-%d")

def hour():
    """Restituisce l'ora corrente in formato 'HH:MM:SS'."""
    return datetime.now().strftime("%H:%M:%S")
