import pandas as pd
import numpy as np

print("="*60)
print("ОБРАБОТКА ПРОПУЩЕННЫХ ДАННЫХ В Pandas")
print("="*60)

print("\n1. Данные с пропусками:")

data = {
    'Имя': ['Иван', 'Мария', 'Пётр', None, 'Сергей', 'Ольга', 'Дмитрий'],
    'Возраст': [25, 30, np.nan, 35, 22, np.nan, 28],
    'Город': ['Москва', None, 'Казань', 'Москва', 'СПб', 'Москва', None],
    'Зарплата': [50000, 60000, np.nan, 70000, 40000, 55000, np.nan],
    'Опыт': [2, 5, 3, np.nan, 1, 4, 6]
}

df = pd.DataFrame(data)
print(f"\nDataFrame с пропусками:\n{df}")
"""
NaN (Not a Number) - отсутствующее значение
None - то же самое для объектных типов
"""

print("\n" + "="*60)
print("2. Обнаружение пропусков:")
print("="*60)

# Булева маска (True = пропуск)
print(f"\nisnull():\n{df.isnull()}")

# Обратная маска (True = не пропуск)
print(f"\nnotnull():\n{df.notnull()}")

# Количество пропусков в каждом столбце
print(f"\nПропусков в столбцах:\n{df.isnull().sum()}")

# Процент пропусков
print(f"\nПроцент пропусков:")
for col in df.columns:
    pct = df[col].isnull().sum() / len(df) * 100
    print(f"  {col}: {pct:.1f}%")

# Общее количество пропусков
total_missing = df.isnull().sum().sum()
print(f"\nВсего пропусков: {total_missing}")

# Строки с хотя бы одним пропуском
rows_with_missing = df.isnull().any(axis=1).sum()
print(f"Строк с пропусками: {rows_with_missing}")

# Строки без пропусков
rows_complete = df.notnull().all(axis=1).sum()
print(f"Полных строк: {rows_complete}")



print("\n" + "="*60)
print("3. Удаление пропусков:")
print("="*60)

# Удалить строки с любыми пропусками
df_dropped_rows = df.dropna()
print(f"\nУдалены строки с пропусками:\n{df_dropped_rows}")
print(f"Было строк: {len(df)}, осталось: {len(df_dropped_rows)}")

# Удалить столбцы с любыми пропусками
df_dropped_cols = df.dropna(axis=1)
print(f"\nУдалены столбцы с пропусками:")
print(f"Было: {df.columns.tolist()}")
print(f"Осталось: {df_dropped_cols.columns.tolist()}")

# Удалить строки где пропуск в определённом столбце
df_dropped_age = df.dropna(subset=['Возраст'])
print(f"\nУдалены строки где пропуск в Возрасте:\n{df_dropped_age}")

# Удалить строки где все значения - пропуски
df_all_na = pd.DataFrame([[np.nan, np.nan], [1, 2], [np.nan, np.nan]])
df_cleaned = df_all_na.dropna(how='all')
print(f"\nУдалены строки где ВСЕ значения пропуски:")
print(f"Было:\n{df_all_na}")
print(f"Стало:\n{df_cleaned}")

# Удалить если минимум N значений не-пропусков
df_thresh = df.dropna(thresh=4)  # Минимум 4 не-NaN
print(f"\nМинимум 4 значения не-NaN:\n{df_thresh}")




print("\n" + "="*60)
print("4. Заполнение пропусков:")
print("="*60)

# Заполнить константой
df_filled_zero = df.fillna(0)
print(f"\nЗаполнено нулями (Возраст):\n{df_filled_zero['Возраст']}")

# Разные значения для разных столбцов
df_filled_dict = df.fillna({
    'Имя': 'Неизвестно',
    'Возраст': df['Возраст'].mean(),
    'Город': 'Москва',
    'Зарплата': df['Зарплата'].median(),
    'Опыт': 0
})
print(f"\nЗаполнено разными значениями:\n{df_filled_dict}")

# Заполнить средним
df_filled_mean = df.copy()
df_filled_mean['Возраст'] = df_filled_mean['Возраст'].fillna(df['Возраст'].mean())
df_filled_mean['Зарплата'] = df_filled_mean['Зарплата'].fillna(df['Зарплата'].mean())
print(f"\nЗаполнено средним:\n{df_filled_mean[['Возраст', 'Зарплата']]}")


# Заполнить медианой
df_filled_median = df.copy()
df_filled_median['Зарплата'] = df_filled_median['Зарплата'].fillna(df['Зарплата'].median())
print(f"\nЗарплата заполнена медианой:\n{df_filled_median['Зарплата']}")



print("\n" + "="*60)
print("5. Forward/Backward Fill:")
print("="*60)

# Данные временного ряда
ts_data = pd.DataFrame({
    'Дата': pd.date_range('2025-01-01', periods=7),
    'Значение': [10, np.nan, np.nan, 20, np.nan, 30, np.nan]
})
print(f"\nВременной ряд:\n{ts_data}")


# Forward fill (заполнить предыдущим)
ts_ffill = ts_data.copy()
ts_ffill['Значение'] = ts_ffill['Значение'].fillna(method='ffill')
print(f"\nForward fill:\n{ts_ffill}")
"""
10 → 10, 10, 20, 20, 30, 30
Заполняет предыдущим значением
"""

