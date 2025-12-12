# 06_numpy_practice.py - Практические задачи

import numpy as np

print("="*60)
print("ПРАКТИЧЕСКИЕ ЗАДАЧИ NumPy")
print("="*60)

# ==========================================
# ЗАДАЧА 1: АНАЛИЗ ОЦЕНОК СТУДЕНТОВ
# ==========================================

print("\n" + "="*60)
print("ЗАДАЧА 1: Анализ оценок студентов")
print("="*60)

# Оценки 5 студентов по 4 предметам
grades = np.array([
    [85, 90, 78, 92],  # Студент 1
    [88, 85, 90, 87],  # Студент 2
    [92, 88, 95, 90],  # Студент 3
    [75, 80, 70, 85],  # Студент 4
    [95, 92, 88, 94]   # Студент 5
])

subjects = ['Математика', 'Физика', 'Химия', 'Биология']

print(f"Оценки:\n{grades}\n")

# Средняя оценка каждого студента
avg_per_student = np.mean(grades, axis=1)
print("Средняя оценка по студентам:")
for i, avg in enumerate(avg_per_student):
    print(f"  Студент {i+1}: {avg:.2f}")

# Средняя оценка по каждому предмету
avg_per_subject = np.mean(grades, axis=0)
print("\nСредняя оценка по предметам:")
for subject, avg in zip(subjects, avg_per_subject):
    print(f"  {subject}: {avg:.2f}")

# Лучший студент
best_student = np.argmax(avg_per_student)
print(f"\nЛучший студент: #{best_student + 1} (средняя {avg_per_student[best_student]:.2f})")

# Самый сложный предмет
hardest_subject = np.argmin(avg_per_subject)
print(f"Самый сложный предмет: {subjects[hardest_subject]} (средняя {avg_per_subject[hardest_subject]:.2f})")

# Студенты с оценкой выше 85
high_achievers = np.sum(grades > 85, axis=1)
print("\nКоличество оценок > 85 у каждого студента:")
for i, count in enumerate(high_achievers):
    print(f"  Студент {i+1}: {count} предметов")

# ==========================================
# ЗАДАЧА 2: ОБРАБОТКА ИЗОБРАЖЕНИЯ
# ==========================================

print("\n" + "="*60)
print("ЗАДАЧА 2: Обработка изображения (симуляция)")
print("="*60)

# Создать "изображение" 10x10 пикселей (значения 0-255)
image = np.random.randint(0, 256, size=(10, 10))
print(f"Оригинальное изображение (10x10):\n{image[:5, :5]}...\n")

# Яркость
brightness = np.mean(image)
print(f"Средняя яркость: {brightness:.2f}")

# Нормализация (0-1)
normalized = image / 255.0
print(f"\nНормализованное (первые 3x3):\n{normalized[:3, :3]}\n")

# Увеличить яркость на 20%
brightened = np.clip(image * 1.2, 0, 255).astype(int)
"""
np.clip(array, min, max) - ограничить значения
"""
print(f"После увеличения яркости:\n{brightened[:3, :3]}\n")

# Инвертировать (негатив)
inverted = 255 - image
print(f"Негатив:\n{inverted[:3, :3]}\n")

# Бинаризация (порог 128)
binary = (image > 128).astype(int)
print(f"Бинарное (порог 128):\n{binary}\n")

# ==========================================
# ЗАДАЧА 3: ФИНАНСОВЫЙ АНАЛИЗ
# ==========================================

print("\n" + "="*60)
print("ЗАДАЧА 3: Финансовый анализ")
print("="*60)

# Цены акций за 10 дней
prices = np.array([100, 102, 105, 103, 107, 110, 108, 112, 115, 113])
print(f"Цены по дням: {prices}")

# Дневные изменения
daily_changes = np.diff(prices)
print(f"\nДневные изменения: {daily_changes}")
"""
np.diff() - разности между соседними элементами
[102-100, 105-102, ...]
"""

# Процентные изменения
pct_changes = (daily_changes / prices[:-1]) * 100
print(f"Процентные изменения: {pct_changes}")
print(f"Средний рост: {np.mean(pct_changes):.2f}%")

# Волатильность (стандартное отклонение изменений)
volatility = np.std(pct_changes)
print(f"Волатильность: {volatility:.2f}%")

# Максимальный рост и падение
max_gain = np.max(daily_changes)
max_loss = np.min(daily_changes)
print(f"\nМаксимальный рост: +{max_gain}")
print(f"Максимальное падение: {max_loss}")

