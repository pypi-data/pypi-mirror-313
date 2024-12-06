import time
import requests

def fetch_urls(urls):
    """Fetches the content from a list of URLs and returns a dictionary with the URL and its content."""
    results = {}  # Create a dictionary to hold the results
    for url in urls:
        try:
            response = requests.get(url)  # Send a GET request to the URL
            if response.status_code == 200:
                results[url] = response.text  # Store the content if the request was successful
            else:
                results[url] = f"Error: {response.status_code}"  # Store the error status code
        except requests.exceptions.RequestException as e:
            results[url] = f"Request failed: {e}"  # Store the error message if a request fails
    return results  # Return the dictionary with results