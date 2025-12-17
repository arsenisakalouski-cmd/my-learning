# 01_matplotlib_basics.py - Основы Matplotlib

import matplotlib.pyplot as plt
import numpy as np

print("="*60)
print("ОСНОВЫ Matplotlib")
print("="*60)

# ==========================================
# ПЕРВЫЙ ГРАФИК
# ==========================================

print("\n1. Создание первого графика:")

# Данные
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Создать график
plt.plot(x, y)

# Показать
plt.show()
"""
plt.plot() - создаёт линейный график
plt.show() - отображает окно с графиком

Окно интерактивное:
- Масштабирование
- Перемещение
- Сохранение
"""

print("✓ График показан")

# ==========================================
# С ПОДПИСЯМИ
# ==========================================

print("\n2. График с подписями:")

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.plot(x, y)

# Добавить подписи
plt.title('Мой первый график')
plt.xlabel('Ось X')
plt.ylabel('Ось Y')

plt.show()

print("✓ График с подписями показан")

# ==========================================
# НЕСКОЛЬКО ЛИНИЙ
# ==========================================

print("\n3. Несколько линий на одном графике:")

x = np.linspace(0, 10, 100)
y1 = x
y2 = x ** 2
y3 = x ** 0.5

plt.plot(x, y1, label='Линейная')
plt.plot(x, y2, label='Квадратичная')
plt.plot(x, y3, label='Корень')

plt.title('Различные функции')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()  # Показать легенду
plt.grid(True)  # Сетка

plt.show()

print("✓ График с несколькими линиями показан")

# ==========================================
# СТИЛИ ЛИНИЙ
# ==========================================

print("\n4. Стили линий:")

x = np.linspace(0, 10, 20)

# Разные стили
plt.plot(x, x + 0, linestyle='-', label='Сплошная')
plt.plot(x, x + 1, linestyle='--', label='Пунктир')
plt.plot(x, x + 2, linestyle='-.', label='Штрих-пунктир')
plt.plot(x, x + 3, linestyle=':', label='Точки')

# Или короткая запись
plt.plot(x, x + 4, '-', label='Сплошная (короткая)')
plt.plot(x, x + 5, '--', label='Пунктир (короткая)')

plt.title('Стили линий')
plt.legend()
plt.grid(True)

plt.show()

print("✓ Стили линий показаны")

# ==========================================
# ЦВЕТА
# ==========================================

print("\n5. Цвета линий:")

x = np.linspace(0, 10, 100)

# Базовые цвета (однобуквенные коды)
plt.plot(x, x + 0, 'r', label='Красный (r)')
plt.plot(x, x + 1, 'g', label='Зелёный (g)')
plt.plot(x, x + 2, 'b', label='Синий (b)')
plt.plot(x, x + 3, 'c', label='Голубой (c)')
plt.plot(x, x + 4, 'm', label='Пурпурный (m)')
plt.plot(x, x + 5, 'y', label='Жёлтый (y)')
plt.plot(x, x + 6, 'k', label='Чёрный (k)')

plt.title('Цвета линий')
plt.legend()
plt.grid(True)

plt.show()

print("✓ Цвета показаны")

# ==========================================
# МАРКЕРЫ
# ==========================================

print("\n6. Маркеры:")

x = np.linspace(0, 10, 10)

# Разные маркеры
plt.plot(x, x + 0, 'o', label='Круги (o)')
plt.plot(x, x + 1, 's', label='Квадраты (s)')
plt.plot(x, x + 2, '^', label='Треугольники (^)')
plt.plot(x, x + 3, 'D', label='Ромбы (D)')
plt.plot(x, x + 4, '*', label='Звёзды (*)')
plt.plot(x, x + 5, '+', label='Плюсы (+)')

plt.title('Маркеры')
plt.legend()
plt.grid(True)

plt.show()

print("✓ Маркеры показаны")

# ==========================================
# КОМБИНАЦИЯ: ЦВЕТ + СТИЛЬ + МАРКЕР
# ==========================================

print("\n7. Комбинация стилей:")

x = np.linspace(0, 10, 10)

