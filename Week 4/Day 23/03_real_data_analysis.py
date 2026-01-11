import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Применить стиль
sns.set_theme(style="whitegrid")
sns.set_palette("husl")  # Красивая цветовая палитра

print("="*60)
print("АНАЛИЗ РЕАЛЬНЫХ ДАННЫХ")
print("="*60)

print("\n1. Загружаем встроенный датасет 'tips' (чаевые):")

# Seaborn имеет встроенные датасеты для практики
tips = sns.load_dataset('tips')
"""
Датасет 'tips' - реальные данные о чаевых в ресторане

Столбцы:
- total_bill: общий счёт (сколько заплатили за еду)
- tip: чаевые (сколько оставили официанту)
- sex: пол (Male/Female)
- smoker: курильщик (Yes/No)
- day: день недели (Thur, Fri, Sat, Sun)
- time: время (Lunch/Dinner)
- size: размер компании (сколько человек)
"""

print("\nПервые 10 строк:")
print(tips.head(10))

print("\nИнформация о данных:")
print(tips.info())
"""
info() показывает:
- Количество строк
- Типы данных каждого столбца
- Есть ли пропущенные значения
"""

print("\nСтатистика:")
print(tips.describe())
"""
describe() для числовых столбцов показывает:
- count: количество значений
- mean: среднее
- std: стандартное отклонение
- min, max: минимум и максимум
- 25%, 50%, 75%: квартили
"""

print("\n2. Анализируем связь между счётом и чаевыми:")

plt.figure(figsize=(12, 6))

# Scatter plot с линией регрессии
sns.scatterplot(data=tips, x='total_bill', y='tip', 
                hue='time', style='sex', s=100, alpha=0.7)
"""
РАЗБОР ПАРАМЕТРОВ:

x='total_bill' - счёт по горизонтали
y='tip' - чаевые по вертикали

hue='time' - ЦВЕТ зависит от времени (обед/ужин)
  Обед = один цвет
  Ужин = другой цвет

style='sex' - ФОРМА маркера зависит от пола
  Мужчина = один символ
  Женщина = другой символ

s=100 - размер точек
alpha=0.7 - прозрачность (0=прозрачно, 1=непрозрачно)

РЕЗУЛЬТАТ:
Один график показывает 4 измерения данных!
1. Счёт (X)
2. Чаевые (Y)
3. Время (цвет)
4. Пол (форма)
"""

# Добавить линию тренда
sns.regplot(data=tips, x='total_bill', y='tip', 
            scatter=False, color='red', line_kws={'linewidth': 2})
"""
regplot - добавляет линию регрессии (тренд)

scatter=False - НЕ рисовать точки (они уже есть)
color='red' - красная линия
line_kws - настройки линии

Линия показывает общую тенденцию:
Чем больше счёт → тем больше чаевые
"""

