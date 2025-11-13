print("=== Практика с исключениями ===\n")

print("--- Задача 1: Список ---")

fruits = ["яблоко", "банан", "апельсин"]
print(f"Список фруктов: {fruits}")
print(f"Доступные индексы: 0, 1, 2\n")


try:
    index = int(input("Введите индекс (0-2): "))
    fruit = fruits[index]
    print(f"Фрукт: {fruit}")
except ValueError:
        print(" Это не число!")
except IndexError:
    # ЧТО ПРОИЗОШЛО: Индекс вне диапазона (например, 10)
    print(f" Индекс должен быть от 0 до {len(fruits)-1}")

print()    

print("--- Задача 2: Словарь ---")

person = {
    "name": "Иван",
    "age": 25,
    "city": "Москва"
}

print(f"Доступные ключи: {list(person.keys())}\n")

# КАК ЭТО РАБОТАЕТ:
# 1. Пользователь вводит ключ
# 2. Мы пытаемся получить значение
# 3. Если ключа нет → KeyError
# 4. Мы ловим и показываем доступные ключи

try:
    key = input("Введите ключ (name/age/city): ")
    value = person[key]  # Может быть KeyError!
    print(f"✅ {key}: {value}")
except KeyError:
    # ЧТО ПРОИЗОШЛО: Такого ключа нет в словаре
    print(f" Ключа '{key}' нет!")
    print(f"   Доступные: {', '.join(person.keys())}")

print()

