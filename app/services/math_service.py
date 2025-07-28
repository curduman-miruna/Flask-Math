import math
import gmpy2

import decimal

def power(base, exponent):
    if abs(exponent) > 10000:
        raise ValueError("Exponentul este prea mare")

    try:
        base = decimal.Decimal(str(base))
        exponent = decimal.Decimal(str(exponent))
        result = base ** exponent
    except (decimal.Overflow, decimal.InvalidOperation):
        raise ValueError("Numar prea mare pentru calcul")
    return float(result)


def fibonacci(n):
    if n < 0:
        raise ValueError("n trebuie sa fie pozitiv")
    if n > 1_000_000:
        raise ValueError("n este prea mare (max 1 milion)")
    try:
        return gmpy2.fib(n)
    except Exception as e:
        raise ValueError(f"Eroare la calcul Fibonacci: {str(e)}")


import gmpy2

def factorial(n):
    if n < 0:
        raise ValueError("n trebuie sa fie pozitiv")
    if n > 100_000:
        raise ValueError("n este prea mare (max 100000)")
    try:
        return int(gmpy2.fac(n))
    except Exception as e:
        raise ValueError(f"Eroare la factorial: {str(e)}")
