from flask import Flask, jsonify, request
import sys
import os
import secrets
from functools import wraps

# Добавить путь к модулям
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Day 18'))

import database as db

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Инициализация БД
db.init_db()


tokens = {}
"""
tokens = {
    'abc123def456': {
        'user_id': 1,
        'username': 'ivan'
    }
}
"""



def generate_token():
    """Создать случайный токен"""
    return secrets.token_hex(32)
    """
    secrets.token_hex(32):
    Генерирует безопасную случайную строку
    32 байта = 64 hex символа
    
    Пример: 'a1b2c3d4e5f6...'
    """

def token_required(f):
    """
    Декоратор для защиты endpoints
    Требует валидный токен в заголовке
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Получить токен из заголовка
        token = request.headers.get('Authorization')
        """
        Authorization header:
        Authorization: Bearer abc123def456
        или
        Authorization: abc123def456
        """
        
        # Убрать "Bearer " если есть
        if token and token.startswith('Bearer '):
            token = token.replace('Bearer ', '')
        
        if not token:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Токен отсутствует'
            }), 401
        
        # Проверить токен
        user_data = tokens.get(token)
        
        if not user_data:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Неверный токен'
            }), 401
        
        # Передать данные пользователя в функцию
        return f(user_data, *args, **kwargs)
    
    return decorated


@app.route('/api/auth/register', methods=['POST'])
def register():
    """
    Регистрация
    
    Body:
    {
        "username": "ivan",
        "email": "ivan@mail.com",
        "password": "password123"
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'JSON данные отсутствуют'
        }), 400
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    # Регистрация
    success, result = db.register_user(username, email, password)
    
    if not success:
        return jsonify({
            'error': 'Registration Failed',
            'message': result
        }), 400
    
    return jsonify({
        'message': 'User registered successfully',
        'user_id': result
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    Вход
    
    Body:
    {
        "username": "ivan",
        "password": "password123"
    }
    
    Response:
    {
        "token": "abc123...",
        "user": {...}
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'JSON данные отсутствуют'
        }), 400
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    # Проверить логин/пароль
    success, result = db.login_user(username, password)
    
    if not success:
        return jsonify({
            'error': 'Login Failed',
            'message': result
        }), 401
    
    # Создать токен
    token = generate_token()
    
    # Сохранить токен
    tokens[token] = {
        'user_id': result['id'],
        'username': result['username']
    }
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': result
    }), 200


@app.route('/api/auth/logout', methods=['POST'])
@token_required
def logout(current_user):
    """
    Выход
    
    Headers:
    Authorization: Bearer abc123...
    """
    # Получить токен
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    # Удалить токен
    if token in tokens:
        del tokens[token]
    
    return jsonify({
        'message': 'Logout successful'
    }), 200


@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """
    Получить данные текущего пользователя
    
    Headers:
    Authorization: Bearer abc123...
    """
    user = db.get_user_by_id(current_user['user_id'])
    
    return jsonify(user), 200


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Получить все посты (публичный)"""
    posts = db.get_all_posts()
    
    for post in posts:
        post['comment_count'] = db.get_comment_count(post['id'])
    
    return jsonify({
        'posts': posts,
        'count': len(posts)
    }), 200




@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Получить пост (публичный)"""
    post = db.get_post_by_id(post_id)
    
    if not post:
        return jsonify({
            'error': 'Not Found',
            'message': f'Пост {post_id} не найден'
        }), 404
    
    post['comments'] = db.get_comments_for_post(post_id)
    
    return jsonify(post), 200


