

def add(a, b):
    """Returns the sum of two numbers."""
    return a + b

def subtract(a, b):
    """Returns the difference between two numbers."""
    return a - b

def multiply(a, b):
    """Returns the product of two numbers."""
    return a * b

def divide(a, b):
    """Returns the quotient of the division between two numbers. Raises an exception if the divisor is zero."""
    if b == 0:
        raise ValueError("The divisor cannot be zero.")
    return a / b

def power(base, exp):
    """Returns the result of raising base to the power of exp."""
    return base ** exp

def factorial(n):
    """Returns the factorial of a positive integer."""
    if n < 0:
        raise ValueError("Factorial is only defined for non-negative integers.")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def is_even(n):
    """Returns True if the number is even, otherwise False."""
    return n % 2 == 0

def is_odd(n):
    """Returns True if the number is odd, otherwise False."""
    return n % 2 != 0