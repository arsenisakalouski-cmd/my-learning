# view_db.py - Просмотр содержимого БД

import sqlite3

def view_database(db_name):
    """Показать содержимое БД"""
    with sqlite3.connect(db_name) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Получить список таблиц
        cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table'
        """)
        """
        sqlite_master:
        Системная таблица со списком всех таблиц
        """
        
        tables = cursor.fetchall()
        
        print(f"\n{'='*60}")
        print(f"База данных: {db_name}")
        print(f"{'='*60}")
        
        for table in tables:
            table_name = table['name']
            print(f"\nТаблица: {table_name}")
            print("-"*60)
            
            # Получить все строки из таблицы
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            if rows:
                # Заголовки столбцов
                headers = rows[0].keys()
                print(" | ".join(headers))
                print("-"*60)
                
                # Данные
                for row in rows:
                    values = [str(row[key]) for key in headers]
                    print(" | ".join(values))
            else:
                print("Таблица пуста")


if __name__ == '__main__':
    view_database('blog.db')