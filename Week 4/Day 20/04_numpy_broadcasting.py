# 04_numpy_broadcasting.py - Broadcasting (трансляция)

import numpy as np

print("="*60)
print("BROADCASTING В NumPy")
print("="*60)

"""
Broadcasting - автоматическое расширение массивов
для выполнения операций между массивами разных форм
"""

# ==========================================
# ОСНОВЫ BROADCASTING
# ==========================================

print("\n1. Основы Broadcasting:")

# Скаляр + массив
arr = np.array([1, 2, 3, 4])
print(f"arr = {arr}")
print(f"arr + 10 = {arr + 10}")
"""
10 "растягивается" до [10, 10, 10, 10]
"""

# 1D + 1D (одинаковая форма)
arr1 = np.array([1, 2, 3])
arr2 = np.array([10, 20, 30])
print(f"\narr1 = {arr1}")
print(f"arr2 = {arr2}")
print(f"arr1 + arr2 = {arr1 + arr2}")

# ==========================================
# BROADCASTING С РАЗНЫМИ ФОРМАМИ
# ==========================================

print("\n" + "="*60)
print("2. Broadcasting с разными формами:")
print("="*60)

# 2D + 1D
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

arr1d = np.array([10, 20, 30])

print(f"2D массив:\n{arr2d}")
print(f"Форма: {arr2d.shape}")

print(f"\n1D массив: {arr1d}")
print(f"Форма: {arr1d.shape}")

result = arr2d + arr1d
print(f"\n2D + 1D:\n{result}")
"""
arr1d [10, 20, 30] "растягивается" до:
[[10, 20, 30],
 [10, 20, 30],
 [10, 20, 30]]

Каждая строка складывается с [10, 20, 30]
"""

# ==========================================
# ПРАВИЛА BROADCASTING
# ==========================================

print("\n" + "="*60)
print("3. Правила Broadcasting:")
print("="*60)

print("""
Правила:
1. Если массивы имеют разное количество измерений,
   форма с меньшим количеством дополняется 1 слева

2. Размеры сравниваются справа налево

3. Два размера совместимы если они:
   - равны
   - один из них равен 1

4. Если несовместимы - ошибка
""")

# Примеры совместимых форм
print("\nСовместимые формы:")
print("(3, 1) + (3,)     -> (3, 3)  ✓")
print("(3, 4) + (4,)     -> (3, 4)  ✓")
print("(3, 1) + (1, 4)   -> (3, 4)  ✓")
print("(3, 4, 5) + (5,)  -> (3, 4, 5)  ✓")

print("\nНесовместимые формы:")
print("(3,) + (4,)       -> Ошибка  ✗")
print("(3, 2) + (3,)     -> Ошибка  ✗")

# ==========================================
# ПРИМЕРЫ BROADCASTING
# ==========================================

print("\n" + "="*60)
print("4. Примеры Broadcasting:")
print("="*60)

# Пример 1: Столбец + строка
col = np.array([[1], [2], [3]])  # (3, 1)
row = np.array([10, 20, 30])     # (3,)

print(f"Столбец:\n{col}")
print(f"Форма: {col.shape}")

print(f"\nСтрока: {row}")
print(f"Форма: {row.shape}")

result = col + row
print(f"\nСтолбец + строка:\n{result}")
print(f"Форма: {result.shape}")
"""
col (3, 1) "растягивается" до (3, 3)
row (3,) становится (1, 3) затем (3, 3)

[[1],     [10, 20, 30]     [[11, 21, 31],
 [2],  +  [10, 20, 30]  =   [12, 22, 32],
 [3]]     [10, 20, 30]      [13, 23, 33]]
"""

# Пример 2: Нормализация по столбцам
print("\n" + "="*60)
print("5. Практический пример - нормализация:")
print("="*60)

data = np.array([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]])

print(f"Данные:\n{data}")

# Среднее по каждому столбцу
mean = np.mean(data, axis=0)
print(f"\nСреднее по столбцам: {mean}")
print(f"Форма: {mean.shape}")

# Вычесть среднее (broadcasting!)
centered = data - mean
print(f"\nДанные - среднее:\n{centered}")
"""
mean [4, 5, 6] "растягивается" для вычитания
из каждой строки
"""

# Стандартное отклонение
std = np.std(data, axis=0)
print(f"\nStd по столбцам: {std}")

# Нормализация (z-score)
normalized = (data - mean) / std
print(f"\nНормализованные данные:\n{normalized}")

# ==========================================
# BROADCASTING В ВЫЧИСЛЕНИЯХ
# ==========================================

print("\n" + "="*60)
print("6. Broadcasting в вычислениях:")
print("="*60)

# Создать таблицу умножения
x = np.arange(1, 6).reshape(5, 1)  # (5, 1)
y = np.arange(1, 6)                # (5,)

print(f"x:\n{x}")
print(f"y: {y}")

multiplication_table = x * y
print(f"\nТаблица умножения:\n{multiplication_table}")
"""
[[1],      [1, 2, 3, 4, 5]
 [2],   *
 [3],
 [4],
 [5]]

Каждый элемент x умножается на всю строку y
"""

# Расстояния между точками
print("\n" + "="*60)
print("7. Евклидовы расстояния:")
print("="*60)

points = np.array([[0, 0],
                   [1, 1],
                   [2, 2]])

print(f"Точки:\n{points}")

# Расстояния от каждой точки до каждой
# (broadcasting в 3D!)
diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
print(f"\nРазности (форма {diff.shape}):")

distances = np.sqrt(np.sum(diff**2, axis=2))
print(f"\nМатрица расстояний:\n{distances}")
"""
distances[i, j] = расстояние от точки i до точки j

[[0.   , 1.41, 2.83],
 [1.41, 0.  , 1.41],
 [2.83, 1.41, 0.  ]]
"""

# ==========================================
# КОГДА BROADCASTING НЕ РАБОТАЕТ
# ==========================================

print("\n" + "="*60)
print("8. Ошибки Broadcasting:")
print("="*60)

arr1 = np.array([1, 2, 3])      # (3,)
arr2 = np.array([1, 2, 3, 4])   # (4,)

print(f"arr1: {arr1}, форма: {arr1.shape}")
print(f"arr2: {arr2}, форма: {arr2.shape}")

try:
    result = arr1 + arr2
except ValueError as e:
    print(f"\n✗ Ошибка: {e}")
    print("Формы несовместимы!")

# Решение: изменить форму
arr1_reshaped = arr1.reshape(3, 1)  # (3, 1)
arr2_reshaped = arr2.reshape(1, 4)  # (1, 4)

print(f"\narr1_reshaped:\n{arr1_reshaped}, форма: {arr1_reshaped.shape}")
print(f"arr2_reshaped: {arr2_reshaped}, форма: {arr2_reshaped.shape}")

result = arr1_reshaped + arr2_reshaped
print(f"\nРезультат (3, 4):\n{result}")

print("\n" + "="*60)
print("ИТОГИ:")
print("="*60)
