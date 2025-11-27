import pytest
from transaction import Transaction
from datetime import datetime

def test_create_expense():

    t = Transaction(100,"Еда", "Хлеб", "expense")
     # Проверяем все поля
    # assert условие - если условие False, тест упадёт
    assert t.amount == 100
    assert t.category == "Еда"
    assert t.description == "Хлеб"
    assert t.transaction_type == "expense"
    
    # Проверяем что ID числовой и положительный
    assert isinstance(t.id, int)
    assert t.id > 0
    
    # Проверяем что дата строка и не пустая
    assert isinstance(t.date, str)
    assert len(t.date) > 0

def test_create_income():
    t = Transaction(5000, "Зарплата", "Ноябрь", "income")
    
    assert t.amount == 5000
    assert t.transaction_type == "income"

def test_create_without_description():
    """
    Тест создания без описания
    
    ПРОВЕРЯЕМ:
    description необязательный параметр
    По умолчанию должна быть пустая строка
    """
    t = Transaction(100, "Еда", transaction_type="expense")
    
    assert t.description == ""    

def test_negative_amount():
    """
    Тест отрицательной суммы
    
    КАК РАБОТАЕТ:
    pytest.raises(ValueError) проверяет что код внутри
    вызывает исключение ValueError
    
    ЕСЛИ исключение НЕ вызвано - тест провален
    """
    # Проверяем что отрицательная сумма вызывает ошибку
    with pytest.raises(ValueError):
        Transaction(-100, "Еда", transaction_type="expense")


def test_zero_amount():
    """Тест нулевой суммы"""
    with pytest.raises(ValueError):
        Transaction(0, "Еда", transaction_type="expense")

def test_invalid_type():
    """
    Тест неверного типа транзакции
    
    ПРОВЕРЯЕМ:
    Если type не "income" или "expense" - должна быть ошибка
    """
    with pytest.raises(ValueError):
        Transaction(100, "Еда", transaction_type="invalid")


def test_non_numeric_amount():
    """
    Тест нечислового amount
    
    ПРОВЕРЯЕМ:
    Если передали строку вместо числа - должна быть ошибка
    """
    with pytest.raises(ValueError):
        Transaction("abc", "Еда", transaction_type="expense")

def test_to_dict():
    """
    Тест преобразования в словарь
    
    ПРОВЕРЯЕМ:
    to_dict() возвращает словарь со всеми полями
    """
    t = Transaction(100, "Еда", "Хлеб", "expense")
    
    # Получаем словарь
    data = t.to_dict()
    
    # Проверяем что это словарь
    assert isinstance(data, dict)
    
    # Проверяем что все ключи есть
    assert "id" in data
    assert "amount" in data
    assert "category" in data
    assert "description" in data
    assert "transaction_type" in data
    assert "date" in data
    
    # Проверяем значения
    assert data["amount"] == 100
    assert data["category"] == "Еда"

def test_from_dict():
    """
    Тест создания из словаря
    
    ПРОВЕРЯЕМ:
    from_dict() создаёт правильный объект Transaction
    """
    # Словарь как будто из JSON
    data = {
        "id": 12345,
        "amount": 200,
        "category": "Транспорт",
        "description": "Метро",
        "transaction_type": "expense",
        "date": "2025-11-16 10:00:00"
    }
    
    # Создаём из словаря
    t = Transaction.from_dict(data)
    
    # Проверяем все поля
    assert t.id == 12345
    assert t.amount == 200
    assert t.category == "Транспорт"
    assert t.description == "Метро"
    assert t.transaction_type == "expense"
    assert t.date == "2025-11-16 10:00:00"    

def test_to_dict_from_dict_roundtrip():
    """
    Тест цикла: объект → словарь → объект
    
    ПРОВЕРЯЕМ:
    Что после преобразования туда-обратно
    получаем идентичный объект
    
    ЗАЧЕМ:
    Убедиться что сохранение/загрузка не теряет данные
    """
    # Создаём транзакцию
    original = Transaction(150, "Еда", "Продукты", "expense")
    
    # Превращаем в словарь
    data = original.to_dict()
    
    # Создаём обратно из словаря
    restored = Transaction.from_dict(data)
    
    # Проверяем что все поля совпадают
    assert restored.id == original.id
    assert restored.amount == original.amount
    assert restored.category == original.category
    assert restored.description == original.description
    assert restored.transaction_type == original.transaction_type
    assert restored.date == original.date


def test_str_method():
    """
    Тест __str__ метода
    
    ПРОВЕРЯЕМ:
    Что __str__ возвращает строку
    """
    t = Transaction(100, "Еда", "Хлеб", "expense")
    
    # str(t) вызывает t.__str__()
    result = str(t)
    
    # Проверяем что это строка
    assert isinstance(result, str)
    
    # Проверяем что содержит важную информацию
    assert "100" in result
    assert "Еда" in result



@pytest.mark.parametrize("amount, category, transaction_type", [
    (100, "Еда", "expense"),
    (5000, "Зарплата", "income"),
    (50.5, "Транспорт", "expense"),
    (1000000, "Бизнес", "income"),
    ])



def test_create_various_transactions(amount, category, transaction_type):
    """
    Параметризованный тест создания
    
    ПРЕИМУЩЕСТВО:
    Один тест проверяет много разных случаев
    
    КАК РАБОТАЕТ:
    pytest запустит этот тест 4 раза
    с разными наборами параметров
    
    ДЕКОРАТОР @pytest.mark.parametrize:
    - Первый параметр - имена переменных (строка)
    - Второй параметр - список наборов значений
    """
    t = Transaction(amount, category, transaction_type=transaction_type)
    
    assert t.amount == amount
    assert t.category == category
    assert t.transaction_type == transaction_type


@pytest.mark.parametrize("invalid_amount", [
    -100,    # Отрицательное
    0,       # Ноль
    -0.01,   # Отрицательное дробное
])
def test_invalid_amounts(invalid_amount):
    """Параметризованный тест невалидных сумм"""
    with pytest.raises(ValueError):
        Transaction(invalid_amount, "Еда", transaction_type="expense")






