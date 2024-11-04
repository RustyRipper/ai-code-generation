def fib(n):
    a = 0
    b = 1
    while b < n:
        print(b)
        temp = a
        a = b
        b = temp + b

fib(4)