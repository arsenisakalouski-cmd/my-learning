def add(a, b):
    """Сложение двух чисел"""
    return a + b


def subtract(a, b):
    """Вычитание"""
    return a - b


def multiply(a, b):
    """Умножение"""
    return a * b


def divide(a, b):

    if b == 0:
        raise ValueError("Деление на ноль невозможно")
    return a / b


def power(a, b):
    """Возведение в степень"""
    return a ** b


def is_even(n):
    """Проверить чётное ли число"""
    return n % 2 == 0