import json

def format_to_json(data):
    """
    Formats data into a JSON string.

    Args:
        data (list): The data to format.

    Returns:
        str: The JSON string representation of the data.
    """
    return json.dumps(data, indent=4)