# 02_plot_types.py - Типы графиков

import matplotlib.pyplot as plt
import numpy as np

print("="*60)
print("ТИПЫ ГРАФИКОВ В Matplotlib")
print("="*60)

# ==========================================
# 1. LINE PLOT (ЛИНЕЙНЫЙ)
# ==========================================

print("\n1. Line Plot (линейный график):")

# Данные продаж по месяцам
months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн']
sales = [15000, 18000, 22000, 19000, 25000, 28000]

plt.figure(figsize=(10, 6))
plt.plot(months, sales, marker='o', linewidth=2, markersize=8)

plt.title('Продажи по месяцам', fontsize=16, fontweight='bold')
plt.xlabel('Месяц', fontsize=12)
plt.ylabel('Продажи (руб)', fontsize=12)
plt.grid(True, alpha=0.3)

# Аннотации
for i, v in enumerate(sales):
    plt.text(i, v + 500, f'{v:,}', ha='center')

plt.tight_layout()
plt.show()

print("✓ Линейный график показан")

# ==========================================
# 2. BAR CHART (СТОЛБЧАТАЯ ДИАГРАММА)
# ==========================================

print("\n2. Bar Chart (столбчатая диаграмма):")

# Продажи по категориям
categories = ['Электроника', 'Одежда', 'Продукты', 'Книги', 'Спорт']
values = [45000, 32000, 28000, 15000, 22000]

plt.figure(figsize=(10, 6))
bars = plt.bar(categories, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])

plt.title('Продажи по категориям', fontsize=16, fontweight='bold')
plt.xlabel('Категория', fontsize=12)
plt.ylabel('Продажи (руб)', fontsize=12)
plt.grid(True, alpha=0.3, axis='y')

# Значения на столбцах
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:,.0f}',
             ha='center', va='bottom')

plt.tight_layout()
plt.show()

print("✓ Столбчатая диаграмма показана")

# ==========================================
# 3. HORIZONTAL BAR CHART (ГОРИЗОНТАЛЬНАЯ)
# ==========================================

print("\n3. Horizontal Bar Chart (горизонтальная):")

# Топ-5 городов
cities = ['Москва', 'СПб', 'Казань', 'Новосибирск', 'Екатеринбург']
population = [12.6, 5.4, 1.3, 1.6, 1.5]

plt.figure(figsize=(10, 6))
bars = plt.barh(cities, population, color='skyblue')

plt.title('Население городов (млн)', fontsize=16, fontweight='bold')
plt.xlabel('Население (млн)', fontsize=12)
plt.grid(True, alpha=0.3, axis='x')

# Значения
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2.,
             f'{width:.1f}',
             ha='left', va='center', fontsize=11)

plt.tight_layout()
plt.show()

print("✓ Горизонтальная диаграмма показана")

# ==========================================
# 4. GROUPED BAR CHART (СГРУППИРОВАННАЯ)
# ==========================================

print("\n4. Grouped Bar Chart (сгруппированная):")

# Продажи двух магазинов
categories = ['Янв', 'Фев', 'Мар', 'Апр', 'Май']
store1 = [15, 18, 22, 19, 25]
store2 = [12, 16, 20, 21, 23]

x = np.arange(len(categories))
width = 0.35

plt.figure(figsize=(10, 6))
plt.bar(x - width/2, store1, width, label='Магазин 1', color='#FF6B6B')
plt.bar(x + width/2, store2, width, label='Магазин 2', color='#4ECDC4')

plt.title('Сравнение продаж магазинов', fontsize=16, fontweight='bold')
plt.xlabel('Месяц', fontsize=12)
plt.ylabel('Продажи (тыс. руб)', fontsize=12)
plt.xticks(x, categories)
plt.legend()
plt.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("✓ Сгруппированная диаграмма показана")

# ==========================================
# 5. STACKED BAR CHART (С НАКОПЛЕНИЕМ)
# ==========================================

print("\n5. Stacked Bar Chart (с накоплением):")

categories = ['Q1', 'Q2', 'Q3', 'Q4']
product_a = [30, 35, 40, 45]
product_b = [20, 25, 22, 28]
product_c = [15, 18, 20, 22]

