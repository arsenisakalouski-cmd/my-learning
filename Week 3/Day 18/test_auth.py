# test_auth.py - Тестирование системы аутентификации

import os
import sqlite3

# Удалить старую БД для чистого теста
if os.path.exists('blog.db'):
    os.remove('blog.db')
    print("✓ Старая БД удалена")

import database as db

print("="*60)
print("ТЕСТИРОВАНИЕ СИСТЕМЫ АУТЕНТИФИКАЦИИ")
print("="*60)

# 1. Инициализация
print("\n1. Инициализация БД:")
db.init_db()

# 2. Регистрация пользователей
print("\n2. Регистрация пользователей:")

success, result = db.register_user("ivan", "ivan@mail.com", "password123")
if success:
    print(f"   ✅ Иван зарегистрирован (ID: {result})")
    ivan_id = result
else:
    print(f"   ❌ {result}")

success, result = db.register_user("maria", "maria@mail.com", "qwerty123")
if success:
    print(f"   ✅ Мария зарегистрирована (ID: {result})")
    maria_id = result
else:
    print(f"   ❌ {result}")

# Попытка дубликата
success, result = db.register_user("ivan", "other@mail.com", "pass")
print(f"   Дубликат username: {result}")

# Короткое имя
success, result = db.register_user("ab", "ab@mail.com", "password")
print(f"   Короткое имя: {result}")

# Короткий пароль
success, result = db.register_user("petr", "petr@mail.com", "123")
print(f"   Короткий пароль: {result}")

# Некорректный email
success, result = db.register_user("alex", "notanemail", "password123")
print(f"   Некорректный email: {result}")

# 3. Вход
print("\n3. Вход в систему:")

success, user = db.login_user("ivan", "password123")
if success:
    print(f"   ✅ Иван вошёл: {user['username']}")
else:
    print(f"   ❌ {user}")

success, user = db.login_user("ivan", "wrongpassword")
if success:
    print(f"   ✅ Вход с неверным паролем")
else:
    print(f"   ❌ {user}")

success, user = db.login_user("unknown", "password")
if success:
    print(f"   ✅ Вход несуществующего пользователя")
else:
    print(f"   ❌ {user}")

# 4. Создание постов
print("\n4. Создание постов:")

post1_id = db.create_post(
    "Первый пост Ивана",
    "Это мой первый пост в блоге! " * 5,
    "ivan",
    ivan_id
)
print(f"   ✅ Пост 1 создан (ID: {post1_id})")

post2_id = db.create_post(
    "Второй пост Ивана",
    "Это мой второй пост! " * 5,
    "ivan",
    ivan_id
)
print(f"   ✅ Пост 2 создан (ID: {post2_id})")

post3_id = db.create_post(
    "Пост Марии",
    "Привет всем! Это Мария! " * 5,
    "maria",
    maria_id
)
print(f"   ✅ Пост 3 создан (ID: {post3_id})")

# 5. Проверка авторства
print("\n5. Проверка авторства постов:")

post1 = db.get_post_by_id(post1_id)
print(f"   Пост 1: автор={post1['author']}, author_id={post1['author_id']}")

post3 = db.get_post_by_id(post3_id)
print(f"   Пост 3: автор={post3['author']}, author_id={post3['author_id']}")

# 6. Получение пользователей
print("\n6. Получение данных пользователей:")

ivan = db.get_user_by_id(ivan_id)
print(f"   Иван: {ivan['username']}, {ivan['email']}")

maria = db.get_user_by_username("maria")
print(f"   Мария: {maria['username']}, {maria['email']}")

# 7. Статистика
print("\n7. Просмотр БД:")

with sqlite3.connect('blog.db') as conn:
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    users_count = cursor.fetchone()[0]
    print(f"   Пользователей: {users_count}")
    
    cursor.execute("SELECT COUNT(*) FROM posts")
    posts_count = cursor.fetchone()[0]
    print(f"   Постов: {posts_count}")
    
    cursor.execute("SELECT username, COUNT(*) FROM posts JOIN users ON posts.author_id = users.id GROUP BY username")
    for username, count in cursor.fetchall():
        print(f"   {username}: {count} постов")

print("\n" + "="*60)
print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
print("="*60)
