import pytest
from calculator import add, subtract, multiply, divide, power, is_even

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract():
    """Тест вычитания"""
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5
    assert subtract(10, 10) == 0


def test_multiply():
    """Тест умножения"""
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6
    assert multiply(0, 100) == 0


def test_divide():
    """Тест деления"""
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3
    assert divide(7, 2) == 3.5


def test_power():
    """Тест возведения в степень"""
    assert power(2, 3) == 8
    assert power(5, 2) == 25
    assert power(10, 0) == 1


def test_is_even():
    """Тест проверки чётности"""
    assert is_even(2) == True
    assert is_even(3) == False
    assert is_even(0) == True
    assert is_even(-4) == True

def test_divide_by_zero():
     # Проверяем что divide(5, 0) вызывает ValueError
    with pytest.raises(ValueError):
        divide(5, 0)
    
    # Также можем проверить сообщение об ошибке
    with pytest.raises(ValueError, match="Деление на ноль"):
        divide(10, 0)


@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),      # add(2, 3) должно быть 5
    (0, 0, 0),      # add(0, 0) должно быть 0
    (-1, 1, 0),     # add(-1, 1) должно быть 0
    (100, 200, 300), # add(100, 200) должно быть 300
])

def test_add_parametrized(a, b, expected):
    """
    Параметризованный тест
    
    ПРЕИМУЩЕСТВО:
    Один тест проверяет много случаев
    Если один падает - видно какой именно
    """
    assert add(a, b) == expected

@pytest.mark.parametrize("n, expected", [
    (2, True),
    (3, False),
    (0, True),
    (-4, True),
    (101, False),
])
def test_is_even_parametrized(n, expected):
    """Параметризованный тест чётности"""
    assert is_even(n) == expected
    
        