# Формат: [цвет][маркер][линия]
plt.plot(x, x + 0, 'r-o', label='Красная сплошная с кругами')
plt.plot(x, x + 2, 'g--s', label='Зелёный пунктир с квадратами')
plt.plot(x, x + 4, 'b-.^', label='Синий штрих-пунктир с треугольниками')

plt.title('Комбинированные стили')
plt.legend()
plt.grid(True)

plt.show()

print("✓ Комбинированные стили показаны")

# ==========================================
# РАЗМЕР И ТОЛЩИНА
# ==========================================

print("\n8. Размер и толщина:")

x = np.linspace(0, 10, 100)

# Толщина линий
plt.plot(x, x + 0, linewidth=1, label='Тонкая (1)')
plt.plot(x, x + 2, linewidth=3, label='Средняя (3)')
plt.plot(x, x + 4, linewidth=5, label='Толстая (5)')

plt.title('Толщина линий')
plt.legend()
plt.grid(True)

plt.show()

# Размер маркеров
x = np.linspace(0, 10, 10)

plt.plot(x, x + 0, 'o', markersize=5, label='Маленькие (5)')
plt.plot(x, x + 2, 's', markersize=10, label='Средние (10)')
plt.plot(x, x + 4, '^', markersize=15, label='Большие (15)')

plt.title('Размер маркеров')
plt.legend()
plt.grid(True)

plt.show()

print("✓ Размеры показаны")

# ==========================================
# ПРОЗРАЧНОСТЬ
# ==========================================

print("\n9. Прозрачность (alpha):")

x = np.linspace(0, 10, 100)

plt.plot(x, np.sin(x), linewidth=10, alpha=1.0, label='Непрозрачная (1.0)')
plt.plot(x, np.sin(x + 1), linewidth=10, alpha=0.7, label='Средняя (0.7)')
plt.plot(x, np.sin(x + 2), linewidth=10, alpha=0.3, label='Прозрачная (0.3)')

plt.title('Прозрачность')
plt.legend()
plt.grid(True)

plt.show()

print("✓ Прозрачность показана")

# ==========================================
# ДИАПАЗОНЫ ОСЕЙ
# ==========================================

print("\n10. Настройка диапазонов осей:")

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)

# Установить диапазоны
plt.xlim(0, 10)  # X от 0 до 10
plt.ylim(-1.5, 1.5)  # Y от -1.5 до 1.5

plt.title('Настройка диапазонов')
plt.xlabel('X')
plt.ylabel('sin(X)')
plt.grid(True)

plt.show()

print("✓ Диапазоны показаны")

# ==========================================
# РАЗМЕР ФИГУРЫ
# ==========================================

print("\n11. Размер фигуры:")

x = np.linspace(0, 10, 100)
y = np.sin(x)

# Создать фигуру определённого размера
plt.figure(figsize=(10, 6))  # Ширина 10, высота 6 дюймов
"""
По умолчанию: figsize=(6.4, 4.8)
"""

plt.plot(x, y)
plt.title('Большой график')
plt.xlabel('X')
plt.ylabel('sin(X)')
plt.grid(True)

plt.show()

print("✓ Размер фигуры показан")

print("\n" + "="*60)
print("ИТОГИ:")
print("="*60)
print("""
Основы Matplotlib:

Базовые функции:
- plt.plot(x, y) - линейный график
- plt.show() - показать график
- plt.title() - заголовок
- plt.xlabel(), plt.ylabel() - подписи осей
- plt.legend() - легенда
- plt.grid() - сетка

Стили:
- linestyle: '-', '--', '-.', ':'
- color: 'r', 'g', 'b', 'c', 'm', 'y', 'k'
- marker: 'o', 's', '^', 'D', '*', '+'
- Комбинация: 'r-o', 'g--s', 'b-.^'

Параметры:
- linewidth - толщина линии
- markersize - размер маркера
- alpha - прозрачность (0-1)
- label - название для легенды

Настройка:
- plt.xlim(), plt.ylim() - диапазоны
- plt.figure(figsize=(w, h)) - размер фигуры

Следующий шаг:
- Различные типы графиков
- Субплоты
- Продвинутая настройка
""")
