import random 
import json

WORDS = [
     "python",
    "программирование",
    "компьютер",
    "клавиатура",
    "монитор",
    "интернет",
    "разработка",
    "алгоритм",
    "переменная",
    "функция"
]

MAX_ERRORS = 6

# Файл для статистики
STATS_FILE = "hangman_stats.json"

def load_statistics():
    try:
        # Открываем файл на чтение
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            # json.load(f) - прочитать JSON из файла
            # Вернёт словарь
            stats = json.load(f)
        return stats
    
    except FileNotFoundError:
        return {
            "games_played": 0,
            "games_won": 0,
            "games_lost": 0
        }
    except json.JSONDecodeError:
        # Файл есть но повреждён
        print("Файл статистики поврежден, создаем новый")
        return {
            "games_played": 0,
            "games_won": 0,
            "games_lost": 0
        }
    
def save_statics(stats)  :
    try:
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения статистики: {e}")
          
def show_statistics(stats):

    print("\n" + "="*40)
    print("СТАТИСТИКА")
    print("="*40)

    played = stats["games_played"]
    won = stats["games_won"]
    lost = stats["games_lost"]
    
    print(f"Игр сыграно: {played}")
    print(f"Побед: {won}")
    print(f"Поражений: {lost}")


# Считаем процент побед
    if played > 0:
        # (won / played) даёт число от 0 до 1
        # * 100 превращает в проценты
        win_rate = (won / played) * 100
        print(f"Процент побед: {win_rate:.1f}%")
    
    print("="*40 + "\n")


def draw_hangman(errors):
     stages = [
            # 0 ошибок
        """
           ------
           |    |
           |
           |
           |
           |
        """,
        # 1 ошибка - голова
        """
           ------
           |    |
           |    O
           |
           |
           |
        """,
        # 2 ошибки - тело
        """
           ------
           |    |
           |    O
           |    |
           |
           |
        """,
        # 3 ошибки - левая рука
        """
           ------
           |    |
           |    O
           |   /|
           |
           |
        """,
        # 4 ошибки - правая рука
        """
           ------
           |    |
           |    O
           |   /|\\
           |
           |
        """,
        # 5 ошибок - левая нога
        """
           ------
           |    |
           |    O
           |   /|\\
           |   /
           |
        """,
        # 6 ошибок - правая нога (проигрыш)
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           |
        """
     ]
     print(stages[errors])

def display_word(word, guessed_letters):     
    result = ""

    for letter in word:
        # Проверяем: буква угадана?
        # letter in guessed_letters проверяет есть ли letter в списке
        if letter in guessed_letters:
            # Буква угадана - добавляем её
            result = result + letter + " "
        else:
            # Буква не угадана - добавляем _
            result = result + "_ "
    
    # Возвращаем результат
    # .strip() убирает пробел в конце
    return result.strip()


def check_win(word, guessed_letters):
    for letter in word:
        # Проверяем: буква угадана?
        if letter not in guessed_letters:
            # Буква не угадана - слово не отгадано
            return False
    
    # Все буквы угаданы - победа!
    return True


def play_game():
    word = random.choice(WORDS)
    
    # Переводим в нижний регистр
    # Чтобы "Python" и "python" были одинаковыми
    word = word.lower()
    
    # Список угаданных букв (пока пустой)
    guessed_letters = []
    
    # Список неправильных букв (для показа игроку)
    wrong_letters = []
    
    # Счётчик ошибок
    errors = 0

    print("\n" + "="*40)
    print("ИГРА ВИСЕЛИЦА")
    print("="*40)
    print(f"Угадайте слово из {len(word)} букв")
    print(f"У вас {MAX_ERRORS} попыток\n")

    while True:
        # Показываем виселицу
        draw_hangman(errors)
        
        # Показываем слово с _ вместо неугаданных букв
        print("Слово:", display_word(word, guessed_letters))
        
        # Показываем неправильные буквы
        if wrong_letters:
            print("Неправильные буквы:", ", ".join(wrong_letters))
        
        # Показываем количество ошибок
        print(f"Ошибок: {errors}/{MAX_ERRORS}\n")
        
        # Проверяем победу
        if check_win(word, guessed_letters):
            # Все буквы угаданы - ПОБЕДА!
            print("="*40)
            print(f"ПОЗДРАВЛЯЮ! Вы угадали слово: {word}")
            print("="*40 + "\n")
            return True  # Возвращаем True = победа
        
        # Проверяем поражение
        if errors >= MAX_ERRORS:
            # Ошибок слишком много - ПОРАЖЕНИЕ
            draw_hangman(errors)
            print("="*40)
            print(f"ИГРА ОКОНЧЕНА! Слово было: {word}")
            print("="*40 + "\n")
            return False  # Возвращаем False = поражение
        
        # Получаем букву от игрока
        try:
            # input() получает строку от пользователя
            # .strip() убирает пробелы по краям
            # .lower() переводит в нижний регистр
            # [0] берёт первый символ
            guess = input("Введите букву: ").strip().lower()
            
            # Проверяем что это одна буква
            if len(guess) != 1:
                print("Введите только одну букву\n")
                continue  # Пропускаем остальной код, начинаем цикл заново
            
            # Проверяем что это буква (не цифра)
            if not guess.isalpha():
                print("Это не буква\n")
                continue
            
            # Проверяем что букву ещё не вводили
            if guess in guessed_letters:
                print("Вы уже вводили эту букву\n")
                continue
            
            # Добавляем букву в список угаданных
            guessed_letters.append(guess)

            if guess in word:
                # Буква есть в слове - ПРАВИЛЬНО!
                print(f"Правильно! Буква '{guess}' есть в слове\n")
            else:
                # Буквы нет в слове - ОШИБКА
                print(f"Неправильно! Буквы '{guess}' нет в слове\n")
                wrong_letters.append(guess)
                errors = errors + 1  # errors += 1
        
        except KeyboardInterrupt:
            # Если нажали Ctrl+C
            print("\n\nИгра прервана")
            return False
        
        except Exception as e:
            # Любая другая ошибка
            print(f"Ошибка: {e}\n")


def main():
    """
    Главная функция программы
    
    ЧТО ДЕЛАЕТ:
    1. Загружает статистику
    2. Показывает меню
    3. Запускает игру или показывает статистику
    4. Обновляет статистику после игры
    5. Сохраняет статистику
    """
    # Загружаем статистику
    stats = load_statistics()
    
    print("\n" + "="*40)
    print("ДОБРО ПОЖАЛОВАТЬ В ИГРУ ВИСЕЛИЦА")
    print("="*40)
    
    # Главный цикл меню
    while True:
        print("\n--- МЕНЮ ---")
        print("1. Играть")
        print("2. Статистика")
        print("3. Выход")
        
        choice = input("\nВыбор (1-3): ").strip()
        
        if choice == "1":
            # ИГРАТЬ
            # play_game() возвращает True (победа) или False (поражение)
            won = play_game()
            
            # Обновляем статистику
            stats["games_played"] = stats["games_played"] + 1
            
            if won:
                # Победа
                stats["games_won"] = stats["games_won"] + 1
            else:
                # Поражение
                stats["games_lost"] = stats["games_lost"] + 1
            
            # Сохраняем статистику
            save_statics(stats)
        
        elif choice == "2":
            # СТАТИСТИКА
            show_statistics(stats)
        
        elif choice == "3":
            # ВЫХОД
            print("\nСпасибо за игру! До встречи!")
            break
        
        else:
            print("Выберите 1, 2 или 3")
            
if __name__ == "__main__":
    main()            
    