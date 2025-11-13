import random
import json
from datetime import datetime

def load_records():

    try :
         with open("ercords.json", "r", encoding="utf-8") as f:
           records = json.load(f)
         print("Рекорды загружены")
         return records
    except FileNotFoundError:
        # КОГДА: Файла records.json не существует
        # ЧТО ДЕЛАЕМ: Создаём пустой список (первый запуск)
        print("ℹ Файл рекордов не найден, создаём новый")
        return []
    
    except json.JSONDecodeError:
        # КОГДА: Файл есть, но формат неправильный (повреждён)
        # ЧТО ДЕЛАЕМ: Создаём пустой список
        print(" Файл рекордов повреждён, создаём новый")
        return []
    
def save_records(records):
    try:
        with open("records.json", "w", encoding = "utf-8") as f:
            json.dump(records, f , ensure_ascii = False, indent = 2)
            print(" Рекорды сохранены")
    
    except Exception as e:
        # КОГДА: Любая ошибка при записи (диск полон, нет прав и т.д.)
        # ЧТО ДЕЛАЕМ: Сообщаем об ошибке
        print(f" Ошибка сохранения рекордов: {e}")

def add_record(records, player_name, attempts):
    record = {
        "player": player_name,
        "attempts": attempts,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    records.append(record)

    # Сортируем по количеству попыток (лучшие первыми)
    records.sort(key=lambda x: x["attempts"])
    
    # Оставляем только топ-10
    return records[:10]

def show_records(records):

    print("\n" + "="*60)
    print(" ТАБЛИЦА РЕКОРДОВ (ТОП-10)")
    print("="*60)
    
    if not records:
        print("  (пока нет рекордов)")
    else:
        print(f"{'№':<4} {'Игрок':<20} {'Попытки':<10} {'Дата'}")
        print("-"*60)
        for i, record in enumerate(records[:10], 1):
            print(f"{i:<4} {record['player']:<20} "
                  f"{record['attempts']:<10} {record['date']}")
    
    print("="*60 + "\n")

def get_player_name():    
     while True:
        name = input("Введите ваше имя: ").strip()
        
        if name:  # Если имя не пустое
            return name
        else:
            print(" Имя не может быть пустым!\n")


def get_number_input(prompt, min_value, max_value): 
     while True:
        try:
            # ТУТ может быть ValueError!
            value = int(input(prompt))
            
            # Проверяем диапазон
            if value < min_value or value > max_value:
                print(f" Число должно быть от {min_value} до {max_value}!\n")
                continue
            
            return value
        
        except ValueError:
            # КОГДА: Пользователь ввёл не число (например "abc")
            # ЧТО ДЕЛАЕМ: Сообщаем об ошибке и просим снова
            print(" Введите целое число!\n")

def play_game():
    secret_number = random.randint(1, 100)
    max_attempts = 7
    attempts = 0

    print("\n" + "="*60)
    print("🎮 ИГРА 'УГАДАЙ ЧИСЛО'")
    print("="*60)
    print(f"Я загадал число от 1 до 100")
    print(f"У вас {max_attempts} попыток\n")

    while attempts < max_attempts:
        attempts += 1
        print(f"Попытка {attempts}/{max_attempts}")

        guess = get_number_input("Ваше число: ", 1, 100)

        if guess == secret_number:
            # ПОБЕДА!
            print("\n" + "🎉"*20)
            print(f" ПОЗДРАВЛЯЮ! Вы угадали число {secret_number}!")
            print(f"🎯 Попыток использовано: {attempts}")
            print("🎉"*20 + "\n")
            return attempts
        elif guess < secret_number:
            print("📈 Моё число БОЛЬШЕ\n")
        
        else:  # guess > secret_number
            print("📉 Моё число МЕНЬШЕ\n")
    
    # Если цикл закончился - не угадали
    print("\n" + "😢"*20)
    print(f"💔 Попытки закончились!")
    print(f"🎲 Загаданное число было: {secret_number}")
    print("😢"*20 + "\n")
    return None  # Не угадал


def main_menu():
    records = load_records()

    print("\n" + "🎮"*30)
    print("        ДОБРО ПОЖАЛОВАТЬ В ИГРУ 'УГАДАЙ ЧИСЛО'")
    print("🎮"*30 + "\n")

    while True:
        print("="*60)
        print("ГЛАВНОЕ МЕНЮ")
        print("="*60)
        print("1. 🎮 Играть")
        print("2. 🏆 Таблица рекордов")
        print("3. 🚪 Выход")
        print("="*60)

        try:
            choice = input ("\nВыбор (1-3): ").strip()

            if choice == "1":
                player_name = get_player_name()
                attempts = play_game()
                
                # Если угадал - сохраняем рекорд
                if attempts is not None:
                    records = add_record(records, player_name, attempts)
                    save_records(records)
                    
                    # Проверяем - это новый рекорд?
                    if attempts == records[0]["attempts"]:
                        print(" ЭТО НОВЫЙ РЕКОРД! \n")
            elif choice == "2":
                # ========== РЕКОРДЫ ==========
                show_records(records)
            elif choice == "3":
                # ========== ВЫХОД ==========
                print("\n Спасибо за игру! До встречи!")
                break
            else:
                print(" Выберите 1, 2 или 3\n")

        except KeyboardInterrupt:
            # КОГДА: Пользователь нажал Ctrl+C
            # ЧТО ДЕЛАЕМ: Изящно выходим из игры
            print("\n\n Игра прервана пользователем")
            print(" До встречи!")
            break
        
        except Exception as e:
            # КОГДА: Любая другая неожиданная ошибка
            # ЧТО ДЕЛАЕМ: Показываем ошибку но не падаем
            print(f"\n Неожиданная ошибка: {e}")
            print("Попробуйте снова\n")
        
            
if __name__ == "__main__":
     
    try:
        main_menu()
    except Exception as e:
        print(f"\n💥 Критическая ошибка: {e}")
        print("Программа завершена")
    finally:
        # Выполнится ВСЕГДА (даже если была ошибка)
        print("\n" + "="*60)
        print("Программа завершена")
        print("="*60)



