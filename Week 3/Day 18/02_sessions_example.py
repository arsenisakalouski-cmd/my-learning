from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)

# ОБЯЗАТЕЛЬНО: секретный ключ для сессий
app.secret_key = 'your-secret-key-here-change-in-production'
"""
secret_key:
Используется для шифрования данных сессии

ВАЖНО:
В продакшене используйте случайный ключ:
import secrets
secrets.token_hex(16)
"""

@app.route('/login')
def login():
    """Сохранить данные в сессию"""
    
    # Записать в сессию
    session['username'] = 'Иван'
    session['user_id'] = 123
    session['is_admin'] = False
    """
    session - словарь
    Данные хранятся НА СЕРВЕРЕ
    
    session['key'] = value
    Работает как обычный словарь
    """
    
    return "Вы вошли в систему! <a href='/profile'>Профиль</a>"


@app.route('/profile')
def profile():
    """Прочитать данные из сессии"""
    
    # Проверить есть ли пользователь в сессии
    if 'username' in session:
        """
        'key' in session:
        Проверка существования ключа
        """
        
        username = session['username']
        user_id = session.get('user_id')
        """
        session.get('key'):
        Безопасное получение (вернёт None если нет)
        
        session['key']:
        Вызовет ошибку если ключа нет
        """
        
        return f"""
        <h1>Профиль</h1>
        <p>Имя: {username}</p>
        <p>ID: {user_id}</p>
        <a href="/logout">Выйти</a>
        """
    else:
        return "Вы не вошли. <a href='/login'>Войти</a>"
    

@app.route('/logout')
def logout():
    """Удалить данные из сессии"""
    
    # Способ 1: Удалить конкретный ключ
    session.pop('username', None)
    """
    session.pop('key', default):
    Удаляет ключ и возвращает значение
    default - что вернуть если ключа нет
    """
    
    # Способ 2: Очистить всю сессию
    session.clear()
    """
    session.clear():
    Удаляет ВСЕ данные из сессии
    """
    
    return "Вы вышли. <a href='/login'>Войти снова</a>"


@app.route('/update-profile')
def update_profile():
    """Изменить данные в сессии"""
    
    if 'username' in session:
        # Изменить существующее значение
        session['username'] = 'Иван Обновлённый'
        
        # Добавить новое значение
        session['last_activity'] = 'Обновление профиля'
        
        return "Профиль обновлён! <a href='/profile'>Посмотреть</a>"
    else:
        return "Сначала войдите. <a href='/login'>Войти</a>"
    

@app.route('/add-to-cart/<item>')
def add_to_cart(item):
    """Добавить товар в корзину"""
    
    # Получить корзину из сессии
    cart = session.get('cart', [])
    """
    session.get('cart', []):
    Если cart нет - вернёт пустой список []
    """
    
    # Добавить товар
    cart.append(item)
    
    # Сохранить обратно в сессию
    session['cart'] = cart
    """
    ВАЖНО:
    Для списков и словарей нужно переприсвоить:
    cart.append(item)         # НЕ сработает
    session['cart'] = cart    # Сработает
    
    ИЛИ включить:
    session.modified = True
    """
    
    return f"'{item}' добавлен в корзину. <a href='/cart'>Корзина</a>"    



@app.route('/cart')
def view_cart():
    """Просмотр корзины"""
    
    cart = session.get('cart', [])
    
    if cart:
        items_html = "<ul>"
        for item in cart:
            items_html += f"<li>{item}</li>"
        items_html += "</ul>"
        
        return f"""
        <h1>Корзина</h1>
        {items_html}
        <p>Всего товаров: {len(cart)}</p>
        <a href="/clear-cart">Очистить корзину</a>
        """
    else:
        return """
        <h1>Корзина пуста</h1>
        <p>Добавьте товары:</p>
        <ul>
            <li><a href="/add-to-cart/Ноутбук">Ноутбук</a></li>
            <li><a href="/add-to-cart/Мышь">Мышь</a></li>
            <li><a href="/add-to-cart/Клавиатура">Клавиатура</a></li>
        </ul>
        """
    



@app.route('/')
def index():
    """Главная страница"""
    
    # Проверить залогинен ли пользователь
    is_logged_in = 'username' in session
    
    return f"""
    <h1>Примеры работы с сессиями</h1>
    <p>Статус: {"Вы вошли" if is_logged_in else "Вы не вошли"}</p>
    
    <h2>Аутентификация</h2>
    <ul>
        <li><a href="/login">Войти</a></li>
        <li><a href="/profile">Профиль</a></li>
        <li><a href="/logout">Выйти</a></li>
    </ul>
    
    <h2>Корзина</h2>
    <ul>
        <li><a href="/cart">Посмотреть корзину</a></li>
        <li><a href="/add-to-cart/Товар1">Добавить товар</a></li>
    </ul>
    """


if __name__ == '__main__':
    app.run(debug=True, port=5006)



    
