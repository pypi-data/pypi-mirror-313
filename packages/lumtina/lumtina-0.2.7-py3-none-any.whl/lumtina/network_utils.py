import os
import socket
import requests

def ping_host(host):
    """Pings the specified host and returns the result."""
    response = os.system(f"ping -c 1 {host}")
    if response == 0:
        return f"{host} is reachable."
    else:
        return f"{host} is not reachable."

def get_ip_info(ip_address):
    """Fetches and returns information about the specified IP address."""
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        return response.json()
    except requests.RequestException as e:
        return f"Error fetching IP information: {e}"

def get_local_ip():
    """Returns the local IP address of the machine."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except socket.error as e:
        return f"Error getting local IP: {e}"
