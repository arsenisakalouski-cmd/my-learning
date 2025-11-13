from datetime import datetime
print("=== Best Practices для обработки ошибок ===\n")

def bad_example():
    """ ПЛОХО: Ловим всё"""
    try:
        age = int(input("Возраст: "))
        result = 100 / age
        print(f"Результат: {result}")
    except:  
        print("Ошибка!") 

def good_example():

    try:
        age = int(input("Возраст: "))        
        result = 100/age
        print(f"Результат: {result}")
    except ValueError:  # ← Конкретно!
        print(" Введите целое число!")
    except ZeroDivisionError:  # ← Конкретно!
        print(" Возраст не может быть 0!")

print("Плохой пример:")
bad_example()
2
print("\nХороший пример:")
good_example()


print("--- Пример 3: Когда НЕ нужны исключения ---\n")

person = {
    "name": "Иван",
    "age": 25
}

def bad_example_3():
    """ ПЛОХО: Исключение вместо проверки"""
    try:
        phone = person["phone"]  # KeyError
    except KeyError:
        phone = "Нет телефона"
    print(f"Телефон: {phone}")

def good_example_3():
    """ ХОРОШО: Используем .get()"""
    phone = person.get("phone", "Нет телефона")
    print(f"Телефон: {phone}")

print("Плохой способ (через исключение):")
bad_example_3()

print("\nХороший способ (через .get()):")
good_example_3()

print("\n" + "="*50 + "\n")
