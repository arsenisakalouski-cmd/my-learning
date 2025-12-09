from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/hello')
def hello():
    """Простой JSON ответ"""
    return jsonify({
        'message': 'Hello, World!',
        'status': 'success'
    })
    """
    jsonify():
    Преобразует Python dict в JSON
    Автоматически устанавливает Content-Type: application/json
    
    Результат:
    {
        "message": "Hello, World!",
        "status": "success"
    }
    """

@app.route('/success')
def success():
    """Успешный ответ (200)"""
    return jsonify({'message': 'Success'}), 200
    """
    return data, status_code
    
    200 - всё хорошо (по умолчанию)
    """


@app.route('/not-found')
def not_found():
    """Не найдено (404)"""
    return jsonify({
        'error': 'Not found',
        'message': 'Ресурс не найден'
    }), 404


@app.route('/error')
def error():
    """Ошибка сервера (500)"""
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'Что-то пошло не так'
    }), 500




users = [
    {'id': 1, 'name': 'Иван', 'age': 25},
    {'id': 2, 'name': 'Мария', 'age': 30},
    {'id': 3, 'name': 'Пётр', 'age': 28}
]

@app.route('/api/users', methods=['GET'])
def get_users():
    """Получить всех пользователей"""
    return jsonify({
        'users': users,
        'count': len(users)
    })


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Получить одного пользователя по ID"""
    
    # Найти пользователя
    user = next((u for u in users if u['id'] == user_id), None)
    """
    next(generator, default):
    Возвращает первый элемент или default
    
    (u for u in users if u['id'] == user_id)
    Генератор который ищет пользователя с нужным id
    """
    
    if user:
        return jsonify(user), 200
    else:
        return jsonify({
            'error': 'User not found',
            'message': f'Пользователь с ID {user_id} не найден'
        }), 404
    



@app.route('/api/users', methods=['POST'])
def create_user():
    """Создать нового пользователя"""
    
    # Получить данные из запроса
    data = request.get_json()
    """
    request.get_json():
    Парсит JSON из тела запроса
    Возвращает Python dict
    
    Клиент отправляет:
    {
        "name": "Анна",
        "age": 27
    }
    
    data = {'name': 'Анна', 'age': 27}
    """
    
    # Валидация
    if not data or 'name' not in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Поле name обязательно'
        }), 400
    
    # Создать пользователя
    new_user = {
        'id': len(users) + 1,
        'name': data['name'],
        'age': data.get('age', 0)
    }
    
    users.append(new_user)
    
    return jsonify({
        'message': 'User created',
        'user': new_user
    }), 201
    """
    201 Created:
    Используется когда ресурс успешно создан
    """

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Обновить пользователя"""
    
    # Найти пользователя
    user = next((u for u in users if u['id'] == user_id), None)
    
    if not user:
        return jsonify({
            'error': 'User not found'
        }), 404
    
    # Получить новые данные
    data = request.get_json()
    
    # Обновить
    if 'name' in data:
        user['name'] = data['name']
    if 'age' in data:
        user['age'] = data['age']
    
    return jsonify({
        'message': 'User updated',
        'user': user
    }), 200

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Удалить пользователя"""
    
    global users
    
    # Найти индекс
    user_index = next((i for i, u in enumerate(users) if u['id'] == user_id), None)
    
    if user_index is None:
        return jsonify({
            'error': 'User not found'
        }), 404
    
    # Удалить
    deleted_user = users.pop(user_index)
    
    return jsonify({
        'message': 'User deleted',
        'user': deleted_user
    }), 200


@app.route('/api/search', methods=['GET'])
def search():
    """Поиск с параметрами"""
    
    # GET /api/search?q=Иван&age=25
    query = request.args.get('q', '')
    age = request.args.get('age', type=int)
    
    results = users.copy()
    
    # Фильтр по имени
    if query:
        results = [u for u in results if query.lower() in u['name'].lower()]
    
    # Фильтр по возрасту
    if age:
        results = [u for u in results if u['age'] == age]
    
    return jsonify({
        'query': query,
        'age': age,
        'results': results,
        'count': len(results)
    })



@app.route('/')
def index():
    """Документация API"""
    return """
    <h1>API Documentation</h1>
    <h2>Endpoints:</h2>
    <ul>
        <li>GET /hello - Тестовый endpoint</li>
        <li>GET /api/users - Получить всех пользователей</li>
        <li>GET /api/users/&lt;id&gt; - Получить пользователя по ID</li>
        <li>POST /api/users - Создать пользователя</li>
        <li>PUT /api/users/&lt;id&gt; - Обновить пользователя</li>
        <li>DELETE /api/users/&lt;id&gt; - Удалить пользователя</li>
        <li>GET /api/search?q=query&age=25 - Поиск</li>
    </ul>
    
    <h2>Примеры:</h2>
    <pre>
    # Получить всех
    GET /api/users
    
    # Получить одного
    GET /api/users/1
    
    # Создать
    POST /api/users
    Body: {"name": "Анна", "age": 27}
    
    # Обновить
    PUT /api/users/1
    Body: {"age": 26}
    
    # Удалить
    DELETE /api/users/1
    
    # Поиск
    GET /api/search?q=Иван
    </pre>
    """


# ==========================================
# ОБРАБОТКА ОШИБОК
# ==========================================

@app.errorhandler(404)
def not_found_error(error):
    """Обработка 404"""
    return jsonify({
        'error': 'Not Found',
        'message': 'Endpoint не найден'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Обработка 500"""
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'Ошибка на сервере'
    }), 500


if __name__ == '__main__':
    print("="*60)
    print("API запущен на http://localhost:5008")
    print("="*60)
    print("\nПримеры запросов:")
    print("  GET  http://localhost:5008/api/users")
    print("  GET  http://localhost:5008/api/users/1")
    print("  POST http://localhost:5008/api/users")
    print("\nОткройте http://localhost:5008/ для документации")
    print("="*60)
    
    app.run(debug=True, port=5008)


    