# Backward fill (заполнить следующим)
ts_bfill = ts_data.copy()
ts_bfill['Значение'] = ts_bfill['Значение'].fillna(method='bfill')
print(f"\nBackward fill:\n{ts_bfill}")
"""
10, 20, 20, 20, 30, 30, NaN (последний остаётся NaN)
Заполняет следующим значением
"""


print("\n" + "="*60)
print("6. Интерполяция:")
print("="*60)

# Линейная интерполяция
ts_interp = ts_data.copy()
ts_interp['Значение'] = ts_interp['Значение'].interpolate()
print(f"\nЛинейная интерполяция:\n{ts_interp}")
"""
10 → 13.33, 16.67, 20 → 25, 30 → NaN
Вычисляет промежуточные значения
"""

# Полиномиальная интерполяция
ts_poly = ts_data.copy()
ts_poly['Значение'] = ts_poly['Значение'].interpolate(method='polynomial', order=2)
print(f"\nПолиномиальная:\n{ts_poly}")



print("\n" + "="*60)
print("7. Замена значений:")
print("="*60)

# Заменить конкретное значение
df_replace = df.copy()
df_replace['Город'] = df_replace['Город'].replace('Москва', 'MSK')
print(f"\nЗамена Москва → MSK:\n{df_replace['Город']}")

# Множественная замена
city_mapping = {'Москва': 'MSK', 'СПб': 'SPB', 'Казань': 'KZN'}
df_replace['Город'] = df['Город'].replace(city_mapping)
print(f"\nМножественная замена:\n{df_replace['Город']}")

# Заменить NaN
df_replace_nan = df.replace(np.nan, 'ПУСТО')
print(f"\nЗамена NaN → ПУСТО:\n{df_replace_nan}")



print("\n" + "="*60)
print("8. Проверка конкретных значений:")
print("="*60)

# Заменить нули на NaN
data_with_zeros = pd.DataFrame({
    'A': [1, 0, 3, 0, 5],
    'B': [0, 2, 0, 4, 5]
})
print(f"\nДанные с нулями:\n{data_with_zeros}")

data_zeros_to_nan = data_with_zeros.replace(0, np.nan)
print(f"\nНули → NaN:\n{data_zeros_to_nan}")

# Заменить отрицательные на NaN
data_with_neg = pd.DataFrame({'A': [1, -2, 3, -4, 5]})
data_neg_to_nan = data_with_neg[data_with_neg > 0]
print(f"\nТолько положительные:\n{data_neg_to_nan}")


print("\n" + "="*60)
print("9. Практический пример - очистка данных:")
print("="*60)

# Грязные данные
dirty_data = pd.DataFrame({
    'ID': [1, 2, 3, 4, 5],
    'Имя': ['Иван', None, 'Пётр', 'Анна', None],
    'Возраст': [25, 30, -5, np.nan, 35],  # -5 - ошибка
    'Зарплата': [50000, np.nan, 45000, 70000, 0],  # 0 - не указано
    'Email': ['ivan@mail.ru', None, 'petr@', 'anna@mail.ru', 'sergey@mail.ru']
})

print(f"\nГрязные данные:\n{dirty_data}")

# Очистка
cleaned = dirty_data.copy()

# 1. Заменить невалидные значения на NaN
cleaned.loc[cleaned['Возраст'] < 0, 'Возраст'] = np.nan
cleaned.loc[cleaned['Зарплата'] == 0, 'Зарплата'] = np.nan
cleaned.loc[~cleaned['Email'].str.contains('@', na=False), 'Email'] = np.nan

# 2. Заполнить пропуски
cleaned['Имя'] = cleaned['Имя'].fillna('Неизвестно')
cleaned['Возраст'] = cleaned['Возраст'].fillna(cleaned['Возраст'].median())
cleaned['Зарплата'] = cleaned['Зарплата'].fillna(cleaned['Зарплата'].mean())

# 3. Удалить строки где Email = NaN (критичное поле)
cleaned = cleaned.dropna(subset=['Email'])

print(f"\nОчищенные данные:\n{cleaned}")

# Отчёт
print(f"\nОтчёт об очистке:")
print(f"  Строк было: {len(dirty_data)}")
print(f"  Строк стало: {len(cleaned)}")
print(f"  Удалено: {len(dirty_data) - len(cleaned)}")

print("\n" + "="*60)
print("ИТОГИ:")
print("="*60)
print("""
Обработка пропусков:

Обнаружение:
- df.isnull() - булева маска
- df.isnull().sum() - количество
- df.notnull() - обратная маска

Удаление:
- df.dropna() - удалить строки
- df.dropna(axis=1) - удалить столбцы
- df.dropna(subset=['col']) - по столбцу
- df.dropna(thresh=N) - минимум N значений

Заполнение:
- df.fillna(0) - константой
- df.fillna({'A': 0, 'B': 1}) - разные значения
- df['col'].fillna(df['col'].mean()) - средним
- df['col'].fillna(method='ffill') - предыдущим
- df['col'].interpolate() - интерполяция

Замена:
- df.replace(old, new) - заменить значение
- df.replace({old1: new1, old2: new2}) - словарь
""")
