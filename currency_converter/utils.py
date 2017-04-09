import re


def clean_string(string):
    """
    Make the strings easily comparable by removing non alphanumerical
    and change to lower characters

    Args:
        string: (str) string to clean
    Returns:
        (str) cleaned string
    """
    string = re.sub('[^A-Za-z0-9]+', ' ', string)
    string = string.lower()
    string = ' '.join(string.split())
    return string