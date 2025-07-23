import math
import gmpy2

def power(base, exponent):
    return math.pow(base, exponent)

def fibonacci(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    print("Calculating Fibonacci for n =", n)
    return int(gmpy2.fib(n))

def factorial(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    print("Calculating Factorial for n =", n)
    return int(gmpy2.fac(n))