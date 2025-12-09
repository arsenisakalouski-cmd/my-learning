# test_blog_api.py - Тестирование Blog API

import requests
import json

BASE_URL = 'http://localhost:5009/api'

def print_response(title, response):
    """Красивый вывод ответа"""
    print(f"\n{'='*60}")
    print(title)
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# ==========================================
# ТЕСТИРОВАНИЕ
# ==========================================

print("="*60)
print("ТЕСТИРОВАНИЕ BLOG API")
print("="*60)

# 1. Получить все посты
response = requests.get(f'{BASE_URL}/posts')
print_response("1. GET /api/posts", response)

# 2. Создать пост #1
new_post = {
    'title': 'Изучаем Flask REST API',
    'content': 'Flask позволяет легко создавать REST API. В этом посте мы рассмотрим основные концепции.',
    'author': 'Иван',
    'author_id': 1
}
response = requests.post(f'{BASE_URL}/posts', json=new_post)
print_response("2. POST /api/posts (создать пост #1)", response)
post1_id = response.json()['post']['id']

# 3. Создать пост #2
new_post2 = {
    'title': 'Python для начинающих',
    'content': 'Python - отличный язык программирования для начинающих. Рассмотрим основы.',
    'author': 'Мария'
}
response = requests.post(f'{BASE_URL}/posts', json=new_post2)
print_response("3. POST /api/posts (создать пост #2)", response)
post2_id = response.json()['post']['id']

# 4. Получить пост по ID
response = requests.get(f'{BASE_URL}/posts/{post1_id}')
print_response(f"4. GET /api/posts/{post1_id}", response)

# 5. Обновить пост
update_data = {
    'title': 'Изучаем Flask REST API (обновлено)'
}
response = requests.put(f'{BASE_URL}/posts/{post1_id}', json=update_data)
print_response(f"5. PUT /api/posts/{post1_id}", response)

# 6. Добавить комментарий
comment = {
    'author': 'Пётр',
    'content': 'Отличный пост! Очень полезная информация.'
}
response = requests.post(f'{BASE_URL}/posts/{post1_id}/comments', json=comment)
print_response(f"6. POST /api/posts/{post1_id}/comments", response)

# 7. Добавить ещё комментарий
comment2 = {
    'author': 'Анна',
    'content': 'Спасибо за статью!'
}
response = requests.post(f'{BASE_URL}/posts/{post1_id}/comments', json=comment2)
print_response(f"7. POST /api/posts/{post1_id}/comments (комментарий 2)", response)

# 8. Получить комментарии
response = requests.get(f'{BASE_URL}/posts/{post1_id}/comments')
print_response(f"8. GET /api/posts/{post1_id}/comments", response)

# 9. Поиск
response = requests.get(f'{BASE_URL}/search', params={'q': 'Flask'})
print_response("9. GET /api/search?q=Flask", response)

# 10. Статистика
response = requests.get(f'{BASE_URL}/stats')
print_response("10. GET /api/stats", response)

# 11. Получить все посты (проверка)
response = requests.get(f'{BASE_URL}/posts')
print_response("11. GET /api/posts (финальная проверка)", response)

# 12. Удалить пост
response = requests.delete(f'{BASE_URL}/posts/{post2_id}')
print_response(f"12. DELETE /api/posts/{post2_id}", response)

# 13. Попытка получить удалённый пост (должно быть 404)
response = requests.get(f'{BASE_URL}/posts/{post2_id}')
print_response(f"13. GET /api/posts/{post2_id} (должен быть 404)", response)

# 14. Пагинация
response = requests.get(f'{BASE_URL}/posts', params={'limit': 5, 'offset': 0})
print_response("14. GET /api/posts?limit=5&offset=0", response)

print("\n" + "="*60)
print("✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!")
print("="*60)