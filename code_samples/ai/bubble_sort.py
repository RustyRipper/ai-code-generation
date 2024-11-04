# ai_bubble_sort.py

def bubble_sort(arr):
    """
    Sort a list of numbers using the bubble sort algorithm.

    Parameters:
    arr (list): The list of numbers to sort.

    Returns:
    list: The sorted list of numbers.
    """
    n = len(arr)

    # Loop through the list to perform the sorting
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr
