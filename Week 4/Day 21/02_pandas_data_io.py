# 02_pandas_data_io.py - Чтение и запись данных

import pandas as pd
import numpy as np

print("="*60)
print("ЧТЕНИЕ И ЗАПИСЬ ДАННЫХ В Pandas")
print("="*60)

# ==========================================
# СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ
# ==========================================

print("\n1. Создание тестовых данных:")

# Создать DataFrame
np.random.seed(42)
data = {
    'ID': range(1, 11),
    'Имя': ['Иван', 'Мария', 'Пётр', 'Анна', 'Сергей', 
            'Ольга', 'Дмитрий', 'Елена', 'Алексей', 'Наталья'],
    'Возраст': np.random.randint(20, 40, 10),
    'Город': np.random.choice(['Москва', 'СПб', 'Казань'], 10),
    'Зарплата': np.random.randint(30000, 100000, 10),
    'Опыт': np.random.randint(0, 15, 10)
}

df = pd.DataFrame(data)
print(f"\nТестовый DataFrame:\n{df}")

# ==========================================
# CSV - COMMA SEPARATED VALUES
# ==========================================

print("\n" + "="*60)
print("2. Работа с CSV:")
print("="*60)

# Записать в CSV
df.to_csv('employees.csv', index=False)
"""
index=False - не записывать индекс как столбец
encoding='utf-8' - кодировка (для русских букв)
sep=',' - разделитель (по умолчанию запятая)
"""
print("✓ Сохранено в employees.csv")

# Прочитать CSV
df_read = pd.read_csv('employees.csv')
print(f"\nПрочитано из CSV:\n{df_read.head()}")

# С другим разделителем
df.to_csv('employees_semicolon.csv', index=False, sep=';')
df_semicolon = pd.read_csv('employees_semicolon.csv', sep=';')
print(f"\nС разделителем ';':\n{df_semicolon.head(3)}")

# Указать столбцы для чтения
df_selected = pd.read_csv('employees.csv', usecols=['Имя', 'Возраст', 'Зарплата'])
print(f"\nТолько выбранные столбцы:\n{df_selected.head()}")

# Пропустить строки
df_skip = pd.read_csv('employees.csv', skiprows=2)
"""
skiprows=2 - пропустить первые 2 строки
skiprows=[0, 2] - пропустить строки 0 и 2
"""
print(f"\nС пропуском строк:\n{df_skip.head(3)}")

# ==========================================
# EXCEL
# ==========================================

print("\n" + "="*60)
print("3. Работа с Excel:")
print("="*60)

try:
    # Записать в Excel (требует openpyxl)
    df.to_excel('employees.xlsx', index=False, sheet_name='Сотрудники')
    print("✓ Сохранено в employees.xlsx")
    
    # Прочитать из Excel
    df_excel = pd.read_excel('employees.xlsx', sheet_name='Сотрудники')
    print(f"\nПрочитано из Excel:\n{df_excel.head()}")
    
except ImportError:
    print("\n⚠️ Для Excel нужен openpyxl:")
    print("pip install openpyxl --break-system-packages")

# ==========================================
# JSON
# ==========================================

print("\n" + "="*60)
print("4. Работа с JSON:")
print("="*60)

# Записать в JSON
df.to_json('employees.json', orient='records', indent=2, force_ascii=False)
"""
orient='records' - формат:
[
  {"ID": 1, "Имя": "Иван", ...},
  {"ID": 2, "Имя": "Мария", ...}
]

Другие форматы:
- 'split' - {index: [...], columns: [...], data: [...]}
- 'index' - {0: {...}, 1: {...}}
- 'columns' - {col1: {0: val, 1: val}, col2: {...}}
"""
print("✓ Сохранено в employees.json")

# Прочитать из JSON
df_json = pd.read_json('employees.json', orient='records')
print(f"\nПрочитано из JSON:\n{df_json.head()}")

# ==========================================
# СЛОВАРЬ/СПИСОК
# ==========================================

print("\n" + "="*60)
print("5. Преобразование в словарь/список:")
print("="*60)

# DataFrame → словарь
dict_records = df.to_dict('records')
print(f"\nВ словарь (records):\n{dict_records[:2]}")

dict_list = df.to_dict('list')
print(f"\nВ словарь (list):\n{list(dict_list.items())[:2]}")

# DataFrame → список списков
list_values = df.values.tolist()
print(f"\nВ список списков:\n{list_values[:2]}")

# ==========================================
# ИНФОРМАЦИЯ О ФАЙЛЕ
# ==========================================

