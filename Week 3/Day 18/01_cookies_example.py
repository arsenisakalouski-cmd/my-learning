from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)


@app.route('/set-cookie')
def set_cookie():
    """Установить cookie"""
    
    # Создать response объект
    response = make_response("Cookie установлен!")
    """
    make_response():
    Создаёт Response объект
    Нужен чтобы модифицировать headers, cookies и т.д.
    """
    
    # Установить cookie
    response.set_cookie('username', 'Иван', max_age=60*60*24)
    """
    set_cookie(key, value, max_age):
    - key: имя cookie
    - value: значение
    - max_age: время жизни в секундах
      60*60*24 = 1 день
    
    ДРУГИЕ ПАРАМЕТРЫ:
    - expires: дата истечения
    - path: путь (по умолчанию '/')
    - domain: домен
    - secure: только HTTPS
    - httponly: недоступен из JavaScript (безопаснее)
    """
    
    return response



@app.route('/get-cookie')
def get_cookie():
    """Прочитать cookie"""
    
    # Получить cookie
    username = request.cookies.get('username')
    """
    request.cookies:
    Словарь со всеми cookies
    
    .get('username'):
    Безопасное получение (вернёт None если нет)
    """
    
    if username:
        return f"Привет, {username}!"
    else:
        return "Cookie не найден. <a href='/set-cookie'>Установить</a>"




@app.route('/delete-cookie')
def delete_cookie():
    """Удалить cookie"""
    
    response = make_response("Cookie удалён!")
    
    # Удалить cookie
    response.delete_cookie('username')
    """
    delete_cookie(key):
    Удаляет cookie установив max_age=0
    """
    
    return response




@app.route('/counter')
def counter():
    """Счётчик посещений через cookie"""
    
    # Получить текущее значение
    count = request.cookies.get('visit_count', '0')
    count = int(count)
    
    # Увеличить
    count += 1
    
    # Сохранить
    response = make_response(f"Вы посетили эту страницу {count} раз(а)")
    response.set_cookie('visit_count', str(count))
    
    return response



@app.route('/theme')
def theme():
    """Переключение темы"""
    
    # Получить текущую тему
    current_theme = request.cookies.get('theme', 'light')
    
    # Переключить
    new_theme = 'dark' if current_theme == 'light' else 'light'
    
    # HTML с применением темы
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                background: {'#333' if new_theme == 'dark' else '#fff'};
                color: {'#fff' if new_theme == 'dark' else '#333'};
                font-family: Arial;
                padding: 50px;
                text-align: center;
            }}
            button {{
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        <h1>Текущая тема: {new_theme}</h1>
        <p>Тема сохранена в cookie!</p>
        <a href="/theme"><button>Переключить тему</button></a>
    </body>
    </html>
    """
    
    response = make_response(html)
    response.set_cookie('theme', new_theme)
    
    return response


@app.route('/')
def index():
    """Главная страница с примерами"""
    return """
    <h1>Примеры работы с Cookies</h1>
    <ul>
        <li><a href="/set-cookie">Установить cookie</a></li>
        <li><a href="/get-cookie">Прочитать cookie</a></li>
        <li><a href="/delete-cookie">Удалить cookie</a></li>
        <li><a href="/counter">Счётчик посещений</a></li>
        <li><a href="/theme">Переключение темы</a></li>
    </ul>
    """


if __name__ == '__main__':
    app.run(debug=True, port=5005)