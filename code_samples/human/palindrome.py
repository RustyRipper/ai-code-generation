def palindrome(word):
    return str(word) == str(word)[::-1]


print(palindrome("ekooke"))