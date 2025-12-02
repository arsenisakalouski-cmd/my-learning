# app_forms.py - Работа с формами

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ==========================================
# ГЛАВНАЯ
# ==========================================

@app.route('/')
def home():
    """Главная страница"""
    return render_template('home.html',
                         name='Арсений',
                         features=[
                             'Роутинг',
                             'Шаблоны',
                             'Формы',
                             'Обработка данных'
                         ])


# ==========================================
# О НАС (добавьте этот роут)
# ==========================================

@app.route('/about')
def about():
    """Страница О нас"""
    return render_template('about.html',
                         show_stats=True,
                         days=16,
                         projects=14,
                         user_type='student')


# ==========================================
# КОНТАКТЫ (переименуйте существующий)
# ==========================================

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Контактная форма
    GET  - показывает форму
    POST - обрабатывает данные
    """
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # После обработки - редирект
        return redirect(url_for('contact_success'))
    
    # GET - показываем форму
    return render_template('contact_form.html')


@app.route('/contact/success')
def contact_success():
    """Страница успеха после отправки"""
    return """
    <h1>Сообщение отправлено!</h1>
    <a href="/">На главную</a>
    """


# ==========================================
# ФОРМА - GET (показать форму)
# ==========================================

@app.route('/form')
def form_example():
    """Показать форму"""
    return render_template('form_example.html')


# ==========================================
# ОБРАБОТКА ФОРМЫ - POST
# ==========================================

@app.route('/form-handler', methods=['POST'])
def form_handler():
    """Обработать данные формы"""
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    print(f"Получено сообщение от {name} ({email})")
    print(f"Текст: {message}")
    
    return render_template('form_result.html',
                         name=name,
                         email=email,
                         message=message)


# ==========================================
# РЕГИСТРАЦИЯ
# ==========================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Регистрация с валидацией"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()
        
        # ВАЛИДАЦИЯ
        errors = []
        
        if len(username) < 3:
            errors.append('Имя должно быть минимум 3 символа')
        
        if len(password) < 6:
            errors.append('Пароль должен быть минимум 6 символов')
        
        if '@' not in email or '.' not in email:
            errors.append('Некорректный email')
        
        if errors:
            return render_template('register.html',
                                 errors=errors,
                                 username=username,
                                 email=email)
        
        return f"<h1>Регистрация успешна!</h1><p>Пользователь: {username}</p>"
    
    return render_template('register.html', errors=[])


# ==========================================
# ПОИСК
# ==========================================

@app.route('/search')
def search():
    """Поиск через GET параметры"""
    query = request.args.get('q', '')
    category = request.args.get('category', 'all')
    page = request.args.get('page', 1, type=int)
    
    if query:
        results = [
            f"Результат 1 для '{query}'",
            f"Результат 2 для '{query}'",
            f"Результат 3 для '{query}'",
        ]
    else:
        results = []
    
    return render_template('search.html',
                         query=query,
                         category=category,
                         page=page,
                         results=results)
@app.route('/routes')
def list_routes():
    """Список всех роутов для отладки"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(f"{rule.endpoint}: {rule.rule}")
    return "<br>".join(routes)

if __name__ == '__main__':
    app.run(debug=True, port=5003)