plt.figure(figsize=(10, 6))
plt.bar(categories, product_a, label='Продукт A', color='#FF6B6B')
plt.bar(categories, product_b, bottom=product_a, label='Продукт B', color='#4ECDC4')
plt.bar(categories, product_c, 
        bottom=np.array(product_a) + np.array(product_b),
        label='Продукт C', color='#45B7D1')

plt.title('Продажи по продуктам (кварталы)', fontsize=16, fontweight='bold')
plt.xlabel('Квартал', fontsize=12)
plt.ylabel('Продажи', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("✓ Диаграмма с накоплением показана")

# ==========================================
# 6. HISTOGRAM (ГИСТОГРАММА)
# ==========================================

print("\n6. Histogram (гистограмма распределения):")

# Рост людей (нормальное распределение)
np.random.seed(42)
heights = np.random.normal(170, 10, 1000)

plt.figure(figsize=(10, 6))
plt.hist(heights, bins=30, color='skyblue', edgecolor='black', alpha=0.7)

plt.title('Распределение роста', fontsize=16, fontweight='bold')
plt.xlabel('Рост (см)', fontsize=12)
plt.ylabel('Количество', fontsize=12)
plt.grid(True, alpha=0.3, axis='y')

# Средняя линия
mean_height = heights.mean()
plt.axvline(mean_height, color='red', linestyle='--', linewidth=2, 
            label=f'Среднее: {mean_height:.1f} см')
plt.legend()

plt.tight_layout()
plt.show()

print("✓ Гистограмма показана")

# ==========================================
# 7. SCATTER PLOT (ДИАГРАММА РАССЕЯНИЯ)
# ==========================================

print("\n7. Scatter Plot (диаграмма рассеяния):")

# Связь между площадью и ценой квартир
np.random.seed(42)
area = np.random.uniform(30, 120, 100)
price = area * 100000 + np.random.normal(0, 500000, 100)

plt.figure(figsize=(10, 6))
plt.scatter(area, price, alpha=0.6, s=50, color='coral')

plt.title('Площадь vs Цена квартир', fontsize=16, fontweight='bold')
plt.xlabel('Площадь (м²)', fontsize=12)
plt.ylabel('Цена (руб)', fontsize=12)
plt.grid(True, alpha=0.3)

# Линия тренда
z = np.polyfit(area, price, 1)
p = np.poly1d(z)
plt.plot(area, p(area), "r--", alpha=0.8, linewidth=2, label='Тренд')
plt.legend()

plt.tight_layout()
plt.show()

print("✓ Диаграмма рассеяния показана")

# ==========================================
# 8. PIE CHART (КРУГОВАЯ ДИАГРАММА)
# ==========================================

print("\n8. Pie Chart (круговая диаграмма):")

# Доли рынка
labels = ['Компания A', 'Компания B', 'Компания C', 'Компания D', 'Другие']
sizes = [35, 25, 20, 12, 8]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
explode = (0.1, 0, 0, 0, 0)  # "Выдвинуть" первый сектор

plt.figure(figsize=(10, 8))
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)

plt.title('Доли рынка', fontsize=16, fontweight='bold')
plt.axis('equal')  # Равные пропорции = круг

plt.tight_layout()
plt.show()

print("✓ Круговая диаграмма показана")

print("\n" + "="*60)
print("ИТОГИ:")
print("="*60)
print("""
Типы графиков:

1. Line Plot - тренды, временные ряды
   plt.plot(x, y)

2. Bar Chart - сравнение категорий
   plt.bar(x, y)
   plt.barh(x, y) - горизонтальная

3. Grouped - сравнение групп
   Несколько plt.bar() с разными x

4. Stacked - части целого
   plt.bar() с параметром bottom

5. Histogram - распределение
   plt.hist(data, bins=30)

6. Scatter - связь переменных
   plt.scatter(x, y)

7. Pie Chart - доли
   plt.pie(sizes, labels=labels)

Когда использовать:
- Line: время, тренды
- Bar: категории, сравнение
- Histogram: распределение значений
- Scatter: корреляция
- Pie: проценты, доли
""")