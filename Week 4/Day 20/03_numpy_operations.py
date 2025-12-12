# 03_numpy_operations.py - Операции с массивами

import numpy as np

print("="*60)
print("ОПЕРАЦИИ С МАССИВАМИ NumPy")
print("="*60)

# ==========================================
# ИЗМЕНЕНИЕ ФОРМЫ (RESHAPE)
# ==========================================

print("\n1. Изменение формы (reshape):")

arr = np.arange(12)
print(f"Исходный массив: {arr}")
print(f"Форма: {arr.shape}")

# Преобразовать в 2D
arr2d = arr.reshape(3, 4)
print(f"\nreshape(3, 4):\n{arr2d}")
print(f"Форма: {arr2d.shape}")

# Преобразовать в 3D
arr3d = arr.reshape(2, 3, 2)
print(f"\nreshape(2, 3, 2):\n{arr3d}")
print(f"Форма: {arr3d.shape}")
"""
(2, 3, 2) = 2 блока по 3 строки по 2 столбца
"""

# Автоматический расчёт одного измерения
arr2d_auto = arr.reshape(3, -1)  # -1 = автоматически (4)
print(f"\nreshape(3, -1):\n{arr2d_auto}")

# Выровнять обратно в 1D
flat = arr2d.flatten()
print(f"\nflatten(): {flat}")

# Или ravel (быстрее, но view)
raveled = arr2d.ravel()
print(f"ravel(): {raveled}")
"""
flatten() - создаёт копию
ravel() - создаёт view (быстрее)
"""

# ==========================================
# ТРАНСПОНИРОВАНИЕ
# ==========================================

print("\n" + "="*60)
print("2. Транспонирование:")
print("="*60)

arr = np.array([[1, 2, 3],
                [4, 5, 6]])

print(f"Исходный массив:\n{arr}")
print(f"Форма: {arr.shape}")

# Транспонировать
transposed = arr.T
print(f"\nТранспонированный:\n{transposed}")
print(f"Форма: {transposed.shape}")
"""
Транспонирование = зеркало по диагонали

[[1, 2, 3],      [[1, 4],
 [4, 5, 6]]  ->   [2, 5],
                   [3, 6]]

Строки становятся столбцами
"""

# ==========================================
# ОБЪЕДИНЕНИЕ МАССИВОВ
# ==========================================

print("\n" + "="*60)
print("3. Объединение массивов:")
print("="*60)

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

print(f"arr1: {arr1}")
print(f"arr2: {arr2}")

# Вертикальное (по строкам)
vstacked = np.vstack([arr1, arr2])
print(f"\nvstack:\n{vstacked}")
"""
[[1, 2, 3],
 [4, 5, 6]]
"""

# Горизонтальное (по столбцам)
hstacked = np.hstack([arr1, arr2])
print(f"\nhstack: {hstacked}")
"""
[1, 2, 3, 4, 5, 6]
"""

# Concatenate (универсальное)
concat = np.concatenate([arr1, arr2])
print(f"\nconcatenate: {concat}")

# Для 2D
arr2d1 = np.array([[1, 2], [3, 4]])
arr2d2 = np.array([[5, 6], [7, 8]])

print(f"\narr2d1:\n{arr2d1}")
print(f"arr2d2:\n{arr2d2}")

# Вертикально (axis=0)
vcat = np.concatenate([arr2d1, arr2d2], axis=0)
print(f"\nconcatenate axis=0:\n{vcat}")
"""
[[1, 2],
 [3, 4],
 [5, 6],
 [7, 8]]
"""

# Горизонтально (axis=1)
hcat = np.concatenate([arr2d1, arr2d2], axis=1)
print(f"\nconcatenate axis=1:\n{hcat}")
"""
[[1, 2, 5, 6],
 [3, 4, 7, 8]]
"""

# ==========================================
# РАЗДЕЛЕНИЕ МАССИВОВ
# ==========================================

print("\n" + "="*60)
print("4. Разделение массивов:")
print("="*60)

arr = np.arange(12)
print(f"Массив: {arr}")

# Разделить на 3 части
split = np.split(arr, 3)
print(f"\nsplit(arr, 3):")
for i, part in enumerate(split):
    print(f"  Часть {i}: {part}")

# Разделить по индексам
split_indices = np.split(arr, [3, 7])
print(f"\nsplit(arr, [3, 7]):")
for i, part in enumerate(split_indices):
    print(f"  Часть {i}: {part}")
"""
Разделить на: arr[:3], arr[3:7], arr[7:]
"""

# Для 2D
arr2d = np.arange(16).reshape(4, 4)
print(f"\n2D массив:\n{arr2d}")

# Разделить горизонтально
hsplit = np.hsplit(arr2d, 2)
print(f"\nhsplit на 2:")
for i, part in enumerate(hsplit):
    print(f"Часть {i}:\n{part}\n")

# Разделить вертикально
vsplit = np.vsplit(arr2d, 2)
print(f"vsplit на 2:")
for i, part in enumerate(vsplit):
    print(f"Часть {i}:\n{part}\n")

# ==========================================
# ДОБАВЛЕНИЕ РАЗМЕРНОСТИ
# ==========================================

print("\n" + "="*60)
print("5. Добавление размерности:")
print("="*60)

arr = np.array([1, 2, 3])
print(f"Исходный: {arr}")
print(f"Форма: {arr.shape}")

