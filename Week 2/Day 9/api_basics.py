import requests

print("=== Основы HTTP запросов ===\n")

print("--- Пример 1: Первый запрос ---\n")

url = "https://api.github.com"
response = requests.get(url)

print(f"URL: {url}")
print(f"Статус код: {response.status_code}")
print(f"Успешно: {response.ok}")

# requests.get(url) отправляет GET запрос
# Возвращает объект Response с:
#   - status_code: код ответа (200 = OK)
#   - ok: True если запрос успешен
#   - text: текст ответа
#   - json(): данные в формате JSON

print("\n" + "="*60 + "\n")

print("--- Пример 2: Коды статусов ---\n")

urls = [
    "https://api.github.com",           # 200 - существует
    "https://api.github.com/invalid",   # 404 - не существует
]

for url in urls:
    response = requests.get(url)
    print(f"URL: {url}")
    print(f"Код: {response.status_code}")
    
    if response.status_code == 200:
        print(" Успешно!")
    elif response.status_code == 404:
        print(" Не найдено!")
    else:
        print(f" Код: {response.status_code}")
    
    print()

print("="*60 + "\n")

print("--- Пример 3: JSON данные ---\n")

# МНОГИЕ API возвращают данные в формате JSON
# JSON легко преобразовать в словарь Python

url = "https://api.github.com/users/github"
response = requests.get(url)

if response.ok:
    # Преобразуем JSON в словарь
    data = response.json()
    
    print("Информация о пользователе GitHub:")
    print(f"  Имя: {data['name']}")
    print(f"  Компания: {data['company']}")
    print(f"  Публичных репозиториев: {data['public_repos']}")
    print(f"  Подписчиков: {data['followers']}")
    print(f"  Локация: {data['location']}")
else:
    print(f" Ошибка: {response.status_code}")

print("\n" + "="*60 + "\n")

print("--- Пример 4: Параметры запроса ---\n")

# Часто нужно передать параметры в URL
# Например: поиск репозиториев по ключевому слову

url = "https://api.github.com/search/repositories"

# Параметры запроса
params = {
    "q": "python",      # Ключевое слово поиска
    "sort": "stars",    # Сортировка по звёздам
    "per_page": 5       # Количество результатов
}

# КАК ЭТО РАБОТАЕТ:
# requests автоматически добавит параметры к URL:
# https://api.github.com/search/repositories?q=python&sort=stars&per_page=5

response = requests.get(url, params=params)

if response.ok:
    data = response.json()
    
    print(f"Найдено репозиториев: {data['total_count']}")
    print("\nТоп-5 популярных Python репозиториев:\n")
    
    for i, repo in enumerate(data['items'], 1):
        print(f"{i}. {repo['name']}")
        print(f"   Автор: {repo['owner']['login']}")
        print(f"   Звёзд: {repo['stargazers_count']}")
        print(f"   Описание: {repo['description'][:60]}...")
        print()
else:
    print(f" Ошибка: {response.status_code}")

print("="*60 + "\n")



print("--- Пример 5: Заголовки ---\n")

# Заголовки - дополнительная информация о запросе
# Например: указать что принимаем JSON

url = "https://api.github.com"

headers = {
    "Accept": "application/json",
    "User-Agent": "Python-Learning-App"
}

response = requests.get(url, headers=headers)

#response.headers — это словарь, где хранятся все заголовки ответа.=
#'Content-Type' — ключ (название заголовка).
#Он говорит, какого типа данные вернул сервер.

#response.headers.get('X-RateLimit-Limit', 'N/A')
#ищет заголовок X-RateLimit-Limit — это лимит запросов,
#который GitHub даёт твоему приложению за час.
#.get(..., 'N/A') означает:
# «Если этого заголовка нет — верни 'N/A' (not available) вместо ошибки.»


url = "https://api.github.com"

headers = {
    "Accept": "application/json",
    "User-Agent": "Python-Learning-App"
}

response = requests.get(url, headers=headers)

print("Заголовки ответа:")
print(f"  Content-Type: {response.headers['Content-Type']}")
print(f"  X-RateLimit-Limit: {response.headers.get('X-RateLimit-Limit', 'N/A')}")

print("\n" + "="*60 + "\n")

print("--- Пример 6: Timeout ---\n")

# ЗАЧЕМ: Чтобы запрос не висел вечно
# Если сервер не отвечает больше N секунд - ошибка

url = "https://api.github.com"

try:
    # Ждём максимум 5 секунд
    response = requests.get(url, timeout=5)
    print(" Запрос выполнен за время")
except requests.Timeout:
    print(" Превышено время ожидания!")
except requests.RequestException as e:
    print(f" Ошибка запроса: {e}")

print("\n" + "="*60)