# Скользящее среднее (3 дня)
moving_avg = np.convolve(prices, np.ones(3)/3, mode='valid')
print(f"\nСкользящее среднее (3 дня): {moving_avg}")

# ==========================================
# ЗАДАЧА 4: СТАТИСТИКА ТЕМПЕРАТУР
# ==========================================

print("\n" + "="*60)
print("ЗАДАЧА 4: Статистика температур")
print("="*60)

# Температуры за месяц (30 дней)
np.random.seed(42)
temperatures = np.random.normal(20, 5, 30)  # среднее 20°C, отклонение 5
print(f"Температуры за месяц:\n{temperatures}\n")

# Статистика
print(f"Средняя температура: {np.mean(temperatures):.2f}°C")
print(f"Медиана: {np.median(temperatures):.2f}°C")
print(f"Мин: {np.min(temperatures):.2f}°C")
print(f"Макс: {np.max(temperatures):.2f}°C")
print(f"Диапазон: {np.ptp(temperatures):.2f}°C")
"""
np.ptp() - peak to peak (размах)
max - min
"""

# Стандартное отклонение
std = np.std(temperatures)
print(f"\nСтандартное отклонение: {std:.2f}°C")

# Процентили
p25 = np.percentile(temperatures, 25)
p75 = np.percentile(temperatures, 75)
print(f"25-й процентиль: {p25:.2f}°C")
print(f"75-й процентиль: {p75:.2f}°C")

# Количество дней с температурой выше среднего
above_avg = np.sum(temperatures > np.mean(temperatures))
print(f"\nДней выше среднего: {above_avg}")

# Холодные дни (< 15°C)
cold_days = np.sum(temperatures < 15)
print(f"Холодных дней (< 15°C): {cold_days}")

# ==========================================
# ЗАДАЧА 5: РАССТОЯНИЯ МЕЖДУ ГОРОДАМИ
# ==========================================

print("\n" + "="*60)
print("ЗАДАЧА 5: Расстояния между городами")
print("="*60)

# Координаты городов (x, y)
cities = {
    'A': np.array([0, 0]),
    'B': np.array([3, 4]),
    'C': np.array([6, 0]),
    'D': np.array([3, -2])
}

print("Координаты городов:")
for name, coords in cities.items():
    print(f"  {name}: {coords}")

# Матрица расстояний
city_names = list(cities.keys())
n_cities = len(city_names)
distances = np.zeros((n_cities, n_cities))

for i, city1 in enumerate(city_names):
    for j, city2 in enumerate(city_names):
        if i != j:
            diff = cities[city1] - cities[city2]
            distances[i, j] = np.linalg.norm(diff)

print("\nМатрица расстояний:")
print("     ", "  ".join(city_names))
for i, name in enumerate(city_names):
    row = "  ".join([f"{d:5.2f}" for d in distances[i]])
    print(f"{name}:   {row}")

# Ближайший сосед для каждого города
print("\nБлижайший сосед:")
for i, city in enumerate(city_names):
    # Убрать расстояние до самого себя
    dists = distances[i].copy()
    dists[i] = np.inf
    nearest_idx = np.argmin(dists)
    print(f"  {city} → {city_names[nearest_idx]} ({dists[nearest_idx]:.2f})")

# ==========================================
# ЗАДАЧА 6: ИГРАЛЬНЫЕ КОСТИ
# ==========================================

print("\n" + "="*60)
print("ЗАДАЧА 6: Симуляция бросков костей")
print("="*60)

# Бросить 2 кости 10000 раз
np.random.seed(42)
dice1 = np.random.randint(1, 7, size=10000)
dice2 = np.random.randint(1, 7, size=10000)
sums = dice1 + dice2

print("Бросили 2 кости 10000 раз")

# Частота каждой суммы
for s in range(2, 13):
    count = np.sum(sums == s)
    probability = count / 10000 * 100
    print(f"  Сумма {s:2d}: {count:4d} раз ({probability:5.2f}%)")

# Самая частая сумма
most_common = np.argmax(np.bincount(sums)) 
print(f"\nСамая частая сумма: {most_common}")

# Вероятность выбросить 7 или больше
prob_7_plus = np.sum(sums >= 7) / len(sums) * 100
print(f"Вероятность ≥7: {prob_7_plus:.2f}%")

print("\n" + "="*60)
print("✅ ВСЕ ЗАДАЧИ РЕШЕНЫ!")
print("="*60)