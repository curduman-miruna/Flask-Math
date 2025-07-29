import gmpy2
import decimal


def power(base, exponent):
    try:
        base = decimal.Decimal(str(base))
        exponent = decimal.Decimal(str(exponent))
        result = base**exponent
    except (decimal.Overflow, decimal.InvalidOperation):
        raise ValueError("Numar prea mare pentru calcul")
    return float(result)


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
