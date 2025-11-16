import re

print("=== Продвинутые техники ===\n")

text = "Дата: 15.11.2025"

pattern = r'(\d{2})\.(\d{2})\.(\d{4})'

match = re.search(pattern, text)

if match:
    print("Полное совпадение:", match.group(0))  # Всё: "15.11.2025"
    print("День:", match.group(1))    # Группа 1: "15"
    print("Месяц:", match.group(2))   # Группа 2: "11"
    print("Год:", match.group(3))     # Группа 3: "2025"

    print("\n" + "="*60 + "\n")

text2 = "Email: user@example.com"

pattern2 = r'(?P<username>[a-z]+)@(?P<domain>[a-z]+\.[a-z]+)'

match2 = re.search(pattern2, text2)

if match2:
    print("\nПо имени:")
    print("  Username:", match2.group('username'))
    print("  Domain:", match2.group('domain'))

print("\n" + "="*60 + "\n")

text3 = "Цена: 100 руб, Скидка: 20 долларов, Итого: 80 руб"

pattern3 = r'\d+(?= руб)'

prices = re.findall(pattern3, text3)
print("Цены в рублях:", prices)  # ['100', '80']

# ОБЪЯСНЕНИЕ:
# (?= руб) проверяет что дальше идёт " руб"
# Но " руб" НЕ включается в результат
# Поэтому получаем только числа: 100, 80

print("\n" + "="*60 + "\n")




# ==========================================
# ТЕХНИКА 4: Жадные vs ленивые квантификаторы
# ==========================================

html = "<div>Текст 1</div><div>Текст 2</div>"

# .* - жадный (берёт максимум)
# Найдёт от первого < до последнего >
greedy = re.findall(r'<.*>', html)
print("Жадный .* :", greedy)  # ['<div>Текст 1</div><div>Текст 2</div>']

# .*? - ленивый (берёт минимум)
# Найдёт каждый тег отдельно
lazy = re.findall(r'<.*?>', html)
print("Ленивый .*?:", lazy)  # ['<div>', '</div>', '<div>', '</div>']

# ОБЪЯСНЕНИЕ:
# .* пытается захватить КАК МОЖНО БОЛЬШЕ символов
# .*? пытается захватить КАК МОЖНО МЕНЬШЕ символов

print("\n" + "="*60 + "\n")



text4 = """
Python - язык программирования
PYTHON очень популярен
python используется везде
"""

# БЕЗ флага - чувствительно к регистру
matches1 = re.findall(r'Python', text4)
print(f"Без флага: {len(matches1)} совпадений")  # 1

# С флагом re.IGNORECASE - игнорировать регистр
# Python, PYTHON, python - всё найдёт
matches2 = re.findall(r'Python', text4, re.IGNORECASE)
print(f"С re.IGNORECASE: {len(matches2)} совпадений")  # 3

# ОБЪЯСНЕНИЕ:
# re.IGNORECASE (или re.I) - третий параметр
# Делает поиск без учёта регистра

print("\n" + "="*60 + "\n")



def hide_phone(match):

    phone = match.group(0)  # Полный номер
    # Показываем только последние 4 цифры
    return "XXX-XXX-XX-" + phone[-2:]

text5 = "Телефон: +7-900-123-45-67"
# re.sub может принимать ФУНКЦИЮ вместо строки замены
# Функция вызывается для каждого совпадения
hidden = re.sub(r'\+7-\d{3}-\d{3}-\d{2}-\d{2}', hide_phone, text5)
print("Оригинал:", text5)
print("Скрыто:", hidden)

# ОБЪЯСНЕНИЕ:
# hide_phone вызывается для каждого найденного номера
# match.group(0) содержит найденный номер
# Функция возвращает строку замены

print("\n" + "="*60 + "\n")



log = """
[2025-11-14 10:30:15] ERROR: Connection failed
[2025-11-14 10:31:20] INFO: Retry attempt 1
[2025-11-14 10:31:25] ERROR: Connection failed
[2025-11-14 10:32:00] INFO: Connection established
"""

# Паттерн с именованными группами
# \[         - открывающая скобка (экранируем)
# (?P<date>...) - группа "date"
# (?P<level>...) - группа "level"
# (?P<message>...) - группа "message"
pattern_log = r'\[(?P<date>[\d\-: ]+)\] (?P<level>\w+): (?P<message>.+)'

print("Парсинг лога:\n")
for match in re.finditer(pattern_log, log):
    # match.groupdict() возвращает словарь всех именованных групп
    log_entry = match.groupdict()
    print(f"Дата: {log_entry['date']}")
    print(f"Уровень: {log_entry['level']}")
    print(f"Сообщение: {log_entry['message']}")
    print()

# ОБЪЯСНЕНИЕ:
# re.finditer() возвращает итератор по всем совпадениям
# match.groupdict() возвращает словарь вида:
# {'date': '2025-11-14 10:30:15', 'level': 'ERROR', 'message': '...'}

print("="*60 + "\n")





# ==========================================
# ПРАКТИКА: Извлечение данных из HTML
# ==========================================

html_text = """
<div class="product">
    <h2>Ноутбук</h2>
    <span class="price">50000 руб</span>
</div>
<div class="product">
    <h2>Мышь</h2>
    <span class="price">500 руб</span>
</div>
"""

# Найти все названия товаров
# <h2> - открывающий тег
# (.*?) - содержимое (ленивый)
# </h2> - закрывающий тег
titles = re.findall(r'<h2>(.*?)</h2>', html_text)
print("Товары:", titles)

# Найти все цены
# \d+ - одна или больше цифр
# (?= руб) - после идёт " руб" (не включается в результат)
prices = re.findall(r'<span class="price">(\d+)', html_text)
print("Цены:", prices)



# re.findall возвращает только содержимое групп
# Поэтому получаем ['Ноутбук', 'Мышь'] а не ['<h2>Ноутбук</h2>', ...]

print("\n" + "="*60 + "\n")

def format_phone(phone):

     # Оставляем только цифры
    digits = re.sub(r'\D', '', phone)

     #Если начинается с 8, меняем на 7
    if digits.startswith('8'):
        digits = '7' + digits[1:]
    
    # Форматируем: +7 (XXX) XXX-XX-XX
    if len(digits) == 11 and digits[0] == '7':
        formatted = f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
        return formatted
    
    return phone  # Не смогли отформатировать

# Тесты
phones = [
    "+79001234567",
    "89001234567",
    "8-900-123-45-67",
    "900-123-45-67",
]

print("Форматирование телефонов:\n")
for phone in phones:
    formatted = format_phone(phone)
    print(f"{phone:20} -> {formatted}")

# ОБЪЯСНЕНИЕ digits[1:4]:
# digits = "79001234567"
# digits[1:4] берёт символы с индекса 1 по 3 (не включая 4)
# Результат: "900"