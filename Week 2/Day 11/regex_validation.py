import re

print("=== Валидация данных ===\n")

def validate_email(email):

    pattern = r'^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True
    return False


# Тесты
emails = [
    "user@example.com",      # OK
    "test.name@mail.ru",     # OK
    "invalid@",              # Плохой
    "@example.com",          # Плохой
    "user@mail",             # Плохой
]

print("--- Проверка Email ---")
for email in emails:
    result = "OK" if validate_email(email) else "Плохой"
    print(f"{email:25} - {result}")

print("\n" + "="*60 + "\n")

def validate_phone(phone):

      # Убираем все кроме цифр и +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Проверяем паттерны
    patterns = [
        r'^\+7\d{10}$',      # +79001234567
        r'^8\d{10}$',        # 89001234567
    ]
    
    for pattern in patterns:
        if re.match(pattern, cleaned):
            return True
    
    return False


# Тесты
phones = [
    "+79001234567",
    "89001234567",
    "8-900-123-45-67",
    "+7 (900) 123-45-67",
    "123",
    "+1234567890",
]

print("--- Проверка Телефона ---")
for phone in phones:
    result = "OK" if validate_phone(phone) else "Плохой"
    print(f"{phone:25} - {result}")

print("\n" + "="*60 + "\n")


def validate_password(password):

    if len(password) < 8:
        return False, "Минимум 8 символов"
    
    if not re.search(r'[A-Z]', password):
        return False, "Нужна заглавная буква"
    
    if not re.search(r'[a-z]', password):
        return False, "Нужна строчная буква"
    
    if not re.search(r'\d', password):
        return False, "Нужна цифра"
    
    return True, "Надёжный пароль"


# Тесты
passwords = [
    "Password123",   # OK
    "pass",          # Короткий
    "password123",   # Нет заглавной
    "PASSWORD123",   # Нет строчной
    "PasswordABC",   # Нет цифры
]

print("--- Проверка Пароля ---")
for pwd in passwords:
    valid, message = validate_password(pwd)
    status = "OK" if valid else "Плохой"
    print(f"{pwd:20} - {status:10} ({message})")

print("\n" + "="*60 + "\n")

def extract_emails(text):
    """Найти все email адреса в тексте"""
    pattern = r'[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)


text = """
Контакты:
Email: john@example.com
Поддержка: support@company.ru
Также можете писать на info@test.org
"""

print("--- Извлечение Email ---")
print("Текст:")
print(text)
print("\nНайденные email:")
emails = extract_emails(text)
for email in emails:
    print(f"  - {email}")

print("\n" + "="*60 + "\n")

def extract_phones(text):
    """Найти все телефоны в тексте"""
    # Паттерн для разных форматов
    pattern = r'(\+7|8)[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}'
    return re.findall(pattern, text)

print("--- Извлечение Телефонов ---")
print("Текст:")
print(text2)
print("\nНайденные телефоны:")
phones = extract_phones(text2)
for phone in phones:
    print(f"  - {phone}")