# 01_sqlite_basics.py - Основы SQLite

import sqlite3

"""
МОДУЛЬ sqlite3:
Встроенный модуль Python для работы с SQLite
Не требует установки
"""

# ==========================================
# ПОДКЛЮЧЕНИЕ К БД
# ==========================================

# Создание/подключение к БД
conn = sqlite3.connect('test.db')
"""
sqlite3.connect(filename):
- Если файл существует - подключается
- Если нет - создаёт новый
- Возвращает объект Connection

'test.db' - имя файла БД
После выполнения появится файл test.db
"""

# Создание курсора
cursor = conn.cursor()
"""
Курсор (cursor):
Объект для выполнения SQL команд

Аналогия:
Connection = соединение с БД (канал связи)
Cursor = указатель для работы (выполняет команды)
"""

# ==========================================
# СОЗДАНИЕ ТАБЛИЦЫ
# ==========================================

# SQL команда для создания таблицы
create_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

"""
РАЗБОР SQL КОМАНДЫ:

CREATE TABLE IF NOT EXISTS users
- CREATE TABLE - создать таблицу
- IF NOT EXISTS - если не существует (избегаем ошибки)
- users - имя таблицы

Столбцы:

id INTEGER PRIMARY KEY AUTOINCREMENT
- id - имя столбца
- INTEGER - целое число
- PRIMARY KEY - первичный ключ (уникальный идентификатор)
- AUTOINCREMENT - автоматическое увеличение (1, 2, 3...)

name TEXT NOT NULL
- TEXT - текст (строка)
- NOT NULL - обязательное поле (не может быть пустым)

email TEXT UNIQUE NOT NULL
- UNIQUE - уникальное значение (нельзя дублировать)
- NOT NULL - обязательное

age INTEGER
- Необязательное поле (может быть NULL)

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- TIMESTAMP - дата и время
- DEFAULT - значение по умолчанию
- CURRENT_TIMESTAMP - текущая дата/время
"""

# Выполнить SQL команду
cursor.execute(create_table_sql)
print("✓ Таблица users создана")

# ==========================================
# ДОБАВЛЕНИЕ ДАННЫХ (INSERT)
# ==========================================

# Способ 1: Безопасный (с параметрами)
insert_sql = "INSERT INTO users (name, email, age) VALUES (?, ?, ?)"
"""
Плейсхолдеры (?):
- Заменяются на значения из tuple
- Автоматически экранируют данные
- Защищают от SQL-инъекций

SQL-инъекция - хакерская атака:
name = "'; DROP TABLE users; --"
Без защиты уничтожит таблицу!
С плейсхолдерами - безопасно
"""

cursor.execute(insert_sql, ('Иван', 'ivan@mail.com', 25))
cursor.execute(insert_sql, ('Мария', 'maria@mail.com', 30))
cursor.execute(insert_sql, ('Пётр', 'petr@mail.com', 28))

print("✓ Добавлено 3 пользователя")

# Способ 2: Несколько записей сразу
users_data = [
    ('Анна', 'anna@mail.com', 27),
    ('Сергей', 'sergey@mail.com', 35),
]

cursor.executemany(insert_sql, users_data)
"""
executemany():
Выполняет команду для каждого элемента списка
Быстрее чем несколько execute()
"""

print("✓ Добавлено ещё 2 пользователя")

# ==========================================
# СОХРАНЕНИЕ ИЗМЕНЕНИЙ
# ==========================================

conn.commit()
"""
commit():
Сохраняет все изменения в БД

БЕЗ commit():
Изменения НЕ сохранятся!

Транзакция:
1. Начало (автоматически)
2. Изменения (INSERT, UPDATE, DELETE)
3. commit() - сохранить ВСЁ
или
3. rollback() - отменить ВСЁ
"""

print("✓ Изменения сохранены")

# ==========================================
# ЧТЕНИЕ ДАННЫХ (SELECT)
# ==========================================

# Получить все записи
cursor.execute("SELECT * FROM users")
"""
SELECT * FROM users:
- SELECT - выбрать
- * - все столбцы
- FROM users - из таблицы users
"""

# Получить результаты
all_users = cursor.fetchall()
"""
fetchall():
Возвращает список всех строк
Каждая строка - tuple
"""

print("\nВсе пользователи:")
for user in all_users:
    print(user)
    # (id, name, email, age, created_at)

# Получить конкретные столбцы
cursor.execute("SELECT name, email FROM users")
users_name_email = cursor.fetchall()

print("\nИмена и email:")
for name, email in users_name_email:
    print(f"{name}: {email}")

# Фильтрация (WHERE)
cursor.execute("SELECT * FROM users WHERE age > 28")
"""
WHERE - условие фильтрации
age > 28 - возраст больше 28
"""

older_users = cursor.fetchall()
print("\nПользователи старше 28:")
for user in older_users:
    print(user)

# Поиск по имени
cursor.execute("SELECT * FROM users WHERE name = ?", ('Иван',))
"""
ВАЖНО:
('Иван',) - tuple с одним элементом
Запятая обязательна!
"""

ivan = cursor.fetchone()
"""
fetchone():
Возвращает ОДНУ строку (tuple)
Или None если ничего не найдено
"""

print(f"\nПользователь Иван: {ivan}")

# ==========================================
# ОБНОВЛЕНИЕ ДАННЫХ (UPDATE)
# ==========================================

update_sql = "UPDATE users SET age = ? WHERE name = ?"
cursor.execute(update_sql, (26, 'Иван'))
"""
UPDATE users SET age = 26 WHERE name = 'Иван'
Изменяет возраст Ивана на 26
"""

conn.commit()
print("\n✓ Возраст Ивана обновлён")

# Проверим
cursor.execute("SELECT * FROM users WHERE name = 'Иван'")
print(cursor.fetchone())

# ==========================================
# УДАЛЕНИЕ ДАННЫХ (DELETE)
# ==========================================

delete_sql = "DELETE FROM users WHERE name = ?"
cursor.execute(delete_sql, ('Пётр',))
"""
DELETE FROM users WHERE name = 'Пётр'
Удаляет пользователя Пётр
"""

conn.commit()
print("\n✓ Пользователь Пётр удалён")

# Проверим количество записей
cursor.execute("SELECT COUNT(*) FROM users")
"""
COUNT(*) - подсчитать количество строк
"""

count = cursor.fetchone()[0]
print(f"Осталось пользователей: {count}")

# ==========================================
# ЗАКРЫТИЕ СОЕДИНЕНИЯ
# ==========================================

cursor.close()
conn.close()
"""
ВАЖНО:
Всегда закрывать соединение!

cursor.close() - закрыть курсор
conn.close() - закрыть соединение
"""

print("\n✓ Соединение с БД закрыто")

# ==========================================
# ИТОГИ
# ==========================================

print("\n" + "="*50)
print("БАЗОВЫЕ ОПЕРАЦИИ SQLite:")
print("="*50)
print("""
1. Подключение:  conn = sqlite3.connect('db.db')
2. Курсор:       cursor = conn.cursor()
3. Выполнение:   cursor.execute(sql)
4. Сохранение:   conn.commit()
5. Чтение:       cursor.fetchall() или fetchone()
6. Закрытие:     cursor.close(), conn.close()

CRUD операции:
- CREATE (INSERT): cursor.execute("INSERT INTO ...")
- READ (SELECT):   cursor.execute("SELECT ...")
- UPDATE:          cursor.execute("UPDATE ...")
- DELETE:          cursor.execute("DELETE ...")
""")






