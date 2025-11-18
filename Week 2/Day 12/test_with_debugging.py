import pytest

def find_max(numbers):
    if not numbers:
        raise ValueError("Список пуст")
    
    max_value = numbers[0]  # Начинаем с первого элемента
    
    for num in numbers:
        if num > max_value:
            max_value = num
    
    return max_value

def test_find_max_positive():
    """Тест с положительными числами - пройдёт"""
    assert find_max([1, 2, 3, 4, 5]) == 5



def test_find_max_negative():

    result = find_max([-5, -2, -10, -1])
    assert result == -1  # Ожидаем -1, но получим 0


def test_find_max_mixed():
    """Тест со смешанными числами"""
    assert find_max([-5, 3, -2, 8]) == 8


def test_with_debug_output():    
    numbers = [1, 2, 3]
    print(f"\n[DEBUG] Тестируем с numbers = {numbers}")
    
    result = find_max(numbers)
    print(f"[DEBUG] Результат: {result}")
    
    assert result == 3


import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_with_logging():
    """Тест с логированием"""
    numbers = [5, 10, 3]
    logger.debug(f"Входные данные: {numbers}")
    
    result = find_max(numbers)
    logger.debug(f"Результат: {result}")
    
    assert result == 10



@pytest.mark.xfail(reason="Известный баг с отрицательными числами")
def test_expected_failure():
    """
    Тест который ожидаемо падает
    
    xfail = expected fail
    Тест запустится, но если упадёт - не будет ошибкой
    """
    assert find_max([-5, -2]) == -2