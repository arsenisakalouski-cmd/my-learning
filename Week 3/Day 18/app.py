# app.py - Flask блог с аутентификацией

from flask import Flask, render_template, request, redirect, url_for, flash, session
import database as db
from auth_decorators import login_required, logout_required, author_required

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Инициализация БД при запуске
db.init_db()

# ==========================================
# РЕГИСТРАЦИЯ
# ==========================================

@app.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # Проверка совпадения паролей
        if password != password_confirm:
            flash('Пароли не совпадают', 'error')
            return render_template('register.html',
                                 username=username,
                                 email=email)
        
        # Регистрация
        success, result = db.register_user(username, email, password)
        
        if success:
            flash('Регистрация успешна! Теперь войдите', 'success')
            return redirect(url_for('login'))
        else:
            flash(result, 'error')
            return render_template('register.html',
                                 username=username,
                                 email=email)
    
    return render_template('register.html')


# ==========================================
# ВХОД
# ==========================================

@app.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    """Вход в систему"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        success, result = db.login_user(username, password)
        
        if success:
            # Сохранить данные в сессию
            user = result
            session['user_id'] = user['id']
            session['username'] = user['username']
            
            flash(f'Добро пожаловать, {user["username"]}!', 'success')
            
            # Перенаправить на страницу откуда пришли или на главную
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash(result, 'error')
            return render_template('login.html', username=username)
    
    return render_template('login.html')


# ==========================================
# ВЫХОД
# ==========================================

@app.route('/logout')
@login_required
def logout():
    """Выход из системы"""
    username = session.get('username', 'Пользователь')
    session.clear()
    flash(f'До свидания, {username}!', 'success')
    return redirect(url_for('index'))


# ==========================================
# ГЛАВНАЯ СТРАНИЦА
# ==========================================

@app.route('/')
def index():
    """Главная - список всех постов"""
    posts = db.get_all_posts()
    
    for post in posts:
        post['comment_count'] = db.get_comment_count(post['id'])
    
    return render_template('index.html', posts=posts)


# ==========================================
# ПРОСМОТР ПОСТА
# ==========================================

@app.route('/post/<int:post_id>')
def view_post(post_id):
    """Просмотр конкретного поста"""
    post = db.get_post_by_id(post_id)
    
    if not post:
        flash('Пост не найден', 'error')
        return redirect(url_for('index'))
    
    db.increment_views(post_id)
    comments = db.get_comments_for_post(post_id)
    
    # Проверить является ли текущий пользователь автором
    is_author = (post.get('author_id') == session.get('user_id'))
    
    return render_template('post.html', 
                         post=post, 
                         comments=comments,
                         is_author=is_author)


# ==========================================
# СОЗДАНИЕ ПОСТА (требует авторизации)
# ==========================================

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    """Создать новый пост"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        # Валидация
        errors = []
        
        if not title or len(title) < 5:
            errors.append('Заголовок должен быть минимум 5 символов')
        
        if not content or len(content) < 20:
            errors.append('Содержимое должно быть минимум 20 символов')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('new_post.html',
                                 title=title,
                                 content=content)
        
        # Создать пост
        author = session['username']
        author_id = session['user_id']
        post_id = db.create_post(title, content, author, author_id)
        
        flash('Пост успешно создан!', 'success')
        return redirect(url_for('view_post', post_id=post_id))
    
    return render_template('new_post.html')


# ==========================================
# РЕДАКТИРОВАНИЕ ПОСТА (только автор)
# ==========================================

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
@author_required
def edit_post(post_id):
    """Редактировать пост"""
    post = db.get_post_by_id(post_id)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or len(title) < 5:
            flash('Заголовок должен быть минимум 5 символов', 'error')
            return render_template('edit_post.html', post=post)
        
        if not content or len(content) < 20:
            flash('Содержимое должно быть минимум 20 символов', 'error')
            return render_template('edit_post.html', post=post)
        
        db.update_post(post_id, title, content)
        flash('Пост обновлён!', 'success')
        return redirect(url_for('view_post', post_id=post_id))
    
    return render_template('edit_post.html', post=post)


# ==========================================
# УДАЛЕНИЕ ПОСТА (только автор)
# ==========================================

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
@author_required
def delete_post(post_id):
    """Удалить пост"""
    db.delete_post(post_id)
    flash('Пост удалён', 'success')
    return redirect(url_for('index'))


# ==========================================
# ДОБАВЛЕНИЕ КОММЕНТАРИЯ (требует авторизации)
# ==========================================

@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    """Добавить комментарий к посту"""
    content = request.form.get('content', '').strip()
    
    if not content or len(content) < 3:
        flash('Комментарий слишком короткий', 'error')
        return redirect(url_for('view_post', post_id=post_id))
    
    author = session['username']
    db.add_comment(post_id, author, content)
    flash('Комментарий добавлен!', 'success')
    return redirect(url_for('view_post', post_id=post_id))


# ==========================================
# ПОИСК
# ==========================================

@app.route('/search')
def search():
    """Поиск постов"""
    query = request.args.get('q', '').strip()
    
    if not query:
        flash('Введите запрос для поиска', 'warning')
        return redirect(url_for('index'))
    
    posts = db.search_posts(query)
    
    for post in posts:
        post['comment_count'] = db.get_comment_count(post['id'])
    
    return render_template('search.html', posts=posts, query=query)


# ==========================================
# СТАТИСТИКА
# ==========================================

@app.route('/stats')
def stats():
    """Статистика блога"""
    statistics = db.get_stats()
    return render_template('stats.html', stats=statistics)


# ==========================================
# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
# ==========================================

@app.route('/profile')
@login_required
def profile():
    """Профиль текущего пользователя"""
    user = db.get_user_by_id(session['user_id'])
    
    # Получить посты пользователя
    all_posts = db.get_all_posts()
    user_posts = [p for p in all_posts if p.get('author_id') == session['user_id']]
    
    return render_template('profile.html', user=user, posts=user_posts)


# ==========================================
# ФИЛЬТР timeago (уже есть)
# ==========================================

@app.template_filter('timeago')
def timeago_filter(timestamp):
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
    app.run(debug=True, port=5007)