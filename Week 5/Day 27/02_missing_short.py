# 02_missing_short.py - Обработка пропусков (краткая версия)

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

np.random.seed(42)

print("="*60)
print("ОБРАБОТКА ПРОПУСКОВ - Основное")
print("="*60)

# ============================================
# СОЗДАНИЕ ДАННЫХ С ПРОПУСКАМИ
# ============================================

n = 100
data = {
    'возраст': np.random.randint(20, 60, n),
    'зарплата': np.random.randint(30000, 150000, n),
    'опыт': np.random.randint(0, 30, n)
}

df = pd.DataFrame(data)

# Добавляем 20% пропусков в зарплату
mask = np.random.random(n) < 0.2
df.loc[mask, 'зарплата'] = np.nan

# Добавляем 10% пропусков в возраст  
mask = np.random.random(n) < 0.1
df.loc[mask, 'возраст'] = np.nan

print(f"\nСоздано {len(df)} строк")
print("\nПропуски:")
print(df.isnull().sum())
"""
isnull() - проверить на NaN
sum() - посчитать количество
"""

# ============================================
# СПОСОБ 1: УДАЛЕНИЕ
# ============================================

print("\n" + "="*60)
print("СПОСОБ 1: Удаление строк")
print("="*60)

df_clean = df.dropna()
"""
dropna() - удалить строки с NaN
"""

print(f"Было: {len(df)} строк")
print(f"Стало: {len(df_clean)} строк")
print(f"Потеряно: {len(df) - len(df_clean)} строк")

# ============================================
# СПОСОБ 2: ЗАПОЛНЕНИЕ СРЕДНИМ
# ============================================

print("\n" + "="*60)
print("СПОСОБ 2: Заполнение средним")
print("="*60)

df_mean = df.copy()
df_mean['зарплата'] = df_mean['зарплата'].fillna(df_mean['зарплата'].mean())
df_mean['возраст'] = df_mean['возраст'].fillna(df_mean['возраст'].mean())
"""
fillna(value) - заполнить пропуски
mean() - среднее значение
"""

print(f"Средняя зарплата: {df['зарплата'].mean():.0f}")
print(f"Пропусков осталось: {df_mean.isnull().sum().sum()}")

# ============================================
# СПОСОБ 3: ЗАПОЛНЕНИЕ МЕДИАНОЙ
# ============================================

print("\n" + "="*60)
print("СПОСОБ 3: Заполнение медианой")
print("="*60)

df_median = df.copy()
df_median['зарплата'] = df_median['зарплата'].fillna(df_median['зарплата'].median())
df_median['возраст'] = df_median['возраст'].fillna(df_median['возраст'].median())
"""
median() - медиана (значение посередине)

ЛУЧШЕ ЧЕМ MEAN КОГДА:
- Есть выбросы (очень большие/маленькие значения)
"""

print(f"Медиана зарплаты: {df['зарплата'].median():.0f}")
print(f"Пропусков: {df_median.isnull().sum().sum()}")

# ============================================
# СПОСОБ 4: SimpleImputer (для ML)
# ============================================

print("\n" + "="*60)
print("СПОСОБ 4: SimpleImputer (sklearn)")
print("="*60)

imputer = SimpleImputer(strategy='median')
"""
SimpleImputer - для ML пайплайнов

strategy:
  'mean' - среднее
  'median' - медиана
  'most_frequent' - мода
"""

df_imputed = pd.DataFrame(
    imputer.fit_transform(df),
    columns=df.columns
)
"""
fit_transform() - обучить и применить

ВАЖНО:
На train: fit_transform()
На test: transform()
"""

print(f"Пропусков: {df_imputed.isnull().sum().sum()}")

# ============================================
# РЕЗЮМЕ
# ============================================

print("\n" + "="*60)
print("РЕЗЮМЕ:")
print("="*60)

print("""
ТРИ ГЛАВНЫХ СПОСОБА:

1. dropna() - удалить строки
   → Когда пропусков < 5%

2. fillna(mean/median) - заполнить
   → Когда пропусков 5-30%
   → median если есть выбросы

3. SimpleImputer - для ML
   → Удобно для train/test
   → Вписывается в pipeline
""")

print("\n✅ Основы обработки пропусков освоены!")