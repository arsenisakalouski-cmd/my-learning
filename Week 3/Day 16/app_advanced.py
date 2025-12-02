# app_advanced.py - Продвинутые роуты

from flask import Flask, redirect, url_for, request

app = Flask(__name__)

# ==========================================
# ДИНАМИЧЕСКИЕ URL
# ==========================================

@app.route('/user/<username>')
def user_profile(username):
    """
    Динамический URL с переменной
    
    <username> захватывает часть URL и передаёт в функцию
    
    Примеры:
    /user/john  -> username = "john"
    /user/mary  -> username = "mary"
    """
    return f"<h1>Профиль пользователя: {username}</h1>"


@app.route('/post/<int:post_id>')
def show_post(post_id):
    """
    URL с конвертером типа
    
    <int:post_id> - только целые числа
    
    /post/123  -> post_id = 123 (int)
    /post/abc  -> 404 ошибка
    """
    return f"""
    <h1>Пост #{post_id}</h1>
    <p>Содержимое поста номер {post_id}</p>
    <a href="/">На главную</a>
    """


@app.route('/calculate/<int:a>/<int:b>')
def calculate(a, b):
    """
    Несколько переменных в URL
    /calculate/5/3  -> a=5, b=3
    """
    result = a + b
    return f"""
    <h1>Калькулятор</h1>
    <p>{a} + {b} = {result}</p>
    """


# ==========================================
# HTTP МЕТОДЫ
# ==========================================

@app.route('/form', methods=['GET', 'POST'])
def form():
    """
    Роут с несколькими HTTP методами
    
    methods=['GET', 'POST'] разрешает оба метода
    """
    return "<h1>Форма</h1><p>GET и POST разрешены</p>"


# ==========================================
# РЕДИРЕКТ
# ==========================================

@app.route('/old-page')
def old_page():
    """
    Перенаправление на другой URL
    
    redirect() - перенаправить
    url_for('home') - получить URL функции home
    """
    return redirect(url_for('home'))


@app.route('/')
def home():
    """Главная страница"""
    return "<h1>Главная страница</h1>"


# ==========================================
# ОБРАБОТКА ОШИБОК
# ==========================================

@app.errorhandler(404)
def page_not_found(error):
    """
    Обработчик ошибки 404
    Вызывается когда страница не найдена
    """
    return """
    <h1>404 - Страница не найдена</h1>
    <p>Извините, такой страницы не существует</p>
    <a href="/">На главную</a>
    """, 404


@app.errorhandler(500)
def internal_error(error):
    """Обработчик ошибки 500"""
    return """
    <h1>500 - Внутренняя ошибка</h1>
    <p>Что-то пошло не так на сервере</p>
    """, 500


# ==========================================
# URL ПАРАМЕТРЫ
# ==========================================

@app.route('/search')
def search():
    """
    Получение параметров из URL
    
    /search?q=python&page=1
    request.args.get('q') получает параметр q
    """
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    return f"""
    <h1>Поиск</h1>
    <p>Запрос: {query}</p>
    <p>Страница: {page}</p>
    """


if __name__ == '__main__':
    app.run(debug=True, port=5001)