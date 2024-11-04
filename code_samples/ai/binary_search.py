# ai_binary_search.py

def binary_search(arr, target):
    """
    Perform a binary search on a sorted list to find the index of a target value.

    Parameters:
    arr (list): The sorted list of elements to search.
    target (int): The value to search for in the list.

    Returns:
    int: The index of the target in the list, or -1 if the target is not found.
    """
    left = 0
    right = len(arr) - 1

    # Loop until the left index exceeds the right index
    while left <= right:
        middle = (left + right) // 2
        if arr[middle] == target:
            return middle
        elif arr[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1
