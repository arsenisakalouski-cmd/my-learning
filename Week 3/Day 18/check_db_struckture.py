# check_db_structure.py - Проверка структуры БД

import sqlite3

DATABASE = 'blog.db'

print("="*60)
print("СТРУКТУРА БАЗЫ ДАННЫХ")
print("="*60)

try:
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        # Получить список всех таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"\nТаблицы: {tables}")
        
        # Для каждой таблицы показать структуру
        for table in tables:
            print(f"\n{'='*60}")
            print(f"Таблица: {table}")
            print(f"{'='*60}")
            
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            
            print(f"{'ID':<5} {'Имя':<20} {'Тип':<15} {'NOT NULL':<10} {'По умолчанию'}")
            print("-"*60)
            for col in columns:
                cid, name, type_, notnull, default, pk = col
                print(f"{cid:<5} {name:<20} {type_:<15} {notnull:<10} {default}")
            
            # Количество записей
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"\nЗаписей: {count}")

except sqlite3.OperationalError as e:
    print(f"\n❌ Ошибка: {e}")
    print("\nБД не существует или повреждена.")
    print("Запустите: python test_auth.py")

print("\n" + "="*60)