plt.title('Связь между счётом и чаевыми', fontsize=16, fontweight='bold')
plt.xlabel('Счёт ($)', fontsize=12)
plt.ylabel('Чаевые ($)', fontsize=12)
plt.legend(title='Легенда', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

print("✓ График связи показан")

print("\n3. Сравниваем чаевые по дням недели:")

plt.figure(figsize=(12, 6))

# Box plot с точками
sns.boxplot(data=tips, x='day', y='tip', hue='time')
"""
Box plot показывает статистику для каждого дня:

[----]     = диапазон "нормальных" значений
 ◻️         = медиана (середина)
 -         = выбросы (необычные значения)

hue='time' - разделить по времени (обед/ужин)
"""

# Добавить все точки поверх box plot
sns.swarmplot(data=tips, x='day', y='tip', 
              color='black', size=3, alpha=0.3)
"""
Зачем добавлять swarm поверх box?

Box показывает СТАТИСТИКУ
Swarm показывает РЕАЛЬНЫЕ ТОЧКИ

Вместе = полная картина!
"""

plt.title('Чаевые по дням недели', fontsize=16, fontweight='bold')
plt.xlabel('День недели', fontsize=12)
plt.ylabel('Чаевые ($)', fontsize=12)
plt.legend(title='Время')
plt.tight_layout()
plt.show()

print("✓ Сравнение по дням показано")


print("\n4. Анализируем распределения:")

# Создать сетку 2x2 для нескольких графиков
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
"""
subplots(2, 2) создаёт 4 графика:
[ax1] [ax2]
[ax3] [ax4]

axes[0, 0] = верхний левый
axes[0, 1] = верхний правый
axes[1, 0] = нижний левый
axes[1, 1] = нижний правый
"""

# График 1: Распределение счетов
sns.histplot(data=tips, x='total_bill', kde=True, 
             bins=20, ax=axes[0, 0])
"""
ax=axes[0, 0] - рисовать на первом графике

bins=20 - разделить на 20 интервалов
kde=True - добавить плавную кривую

Гистограмма показывает:
Какие счета встречаются чаще всего
"""
axes[0, 0].set_title('Распределение счетов', fontweight='bold')
axes[0, 0].set_xlabel('Счёт ($)')

# График 2: Распределение чаевых
sns.histplot(data=tips, x='tip', kde=True, 
             bins=20, ax=axes[0, 1], color='coral')
axes[0, 1].set_title('Распределение чаевых', fontweight='bold')
axes[0, 1].set_xlabel('Чаевые ($)')

# График 3: Чаевые по времени
sns.violinplot(data=tips, x='time', y='tip', ax=axes[1, 0])
"""
Violin plot = box plot + распределение

Широкая часть = много значений здесь
Узкая часть = мало значений
"""
axes[1, 0].set_title('Чаевые по времени суток', fontweight='bold')
axes[1, 0].set_xlabel('Время')
axes[1, 0].set_ylabel('Чаевые ($)')

# График 4: Размер компании
sns.countplot(data=tips, x='size', ax=axes[1, 1], palette='Set2')
"""
Count plot - подсчёт частот

Автоматически считает:
Сколько раз встречается каждый размер компании
"""
axes[1, 1].set_title('Размер компаний', fontweight='bold')
axes[1, 1].set_xlabel('Количество человек')
axes[1, 1].set_ylabel('Частота')

plt.tight_layout()
plt.show()

print("✓ Распределения показаны")


print("\n5. Вычисляем процент чаевых:")

# Добавить новый столбец - процент чаевых
tips['tip_percent'] = (tips['tip'] / tips['total_bill']) * 100
"""
ВАЖНЫЙ МОМЕНТ!

Можно создавать НОВЫЕ столбцы из существующих:
tips['новый_столбец'] = вычисление

Здесь мы вычислили:
процент = (чаевые / счёт) × 100

Пример:
Счёт = $50, Чаевые = $10
Процент = (10 / 50) × 100 = 20%
"""

print("\nПервые строки с процентами:")
print(tips[['total_bill', 'tip', 'tip_percent']].head())

# График процентов чаевых
plt.figure(figsize=(12, 6))

sns.boxplot(data=tips, x='day', y='tip_percent', hue='time')

plt.title('Процент чаевых по дням недели', fontsize=16, fontweight='bold')
plt.xlabel('День недели', fontsize=12)
plt.ylabel('Процент чаевых (%)', fontsize=12)
plt.legend(title='Время')
plt.axhline(y=15, color='red', linestyle='--', linewidth=2, 
            label='Стандарт 15%')
"""
axhline - горизонтальная линия

y=15 - на уровне 15%
linestyle='--' - пунктир
label='Стандарт 15%' - подпись в легенде

Показывает стандартный размер чаевых для сравнения
"""
plt.legend()
plt.tight_layout()
plt.show()

print("✓ Процент чаевых показан")


print("\n6. Создаём тепловую карту средних чаевых:")

# Сгруппировать данные по дню и времени, вычислить среднее
pivot_data = tips.pivot_table(values='tip', 
                               index='day', 
                               columns='time', 
                               aggfunc='mean')
"""
pivot_table - создать сводную таблицу (как в Excel)

values='tip' - что вычислять (чаевые)
index='day' - строки (дни недели)
columns='time' - столбцы (обед/ужин)
aggfunc='mean' - функция агрегации (среднее)

РЕЗУЛЬТАТ - таблица:
           Dinner  Lunch
Thur       2.77    2.77
Fri        2.73    ...
Sat        2.99    ...
Sun        3.26    ...
"""

print("\nСводная таблица средних чаевых:")
print(pivot_data)

# Нарисовать тепловую карту
plt.figure(figsize=(8, 6))

sns.heatmap(pivot_data, annot=True, fmt='.2f', 
            cmap='YlOrRd', cbar_kws={'label': 'Средние чаевые ($)'})
"""
РАЗБОР:

annot=True - показать числа в ячейках
fmt='.2f' - формат чисел (2 знака после запятой)
cmap='YlOrRd' - цветовая схема (жёлтый-оранжевый-красный)
cbar_kws - настройки цветовой шкалы

ЦВЕТА:
Светлый = маленькие чаевые
Тёмный = большие чаевые

Быстро видно где чаевые больше!
"""

plt.title('Средние чаевые: день × время', fontsize=16, fontweight='bold')
plt.xlabel('Время суток', fontsize=12)
plt.ylabel('День недели', fontsize=12)
plt.tight_layout()
plt.show()

print("✓ Тепловая карта показана")


print("\n7. Категориальный анализ:")

# Создать FacetGrid - сетку графиков по категориям
g = sns.FacetGrid(tips, col='time', row='smoker', 
                  height=4, aspect=1.5)
"""
FacetGrid - создать НЕСКОЛЬКО графиков сразу

col='time' - столбцы = время (Lunch/Dinner)
row='smoker' - строки = курильщик (Yes/No)

РЕЗУЛЬТАТ - сетка 2×2:
           Lunch    Dinner
Yes        [graf]   [graf]
No         [graf]   [graf]

height=4 - высота каждого графика
aspect=1.5 - соотношение сторон (ширина/высота)
"""

# На каждый график нарисовать scatter
g.map(sns.scatterplot, 'total_bill', 'tip', alpha=0.7)
"""
map() - применить функцию к КАЖДОМУ графику

Аргументы функции:
'total_bill' - X
'tip' - Y
alpha=0.7 - прозрачность

Результат: 4 графика с одинаковой структурой,
но разными данными
"""

# Добавить заголовки
g.set_axis_labels('Счёт ($)', 'Чаевые ($)')
g.set_titles(col_template='{col_name}', row_template='Курит: {row_name}')
g.add_legend()

plt.suptitle('Чаевые: время × курильщик', 
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

print("✓ Категориальный анализ показан")



print("\n" + "="*60)
print("ВЫВОДЫ ИЗ АНАЛИЗА ДАННЫХ:")
print("="*60)

# Вычислить основную статистику
avg_tip = tips['tip'].mean()
avg_bill = tips['total_bill'].mean()
avg_percent = tips['tip_percent'].mean()

# Чаевые по времени
lunch_tip = tips[tips['time'] == 'Lunch']['tip'].mean()
dinner_tip = tips[tips['time'] == 'Dinner']['tip'].mean()

# По полу
male_tip = tips[tips['sex'] == 'Male']['tip_percent'].mean()
female_tip = tips[tips['sex'] == 'Female']['tip_percent'].mean()

print(f"""
ОСНОВНАЯ СТАТИСТИКА:
- Средний счёт: ${avg_bill:.2f}
- Средние чаевые: ${avg_tip:.2f}
- Средний процент: {avg_percent:.1f}%

ПО ВРЕМЕНИ СУТОК:
- Обед: ${lunch_tip:.2f}
- Ужин: ${dinner_tip:.2f}
- Разница: ${abs(dinner_tip - lunch_tip):.2f}

ПО ПОЛУ:
- Мужчины: {male_tip:.1f}%
- Женщины: {female_tip:.1f}%

ИНТЕРЕСНЫЕ НАХОДКИ:
1. Чаевые коррелируют со счётом (чем больше счёт, тем больше чаевые)
2. В выходные чаевые немного выше
3. Процент чаевых относительно стабилен (~15-16%)
4. Размер компании влияет на общую сумму чаевых
""")

print("="*60)
print("\n Анализ реальных данных завершён!")
print("="*60)