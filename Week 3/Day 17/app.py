from flask import Flask, render_template, request, redirect, url_for, flash
import database as db

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
"""
secret_key:
Нужен для flash сообщений и сессий
Должен быть случайным и секретным в продакшене
"""

# Инициализация БД при запуске
db.init_db()

@app.route('/')
def index():
    """Главная - список всех постов"""
    posts = db.get_all_posts()
    
    # Добавить количество комментариев к каждому посту
    for post in posts:
        post['comment_count'] = db.get_comment_count(post['id'])
    
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    """Просмотр конкретного поста"""
    post = db.get_post_by_id(post_id)
    
    if not post:
        """
        flash():
        Показать одноразовое сообщение пользователю
        
        Категории:
        'success' - успех (зелёный)
        'error' - ошибка (красный)
        'warning' - предупреждение (жёлтый)
        'info' - информация (синий)
        """
        flash('Пост не найден', 'error')
        return redirect(url_for('index'))
    
    # Увеличить счётчик просмотров
    db.increment_views(post_id)
    
    # Получить комментарии
    comments = db.get_comments_for_post(post_id)
    
    return render_template('post.html', post=post, comments=comments)

@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    """Создать новый пост"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author = request.form.get('author', '').strip()
        
        # Валидация
        errors = []
        
        if not title:
            errors.append('Заголовок обязателен')
        elif len(title) < 5:
            errors.append('Заголовок должен быть минимум 5 символов')
        
        if not content:
            errors.append('Содержимое обязательно')
        elif len(content) < 20:
            errors.append('Содержимое должно быть минимум 20 символов')
        
        if not author:
            errors.append('Имя автора обязательно')
        
        if errors:
            # Показать ошибки
            for error in errors:
                flash(error, 'error')
            
            # Вернуть форму с введёнными данными
            return render_template('new_post.html',
                                 title=title,
                                 content=content,
                                 author=author)
        
        # Всё ОК - создать пост
        post_id = db.create_post(title, content, author)
        flash('Пост успешно создан!', 'success')
        return redirect(url_for('view_post', post_id=post_id))
    
    # GET - показать форму
    return render_template('new_post.html')

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    """Редактировать пост"""
    post = db.get_post_by_id(post_id)
    
    if not post:
        flash('Пост не найден', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        # Валидация
        if not title or len(title) < 5:
            flash('Заголовок должен быть минимум 5 символов', 'error')
            return render_template('edit_post.html', post=post)
        
        if not content or len(content) < 20:
            flash('Содержимое должно быть минимум 20 символов', 'error')
            return render_template('edit_post.html', post=post)
        
        # Обновить
        db.update_post(post_id, title, content)
        flash('Пост обновлён!', 'success')
        return redirect(url_for('view_post', post_id=post_id))
    
    # GET - показать форму
    return render_template('edit_post.html', post=post)


@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Удалить пост"""
    if db.delete_post(post_id):
        flash('Пост удалён', 'success')
    else:
        flash('Пост не найден', 'error')
    
    return redirect(url_for('index'))


@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    """Добавить комментарий к посту"""
    author = request.form.get('author', '').strip()
    content = request.form.get('content', '').strip()
    
    if not author or not content:
        flash('Заполните все поля', 'error')
        return redirect(url_for('view_post', post_id=post_id))
    
    if len(content) < 3:
        flash('Комментарий слишком короткий', 'error')
        return redirect(url_for('view_post', post_id=post_id))
    
    db.add_comment(post_id, author, content)
    flash('Комментарий добавлен!', 'success')
    return redirect(url_for('view_post', post_id=post_id))


@app.route('/search')
def search():
    """Поиск постов"""
    query = request.args.get('q', '').strip()
    
    if not query:
        flash('Введите запрос для поиска', 'warning')
        return redirect(url_for('index'))
    
    posts = db.search_posts(query)
    
    # Добавить количество комментариев
    for post in posts:
        post['comment_count'] = db.get_comment_count(post['id'])

    return render_template('search.html', posts=posts, query=query)


@app.route('/stats')
def stats():
    """Статистика блога"""
    statistics = db.get_stats()
    return render_template('stats.html', stats=statistics)




@app.template_filter('timeago')
def timeago_filter(timestamp):
    """
    Преобразовать timestamp в читаемый формат
    
    Кастомный фильтр для Jinja2
    Использование в шаблоне: {{ post.created_at | timeago }}
    """
    from datetime import datetime
    
    if isinstance(timestamp, str):
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except:
            return timestamp
    else:
        dt = timestamp
    
    now = datetime.now()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return 'только что'
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f'{minutes} мин. назад'
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f'{hours} ч. назад'
    else:
        days = int(seconds / 86400)
        if days == 1:
            return 'вчера'
        elif days < 30:
            return f'{days} дн. назад'
        else:
            return dt.strftime('%d.%m.%Y')


if __name__ == '__main__':
    app.run(debug=True, port=5004)
        