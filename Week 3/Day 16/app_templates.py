from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def home():
    """
    render_template() - рендерит шаблон
    
    ПАРАМЕТРЫ:
    1. Имя файла шаблона (в папке templates/)
    2. Переменные для передачи в шаблон
    
    КАК РАБОТАЕТ:
    1. Flask находит templates/home.html
    2. Передаёт переменные name и features
    3. Jinja2 обрабатывает шаблон
    4. Возвращает готовый HTML
    """
    return render_template('home.html',
                         name='Арсений',
                         features=[
                             'Роутинг',
                             'Шаблоны',
                             'Динамические URL',
                             'Обработка форм',
                             'База данных'
                         ])
    # name='Арсений' - в шаблоне будет {{ name }}
    # features=[...] - в шаблоне можно делать {% for feature in features %}


@app.route('/about')
def about():
    """
    Передача нескольких переменных
    
    В шаблоне можем использовать:
    {{ show_stats }}
    {{ days }}
    {{ projects }}
    {{ user_type }}
    """
    return render_template('about.html',
                         show_stats=True,
                         days=16,
                         projects=14,
                         user_type='student')



@app.route('/contact')
def contact():
    """
    Передача списка словарей
    
    В шаблоне:
    {% for contact in contacts %}
        {{ contact['type'] }}
        {{ contact['value'] }}
    {% endfor %}
    """
    contacts_list = [
        {'type': 'Email', 'value': 'example@mail.com'},
        {'type': 'Телефон', 'value': '+7-900-123-45-67'},
        {'type': 'Telegram', 'value': '@username'}
    ]
    
    return render_template('contact.html',
                         contacts=contacts_list,
                         email='test@mail.com')


@app.route('/user/<username>')
def user_profile(username):
    """
    Динамический URL + шаблон
    
    Сначала создадим шаблон user.html
    """
    # Симулируем данные пользователя
    user_data = {
        'username': username,
        'age': 25,
        'city': 'Москва',
        'hobbies': ['Python', 'Flask', 'Web-разработка']
    }
    
    return render_template('user.html', user=user_data)


if __name__ == '__main__':
    app.run(debug=True, port=5002)