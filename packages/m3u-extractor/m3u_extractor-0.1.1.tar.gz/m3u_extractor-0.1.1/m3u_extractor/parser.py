import re

def parse_m3u_content(content):
    """
    Parses M3U content and extracts relevant data.

    Args:
        content (str): The raw M3U content.

    Returns:
        list: A list of dictionaries containing parsed data.
    """
    pattern = r'#EXTINF:-1.*?tvg-name="(.*?)".*?tvg-logo="(.*?)".*?,(.*?)\n(http[^\r\n]+)'
    matches = re.findall(pattern, content)

    # Convert matches to structured data
    extracted_data = []
    for match in matches:
        extracted_data.append({
            "name": match[0],
            "logo": match[1],
            "stream_url": match[3]
        })
    return extracted_data