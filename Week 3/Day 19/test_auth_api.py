# test_auth_api.py - Тестирование Auth API

import requests
import json

BASE_URL = 'http://localhost:5010/api'

def print_response(title, response):
    print(f"\n{'='*60}")
    print(title)
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)

print("="*60)
print("ТЕСТИРОВАНИЕ AUTH API")
print("="*60)

# 1. Регистрация пользователя 1
print("\n" + "="*60)
print("ЧАСТЬ 1: РЕГИСТРАЦИЯ И ВХОД")
print("="*60)

user1 = {
    'username': 'ivan',
    'email': 'ivan@mail.com',
    'password': 'password123'
}
response = requests.post(f'{BASE_URL}/auth/register', json=user1)
print_response("1. Регистрация Ivan", response)

# 2. Регистрация пользователя 2
user2 = {
    'username': 'maria',
    'email': 'maria@mail.com',
    'password': 'qwerty123'
}
response = requests.post(f'{BASE_URL}/auth/register', json=user2)
print_response("2. Регистрация Maria", response)

# 3. Вход Ivan
login_data = {
    'username': 'ivan',
    'password': 'password123'
}
response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
print_response("3. Вход Ivan", response)
ivan_token = response.json()['token']
print(f"\n💾 Токен Ivan сохранён: {ivan_token[:20]}...")

# 4. Вход Maria
login_data2 = {
    'username': 'maria',
    'password': 'qwerty123'
}
response = requests.post(f'{BASE_URL}/auth/login', json=login_data2)
print_response("4. Вход Maria", response)
maria_token = response.json()['token']
print(f"\n💾 Токен Maria сохранён: {maria_token[:20]}...")

# 5. Проверить текущего пользователя
print("\n" + "="*60)
print("ЧАСТЬ 2: ПРОВЕРКА ТОКЕНОВ")
print("="*60)

headers_ivan = {'Authorization': f'Bearer {ivan_token}'}
response = requests.get(f'{BASE_URL}/auth/me', headers=headers_ivan)
print_response("5. GET /api/auth/me (Ivan)", response)

headers_maria = {'Authorization': f'Bearer {maria_token}'}
response = requests.get(f'{BASE_URL}/auth/me', headers=headers_maria)
print_response("6. GET /api/auth/me (Maria)", response)

# 7. Создать пост без токена (должно быть 401)
print("\n" + "="*60)
print("ЧАСТЬ 3: СОЗДАНИЕ ПОСТОВ")
print("="*60)

new_post = {
    'title': 'Тест без токена',
    'content': 'Это не должно работать, нужен токен'
}
response = requests.post(f'{BASE_URL}/posts', json=new_post)
print_response("7. POST /api/posts БЕЗ токена (должно быть 401)", response)

# 8. Создать пост с токеном Ivan
new_post = {
    'title': 'Пост Ивана',
    'content': 'Это пост Ивана. Он создан с использованием токена аутентификации.'
}
response = requests.post(f'{BASE_URL}/posts', json=new_post, headers=headers_ivan)
print_response("8. POST /api/posts (Ivan с токеном)", response)
ivan_post_id = response.json()['post']['id']

# 9. Создать пост Maria
new_post2 = {
    'title': 'Пост Марии',
    'content': 'Привет! Это пост Марии. Она тоже использует токен для создания постов.'
}
response = requests.post(f'{BASE_URL}/posts', json=new_post2, headers=headers_maria)
print_response("9. POST /api/posts (Maria с токеном)", response)
maria_post_id = response.json()['post']['id']

# 10. Maria пытается изменить пост Ivan (должно быть 403)
print("\n" + "="*60)
print("ЧАСТЬ 4: ПРОВЕРКА АВТОРСТВА")
print("="*60)

update_data = {
    'title': 'Попытка взлома'
}
response = requests.put(f'{BASE_URL}/posts/{ivan_post_id}', 
                       json=update_data, 
                       headers=headers_maria)
print_response("10. Maria пытается изменить пост Ivan (должно быть 403)", response)

# 11. Ivan изменяет свой пост (должно работать)
update_data = {
    'title': 'Обновлённый пост Ивана'
}
response = requests.put(f'{BASE_URL}/posts/{ivan_post_id}', 
                       json=update_data, 
                       headers=headers_ivan)
print_response("11. Ivan изменяет свой пост", response)

# 12. Добавить комментарий без токена (должно быть 401)
print("\n" + "="*60)
print("ЧАСТЬ 5: КОММЕНТАРИИ")
print("="*60)

comment = {
    'content': 'Комментарий без токена'
}
response = requests.post(f'{BASE_URL}/posts/{ivan_post_id}/comments', json=comment)
print_response("12. Комментарий БЕЗ токена (должно быть 401)", response)

# 13. Добавить комментарий с токеном
comment = {
    'content': 'Отличный пост, Иван!'
}
response = requests.post(f'{BASE_URL}/posts/{ivan_post_id}/comments', 
                        json=comment, 
                        headers=headers_maria)
print_response("13. Maria комментирует пост Ivan", response)

# 14. Получить все посты (публично)
print("\n" + "="*60)
print("ЧАСТЬ 6: ПУБЛИЧНЫЕ ENDPOINTS")
print("="*60)

response = requests.get(f'{BASE_URL}/posts')
print_response("14. GET /api/posts (публично, без токена)", response)

# 15. Выход Ivan
print("\n" + "="*60)
print("ЧАСТЬ 7: ВЫХОД")
print("="*60)

response = requests.post(f'{BASE_URL}/auth/logout', headers=headers_ivan)
print_response("15. POST /api/auth/logout (Ivan)", response)

# 16. Попытка использовать токен после выхода (должно быть 401)
response = requests.get(f'{BASE_URL}/auth/me', headers=headers_ivan)
print_response("16. Попытка использовать токен после logout (должно быть 401)", response)

print("\n" + "="*60)
print("✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!")
print("="*60)
