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
