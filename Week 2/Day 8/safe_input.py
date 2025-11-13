def get_int(prompt, min_value=None, max_value=None):
    """
    Безопасный ввод целого числа с валидацией
    
    prompt - текст приглашения
    min_value - минимальное значение (необязательно)
    max_value - максимальное значение (необязательно)
    """
    while True:
        try:
            value = int(input(prompt))
            
            # Проверка диапазона
            if min_value is not None and value < min_value:
                print(f"❌ Число должно быть >= {min_value}")
                continue
            
            if max_value is not None and value > max_value:
                print(f"❌ Число должно быть <= {max_value}")
                continue
            
            return value
            
        except ValueError:
            print("❌ Введите целое число!")


def get_float(prompt, positive=False):
    """
    Безопасный ввод числа с плавающей точкой
    
    prompt - текст приглашения
    positive - должно ли быть положительным
    """
    while True:
        try:
            value = float(input(prompt))
            
            if positive and value <= 0:
                print("❌ Число должно быть положительным!")
                continue
            
            return value
            
        except ValueError:
            print("❌ Введите число!")


def get_choice(prompt, choices):
    """
    Безопасный выбор из списка вариантов
    
    prompt - текст приглашения
    choices - список допустимых вариантов
    """
    while True:
        choice = input(prompt).lower()
        
        if choice in choices:
            return choice
        else:
            print(f"❌ Выберите из: {', '.join(choices)}")


# Тестирование
print("=== Тестирование безопасного ввода ===\n")

# Тест 1: Целое число
age = get_int("Введите возраст (0-150): ", min_value=0, max_value=150)
print(f"✅ Возраст: {age}\n")

# Тест 2: Число с плавающей точкой
price = get_float("Введите цену (положительное число): ", positive=True)
print(f"✅ Цена: {price:.2f} руб\n")

# Тест 3: Выбор из списка
answer = get_choice("Продолжить? (да/нет): ", ["да", "нет"])
print(f"✅ Ответ: {answer}\n")

# Тест 4: Меню
print("--- Меню ---")
print("1. Кофе")
print("2. Чай")
print("3. Сок")

choice = get_int("Выберите (1-3): ", min_value=1, max_value=3)

menu = {1: "Кофе", 2: "Чай", 3: "Сок"}
print(f"✅ Вы выбрали: {menu[choice]}")