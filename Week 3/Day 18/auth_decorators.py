from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """
    Декоратор: требует авторизации
    
    Использование:
    @app.route('/protected')
    @login_required
    def protected():
        return "Защищённая страница"
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        """
        Обёртка которая проверяет авторизацию
        
        *args, **kwargs:
        Принимает любые аргументы и передаёт их дальше
        """
        if 'user_id' not in session:
            # Пользователь не авторизован
            flash('Пожалуйста, войдите в систему', 'warning')
            return redirect(url_for('login'))
        
        # Пользователь авторизован - выполнить функцию
        return f(*args, **kwargs)
    return wrapper 
    
def logout_required(f):
    """
    Декоратор: требует НЕавторизации
    
    Использование для страниц логина/регистрации
    Если уже вошли - перенаправить на главную
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            # Пользователь уже авторизован
            flash('Вы уже вошли в систему', 'info')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    
    return wrapper


def author_required(f):
    """
    Декоратор: требует что пользователь - автор поста
    
    Использование:
    @app.route('/post/<int:post_id>/edit')
    @login_required
    @author_required
    def edit_post(post_id):
        ...
    """
    @wraps(f)
    def wrapper(post_id, *args, **kwargs):
        """
        post_id - обязательный параметр
        Используется для проверки авторства
        """
        import database as db
        
        # Получить пост
        post = db.get_post_by_id(post_id)
        
        if not post:
            flash('Пост не найден', 'error')
            return redirect(url_for('index'))
        
        # Проверить авторство
        if post.get('author_id') != session.get('user_id'):
            flash('Вы можете редактировать только свои посты', 'error')
            return redirect(url_for('view_post', post_id=post_id))
        
        return f(post_id, *args, **kwargs)
    
    return wrapper



