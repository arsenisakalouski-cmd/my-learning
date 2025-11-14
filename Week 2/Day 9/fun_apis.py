import requests

print("=== Интересные API ===\n")

print("--- API 1: Факты о числах ---\n")

def get_number_fact(number):
    url = f"http://numbersapi.com/{number}"

    try:
        response=requests.get(url, timeout = 5)
        if response.ok:
            fact = response.text
            print(f"Число {number}:")
            print(f"  {fact}\n")
            return fact
        
    except requests.RequestException as e:
        print(f" Ошибка: {e}\n")
        return None

get_number_fact(42)
get_number_fact(365)
get_number_fact(1000)