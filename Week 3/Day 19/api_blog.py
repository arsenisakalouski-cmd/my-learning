from flask import Flask, jsonify, request
import sys
import os

# Добавить путь к модулям из Day 18
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Day 18'))

import database as db

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Инициализация БД
db.init_db()


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Получить все посты
    
    Query параметры:
        - limit: количество постов (по умолчанию все)
        - offset: смещение (для пагинации)
    
    Пример: GET /api/posts?limit=10&offset=0
    """
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', default=0, type=int)
    
    posts = db.get_all_posts()
    
    # Пагинация
    if limit:
        posts = posts[offset:offset + limit]
    
    # Добавить количество комментариев
    for post in posts:
        post['comment_count'] = db.get_comment_count(post['id'])
    
    return jsonify({
        'posts': posts,
        'count': len(posts),
        'offset': offset,
        'limit': limit
    }), 200


@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """
    Получить один пост по ID
    
    Пример: GET /api/posts/1
    """
    post = db.get_post_by_id(post_id)
    
    if not post:
        return jsonify({
            'error': 'Not Found',
            'message': f'Пост с ID {post_id} не найден'
        }), 404
    
    # Добавить комментарии
    post['comments'] = db.get_comments_for_post(post_id)
    post['comment_count'] = len(post['comments'])
    
    return jsonify(post), 200




@app.route('/api/posts', methods=['POST'])
def create_post():
    """
    Создать новый пост
    
    Body (JSON):
    {
        "title": "Заголовок",
        "content": "Содержимое",
        "author": "Имя автора",
        "author_id": 1  // необязательно
    }
    
    Пример: POST /api/posts
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'JSON данные отсутствуют'
        }), 400
    
    # Валидация
    errors = []
    
    if 'title' not in data or len(data['title'].strip()) < 5:
        errors.append('Заголовок обязателен (минимум 5 символов)')
    
    if 'content' not in data or len(data['content'].strip()) < 20:
        errors.append('Содержимое обязательно (минимум 20 символов)')
    
    if 'author' not in data or len(data['author'].strip()) < 2:
        errors.append('Имя автора обязательно')
    
    if errors:
        return jsonify({
            'error': 'Validation Error',
            'message': 'Ошибки валидации',
            'errors': errors
        }), 400
    
    # Создать пост
    post_id = db.create_post(
        data['title'].strip(),
        data['content'].strip(),
        data['author'].strip(),
        data.get('author_id')
    )
    
    # Получить созданный пост
    post = db.get_post_by_id(post_id)
    
    return jsonify({
        'message': 'Post created successfully',
        'post': post
    }), 201


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Обновить пост
    
    Body (JSON):
    {
        "title": "Новый заголовок",
        "content": "Новое содержимое"
    }
    
    Пример: PUT /api/posts/1
    """
    post = db.get_post_by_id(post_id)
    
    if not post:
        return jsonify({
            'error': 'Not Found',
            'message': f'Пост с ID {post_id} не найден'
        }), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'JSON данные отсутствуют'
        }), 400
    
    # Получить новые значения или оставить старые
    title = data.get('title', post['title']).strip()
    content = data.get('content', post['content']).strip()
    
    # Валидация
    if len(title) < 5:
        return jsonify({
            'error': 'Validation Error',
            'message': 'Заголовок должен быть минимум 5 символов'
        }), 400
    
    if len(content) < 20:
        return jsonify({
            'error': 'Validation Error',
            'message': 'Содержимое должно быть минимум 20 символов'
        }), 400
    
    # Обновить
    db.update_post(post_id, title, content)
    
    # Получить обновлённый пост
    updated_post = db.get_post_by_id(post_id)
    
    return jsonify({
        'message': 'Post updated successfully',
        'post': updated_post
    }), 200



@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Удалить пост
    
    Пример: DELETE /api/posts/1
    """
    post = db.get_post_by_id(post_id)
    
    if not post:
        return jsonify({
            'error': 'Not Found',
            'message': f'Пост с ID {post_id} не найден'
        }), 404
    
    # Удалить
    db.delete_post(post_id)
    
    return jsonify({
        'message': 'Post deleted successfully',
        'post': post
    }), 200



