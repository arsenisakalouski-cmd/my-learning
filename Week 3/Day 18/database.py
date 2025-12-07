import sqlite3
from datetime import datetime

DATABASE = 'blog.db'

def init_db():
    """Создать БД и таблицы"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        # Таблица постов
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
        
        # Таблица комментариев
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts (id)
        )
        """)
        """
        FOREIGN KEY:
        Связь между таблицами
        
        post_id INTEGER NOT NULL - столбец для связи
        FOREIGN KEY (post_id) REFERENCES posts (id)
        - post_id ссылается на id из таблицы posts
        
        Это значит:
        Комментарий всегда привязан к конкретному посту
        """

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        conn.commit()
        print("✓ База данных инициализирована")


def dict_factory(cursor, row):
    """
    Преобразовать строку БД в словарь
    
    Вместо: (1, 'Title', 'Content')
    Получим: {'id': 1, 'title': 'Title', 'content': 'Content'}
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



def create_post(title, content, author, author_id=None):
    """Создать новый пост"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO posts (title, content, author, author_id)
        VALUES (?, ?, ?, ?)
        """, (title, content, author, author_id))
        conn.commit()
        return cursor.lastrowid
    
def get_all_posts():
    """Получить все посты"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM posts 
        ORDER BY created_at DESC
        """)
        return cursor.fetchall()


def get_post_by_id(post_id):
    """Получить пост по ID"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        return cursor.fetchone()


def update_post(post_id, title, content):
    """Обновить пост"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE posts 
        SET title = ?, content = ?
        WHERE id = ?
        """, (title, content, post_id))
        conn.commit()
        return cursor.rowcount > 0


def delete_post(post_id):
    """Удалить пост"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        # Сначала удалить все комментарии к посту
        cursor.execute("DELETE FROM comments WHERE post_id = ?", (post_id,))
        
        # Потом удалить сам пост
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        
        conn.commit()
        return cursor.rowcount > 0



def increment_views(post_id):
    """Увеличить счётчик просмотров"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE posts 
        SET views = views + 1
        WHERE id = ?
        """, (post_id,))
        conn.commit()


def search_posts(query):
    """Поиск постов"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM posts 
        WHERE title LIKE ? OR content LIKE ?
        ORDER BY created_at DESC
        """, (f'%{query}%', f'%{query}%'))
        return cursor.fetchall()


def add_comment(post_id, author, content):
    """Добавить комментарий к посту"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO comments (post_id, author, content)
        VALUES (?, ?, ?)
        """, (post_id, author, content))
        conn.commit()
        return cursor.lastrowid


def get_comments_for_post(post_id):
    """Получить все комментарии к посту"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM comments 
        WHERE post_id = ?
        ORDER BY created_at ASC
        """, (post_id,))
        return cursor.fetchall()


def get_comment_count(post_id):
    """Получить количество комментариев"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT COUNT(*) FROM comments WHERE post_id = ?
        """, (post_id,))
        return cursor.fetchone()[0]

def get_stats():
    """Получить статистику блога"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        # Общее количество постов
        cursor.execute("SELECT COUNT(*) FROM posts")
        total_posts = cursor.fetchone()[0]
        
        # Общее количество комментариев
        cursor.execute("SELECT COUNT(*) FROM comments")
        total_comments = cursor.fetchone()[0]
        
        # Общее количество просмотров
        cursor.execute("SELECT SUM(views) FROM posts")
        total_views = cursor.fetchone()[0] or 0
        
        # Самый популярный пост
        cursor.execute("""
        SELECT title, views FROM posts 
        ORDER BY views DESC LIMIT 1
        """)
        popular = cursor.fetchone()
        
        return {
            'total_posts': total_posts,
            'total_comments': total_comments,
            'total_views': total_views,
            'popular_post': popular[0] if popular else None,
            'popular_views': popular[1] if popular else 0
        }
    





















import bcrypt

def create_users_table():
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
        conn.commit()



def register_user(username, email, password):
    """
    Зарегистрировать нового пользователя
    
    Возвращает:
        (bool, str или int): (успех, сообщение_об_ошибке или user_id)
    """
    # Валидация
    if len(username) < 3:
        return False, "Имя должно быть минимум 3 символа"
    
    if len(password) < 6:
        return False, "Пароль должен быть минимум 6 символов"
    
    if '@' not in email or '.' not in email:
        return False, "Некорректный email"
    
    # Хеширование пароля
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt)
    password_hash_str = password_hash.decode('utf-8')
    
    # Сохранение
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
            """, (username, email, password_hash_str))
            conn.commit()
            return True, cursor.lastrowid
    
    except sqlite3.IntegrityError:
        return False, "Пользователь с таким именем или email уже существует"




def login_user(username, password):
    """
    Проверить логин/пароль
    
    Возвращает:
        (bool, dict или str): (успех, данные_пользователя или сообщение)
    """
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if not user:
            return False, "Пользователь не найден"
        
        # Проверить пароль
        password_bytes = password.encode('utf-8')
        stored_hash = user['password_hash'].encode('utf-8')
        
        if bcrypt.checkpw(password_bytes, stored_hash):
            # Удалить пароль из результата
            del user['password_hash']
            return True, user
        else:
            return False, "Неверный пароль"
        
def get_user_by_id(user_id):
    """Получить пользователя по ID"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, created_at FROM users WHERE id = ?", 
                      (user_id,))
        return cursor.fetchone()


def get_user_by_username(username):
    """Получить пользователя по username"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, created_at FROM users WHERE username = ?", 
                      (username,))
        return cursor.fetchone()



