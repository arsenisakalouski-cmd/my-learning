# 03_subplots.py - Субплоты (несколько графиков)

import matplotlib.pyplot as plt
import numpy as np

print("="*60)
print("СУБПЛОТЫ В Matplotlib")
print("="*60)

# ==========================================
# 1. ПРОСТЫЕ СУБПЛОТЫ (2x1)
# ==========================================

print("\n1. Два графика вертикально:")

x = np.linspace(0, 10, 100)

# Создать фигуру с 2 субплотами (2 строки, 1 столбец)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
"""
plt.subplots(nrows, ncols) возвращает:
- fig - фигуру (весь холст)
- ax1, ax2 - оси (отдельные графики)
"""

# Первый график
ax1.plot(x, np.sin(x), 'b-', linewidth=2)
ax1.set_title('Синус', fontsize=14, fontweight='bold')
ax1.set_xlabel('X')
ax1.set_ylabel('sin(X)')
ax1.grid(True, alpha=0.3)

# Второй график
ax2.plot(x, np.cos(x), 'r-', linewidth=2)
ax2.set_title('Косинус', fontsize=14, fontweight='bold')
ax2.set_xlabel('X')
ax2.set_ylabel('cos(X)')
ax2.grid(True, alpha=0.3)

plt.tight_layout()  # Автоматическая настройка отступов
plt.show()

print("✓ Вертикальные субплоты показаны")

# ==========================================
# 2. СУБПЛОТЫ (1x2)
# ==========================================

print("\n2. Два графика горизонтально:")

# 1 строка, 2 столбца
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Данные
categories = ['A', 'B', 'C', 'D', 'E']
values1 = [23, 45, 56, 78, 32]
values2 = [34, 54, 43, 65, 48]

# Левый график - столбчатая
ax1.bar(categories, values1, color='skyblue')
ax1.set_title('Продажи продукта 1', fontsize=14, fontweight='bold')
ax1.set_ylabel('Количество')
ax1.grid(True, alpha=0.3, axis='y')

# Правый график - линейный
ax2.plot(categories, values2, 'ro-', linewidth=2, markersize=8)
ax2.set_title('Продажи продукта 2', fontsize=14, fontweight='bold')
ax2.set_ylabel('Количество')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("✓ Горизонтальные субплоты показаны")

# ==========================================
# 3. СЕТКА 2x2
# ==========================================

print("\n3. Сетка 2x2:")

# 2 строки, 2 столбца
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
"""
((ax1, ax2), (ax3, ax4)) - матрица осей:
ax1  ax2
ax3  ax4
"""

x = np.linspace(0, 10, 100)

# График 1 - синус
ax1.plot(x, np.sin(x), 'b-')
ax1.set_title('sin(x)', fontweight='bold')
ax1.grid(True, alpha=0.3)

# График 2 - косинус
ax2.plot(x, np.cos(x), 'r-')
ax2.set_title('cos(x)', fontweight='bold')
ax2.grid(True, alpha=0.3)

# График 3 - тангенс
ax3.plot(x, np.tan(x), 'g-')
ax3.set_title('tan(x)', fontweight='bold')
ax3.set_ylim(-5, 5)
ax3.grid(True, alpha=0.3)

# График 4 - экспонента
ax4.plot(x, np.exp(x/5), 'm-')
ax4.set_title('exp(x/5)', fontweight='bold')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("✓ Сетка 2x2 показана")

# ==========================================
# 4. ИНДЕКСАЦИЯ СУБПЛОТОВ
# ==========================================

print("\n4. Индексация субплотов:")

# Альтернативный способ - массив осей
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
"""
axes - двумерный массив:
axes[0, 0]  axes[0, 1]  axes[0, 2]
axes[1, 0]  axes[1, 1]  axes[1, 2]
"""

# Заполнить графики
for i in range(2):
    for j in range(3):
        x = np.linspace(0, 10, 100)
        y = np.sin(x + i + j)
        
        axes[i, j].plot(x, y)
        axes[i, j].set_title(f'График [{i}, {j}]', fontweight='bold')
        axes[i, j].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("✓ Индексированные субплоты показаны")

# ==========================================
# 5. НЕРАВНОМЕРНЫЕ СУБПЛОТЫ
# ==========================================

print("\n5. Неравномерные субплоты:")

fig = plt.figure(figsize=(12, 8))

# Большой график сверху (занимает 2 столбца)
ax1 = plt.subplot(2, 2, (1, 2))  # Строка 1, столбцы 1-2
"""
subplot(nrows, ncols, index)
или
subplot(nrows, ncols, (start, end))
"""

# Два маленьких снизу
ax2 = plt.subplot(2, 2, 3)  # Строка 2, столбец 1
ax3 = plt.subplot(2, 2, 4)  # Строка 2, столбец 2

# Данные
months = range(1, 13)
sales = np.random.randint(10000, 50000, 12)

# Большой график - линия продаж
ax1.plot(months, sales, 'b-o', linewidth=2, markersize=6)
ax1.set_title('Продажи за год', fontsize=14, fontweight='bold')
ax1.set_xlabel('Месяц')
ax1.set_ylabel('Продажи')
ax1.grid(True, alpha=0.3)

# Маленький 1 - среднее по кварталам
q1 = sales[:3].mean()
q2 = sales[3:6].mean()
q3 = sales[6:9].mean()
q4 = sales[9:].mean()
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
quarter_sales = [q1, q2, q3, q4]