@app.route('/api/posts', methods=['POST'])
@token_required
def create_post(current_user):
    """Создать пост (требует токен)"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'JSON данные отсутствуют'
        }), 400
    
    # Валидация
    if 'title' not in data or len(data['title'].strip()) < 5:
        return jsonify({
            'error': 'Validation Error',
            'message': 'Заголовок обязателен (минимум 5 символов)'
        }), 400
    
    if 'content' not in data or len(data['content'].strip()) < 20:
        return jsonify({
            'error': 'Validation Error',
            'message': 'Содержимое обязательно (минимум 20 символов)'
        }), 400
    
    # Создать пост от имени текущего пользователя
    post_id = db.create_post(
        data['title'].strip(),
        data['content'].strip(),
        current_user['username'],
        current_user['user_id']
    )
    
    post = db.get_post_by_id(post_id)
    
    return jsonify({
        'message': 'Post created successfully',
        'post': post
    }), 201



@app.route('/api/posts/<int:post_id>', methods=['PUT'])
@token_required
def update_post(current_user, post_id):
    """Обновить пост (только автор)"""
    post = db.get_post_by_id(post_id)
    
    if not post:
        return jsonify({
            'error': 'Not Found',
            'message': f'Пост {post_id} не найден'
        }), 404
    
    # Проверить авторство
    if post.get('author_id') != current_user['user_id']:
        return jsonify({
            'error': 'Forbidden',
            'message': 'Вы можете редактировать только свои посты'
        }), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'JSON данные отсутствуют'
        }), 400
    
    title = data.get('title', post['title']).strip()
    content = data.get('content', post['content']).strip()
    
    # Валидация
    if len(title) < 5 or len(content) < 20:
        return jsonify({
            'error': 'Validation Error',
            'message': 'Заголовок >= 5, содержимое >= 20 символов'
        }), 400
    
    db.update_post(post_id, title, content)
    updated_post = db.get_post_by_id(post_id)
    
    return jsonify({
        'message': 'Post updated successfully',
        'post': updated_post
    }), 200



@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, post_id):
    """Удалить пост (только автор)"""
    post = db.get_post_by_id(post_id)
    
    if not post:
        return jsonify({
            'error': 'Not Found',
            'message': f'Пост {post_id} не найден'
        }), 404
    
    # Проверить авторство
    if post.get('author_id') != current_user['user_id']:
        return jsonify({
            'error': 'Forbidden',
            'message': 'Вы можете удалять только свои посты'
        }), 403
    
    db.delete_post(post_id)
    
    return jsonify({
        'message': 'Post deleted successfully',
        'post': post
    }), 200


@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
@token_required
def add_comment(current_user, post_id):
    """Добавить комментарий (требует токен)"""
    post = db.get_post_by_id(post_id)
    
    if not post:
        return jsonify({
            'error': 'Not Found',
            'message': f'Пост {post_id} не найден'
        }), 404
    
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Поле content обязательно'
        }), 400
    
    content = data['content'].strip()
    
    if len(content) < 3:
        return jsonify({
            'error': 'Validation Error',
            'message': 'Комментарий должен быть минимум 3 символа'
        }), 400
    
    # Добавить от имени текущего пользователя
    comment_id = db.add_comment(
        post_id,
        current_user['username'],
        content
    )
    
    comments = db.get_comments_for_post(post_id)
    new_comment = next((c for c in comments if c['id'] == comment_id), None)
    
    return jsonify({
        'message': 'Comment added successfully',
        'comment': new_comment
    }), 201



@app.route('/')
def index():
    return """
    <h1>Blog API с аутентификацией</h1>
    
    <h2>Auth Endpoints:</h2>
    <ul>
        <li><code>POST /api/auth/register</code> - Регистрация</li>
        <li><code>POST /api/auth/login</code> - Вход (получить токен)</li>
        <li><code>POST /api/auth/logout</code> - Выход (требует токен)</li>
        <li><code>GET /api/auth/me</code> - Мои данные (требует токен)</li>
    </ul>
    
    <h2>Posts (защищённые):</h2>
    <ul>
        <li><code>GET /api/posts</code> - Все посты (публично)</li>
        <li><code>GET /api/posts/{id}</code> - Один пост (публично)</li>
        <li><code>POST /api/posts</code> - Создать (🔒 токен)</li>
        <li><code>PUT /api/posts/{id}</code> - Обновить (🔒 токен + автор)</li>
        <li><code>DELETE /api/posts/{id}</code> - Удалить (🔒 токен + автор)</li>
        <li><code>POST /api/posts/{id}/comments</code> - Комментарий (🔒 токен)</li>
    </ul>
    
    <h2>Пример использования:</h2>
    <pre>
# 1. Регистрация
POST /api/auth/register
Body: {"username": "ivan", "email": "ivan@mail.com", "password": "password123"}

# 2. Вход
POST /api/auth/login
Body: {"username": "ivan", "password": "password123"}
Response: {"token": "abc123..."}

# 3. Использование токена
POST /api/posts
Headers: Authorization: Bearer abc123...
Body: {"title": "Пост", "content": "Содержимое минимум 20 символов"}

# 4. Выход
POST /api/auth/logout
Headers: Authorization: Bearer abc123...
    </pre>
    """



@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'Endpoint не найден'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'Ошибка сервера'
    }), 500


if __name__ == '__main__':
    print("="*60)
    print("AUTH API запущен на http://localhost:5010")
    print("="*60)
    print("\nАутентификация через токены!")
    print("Сначала зарегистрируйтесь и получите токен")
    print("\nОткройте http://localhost:5010/ для документации")
    print("="*60)
    
    app.run(debug=True, port=5010)

    