@app.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    """
    Получить комментарии к посту
    
    Пример: GET /api/posts/1/comments
    """
    post = db.get_post_by_id(post_id)
    
    if not post:
        return jsonify({
            'error': 'Not Found',
            'message': f'Пост с ID {post_id} не найден'
        }), 404
    
    comments = db.get_comments_for_post(post_id)
    
    return jsonify({
        'post_id': post_id,
        'comments': comments,
        'count': len(comments)
    }), 200



@app.route('/api/search', methods=['GET'])
def search():
    """
    Поиск постов
    
    Query параметры:
        - q: поисковый запрос
    
    Пример: GET /api/search?q=python
    """
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Параметр q обязателен'
        }), 400
    
    posts = db.search_posts(query)
    
    # Добавить количество комментариев
    for post in posts:
        post['comment_count'] = db.get_comment_count(post['id'])
    
    return jsonify({
        'query': query,
        'posts': posts,
        'count': len(posts)
    }), 200


@app.route('/api/stats', methods=['GET'])
def stats():
    """
    Статистика блога
    
    Пример: GET /api/stats
    """
    statistics = db.get_stats()
    
    return jsonify(statistics), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Получить пользователя по ID
    
    Пример: GET /api/users/1
    """
    user = db.get_user_by_id(user_id)
    
    if not user:
        return jsonify({
            'error': 'Not Found',
            'message': f'Пользователь с ID {user_id} не найден'
        }), 404
    
    return jsonify(user), 200






@app.route('/')
def index():
    """API документация"""
    return """
    <h1>Blog REST API</h1>
    
    <h2>Posts Endpoints:</h2>
    <ul>
        <li><code>GET /api/posts</code> - Получить все посты</li>
        <li><code>GET /api/posts?limit=10&offset=0</code> - С пагинацией</li>
        <li><code>GET /api/posts/{id}</code> - Получить пост по ID</li>
        <li><code>POST /api/posts</code> - Создать пост</li>
        <li><code>PUT /api/posts/{id}</code> - Обновить пост</li>
        <li><code>DELETE /api/posts/{id}</code> - Удалить пост</li>
    </ul>
    
    <h2>Comments Endpoints:</h2>
    <ul>
        <li><code>GET /api/posts/{id}/comments</code> - Получить комментарии</li>
        <li><code>POST /api/posts/{id}/comments</code> - Добавить комментарий</li>
    </ul>
    
    <h2>Other Endpoints:</h2>
    <ul>
        <li><code>GET /api/search?q=query</code> - Поиск постов</li>
        <li><code>GET /api/stats</code> - Статистика</li>
        <li><code>GET /api/users/{id}</code> - Получить пользователя</li>
    </ul>
    
    <h2>Примеры:</h2>
    <pre>
# Получить все посты
GET /api/posts

# Получить пост #1
GET /api/posts/1

# Создать пост
POST /api/posts
Body: {
    "title": "Новый пост",
    "content": "Содержимое поста минимум 20 символов",
    "author": "Иван"
}

# Обновить пост
PUT /api/posts/1
Body: {
    "title": "Обновлённый заголовок"
}

# Добавить комментарий
POST /api/posts/1/comments
Body: {
    "author": "Мария",
    "content": "Отличный пост!"
}

# Поиск
GET /api/search?q=python

# Статистика
GET /api/stats
    </pre>
    
    <h2>Status коды:</h2>
    <ul>
        <li><code>200 OK</code> - Успех</li>
        <li><code>201 Created</code> - Создано</li>
        <li><code>400 Bad Request</code> - Неправильный запрос</li>
        <li><code>404 Not Found</code> - Не найдено</li>
        <li><code>500 Internal Server Error</code> - Ошибка сервера</li>
    </ul>
    """


# ==========================================
# ОБРАБОТКА ОШИБОК
# ==========================================

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'Endpoint не найден'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'Ошибка на сервере'
    }), 500


if __name__ == '__main__':
    print("="*60)
    print("BLOG API запущен на http://localhost:5009")
    print("="*60)
    print("\nОсновные endpoints:")
    print("  GET    /api/posts")
    print("  POST   /api/posts")
    print("  GET    /api/posts/{id}")
    print("  PUT    /api/posts/{id}")
    print("  DELETE /api/posts/{id}")
    print("\nОткройте http://localhost:5009/ для документации")
    print("="*60)
    
    app.run(debug=True, port=5009)