# custom_exceptions.py - Свои исключения

print("=== Пользовательские исключения ===\n")

# Определение своих исключений
class ValidationError(Exception):
    """Ошибка валидации данных"""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"[{field}] {message}")

class AgeError(ValidationError):
    """Ошибка возраста"""
    def __init__(self, age, message="Некорректный возраст"):
        self.age = age
        super().__init__("age", f"{message} (получено: {age})")

class EmailError(ValidationError):
    """Ошибка email"""
    def __init__(self, email):
        self.email = email
        super().__init__("email", f"Некорректный email: {email}")

class PasswordError(ValidationError):
    """Ошибка пароля"""
    def __init__(self, reason):
        super().__init__("password", reason)

# Класс пользователя с валидацией
class User:
    """Пользователь системы"""
    
    def __init__(self, username, email, password, age):
        self.username = self._validate_username(username)
        self.email = self._validate_email(email)
        self.password = self._validate_password(password)
        self.age = self._validate_age(age)
    
    def _validate_username(self, username):
        """Валидация имени пользователя"""
        if not username:
            raise ValidationError("username", "Имя не может быть пустым")
        
        if len(username) < 3:
            raise ValidationError("username", "Минимум 3 символа")
        
        if len(username) > 20:
            raise ValidationError("username", "Максимум 20 символов")
        
        if not username.isalnum():
            raise ValidationError("username", "Только буквы и цифры")
        
        return username
    
    def _validate_email(self, email):
        """Валидация email"""
        if not email:
            raise EmailError("Email не может быть пустым")
        
        if "@" not in email or "." not in email:
            raise EmailError(email)
        
        return email
    
    def _validate_password(self, password):
        """Валидация пароля"""
        if len(password) < 8:
            raise PasswordError("Минимум 8 символов")
        
        if not any(c.isupper() for c in password):
            raise PasswordError("Должна быть хотя бы одна заглавная буква")
        
        if not any(c.isdigit() for c in password):
            raise PasswordError("Должна быть хотя бы одна цифра")
        
        return password
    
    def _validate_age(self, age):
        """Валидация возраста"""
        if not isinstance(age, int):
            raise AgeError(age, "Возраст должен быть целым числом")
        
        if age < 0:
            raise AgeError(age, "Возраст не может быть отрицательным")
        
        if age > 150:
            raise AgeError(age, "Возраст не может быть больше 150")
        
        if age < 18:
            raise AgeError(age, "Минимальный возраст 18 лет")
        
        return age
    
    def __str__(self):
        return f"User(username='{self.username}', email='{self.email}', age={self.age})"


# Функция регистрации с обработкой ошибок
def register_user(username, email, password, age):
    """Регистрация пользователя с обработкой всех ошибок"""
    try:
        user = User(username, email, password, age)
        print(f" Пользователь создан: {user}\n")
        return user
    
    except AgeError as e:
        print(f" Ошибка возраста: {e.message}")
        print(f"   Получен возраст: {e.age}\n")
        return None
    
    except EmailError as e:
        print(f" Ошибка email: {e.message}")
        print(f"   Получен email: {e.email}\n")
        return None
    
    except PasswordError as e:
        print(f" Ошибка пароля: {e.message}\n")
        return None
    
    except ValidationError as e:
        print(f" Ошибка валидации: {e}\n")
        return None


# Тестирование
print("--- Тест 1: Правильные данные ---")
register_user("johndoe", "john@example.com", "Password123", 25)

print("--- Тест 2: Короткое имя ---")
register_user("ab", "john@example.com", "Password123", 25)

print("--- Тест 3: Неверный email ---")
register_user("john_doe", "invalid-email", "Password123", 25)

print("--- Тест 4: Слабый пароль (короткий) ---")
register_user("john_doe", "john@example.com", "pass", 25)

print("--- Тест 5: Слабый пароль (нет заглавных) ---")
register_user("john_doe", "john@example.com", "password123", 25)

print("--- Тест 6: Слабый пароль (нет цифр) ---")
register_user("john_doe", "john@example.com", "Password", 25)

print("--- Тест 7: Отрицательный возраст ---")
register_user("john_doe", "john@example.com", "Password123", -5)

print("--- Тест 8: Слишком большой возраст ---")
register_user("john_doe", "john@example.com", "Password123", 200)

print("--- Тест 9: Несовершеннолетний ---")
register_user("john_doe", "john@example.com", "Password123", 16)

print("--- Тест 10: Неверный тип возраста ---")
register_user("john_doe", "john@example.com", "Password123", "двадцать пять")