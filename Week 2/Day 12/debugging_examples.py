import logging 

def calculate_average(numbers):
    print(f"[DEBUG] Получен список: {numbers}")
    print(f"[DEBUG] Длина списка: {len(numbers)}")
    
    total = sum(numbers)
    print(f"[DEBUG] Сумма: {total}")
    
    # Здесь может быть деление на ноль!
    average = total / len(numbers)
    print(f"[DEBUG] Среднее: {average}")
    
    return average



print("=== Тест calculate_average ===")
try:
    result = calculate_average([1, 2, 3, 4, 5])
    print(f"Результат: {result}\n")
    
    # Вызовем ошибку
    result = calculate_average([])
except ZeroDivisionError as e:
    print(f"Ошибка: {e}\n")







# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def process_data(data):
    """
    Обработка данных с логированием
    
    ПРЕИМУЩЕСТВА logging над print:
    1. Можно включать/выключать уровни (DEBUG, INFO, ERROR)
    2. Можно писать в файл
    3. Можно форматировать
    4. Не нужно удалять из кода
    """
    logger.debug(f"Начало обработки данных: {data}")

    if not data:
        logger.warning("Пустые данные!")
        return []
    
    logger.info(f"Обработка {len(data)} элементов")
    
    result = []
    for i, item in enumerate(data):
        logger.debug(f"Обработка элемента {i}: {item}")
        
        try:
            processed = item * 2
            result.append(processed)
            logger.debug(f"Результат: {processed}")
        except Exception as e:
            logger.error(f"Ошибка при обработке {item}: {e}")
    
    logger.info(f"Обработка завершена. Результатов: {len(result)}")
    return result


print("\n=== Тест process_data ===")
result = process_data([1, 2, 3])
print(f"Результат: {result}\n")

def divide_numbers(a, b):
    """
    Деление с проверками
    
    assert используется для проверки предусловий
    """
    # Проверяем входные данные
    assert isinstance(a, (int, float)), f"a должно быть числом, получено {type(a)}"
    assert isinstance(b, (int, float)), f"b должно быть числом, получено {type(b)}"
    assert b != 0, "b не может быть нулём"
    
    result = a / b
    
    # Проверяем результат
    assert isinstance(result, (int, float)), "Результат должен быть числом"
    
    return result


print("=== Тест divide_numbers ===")
try:
    print(divide_numbers(10, 2))
    print(divide_numbers(10, 0))  # Вызовет AssertionError
except AssertionError as e:
    print(f"Ошибка проверки: {e}\n")


def debug_print(name, value):
    """Красивый вывод для отладки"""
    print(f"[DEBUG] {name} = {value} (type: {type(value).__name__})")


def find_bugs_in_list(items):
    """Функция с багами для практики отладки"""
    debug_print("items", items)
    
    result = []
    
    for i, item in enumerate(items):
        debug_print(f"items[{i}]", item)
        
        # Проверяем условия
        if item > 0:
            processed = item * 2
            debug_print(f"processed[{i}]", processed)
            result.append(processed)
    
    debug_print("result", result)
    return result


print("=== Тест find_bugs_in_list ===")
output = find_bugs_in_list([1, -2, 3, 0, 5])
print(f"Итог: {output}\n")