# Добавить новую ось
arr_newaxis = arr[np.newaxis, :]
print(f"\narr[np.newaxis, :]: {arr_newaxis}")
print(f"Форма: {arr_newaxis.shape}")
"""
(3,) -> (1, 3)
1D массив стал 2D с одной строкой
"""

arr_newaxis2 = arr[:, np.newaxis]
print(f"\narr[:, np.newaxis]:\n{arr_newaxis2}")
print(f"Форма: {arr_newaxis2.shape}")
"""
(3,) -> (3, 1)
1D массив стал 2D с одним столбцом
"""

# Или через reshape
arr_reshaped = arr.reshape(-1, 1)
print(f"\narr.reshape(-1, 1):\n{arr_reshaped}")

# ==========================================
# ПОВТОРЕНИЕ
# ==========================================

print("\n" + "="*60)
print("6. Повторение элементов:")
print("="*60)

arr = np.array([1, 2, 3])
print(f"Исходный: {arr}")

# Повторить элементы
repeated = np.repeat(arr, 3)
print(f"\nrepeat(arr, 3): {repeated}")
"""
[1, 1, 1, 2, 2, 2, 3, 3, 3]
"""

# Повторить массив целиком
tiled = np.tile(arr, 3)
print(f"tile(arr, 3): {tiled}")
"""
[1, 2, 3, 1, 2, 3, 1, 2, 3]
"""

# Для 2D
arr2d = np.array([[1, 2], [3, 4]])
print(f"\n2D массив:\n{arr2d}")

tiled2d = np.tile(arr2d, (2, 3))
print(f"\ntile(arr2d, (2, 3)):\n{tiled2d}")
"""
Повторить 2 раза по вертикали, 3 раза по горизонтали
"""

# ==========================================
# СОРТИРОВКА
# ==========================================

print("\n" + "="*60)
print("7. Сортировка:")
print("="*60)

arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])
print(f"Исходный: {arr}")

# Отсортировать (создаёт копию)
sorted_arr = np.sort(arr)
print(f"\nnp.sort(arr): {sorted_arr}")
print(f"Исходный не изменился: {arr}")

# Сортировать на месте
arr.sort()
print(f"\nПосле arr.sort(): {arr}")

# Индексы сортировки
arr = np.array([3, 1, 4, 1, 5])
indices = np.argsort(arr)
print(f"\nИсходный: {arr}")
print(f"argsort: {indices}")
print(f"Отсортированный: {arr[indices]}")
"""
argsort возвращает индексы которые отсортируют массив

arr = [3, 1, 4, 1, 5]
indices = [1, 3, 0, 2, 4]

arr[1] = 1 (минимум)
arr[3] = 1
arr[0] = 3
arr[2] = 4
arr[4] = 5 (максимум)
"""

# Для 2D (сортировка по строкам)
arr2d = np.array([[3, 1, 4],
                  [1, 5, 9],
                  [2, 6, 5]])

print(f"\n2D массив:\n{arr2d}")
sorted2d = np.sort(arr2d, axis=1)
print(f"\nОтсортировано по строкам:\n{sorted2d}")

# ==========================================
# УНИКАЛЬНЫЕ ЗНАЧЕНИЯ
# ==========================================

print("\n" + "="*60)
print("8. Уникальные значения:")
print("="*60)

arr = np.array([1, 2, 2, 3, 3, 3, 4, 4, 4, 4])
print(f"Массив: {arr}")

# Уникальные
unique = np.unique(arr)
print(f"\nnp.unique(arr): {unique}")

# С подсчётом
unique, counts = np.unique(arr, return_counts=True)
print(f"\nУникальные: {unique}")
print(f"Количество: {counts}")
for val, count in zip(unique, counts):
    print(f"  {val}: {count} раз")

# ==========================================
# КОПИРОВАНИЕ
# ==========================================

print("\n" + "="*60)
print("9. Копирование массивов:")
print("="*60)

arr = np.array([1, 2, 3, 4, 5])
print(f"Исходный: {arr}")

# Присваивание (НЕ копия!)
arr2 = arr
arr2[0] = 100
print(f"\nПосле arr2[0] = 100:")
print(f"arr: {arr}")
print(f"arr2: {arr2}")
print("⚠️ Оба массива изменились!")

# Срез (view, НЕ копия!)
arr = np.array([1, 2, 3, 4, 5])
arr3 = arr[:]
arr3[0] = 200
print(f"\nПосле среза arr3[0] = 200:")
print(f"arr: {arr}")
print(f"arr3: {arr3}")
print("⚠️ Оба массива изменились!")

# Правильное копирование
arr = np.array([1, 2, 3, 4, 5])
arr4 = arr.copy()
arr4[0] = 300
print(f"\nПосле arr.copy() и arr4[0] = 300:")
print(f"arr: {arr}")
print(f"arr4: {arr4}")
print("✅ Только arr4 изменился!")

print("\n" + "="*60)
print("ИТОГИ:")
print("="*60)
print("""
Изменение формы:
- reshape(shape) - изменить форму
- flatten() - выровнять в 1D (копия)
- ravel() - выровнять в 1D (view)
- T - транспонировать

Объединение:
- vstack() - вертикально
- hstack() - горизонтально
- concatenate() - универсальное

Разделение:
- split() - разделить
- hsplit() - горизонтально
- vsplit() - вертикально

Другое:
- repeat() - повторить элементы
- tile() - повторить массив
- sort() - сортировать
- unique() - уникальные значения
- copy() - создать копию (важно!)
""")