# ai_is_prime.py

def is_prime(num):
    """
    Determine if a number is prime.

    Parameters:
    num (int): The number to check.

    Returns:
    bool: True if the number is prime, False otherwise.
    """
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False

    i = 5
    # Loop to check for factors of the number
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6

    return True
