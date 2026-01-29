import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 

import seaborn as sns

sns.set_theme()
np.random.seed(42)

print("="*60)
print("ОБРАБОТКА ВЫБРОСОВ (Outliers)")
print("="*60)

print("""
ВЫБРОС (outlier) - значение сильно отличающееся от остальных

ПРИМЕРЫ:
Возраст: [25, 30, 28, 999, 32] ← 999 выброс (ошибка)
Зарплата: [50k, 60k, 70k, 5000k] ← 5000k выброс (миллионер)

ПРИЧИНЫ:
1. Ошибка ввода (999 вместо 29)
2. Ошибка измерения
3. Реальное исключение (очень богатый человек)

ПРОБЛЕМА:
Выбросы искажают модель!
Mean сильно сдвигается
""")


print("\n" + "="*60)
print("Создаём данные с выбросами")
print("="*60)

n = 100
zarplata = np.random.randint(30000, 100000, n)
vozrast = np.random.randint(20, 60, n)

df = pd.DataFrame({
    'zarplata': zarplata,
    'vozrast': vozrast
})

# Добавляем выбросы
df.loc[5, 'zarplata'] = 5000000  # миллионер
df.loc[10, 'vozrast'] = 5        # ошибка ввода
df.loc[15, 'zarplata'] = 1000    # слишком мало
df.loc[20, 'vozrast'] = 150      # невозможно

print(f"Создано {len(df)} строк")
print("\nСтатистика zarplata:")
print(df['zarplata'].describe())
"""
describe() показывает:
- min/max (если странные - выбросы!)
- mean vs median (если сильно отличаются - выбросы!)
"""

print(f"\nМинимум: {df['zarplata'].min()}")
print(f"Максимум: {df['zarplata'].max()}")
print(f"Среднее: {df['zarplata'].mean():.0f}")
print(f"Медиана: {df['zarplata'].median():.0f}")


print("\n" + "="*60)
print("МЕТОД 1: Визуализация (boxplot)")
print("="*60)

print("Смотрите график...")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Boxplot zarplata
axes[0].boxplot(df['zarplata'])
axes[0].set_title('Зарплата (видны выбросы)', fontweight='bold')
axes[0].set_ylabel('Зарплата')
axes[0].grid(True, alpha=0.3, axis='y')

# Boxplot vozrast
axes[1].boxplot(df['vozrast'])
axes[1].set_title('Возраст (видны выбросы)', fontweight='bold')
axes[1].set_ylabel('Возраст')
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()



# ============================================
# МЕТОД 2: IQR (Межквартильный размах)
# ============================================

print("\n" + "="*60)
print("МЕТОД 2: IQR метод")
print("="*60)

"""
IQR (Interquartile Range) - межквартильный размах

Q1 = 25% данных (первый квартиль)
Q3 = 75% данных (третий квартиль)
IQR = Q3 - Q1

ПРАВИЛО:
Выброс если:
  value < Q1 - 1.5 * IQR
  value > Q3 + 1.5 * IQR
"""

Q1 = df['zarplata'].quantile(0.25)
Q3 = df['zarplata'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"Q1 (25%): {Q1:.0f}")
print(f"Q3 (75%): {Q3:.0f}")
print(f"IQR: {IQR:.0f}")
print(f"\nГраницы нормы:")
print(f"  Нижняя: {lower_bound:.0f}")
print(f"  Верхняя: {upper_bound:.0f}")

# Найти выбросы
outliers = df[(df['zarplata'] < lower_bound) | (df['zarplata'] > upper_bound)]
"""
| - логическое ИЛИ
(condition1) | (condition2) - любое из условий
"""

print(f"\nНайдено выбросов: {len(outliers)}")
print("\nВыбросы:")
print(outliers[['zarplata']])


print("\n" + "="*60)
print("МЕТОД 3: Z-score")
print("="*60)

"""
Z-score показывает: на сколько стандартных отклонений 
значение отличается от среднего

z = (value - mean) / std

ПРАВИЛО:
Если |z| > 3 → выброс (слишком далеко от среднего)
"""

mean_zarplata = df['zarplata'].mean()
std_zarplata = df['zarplata'].std()

df['z_score'] = (df['zarplata'] - mean_zarplata) / std_zarplata

outliers_z = df[abs(df['z_score']) > 3]

print(f"Среднее: {mean_zarplata:.0f}")
print(f"Std: {std_zarplata:.0f}")
print(f"\nВыбросов (|z| > 3): {len(outliers_z)}")
print("\nВыбросы:")
print(outliers_z[['zarplata', 'z_score']])

# ============================================
# ОБРАБОТКА ВЫБРОСОВ
# ============================================

print("\n" + "="*60)
print("ОБРАБОТКА ВЫБРОСОВ")
print("="*60)

print("""
3 СПОСОБА:

1. УДАЛЕНИЕ
   - Просто убрать строки с выбросами
   - Когда: явная ошибка

2. ЗАМЕНА (CAPPING)
   - Заменить на границу (upper/lower bound)
   - Когда: хотим сохранить строку

3. ТРАНСФОРМАЦИЯ
   - log() - сжимает большие значения
   - Когда: распределение скошенное
""")

# Способ 1: Удаление
df_no_outliers = df[(df['zarplata'] >= lower_bound) & 
                     (df['zarplata'] <= upper_bound)]
"""
& - логическое И
(condition1) & (condition2) - оба условия
"""

print(f"\n1. Удаление:")
print(f"   Было: {len(df)} строк")
print(f"   Стало: {len(df_no_outliers)} строк")

# Способ 2: Замена (Capping)
df_capped = df.copy()
df_capped['zarplata'] = df_capped['zarplata'].clip(lower=lower_bound, 
                                                     upper=upper_bound)
"""
clip(lower, upper) - обрезать значения

Если value < lower → заменить на lower
Если value > upper → заменить на upper
"""

print(f"\n2. Замена (capping):")
print(f"   Мин до: {df['zarplata'].min()}")
print(f"   Мин после: {df_capped['zarplata'].min()}")
print(f"   Макс до: {df['zarplata'].max()}")
print(f"   Макс после: {df_capped['zarplata'].max()}")

# Способ 3: Log трансформация
df_log = df.copy()
df_log['zarplata_log'] = np.log1p(df_log['zarplata'])
"""
log1p(x) = log(1 + x)

Зачем +1? Чтобы избежать log(0)

ЭФФЕКТ:
Большие значения сжимаются:
1000 → log(1001) ≈ 6.9
1000000 → log(1000001) ≈ 13.8
Разница уменьшилась!
"""

print(f"\n3. Log трансформация:")
print(f"   Оригинал: min={df['zarplata'].min()}, max={df['zarplata'].max()}")
print(f"   Log: min={df_log['zarplata_log'].min():.2f}, max={df_log['zarplata_log'].max():.2f}")

# ============================================
# РЕЗЮМЕ
# ============================================

print("\n" + "="*60)
print("РЕЗЮМЕ:")
print("="*60)

print("""
ОБНАРУЖЕНИЕ ВЫБРОСОВ:

1. Визуально - boxplot
2. IQR метод (рекомендуется)
3. Z-score метод

ОБРАБОТКА:

1. Удаление - если явная ошибка
2. Capping - если хотим сохранить
3. Log - если сильно скошенное распределение

КОГДА ЧТО:
- Ошибка ввода (возраст 999) → Удалить
- Реальное исключение (миллионер) → Capping или оставить
- Сильный перекос данных → Log трансформация
""")

print("\n Обработка выбросов освоена!")
print("="*60)