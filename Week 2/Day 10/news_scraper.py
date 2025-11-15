import requests
import json
from datetime import datetime

# API для новостей (бесплатный, без регистрации)
NEWS_API = "https://newsapi.org/v2/top-headlines"
API_KEY = "ce699135479442ae824bc5d29dc3a8e3"

NEWS_FILE = "saved_news.json"

def get_news(country="us", category=None):

    params = {
        "country": country,
        "apiKey": API_KEY,
    }
    if category:
        params["category"] = category

    try:
        response = requests.get(NEWS_API, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            # data["articles"] - список новостей
            # Каждая новость = словарь с title, description, url
            return data["articles"]
        
        elif response.status_code == 401:
            print("Неверный API ключ")
            return None
        else:
            print(f"Ошибка {response.status_code}")
            return None
    
    except requests.RequestException as e:
        print(f"Ошибка: {e}")
        return None
    
def display_news(articles):
    """Показать новости"""
    if not articles:
        print("Нет новостей")
        return
    
    print("\n" + "="*70)
    print("ПОСЛЕДНИЕ НОВОСТИ")
    print("="*70)

    for i, article in enumerate(articles[:10], 1):
        print(f"\n{i}. {article['title']}")

        desc = article.get('description', 'Нет описания')
        if desc:
            # [:100] берёт первые 100 символов
            print(f"   {desc[:100]}...")
        
        print(f"   Ссылка: {article['url']}")
    
    print("\n" + "="*70 + "\n")


def save_news(articles):
     data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "articles": articles[:10]  # Сохраняем только 10
    }
     try:
        with open(NEWS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Новости сохранены")
     except Exception as e:
        print(f"Ошибка сохранения: {e}")


def load_saved_news():
    """Загрузить сохранённые новости"""
    try:
        with open(NEWS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        print(f"\nСохранено: {data['timestamp']}")
        return data["articles"]
    
    except FileNotFoundError:
        print("Нет сохранённых новостей")
        return None
    except json.JSONDecodeError:
        print("Файл повреждён")
        return None

def main():
    """Главное меню"""
    
    if not API_KEY or API_KEY == "ce699135479442ae824bc5d29dc3a8e3":
        print("\n  Укажите API ключ!")
        print("1. Зарегистрируйтесь на newsapi.org")
        print("2. Скопируйте ключ")
        print("3. Вставьте в строку API_KEY\n")
        return
    print("\n=== НОВОСТНОЙ АГРЕГАТОР ===\n")

    while True:
        print("--- МЕНЮ ---")
        print("1. Получить новости")
        print("2. Новости по категориям")
        print("3. Показать сохранённые")
        print("4. Выход")
        
        choice = input("\nВыбор (1-4): ").strip()
        
        if choice == "1":
            print("\nПолучаю новости...")
            articles = get_news()
            if articles:
                display_news(articles)
                
                save_choice = input("Сохранить? (да/нет): ").lower()
                if save_choice == "да":
                    save_news(articles)
        
        elif choice == "2":
            print("\nКатегории:")
            print("business, entertainment, health,")
            print("science, sports, technology")
            
            category = input("\nКатегория: ").strip().lower()
            
            print(f"\nПолучаю новости ({category})...")
            articles = get_news(category=category)
            if articles:
                display_news(articles)
        
        elif choice == "3":
            articles = load_saved_news()
            if articles:
                display_news(articles)
        
        elif choice == "4":
            print("\nДо встречи!")
            break
        
        else:
            print("Выберите 1-4")


if __name__ == "__main__":
    main()




            