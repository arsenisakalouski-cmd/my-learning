# test_api.py - Тестирование API

import requests

BASE_URL = 'http://localhost:5008/api'

print("="*60)
print("ТЕСТИРОВАНИЕ API")
print("="*60)

# 1. GET все пользователи
print("\n1. GET /api/users:")
response = requests.get(f'{BASE_URL}/users')
print(f"   Status: {response.status_code}")
print(f"   Data: {response.json()}")

# 2. GET один пользователь
print("\n2. GET /api/users/1:")
response = requests.get(f'{BASE_URL}/users/1')
print(f"   Status: {response.status_code}")
print(f"   Data: {response.json()}")

# 3. POST создать
print("\n3. POST /api/users:")
new_user = {'name': 'Анна', 'age': 27}
response = requests.post(f'{BASE_URL}/users', json=new_user)
print(f"   Status: {response.status_code}")
print(f"   Data: {response.json()}")

# 4. PUT обновить
print("\n4. PUT /api/users/1:")
update_data = {'age': 26}
response = requests.put(f'{BASE_URL}/users/1', json=update_data)
print(f"   Status: {response.status_code}")
print(f"   Data: {response.json()}")

# 5. GET поиск
print("\n5. GET /api/search?q=Иван:")
response = requests.get(f'{BASE_URL}/search', params={'q': 'Иван'})
print(f"   Status: {response.status_code}")
print(f"   Data: {response.json()}")

# 6. DELETE удалить
print("\n6. DELETE /api/users/2:")
response = requests.delete(f'{BASE_URL}/users/2')
print(f"   Status: {response.status_code}")
print(f"   Data: {response.json()}")

# 7. GET проверка
print("\n7. GET /api/users (после удаления):")
response = requests.get(f'{BASE_URL}/users')
print(f"   Status: {response.status_code}")
print(f"   Data: {response.json()}")

print("\n" + "="*60)