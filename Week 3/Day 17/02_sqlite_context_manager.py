import sqlite3
from datetime import datetime

def create_database():
    with sqlite3.connect('blog.db') as conn:
        """
        with - контекстный менеджер
        Автоматически:
        1. Открывает соединение
        2. Выполняет код внутри
        3. Закрывает соединение (даже при ошибке)
        """
        cursor = conn.cursor()
        
        # Создаём таблицу постов
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            views INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        conn.commit()
        print("✓ База данных создана")

def add_post(title, content, author):
    """Добавить новый пост"""
    with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO posts (title, content, author)
        VALUES (?, ?, ?)
        """, (title, content, author))
        
        conn.commit()
        
        # Получить ID последней добавленной записи
        post_id = cursor.lastrowid
        """
        lastrowid:
        ID последней вставленной строки
        """
        
        print(f"✓ Пост добавлен с ID: {post_id}")
        return post_id





def get_all_posts():
    """Получить все посты"""
    with sqlite3.connect('blog.db') as conn:
        # Включаем Row factory
        conn.row_factory = sqlite3.Row
        """
        row_factory = sqlite3.Row:
        Позволяет обращаться к столбцам по имени
        
        БЕЗ Row:
        row[0], row[1], row[2]  # По индексу
        
        С Row:
        row['title'], row['author']  # По имени
        """
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
        """
        ORDER BY created_at DESC:
        Сортировка по дате создания
        DESC - по убыванию (новые первые)
        ASC - по возрастанию (старые первые)
        """
        
        posts = cursor.fetchall()
        return posts
    



def get_post_by_id(post_id):
    """Получить пост по ID"""
    with sqlite3.connect('blog.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        post = cursor.fetchone()
        
        return post
    

def update_post(post_id, title, content):
    """Обновить пост"""
    with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
        UPDATE posts 
        SET title = ?, content = ?
        WHERE id = ?
        """, (title, content, post_id))
        
        conn.commit()
        
        # Проверить сколько строк изменено
        if cursor.rowcount > 0:
            """
            rowcount:
            Количество затронутых строк
            """
            print(f"✓ Пост {post_id} обновлён")
            return True
        else:
            print(f"✗ Пост {post_id} не найден")
            return False


def delete_post(post_id):
    """Удалить пост"""
    with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"✓ Пост {post_id} удалён")
            return True
        else:
            print(f"✗ Пост {post_id} не найден")
            return False
        



def increment_views(post_id):
    """Увеличить счётчик просмотров"""
    with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
        UPDATE posts 
        SET views = views + 1
        WHERE id = ?
        """, (post_id,))
        """
        views = views + 1:
        Увеличить текущее значение на 1
        """
        
        conn.commit()


def search_posts(query):
    """Поиск постов"""
    with sqlite3.connect('blog.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT * FROM posts 
        WHERE title LIKE ? OR content LIKE ?
        ORDER BY created_at DESC
        """, (f'%{query}%', f'%{query}%'))
        """
        LIKE:
        Поиск по шаблону
        
        % - любые символы
        'Python%' - начинается с Python
        '%Python' - заканчивается на Python
        '%Python%' - содержит Python
        
        OR:
        Логическое ИЛИ
        title LIKE ... OR content LIKE ...
        """
        
        posts = cursor.fetchall()
        return posts



if __name__ == '__main__':
    print("="*60)
    print("ТЕСТИРОВАНИЕ ФУНКЦИЙ БД")
    print("="*60)
    
    # 1. Создать БД
    create_database()
    
    # 2. Добавить посты
    print("\n1. Добавление постов:")
    post1_id = add_post(
        "Изучаем Python",
        "Python - отличный язык для начинающих",
        "Иван"
    )
    
    post2_id = add_post(
        "Изучаем Flask",
        "Flask - микрофреймворк для веб-разработки",
        "Мария"
    )
    
    post3_id = add_post(
        "Базы данных SQLite",
        "SQLite - встроенная БД в Python",
        "Иван"
    )
     # 3. Получить все посты
    print("\n2. Все посты:")
    all_posts = get_all_posts()
    for post in all_posts:
        print(f"  [{post['id']}] {post['title']} by {post['author']}")
    
    # 4. Получить один пост
    print("\n3. Пост #1:")
    post = get_post_by_id(post1_id)
    if post:
        print(f"  Заголовок: {post['title']}")
        print(f"  Автор: {post['author']}")
        print(f"  Просмотры: {post['views']}")
    
    # 5. Увеличить просмотры
    print("\n4. Увеличение просмотров:")
    increment_views(post1_id)
    increment_views(post1_id)
    increment_views(post1_id)
    
    post = get_post_by_id(post1_id)
    print(f"  Просмотры поста #1: {post['views']}")
    
    # 6. Обновить пост
    print("\n5. Обновление поста:")
    update_post(post2_id, "Flask для начинающих", "Обновлённый контент")
    
    # 7. Поиск
    print("\n6. Поиск по слову 'Python':")
    results = search_posts("Python")
    for post in results:
        print(f"  [{post['id']}] {post['title']}")
    
    # 8. Удаление
    print("\n7. Удаление поста:")
    delete_post(post3_id)
    
    # 9. Финальный список
    print("\n8. Финальный список:")
    all_posts = get_all_posts()
    for post in all_posts:
        print(f"  [{post['id']}] {post['title']} (просмотров: {post['views']})")
    
    print("\n" + "="*60)
    print("✓ Все операции выполнены успешно!")
    print("✓ Создан файл blog.db")
    


