import gmpy2
from gmpy2 import mpz

def power(base, exponent):
    try:
        base = mpz(base)
        exponent = mpz(exponent)
        result = base**exponent
    except OverflowError:
        raise ValueError("Numar prea mare pentru calcul")
    return result


def fibonacci(n):
    try:
        return gmpy2.fib(n)
    except Exception as e:
        raise ValueError(f"Eroare la calcul Fibonacci: {str(e)}")


def factorial(n):
    try:
        return int(gmpy2.fac(n))
    except Exception as e:
        raise ValueError(f"Eroare la factorial: {str(e)}")