print("\n" + "="*60)
print("6. Информация о прочитанных данных:")
print("="*60)

df_info = pd.read_csv('employees.csv')

print(f"Размер: {df_info.shape}")
print(f"Столбцы: {df_info.columns.tolist()}")
print(f"Типы данных:\n{df_info.dtypes}")
print(f"\nПамять:")
print(df_info.memory_usage(deep=True))

# ==========================================
# ЧТЕНИЕ С ПАРАМЕТРАМИ
# ==========================================

print("\n" + "="*60)
print("7. Чтение с дополнительными параметрами:")
print("="*60)

# Изменить типы данных при чтении
df_types = pd.read_csv('employees.csv', dtype={'ID': str, 'Возраст': float})
print(f"\nС изменёнными типами:\n{df_types.dtypes}")

# Указать столбец как индекс
df_index = pd.read_csv('employees.csv', index_col='ID')
print(f"\nС индексом ID:\n{df_index.head()}")

# Переименовать столбцы при чтении
df_renamed = pd.read_csv('employees.csv', 
                         names=['Айди', 'ФИО', 'Лет', 'Локация', 'Деньги', 'Стаж'],
                         skiprows=1)  # Пропустить заголовок
print(f"\nС переименованными столбцами:\n{df_renamed.head(3)}")

# ==========================================
# ОБРАБОТКА БОЛЬШИХ ФАЙЛОВ
# ==========================================

print("\n" + "="*60)
print("8. Чтение больших файлов частями:")
print("="*60)

# Создать большой CSV для примера
big_data = pd.DataFrame({
    'A': range(1000),
    'B': np.random.rand(1000),
    'C': np.random.choice(['X', 'Y', 'Z'], 1000)
})
big_data.to_csv('big_file.csv', index=False)

# Читать частями (chunks)
chunk_size = 100
chunks = []

for chunk in pd.read_csv('big_file.csv', chunksize=chunk_size):
    """
    chunksize - читать по N строк за раз
    Полезно для огромных файлов которые не влезают в память
    """
    # Обработать chunk
    chunks.append(chunk.shape[0])

print(f"Прочитано {len(chunks)} частей по {chunk_size} строк")
print(f"Размеры частей: {chunks}")

# Объединить все части
df_combined = pd.concat(pd.read_csv('big_file.csv', chunksize=chunk_size))
print(f"\nОбъединённый размер: {df_combined.shape}")

# ==========================================
# СОХРАНЕНИЕ С ДОПОЛНИТЕЛЬНЫМИ ПАРАМЕТРАМИ
# ==========================================

print("\n" + "="*60)
print("9. Сохранение с параметрами:")
print("="*60)

# Сохранить только определённые столбцы
df[['Имя', 'Зарплата']].to_csv('salaries.csv', index=False)
print("✓ Сохранены только Имя и Зарплата")

# Добавить к существующему файлу
df.head(2).to_csv('append_test.csv', index=False)
df.tail(2).to_csv('append_test.csv', mode='a', header=False, index=False)
"""
mode='a' - append (добавить)
header=False - не писать заголовок повторно
"""
print("✓ Добавлено к файлу")

# Сжатие
df.to_csv('employees.csv.gz', index=False, compression='gzip')
print("✓ Сохранено со сжатием gzip")

# Прочитать сжатый файл
df_compressed = pd.read_csv('employees.csv.gz')
print(f"Прочитано из .gz: {df_compressed.shape}")

print("\n" + "="*60)
print("ИТОГИ:")
print("="*60)
print("""
Чтение данных:

CSV:
- pd.read_csv('file.csv')
- sep=';' - разделитель
- usecols=['A', 'B'] - выбор столбцов
- skiprows=2 - пропустить строки
- dtype={'A': str} - типы данных

Excel:
- pd.read_excel('file.xlsx', sheet_name='Sheet1')

JSON:
- pd.read_json('file.json', orient='records')

Запись:

CSV:
- df.to_csv('file.csv', index=False)
- sep=';' - разделитель
- mode='a' - добавить
- compression='gzip' - сжатие

Excel:
- df.to_excel('file.xlsx', index=False)

JSON:
- df.to_json('file.json', orient='records')

Большие файлы:
- chunksize=1000 - читать частями
""")

# Очистка
import os
files = ['employees.csv', 'employees_semicolon.csv', 'employees.json', 
         'salaries.csv', 'append_test.csv', 'employees.csv.gz', 'big_file.csv']
for f in files:
    if os.path.exists(f):
        os.remove(f)
print("\n✓ Временные файлы удалены")


