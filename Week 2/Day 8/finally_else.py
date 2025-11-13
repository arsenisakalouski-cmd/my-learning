print("=== Блоки Finally и Else ===\n")

print("--- Пример 1: Работа с файлом ---")

def read_file(filename):
    file_handle = None 
    try:
        print(f" Открываю файл '{filename}'...")
        file_handle = open(filename, "r", encoding="utf-8")
        content = file_handle.read()
        print(f" Прочитано {len(content)} символов")
        return content
    except FileNotFoundError:
        print(f" Файл '{filename}' не найден!")
        return None
    except PermissionError:
        print(f" Нет прав на чтение '{filename}'!")
        return None
    finally:
        if file_handle:
            file_handle.close()
            print(" Файл закрыт")
        print(" Операция завершена\n")

read_file("test.txt")  
read_file("nonexistent.txt")