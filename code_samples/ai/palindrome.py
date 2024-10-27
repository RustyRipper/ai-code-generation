# ai_palindrome.py

def is_palindrome(s):
    """
    Check if a given string is a palindrome.

    Parameters:
    s (str): The string to check.

    Returns:
    bool: True if the string is a palindrome, False otherwise.
    """
    # Normalize the string by removing non-alphanumeric characters and converting to lowercase
    s = ''.join(filter(str.isalnum, s)).lower()
    return s == s[::-1]
