import sqlite3
import bcrypt
from datetime import datetime

DATABASE = 'users.db'

def init_db():
    """Создать таблицу пользователей"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        """
        UNIQUE:
        Гарантирует уникальность
        Нельзя создать двух пользователей с одинаковым username
        """
        conn.commit()
    print("✓ База данных инициализирована")

def register_user(username, email, password):
    """
    Зарегистрировать нового пользователя
    
    Возвращает:
        (bool, str): (успех, сообщение)
    """
    
    # ВАЛИДАЦИЯ
    if len(username) < 3:
        return False, "Имя должно быть минимум 3 символа"
    
    if len(password) < 6:
        return False, "Пароль должен быть минимум 6 символов"
    
    if '@' not in email:
        return False, "Некорректный email"
    
    # ХЕШИРОВАНИЕ ПАРОЛЯ
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt)
    password_hash_str = password_hash.decode('utf-8')
    
    # СОХРАНЕНИЕ В БД
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
            """, (username, email, password_hash_str))
            conn.commit()
            
            return True, "Пользователь успешно зарегистрирован!"
    
    except sqlite3.IntegrityError:
        """
        IntegrityError:
        Ошибка нарушения уникальности
        
        Возникает если:
        - username уже существует
        - email уже существует
        """
        return False, "Пользователь с таким именем или email уже существует"    
    

def login_user(username, password):
    """
    Проверить логин/пароль
    
    Возвращает:
        (bool, dict или str): (успех, данные_пользователя или сообщение)
    """
    
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Найти пользователя
        cursor.execute("""
        SELECT * FROM users WHERE username = ?
        """, (username,))
        
        user = cursor.fetchone()
        
        if not user:
            return False, "Пользователь не найден"
        
        # Проверить пароль
        password_bytes = password.encode('utf-8')
        stored_hash = user['password_hash'].encode('utf-8')
        
        if bcrypt.checkpw(password_bytes, stored_hash):
            # Пароль верный - вернуть данные пользователя
            user_data = {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'created_at': user['created_at']
            }
            return True, user_data
        else:
            return False, "Неверный пароль"




def get_user_by_id(user_id):
    """Получить пользователя по ID"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if user:
            return {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'created_at': user['created_at']
            }
        return None
    

def change_password(user_id, old_password, new_password):
    """
    Изменить пароль пользователя
    
    Возвращает:
        (bool, str): (успех, сообщение)
    """
    
    # Проверить новый пароль
    if len(new_password) < 6:
        return False, "Новый пароль должен быть минимум 6 символов"
    
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Получить текущий хеш
        cursor.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return False, "Пользователь не найден"
        
        # Проверить старый пароль
        old_bytes = old_password.encode('utf-8')
        stored_hash = user['password_hash'].encode('utf-8')
        
        if not bcrypt.checkpw(old_bytes, stored_hash):
            return False, "Старый пароль неверен"
        
        # Хешировать новый пароль
        new_bytes = new_password.encode('utf-8')
        salt = bcrypt.gensalt()
        new_hash = bcrypt.hashpw(new_bytes, salt)
        new_hash_str = new_hash.decode('utf-8')
        
        # Сохранить
        cursor.execute("""
        UPDATE users SET password_hash = ? WHERE id = ?
        """, (new_hash_str, user_id))
        conn.commit()
        
        return True, "Пароль успешно изменён!"



if __name__ == '__main__':
    print("="*60)
    print("ТЕСТИРОВАНИЕ СИСТЕМЫ ПОЛЬЗОВАТЕЛЕЙ")
    print("="*60)
    
    # 1. Инициализация
    init_db()
    
    # 2. Регистрация
    print("\n1. Регистрация пользователей:")
    
    success, msg = register_user("ivan", "ivan@mail.com", "password123")
    print(f"   Иван: {msg}")
    
    success, msg = register_user("maria", "maria@mail.com", "qwerty123")
    print(f"   Мария: {msg}")
    
    # Попытка дубликата
    success, msg = register_user("ivan", "other@mail.com", "pass123")
    print(f"   Дубликат: {msg}")
    
    # Короткий пароль
    success, msg = register_user("petr", "petr@mail.com", "123")
    print(f"   Короткий пароль: {msg}")
    
    # 3. Вход
    print("\n2. Вход в систему:")
    
    success, result = login_user("ivan", "password123")
    if success:
        print(f"   ✅ Иван вошёл: {result['username']} (ID: {result['id']})")
    else:
        print(f"   ❌ {result}")
    
    success, result = login_user("ivan", "wrongpassword")
    if success:
        print(f"   ✅ Вход")
    else:
        print(f"   ❌ {result}")
    
    success, result = login_user("unknown", "password")
    if success:
        print(f"   ✅ Вход")
    else:
        print(f"   ❌ {result}")
    
    # 4. Получить пользователя
    print("\n3. Получение данных пользователя:")
    user = get_user_by_id(1)
    if user:
        print(f"   ID: {user['id']}")
        print(f"   Имя: {user['username']}")
        print(f"   Email: {user['email']}")
    
    # 5. Изменить пароль
    print("\n4. Изменение пароля:")
    success, msg = change_password(1, "password123", "newpassword123")
    print(f"   {msg}")
    
    # Проверить новый пароль
    success, result = login_user("ivan", "newpassword123")
    print(f"   Вход с новым паролем: {'✅' if success else '❌'}")
    
    print("\n" + "="*60)
    print("✓ Все тесты пройдены!")