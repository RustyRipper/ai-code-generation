# ai_fibonacci.py

def fibonacci_sequence(n):
    """
    Calculate the Fibonacci sequence up to the nth term.

    Parameters:
    n (int): The position up to which the Fibonacci sequence will be calculated.

    Returns:
    list: A list containing the Fibonacci sequence up to the nth term.
    """
    sequence = [0, 1]

    # Loop through the range to calculate the sequence
    for i in range(2, n):
        next_value = sequence[i - 1] + sequence[i - 2]
        sequence.append(next_value)

    return sequence
