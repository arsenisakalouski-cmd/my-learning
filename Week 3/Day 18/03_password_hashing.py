import bcrypt

# 03_password_hashing.py - Хеширование паролей

import bcrypt

# ==========================================
# ХЕШИРОВАНИЕ ПАРОЛЯ
# ==========================================

def hash_password(password):
    """
    Хешировать пароль
    
    Параметры:
        password (str): Пароль открытым текстом
    
    Возвращает:
        str: Хешированный пароль
    """
    
    # Преобразовать строку в bytes
    password_bytes = password.encode('utf-8')
    """
    .encode('utf-8'):
    Преобразовать строку в байты
    
    bcrypt работает с байтами, не строками
    """
    
    # Сгенерировать salt и хеш
    salt = bcrypt.gensalt()
    """
    gensalt():
    Генерирует случайную "соль"
    
    СОЛЬ (salt):
    Случайные данные которые добавляются к паролю
    
    Зачем:
    Два одинаковых пароля дадут разные хеши!
    
    password123 + salt1 → hash1
    password123 + salt2 → hash2
    hash1 ≠ hash2
    """
    
    hashed = bcrypt.hashpw(password_bytes, salt)
    """
    hashpw(password, salt):
    Хеширует пароль с солью
    
    Возвращает bytes
    """
    
    # Преобразовать обратно в строку для хранения в БД
    return hashed.decode('utf-8')
    """
    .decode('utf-8'):
    Преобразовать bytes обратно в строку
    """


# ==========================================
# ПРОВЕРКА ПАРОЛЯ
# ==========================================

def check_password(password, hashed_password):
    """
    Проверить пароль
    
    Параметры:
        password (str): Введённый пароль
        hashed_password (str): Сохранённый хеш
    
    Возвращает:
        bool: True если пароль верный
    """
    
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    # Проверить пароль
    return bcrypt.checkpw(password_bytes, hashed_bytes)
    """
    checkpw(password, hashed):
    Сравнивает пароль с хешем
    
    КАК РАБОТАЕТ:
    1. Извлекает соль из хеша
    2. Хеширует введённый пароль с той же солью
    3. Сравнивает результаты
    
    Возвращает True/False
    """


# ==========================================
# ТЕСТИРОВАНИЕ
# ==========================================

if __name__ == '__main__':
    print("="*60)
    print("ТЕСТИРОВАНИЕ ХЕШИРОВАНИЯ ПАРОЛЕЙ")
    print("="*60)
    
    # 1. Хешировать пароль
    print("\n1. Хеширование пароля:")
    password = "password123"
    print(f"   Пароль: {password}")
    
    hashed = hash_password(password)
    print(f"   Хеш: {hashed}")
    print(f"   Длина хеша: {len(hashed)} символов")
    
    # 2. Проверить правильный пароль
    print("\n2. Проверка правильного пароля:")
    is_correct = check_password("password123", hashed)
    print(f"   password123 == хеш: {is_correct} ✅")
    
    # 3. Проверить неправильный пароль
    print("\n3. Проверка неправильного пароля:")
    is_correct = check_password("wrongpassword", hashed)
    print(f"   wrongpassword == хеш: {is_correct} ❌")
    
    # 4. Одинаковые пароли дают разные хеши
    print("\n4. Одинаковые пароли → разные хеши:")
    hash1 = hash_password("password123")
    hash2 = hash_password("password123")
    print(f"   Хеш 1: {hash1[:30]}...")
    print(f"   Хеш 2: {hash2[:30]}...")
    print(f"   Одинаковые? {hash1 == hash2} ❌")
    print(f"   Но оба работают с паролем? {check_password('password123', hash1) and check_password('password123', hash2)} ✅")
    
    # 5. Разные пароли
    print("\n5. Разные пароли:")
    passwords = ["password123", "qwerty", "12345678", "admin"]
    
    for pwd in passwords:
        h = hash_password(pwd)
        print(f"   {pwd:15} → {h[:40]}...")
    
    print("\n" + "="*60)
    print("ИТОГИ:")
    print("="*60)
    print("""
    ✅ Пароли хешируются
    ✅ Хеши невозможно расшифровать
    ✅ Проверка работает корректно
    ✅ Одинаковые пароли → разные хеши (соль)
    ✅ Безопасно для хранения в БД
    """)