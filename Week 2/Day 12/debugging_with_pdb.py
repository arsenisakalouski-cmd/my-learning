import pdb

def buggy_function(numbers):
    """
    Функция с багом
    
    ИСПОЛЬЗОВАНИЕ PDB:
    1. Добавить pdb.set_trace() в нужном месте
    2. Запустить программу
    3. Выполнится до этой точки и остановится
    4. Можно проверять переменные, выполнять команды
    """
    print("Начало функции")

     
    total = 0
    
    for i, num in enumerate(numbers):
        print(f"Обработка элемента {i}: {num}")
        
        # ТОЧКА ОСТАНОВА - программа остановится здесь
        # Раскомментируйте чтобы использовать:
        # pdb.set_trace()
        
        total += num
        
        # БАГ: если num чётное, добавляем ещё раз
        if num % 2 == 0:
            total += num
    
    return total

"""
ОСНОВНЫЕ КОМАНДЫ:

n (next)       - выполнить следующую строку
s (step)       - войти внутрь функции
c (continue)   - продолжить до следующей точки останова
l (list)       - показать код вокруг текущей строки
p variable     - вывести значение переменной
pp variable    - вывести красиво (pretty print)
h (help)       - помощь
q (quit)       - выйти из отладчика

ПРИМЕРЫ:
p num          - показать значение num
p total        - показать значение total
p numbers      - показать весь список
"""

def modern_debugging(data):
    """Использование breakpoint() вместо pdb.set_trace()"""
    print("Начало")
    
    result = []
    
    for item in data:
        # breakpoint() - то же что pdb.set_trace()
        # Но более удобный и рекомендуемый
        # Раскомментируйте для отладки:
        # breakpoint()
        
        processed = item * 2
        result.append(processed)
    
    return result

def conditional_breakpoint(numbers):
    """Остановка только при определённом условии"""
    for i, num in enumerate(numbers):
        # Остановимся только если num больше 5
        if num > 5:
            # breakpoint()  # Раскомментируйте
            pass
        
        print(f"Обработка: {num}")


print("\n=== Примеры отладки ===")
print("Раскомментируйте pdb.set_trace() или breakpoint() для отладки")
print("Затем запустите: python debugging_with_pdb.py\n")