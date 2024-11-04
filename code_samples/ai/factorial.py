# ai_factorial.py

def factorial(n):
    """
    Calculate the factorial of a given number.

    Parameters:
    n (int): The number to calculate the factorial for.

    Returns:
    int: The factorial of the input number.
    """
    result = 1

    # Loop to calculate the factorial
    for i in range(2, n + 1):
        result *= i

    return result
