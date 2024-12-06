from .fetcher import fetch_m3u_content
from .parser import parse_m3u_content
from .formatter import format_to_json

def extract_m3u_data(url):
    """
    Main function to fetch, parse, and format M3U data.

    Args:
        url (str): The URL to fetch the M3U file.

    Returns:
        str: A JSON string containing the extracted data.
    """
    try:
        # Step 1: Fetch content
        content = fetch_m3u_content(url)

        # Step 2: Parse content
        parsed_data = parse_m3u_content(content)

        # Step 3: Format data to JSON
        return format_to_json(parsed_data)

    except Exception as e:
        return format_to_json({"error": str(e)})