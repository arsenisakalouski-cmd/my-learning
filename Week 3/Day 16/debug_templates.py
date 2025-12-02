# debug_templates.py - Диагностика шаблонов

import os
from flask import Flask

app = Flask(__name__)

print("="*60)
print("ДИАГНОСТИКА ШАБЛОНОВ")
print("="*60)

# Текущая папка
print(f"\nТекущая папка: {os.getcwd()}")

# Где Flask ищет шаблоны
print(f"\nПапка шаблонов: {app.template_folder}")
print(f"Полный путь: {os.path.join(os.getcwd(), app.template_folder)}")

# Проверяем существует ли папка templates
if os.path.exists('templates'):
    print("\n✓ Папка templates/ найдена")
    
    # Список всех файлов в templates
    print("\nФайлы в templates/:")
    for file in os.listdir('templates'):
        size = os.path.getsize(os.path.join('templates', file))
        print(f"  - {file} ({size} байт)")
        
        # Если файл пустой
        if size == 0:
            print(f"    ⚠️ ФАЙЛ ПУСТОЙ!")
else:
    print("\n✗ Папка templates/ НЕ НАЙДЕНА")

# Проверяем конкретный файл
if os.path.exists('templates/form_example.html'):
    print("\n✓ form_example.html найден")
    size = os.path.getsize('templates/form_example.html')
    print(f"  Размер: {size} байт")
    
    if size > 0:
        print("  ✓ Файл содержит данные")
        
        # Показываем первые 200 символов
        with open('templates/form_example.html', 'r', encoding='utf-8') as f:
            content = f.read(200)
            print(f"\n  Начало файла:\n{content}...")
    else:
        print("  ✗ ФАЙЛ ПУСТОЙ!")
else:
    print("\n✗ form_example.html НЕ НАЙДЕН")

print("\n" + "="*60)