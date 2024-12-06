import requests

def fetch_m3u_content(url):
    """
    Fetches M3U content from a URL.

    Args:
        url (str): The URL to fetch the M3U content.

    Returns:
        str: The content of the M3U file as a string.

    Raises:
        requests.exceptions.RequestException: If there's an error during the request.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.content.decode("utf-8")