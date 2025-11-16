import re

print("=== Основы Regex ===\n")

text = "Python - это язык программирования. Python очень популярен."

result = re.search("Python", text)

if result:
    print("Найдено:", result.group())  # result.group() - найденный текст
    print("Позиция:", result.start())   # Где найдено
else:
    print("Не найдено")


print("\n" + "="*60 + "\n")


matches = re.findall("Python", text)
print(f"Найдено совпадений: {len(matches)}")
print("Все совпадения:", matches)

print("\n" + "="*60 + "\n")

text2 = "Мой номер: 123, твой номер: 456"

# Найти все цифры
digits = re.findall(r"\d", text2)
print("Все цифры:", digits)

numbers = re.findall(r"\d+", text2)
print("Все числа:", numbers)

print("\n" + "="*60 + "\n")

text3 = "Телефон: 1234567890"

# re.sub(шаблон, замена, текст)
# Заменяет все цифры на X
hidden = re.sub(r"\d", "X", text3)
print("Оригинал:", text3)
print("Скрыто:", hidden)

print("\n" + "="*60 + "\n")

email1 = "user@example.com"
email2 = "example.com"

# ^ означает "начало строки"
# Проверяем начинается ли с букв
if re.match(r"^[a-z]", email1):
    print(f"{email1} - начинается с буквы")

if re.match(r"^[a-z]", email2):
    print(f"{email2} - начинается с буквы")

print("\n" + "="*60 + "\n")

print("СПЕЦИАЛЬНЫЕ СИМВОЛЫ:")
print("-" * 60)
print(r"\d   - цифра (0-9)")
print(r"\D   - НЕ цифра")
print(r"\w   - буква, цифра или _ (слово)")
print(r"\W   - НЕ слово")
print(r"\s   - пробел, tab, перенос строки")
print(r"\S   - НЕ пробел")
print(r".    - любой символ")
print(r"^    - начало строки")
print(r"$    - конец строки")
print("-" * 60)

print("\nКВАНТИФИКАТОРЫ:")
print("-" * 60)
print(r"+    - 1 или больше")
print(r"*    - 0 или больше")
print(r"?    - 0 или 1")
print(r"{3}  - точно 3")
print(r"{2,5} - от 2 до 5")
print("-" * 60)