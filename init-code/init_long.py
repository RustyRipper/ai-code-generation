import subprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline


def generate_code():
    print(
        "Generate a Python function that calculates the factorial of a ""number"
    )
    return """
def factorial(n):
    # Ensure the input is a non-negative integer
    if n < 0:
        raise ValueError("Input must be a non-negative integer")
    # Base case: factorial of 0 or 1 is 1
    if n == 0 or n == 1:
        return 1
    # Recursive case: n * factorial(n-1)
    return n * factorial(n - 1)

# Example usage:
print(factorial(5))  # Output will be 120"""


generated_code = generate_code()
print("Generated Code:\n", generated_code)


def analyze_code(code):
    with open("generated_code.py", "w") as f:
        f.write(code)

    result = subprocess.run(["pylint", "generated_code.py"],
                            capture_output=True, text=True)
    print("Pylint Analysis Result:\n", result.stdout)


analyze_code(generated_code)

train_code = [
    "def factorial(n): if n == 0: return 1 else: return n * factorial(n-1)",
    "def quicksort(arr): if len(arr) <= 1: return arr else: pivot = arr[0] "
    "return quicksort([x for x in arr[1:] if x <= pivot]) + [pivot] + "
    "quicksort([x for x in arr[1:] if x > pivot])"
]
train_labels = ["mathematical function", "sorting algorithm"]

model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(train_code, train_labels)


def classify_code(code):
    return model.predict([code])


classification = classify_code(generated_code)
print("Code Classification:", classification)


########################################################################################
# TO TEST WATERMARKING FOR LONGER CODE

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

def binary_search(lst, value):
    #base case here
    if len(lst) == 1:
        return lst[0] == value

    mid = len(lst)/2
    if lst[mid] < value:
        return binary_search(lst[:mid], value)
    elif lst[mid] > value:
        return binary_search(lst[mid+1:], value)
    else:
        return True

def bubble(values):
    length = len(values) - 1
    sorted = False
    while not sorted:
        sorted = True
        for element in range(0,length):
            if values[element] > values[element + 1]:
                 hold = values[element + 1]
                 values[element + 1] = values[element]
                 values[element] = hold
                 sorted = False
    return values

def factorial(n):
    if n < 2:
        return 1
    else:
        return n * factorial(n-1)
    
def fib(n):
    a = 0
    b = 1
    while b < n:
        print(b)
        temp = a
        a = b
        b = temp + b

fib(4)


def isprime(n):

    n = abs(int(n))
    if n < 2:
        return False
    if n == 2:
        return True
    if not n & 1:
        return False

    for x in range(3, int(n**0.5) + 1, 2):
        if n % x == 0:
            return False

    return True


print()
########################################################################################

print()