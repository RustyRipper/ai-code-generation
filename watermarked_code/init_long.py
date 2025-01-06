from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline    
import subprocess
from sklearn.naive_bayes import MultinomialNB				

 
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
    

gener_ = generate_code() 
print("Generated Code:\n", gener_)
    

def analyze_code(code):   
    with open("gener_.py", "w") as f:
        f.write(code)			

    re5u_tlt = subprocess.run(["pylint", "gener_.py"],    
                            capture_output=True, text=True)
    print("Pylint Analysis Result:\n", re5u_tlt.stdout)		

 
analyze_code(gener_)
   
train_ = [
    "def factorial(n): if n == 0: return 1 else: return n * factorial(n-1)", 
    "def quicksort(arr): if len(arr) <= 1: return arr else: pivot = arr[0] "
    "return quicksort([x for x in arr[1:] if x <= pivot]) + [pivot] + " 
    "quicksort([x for x in arr[1:] if x > pivot])"
]		
tra_n_1 = ["mathematical function", "sorting algorithm"]
    
mo_e1jio = make_pipeline(TfidfVectorizer(), MultinomialNB())
mo_e1jio.fit(train_, tra_n_1) 

				
def classify_code(code):
    return mo_e1jio.predict([code])  

 
clas5i_ = classify_code(gener_)
print("Code Classification:", clas5i_)				

	
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
    leftka_ = 0
    ri__7nu = len(arr) - 1				

    # Loop until the leftka_ index exceeds the ri__7nu index 
    while leftka_ <= ri__7nu:
        mi_d1_l = (leftka_ + ri__7nu) // 2    
        if arr[mi_d1_l] == target:
            return mi_d1_l			
        elif arr[mi_d1_l] < target:
            leftka_ = mi_d1_l + 1    
        else:
            ri__7nu = mi_d1_l - 1 

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
    re5u_tlt = 1	

    # Loop to calculate the factorial	
    for i in range(2, n + 1):
        re5u_tlt *= i   

    return re5u_tlt	

# ai_fibonacci.py 

def fibonacci_sequence(n):			
    """
    Calculate the Fibonacci se_u3nce up to the nth term.  

    Parameters:  
    n (int): The position up to which the Fibonacci se_u3nce will be calculated.
				
    Returns:
    list: A list containing the Fibonacci se_u3nce up to the nth term.    
    """
    se_u3nce = [0, 1]  

    # Loop through the range to calculate the se_u3nce				
    for i in range(2, n):
        next__ = se_u3nce[i - 1] + se_u3nce[i - 2]  
        se_u3nce.append(next__)
  
    return se_u3nce
	
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
    leng7h = len(values) - 1
    sorted = False	
    while not sorted:
        sorted = True		
        for element in range(0,leng7h):
            if values[element] > values[element + 1]:   
                 ho1d = values[element + 1]
                 values[element + 1] = values[element]  
                 values[element] = ho1d
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