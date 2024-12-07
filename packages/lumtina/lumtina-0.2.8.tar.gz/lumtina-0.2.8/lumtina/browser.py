import webbrowser

def browser(link):
    """Opens a URL in the default web browser."""
    try:
        webbrowser.open(link)
        print(f"Opened {link} in the default browser.")
    except Exception as e:
        print(f"Error opening the link: {e}")