ax2.bar(quarters, quarter_sales, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
ax2.set_title('По кварталам', fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

# Маленький 2 - распределение
ax3.hist(sales, bins=8, color='skyblue', edgecolor='black')
ax3.set_title('Распределение', fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("✓ Неравномерные субплоты показаны")

# ==========================================
# 6. ОБЩИЕ ПОДПИСИ
# ==========================================

print("\n6. Общие подписи для субплотов:")

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Общий заголовок
fig.suptitle('Анализ функций', fontsize=18, fontweight='bold', y=0.98)

x = np.linspace(0, 10, 100)

# Заполнить
axes[0, 0].plot(x, x, 'r-')
axes[0, 0].set_title('Линейная')

axes[0, 1].plot(x, x**2, 'g-')
axes[0, 1].set_title('Квадратичная')

axes[1, 0].plot(x, np.sqrt(x), 'b-')
axes[1, 0].set_title('Корень')

axes[1, 1].plot(x, np.log(x + 1), 'm-')
axes[1, 1].set_title('Логарифм')

# Общие подписи осей
for ax in axes.flat:
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("✓ Общие подписи показаны")

# ==========================================
# 7. РАЗДЕЛЕНИЕ ОБЩЕЙ ОСИ
# ==========================================

print("\n7. Общая ось X:")

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
"""
sharex=True - все графики используют одну ось X
sharey=True - общая ось Y
"""

x = np.linspace(0, 10, 100)

ax1.plot(x, np.sin(x), 'b-')
ax1.set_title('Синус')
ax1.set_ylabel('sin(x)')
ax1.grid(True, alpha=0.3)

ax2.plot(x, np.cos(x), 'r-')
ax2.set_title('Косинус')
ax2.set_ylabel('cos(x)')
ax2.grid(True, alpha=0.3)

ax3.plot(x, np.sin(x) + np.cos(x), 'g-')
ax3.set_title('Сумма')
ax3.set_xlabel('X')
ax3.set_ylabel('sin(x) + cos(x)')
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("✓ Общая ось X показана")

# ==========================================
# 8. GRIDSPEC (ГИБКАЯ СЕТКА)
# ==========================================

print("\n8. GridSpec - гибкая сетка:")

from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(12, 8))
gs = GridSpec(3, 3, figure=fig)
"""
GridSpec(nrows, ncols) - создаёт гибкую сетку
Можно объединять ячейки
"""

# Большой график - верх (2 строки, 3 столбца)
ax1 = fig.add_subplot(gs[0:2, :])

# Три маленьких - низ
ax2 = fig.add_subplot(gs[2, 0])
ax3 = fig.add_subplot(gs[2, 1])
ax4 = fig.add_subplot(gs[2, 2])

# Данные
x = np.linspace(0, 10, 100)

# Большой
ax1.plot(x, np.sin(x) * np.exp(-x/10), 'b-', linewidth=2)
ax1.set_title('Затухающий синус', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)

# Маленькие
ax2.plot(x, np.sin(x), 'r-')
ax2.set_title('sin(x)')
ax2.grid(True, alpha=0.3)

ax3.plot(x, np.cos(x), 'g-')
ax3.set_title('cos(x)')
ax3.grid(True, alpha=0.3)

ax4.plot(x, np.exp(-x/10), 'm-')
ax4.set_title('exp(-x/10)')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("✓ GridSpec показан")

# ==========================================
# 9. ВСТАВКА ГРАФИКОВ (INSET)
# ==========================================

print("\n9. Вставка графика внутри графика:")

fig, ax = plt.subplots(figsize=(10, 6))

# Основной график
x = np.linspace(0, 10, 1000)
y = np.sin(x)

ax.plot(x, y, 'b-', linewidth=2)
ax.set_title('Основной график', fontsize=14, fontweight='bold')
ax.set_xlabel('X')
ax.set_ylabel('sin(X)')
ax.grid(True, alpha=0.3)

# Создать вставку
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

axins = inset_axes(ax, width="40%", height="30%", loc='upper right')
"""
loc может быть:
'upper right', 'upper left', 'lower left', 'lower right', 'center'
"""

# График во вставке - увеличенная область
x_zoom = np.linspace(3, 4, 100)
y_zoom = np.sin(x_zoom)

axins.plot(x_zoom, y_zoom, 'r-', linewidth=2)
axins.set_title('Увеличение', fontsize=10)
axins.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("✓ Вставка показана")

print("\n" + "="*60)
print("ИТОГИ:")
print("="*60)
print("""
Субплоты:

Создание:
- fig, ax = plt.subplots(nrows, ncols)
- fig, (ax1, ax2) = plt.subplots(1, 2)
- fig, axes = plt.subplots(2, 3) - массив

Доступ:
- ax.plot() - рисовать на оси
- ax.set_title() - заголовок
- ax.set_xlabel/ylabel() - подписи
- axes[i, j] - по индексу

Специальные:
- sharex=True - общая ось X
- sharey=True - общая ось Y
- plt.tight_layout() - автоотступы
- fig.suptitle() - общий заголовок

GridSpec:
- Гибкая сетка
- Объединение ячеек
- gs[start:end, start:end]

Применение:
- Сравнение данных
- Комплексный анализ
- Дашборды
- Отчёты
""")