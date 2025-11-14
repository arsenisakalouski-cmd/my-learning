import requests

print("--- Пример 1: Проверка статуса ---\n")

def get_user_info(username):
      url = f"https://api.github.com/users/{username}"

      try:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            # Успех!
            data = response.json()
            print(f" Пользователь найден: {data['name']}")
            return data
        elif response.status_code == 404:
            # Не найден
            print(f" Пользователь '{username}' не найден")
            return None
        
        else:
            # Другая ошибка
            print(f" Ошибка {response.status_code}")
            return None
      except requests.Timeout:
        print(" Превышено время ожидания")
        return None
    
      except requests.ConnectionError:
        print(" Нет подключения к интернету")
        return None
    
      except requests.RequestException as e:
        print(f" Ошибка запроса: {e}")
        return None  
        
get_user_info("github")        # Существует
get_user_info("user12345xyz")  # Не существует


print("--- Пример 2: raise_for_status() ---\n")

# КАК ЭТО РАБОТАЕТ:
# raise_for_status() вызывает исключение если статус код ошибочный

def get_repo_info(owner, repo):
    """Получить информацию о репозитории"""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    
    try:
        response = requests.get(url, timeout=5)
        
        # Если статус код 4xx или 5xx - вызовет исключение!
        response.raise_for_status()
        
        # Если дошли сюда - значит успешно
        data = response.json()
        print(f" Репозиторий: {data['full_name']}")
        print(f" Звёзд: {data['stargazers_count']}")
        print(f" Форков: {data['forks_count']}")
        return data
    
    except requests.HTTPError as e:
        # Ошибка HTTP (404, 500, etc.)
        print(f" HTTP ошибка: {e}")
        return None
    
    except requests.Timeout:
        print(" Превышено время ожидания")
        return None
    
    except requests.RequestException as e:
        print(f" Ошибка: {e}")
        return None


get_repo_info("python", "cpython")     # Существует
get_repo_info("invalid", "invalid")    # Не существует

print("\n" + "="*60 + "\n")





print("--- Пример 3: Retry (повторные попытки) ---\n")

def get_with_retry(url, max_retries=3):
    """
    Запрос с повторными попытками
    
    ЗАЧЕМ:
    Иногда запрос падает случайно (сеть, сервер)
    Можно попробовать ещё раз
    """
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Попытка {attempt}/{max_retries}...")
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            print(" Успех!")
            return response
        
        except requests.RequestException as e:
            print(f" Ошибка: {e}")
            
            if attempt < max_retries:
                print("Пробую снова...\n")
            else:
                print("Все попытки исчерпаны")
                return None

# Тест (используйте реальный URL)
response = get_with_retry("https://api.github.com")

print("\n" + "="*60)
