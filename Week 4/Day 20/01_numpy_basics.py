# 01_numpy_basics.py - Основы NumPy

import numpy as np

print("="*60)
print("ОСНОВЫ NumPy")
print("="*60)

# ==========================================
# ЧТО ТАКОЕ МАССИВ
# ==========================================

print("\n1. Что такое массив NumPy:")

# Python список
python_list = [1, 2, 3, 4, 5]
print(f"Python список: {python_list}")
print(f"Тип: {type(python_list)}")

# NumPy массив
numpy_array = np.array([1, 2, 3, 4, 5])
print(f"\nNumPy массив: {numpy_array}")
print(f"Тип: {type(numpy_array)}")
print(f"dtype (тип данных): {numpy_array.dtype}")
"""
dtype - тип данных элементов массива

int32/int64 - целые числа
float32/float64 - дробные числа
bool - булевы значения
object - объекты Python
"""

# ==========================================
# СОЗДАНИЕ МАССИВОВ
# ==========================================

print("\n" + "="*60)
print("2. Создание массивов:")
print("="*60)

# Из списка
arr1 = np.array([1, 2, 3, 4, 5])
print(f"\nИз списка: {arr1}")

# Из вложенного списка (2D массив)
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print(f"\n2D массив:\n{arr2d}")

# Нули
zeros = np.zeros(5)
print(f"\nНули: {zeros}")

zeros_2d = np.zeros((3, 4))  # 3 строки, 4 столбца
print(f"\nНули 2D:\n{zeros_2d}")

# Единицы
ones = np.ones(5)
print(f"\nЕдиницы: {ones}")

# Заполнить значением
full = np.full(5, 7)
print(f"\nЗаполнить 7: {full}")

# Диапазон (arange)
range_arr = np.arange(0, 10)
print(f"\narange(0, 10): {range_arr}")

range_arr2 = np.arange(0, 10, 2)  # с шагом 2
print(f"arange(0, 10, 2): {range_arr2}")

# Равномерно распределённые числа (linspace)
linspace_arr = np.linspace(0, 1, 5)
print(f"\nlinspace(0, 1, 5): {linspace_arr}")
"""
linspace(start, stop, num):
Создаёт num чисел равномерно от start до stop
"""

# Случайные числа
random_arr = np.random.rand(5)
print(f"\nСлучайные [0, 1): {random_arr}")

random_int = np.random.randint(0, 10, size=5)
print(f"Случайные целые [0, 10): {random_int}")

# Единичная матрица
identity = np.eye(3)
print(f"\nЕдиничная матрица:\n{identity}")

# ==========================================
# СВОЙСТВА МАССИВОВ
# ==========================================

print("\n" + "="*60)
print("3. Свойства массивов:")
print("="*60)

arr = np.array([[1, 2, 3, 4], 
                [5, 6, 7, 8]])

print(f"\nМассив:\n{arr}")
print(f"shape (форма): {arr.shape}")  # (2, 4) = 2 строки, 4 столбца
print(f"ndim (размерность): {arr.ndim}")  # 2 - двумерный
print(f"size (размер): {arr.size}")  # 8 элементов
print(f"dtype (тип данных): {arr.dtype}")

# ==========================================
# МАТЕМАТИЧЕСКИЕ ОПЕРАЦИИ
# ==========================================

print("\n" + "="*60)
print("4. Математические операции:")
print("="*60)

a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

print(f"\na = {a}")
print(f"b = {b}")

# Сложение
print(f"\na + b = {a + b}")

# Вычитание
print(f"a - b = {a - b}")

# Умножение (поэлементное)
print(f"a * b = {a * b}")

# Деление
print(f"b / a = {b / a}")

# Степень
print(f"a ** 2 = {a ** 2}")

# Операции со скаляром
print(f"\na + 10 = {a + 10}")
print(f"a * 2 = {a * 2}")

# Математические функции
print(f"\nnp.sqrt(a) = {np.sqrt(a)}")
print(f"np.exp(a) = {np.exp(a)}")
print(f"np.log(a) = {np.log(a)}")
print(f"np.sin(a) = {np.sin(a)}")

# ==========================================
# АГРЕГАТНЫЕ ФУНКЦИИ
# ==========================================

print("\n" + "="*60)
print("5. Агрегатные функции:")
print("="*60)

arr = np.array([1, 2, 3, 4, 5])
print(f"\nМассив: {arr}")

print(f"sum (сумма): {np.sum(arr)}")
print(f"mean (среднее): {np.mean(arr)}")
print(f"median (медиана): {np.median(arr)}")
print(f"std (стандартное отклонение): {np.std(arr)}")
print(f"min (минимум): {np.min(arr)}")
print(f"max (максимум): {np.max(arr)}")
print(f"argmin (индекс минимума): {np.argmin(arr)}")
print(f"argmax (индекс максимума): {np.argmax(arr)}")

# Для 2D массивов
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6]])

print(f"\n2D массив:\n{arr2d}")
print(f"Сумма всех: {np.sum(arr2d)}")
print(f"Сумма по строкам (axis=0): {np.sum(arr2d, axis=0)}")
print(f"Сумма по столбцам (axis=1): {np.sum(arr2d, axis=1)}")
"""
axis=0 - операция вдоль строк (по столбцам)
axis=1 - операция вдоль столбцов (по строкам)

[[1, 2, 3],
 [4, 5, 6]]

axis=0: [1+4, 2+5, 3+6] = [5, 7, 9]
axis=1: [1+2+3, 4+5+6] = [6, 15]
"""

# ==========================================
# СРАВНЕНИЕ С PYTHON СПИСКАМИ
# ==========================================

print("\n" + "="*60)
print("6. NumPy vs Python списки:")
print("="*60)

import time

# Python списки
python_list = list(range(1000000))
start = time.time()
result_list = [x * 2 for x in python_list]
python_time = time.time() - start

# NumPy массив
numpy_array = np.arange(1000000)
start = time.time()
result_numpy = numpy_array * 2
numpy_time = time.time() - start

print(f"\nПython список: {python_time:.4f} секунд")
print(f"NumPy массив: {numpy_time:.4f} секунд")
print(f"NumPy быстрее в {python_time / numpy_time:.1f} раз!")

print("\n" + "="*60)
print("ИТОГИ:")
print("="*60)
print("""

Ключевые функции:
- np.array() - создать массив
- np.zeros(), np.ones() - массивы из нулей/единиц
- np.arange() - диапазон чисел
- np.linspace() - равномерное распределение
- np.random - случайные числа
- np.sum(), np.mean(), np.std() - агрегация
""")