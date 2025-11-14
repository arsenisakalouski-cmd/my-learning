import requests

print("=== API Погоды ===\n")

API_KEY = "abf50edc8408656d0c342adb43c7e925"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):

    params ={
        "q": city,              # Название города
        "appid": API_KEY,       # Ваш API ключ
        "units": "metric",      # Метрическая система (Цельсий)
        "lang": "ru"            # Русский язык
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)

        if response.status_code == 200:
            # Успех! Парсим JSON
            data = response.json()
            return data
        

        elif response.status_code == 401:
            print(" Неверный API ключ!")
            print("   Проверьте ключ на openweathermap.org")
            return None
        
        elif response.status_code == 404:
            print(f" Город '{city}' не найден!")
            return None
        
        else:
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



def display_weather(data):
    if not data:
        return
    
    print("\n" + "="*50)
    print(f" Погода в городе: {data['name']}")
    print("="*50)

    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    print(f"  Температура: {temp}°C")
    print(f" Ощущается как: {feels_like}°C")

    description = data['weather'][0]['description'].capitalize()
    print(f"  Состояние: {description}")

    humidity = data['main']['humidity']
    print(f" Влажность: {humidity}%")
    
    # Ветер
    wind_speed = data['wind']['speed']
    print(f" Ветер: {wind_speed} м/с")
    
    print("="*50 + "\n")


if API_KEY == "abf50edc8408656d0c342adb43c7":
    print("   ВНИМАНИЕ: Укажите ваш API ключ!")
    print("   1. Зарегистрируйтесь на openweathermap.org")
    print("   2. Получите API ключ")
    print("   3. Замените строку API_KEY в коде\n")
else:
    # Тестируем с разными городами
    cities = ["Москва", "Санкт-Петербург", "Минск"]
    
    for city in cities:
        print(f"Получаю погоду для {city}...")
        weather_data = get_weather(city)
        display_weather(weather_data)





