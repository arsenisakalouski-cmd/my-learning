import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from scipy.stats import randint, uniform

sns.set_theme()
np.random.seed(42)

print("="*60)
print("RANDOMIZED SEARCH - Случайный поиск параметров")
print("="*60)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from scipy.stats import randint, uniform

sns.set_theme()
np.random.seed(42)

print("="*60)
print("RANDOMIZED SEARCH - Случайный поиск параметров")
print("="*60)


print("\n" + "="*60)
print("Создаём данные")
print("="*60)

X, y = make_regression(
    n_samples=500,
    n_features=20,      # больше признаков = сложнее
    noise=30,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"✓ Train: {len(X_train)}")
print(f"✓ Test: {len(X_test)}")


print("\n" + "="*60)
print("Настройка распределений параметров")
print("="*60)

param_distributions = {
    'n_estimators': randint(50, 300),           # целые от 50 до 300
    'max_depth': randint(5, 30),                # целые от 5 до 30
    'min_samples_split': randint(2, 20),        # целые от 2 до 20
    'min_samples_leaf': randint(1, 10),         # целые от 1 до 10
    'max_features': uniform(0.1, 0.9)           # дробные от 0.1 до 1.0
}
"""
РАСПРЕДЕЛЕНИЯ:

randint(low, high) - случайное ЦЕЛОЕ число
  randint(50, 300) → может быть 50, 51, 52...299

uniform(low, high) - случайное ДРОБНОЕ число
  uniform(0.1, 0.9) → может быть 0.15, 0.67, 0.82...

ВАЖНО:
Задаём ДИАПАЗОНЫ, а не конкретные значения!
RandomSearch САМ выбирает случайные значения
"""

print("\nРаспределения параметров:")
print("  n_estimators: целые от 50 до 300")
print("  max_depth: целые от 5 до 30")
print("  min_samples_split: целые от 2 до 20")
print("  min_samples_leaf: целые от 1 до 10")
print("  max_features: дробные от 0.1 до 1.0")



print("\n" + "="*60)
print("RANDOMIZED SEARCH (50 итераций)")
print("="*60)

random_search = RandomizedSearchCV(
    estimator=RandomForestRegressor(random_state=42),
    param_distributions=param_distributions,    # ← распределения (не конкретные значения!)
    n_iter=50,                                  # ← сколько комбинаций попробовать
    cv=5,
    scoring='r2',
    verbose=1,
    random_state=42,
    n_jobs=-1
)
"""
n_iter=50 - попробовать 50 СЛУЧАЙНЫХ комбинаций

Вместо 1000+ комбинаций GridSearch
Пробуем только 50 случайных

С CV=5: 50 × 5 = 250 обучений
(вместо 5000+ в GridSearch!)
"""

print("\nЗапускаем RandomizedSearch...")
print(f"Попробуем {random_search.n_iter} случайных комбинаций")

start_time = time.time()
random_search.fit(X_train, y_train)
elapsed_random = time.time() - start_time

print(f"\n✓ Поиск завершён за {elapsed_random:.1f} секунд")

# Результаты
print("\n" + "="*60)
print("РЕЗУЛЬТАТЫ RANDOMIZED SEARCH:")
print("="*60)

print("\nЛучшие параметры:")
for param, value in random_search.best_params_.items():
    if isinstance(value, float):
        print(f"  {param}: {value:.3f}")
    else:
        print(f"  {param}: {value}")

random_score = random_search.best_estimator_.score(X_test, y_test)
print(f"\nR² на тесте: {random_score:.4f}")


print("\n" + "="*60)
print("СРАВНЕНИЕ: GridSearch vs RandomizedSearch")
print("="*60)

# Grid Search (меньшая сетка для сравнения)
param_grid = {
    'n_estimators': [50, 100, 150, 200, 250],
    'max_depth': [5, 10, 15, 20, 25],
    'min_samples_split': [2, 5, 10, 15],
}
"""
GridSearch попробует ВСЕ:
5 × 5 × 4 = 100 комбинаций
С CV=5: 500 обучений
"""

print("\nЗапускаем GridSearch для сравнения...")
print(f"Попробуем {5 * 5 * 4} комбинаций")

grid_search = GridSearchCV(
    estimator=RandomForestRegressor(random_state=42),
    param_grid=param_grid,
    cv=5,
    scoring='r2',
    verbose=1,
    n_jobs=-1
)

start_time = time.time()
grid_search.fit(X_train, y_train)
elapsed_grid = time.time() - start_time

print(f"\n✓ GridSearch завершён за {elapsed_grid:.1f} секунд")

grid_score = grid_search.best_estimator_.score(X_test, y_test)

# Сравнение
print("\n" + "="*60)
print("ИТОГОВОЕ СРАВНЕНИЕ:")
print("="*60)

comparison_data = {
    'Метод': ['RandomizedSearch', 'GridSearch'],
    'Комбинаций': [random_search.n_iter, 5 * 5 * 4],
    'Время (сек)': [elapsed_random, elapsed_grid],
    'R² Score': [random_score, grid_score]
}

df_comparison = pd.DataFrame(comparison_data)
print("\n" + df_comparison.to_string(index=False))

# ============================================
# ВИЗУАЛИЗАЦИЯ
# ============================================

print("\nВизуализируем результаты...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# График 1: Сравнение методов
methods = ['Randomized\nSearch', 'Grid\nSearch']
scores = [random_score, grid_score]
times = [elapsed_random, elapsed_grid]

axes[0, 0].bar(methods, scores, color=['orange', 'blue'], alpha=0.7)
axes[0, 0].set_title('📊 Качество моделей', fontweight='bold')
axes[0, 0].set_ylabel('R² Score')
axes[0, 0].grid(True, alpha=0.3, axis='y')

for i, (m, s) in enumerate(zip(methods, scores)):
    axes[0, 0].text(i, s + 0.01, f'{s:.4f}', 
                    ha='center', fontweight='bold')

# График 2: Время выполнения
axes[0, 1].bar(methods, times, color=['orange', 'blue'], alpha=0.7)
axes[0, 1].set_title('⏱️ Время поиска', fontweight='bold')
axes[0, 1].set_ylabel('Время (секунды)')
axes[0, 1].grid(True, alpha=0.3, axis='y')

for i, (m, t) in enumerate(zip(methods, times)):
    axes[0, 1].text(i, t + 0.5, f'{t:.1f}с', 
                    ha='center', fontweight='bold')

# График 3: Прогресс RandomizedSearch
axes[1, 0].plot(range(len(best_scores_so_far)), best_scores_so_far, 
                'o-', linewidth=2, markersize=4)
axes[1, 0].set_title('📈 Прогресс RandomizedSearch', fontweight='bold')
axes[1, 0].set_xlabel('Итерация')
axes[1, 0].set_ylabel('Лучший R² на данный момент')
axes[1, 0].grid(True, alpha=0.3)

# График 4: Распределение scores
axes[1, 1].hist(results_random['mean_test_score'], bins=20, 
                color='skyblue', edgecolor='black', alpha=0.7)
axes[1, 1].axvline(random_score, color='red', linestyle='--', 
                   linewidth=2, label=f'Лучший: {random_score:.4f}')
axes[1, 1].set_title('📊 Распределение результатов', fontweight='bold')
axes[1, 1].set_xlabel('R² Score')
axes[1, 1].set_ylabel('Частота')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# ============================================
# КОГДА ЧТО ИСПОЛЬЗОВАТЬ
# ============================================

print("\n" + "="*60)
print("КОГДА ЧТО ИСПОЛЬЗОВАТЬ:")
print("="*60)

print("""
GRID SEARCH:
✓ Мало параметров (2-3)
✓ Небольшие диапазоны
✓ Нужен точный результат
✓ Есть время
Пример: настройка финальной модели

RANDOMIZED SEARCH:
✓ Много параметров (4+)
✓ Большие диапазоны
✓ Быстрый поиск
✓ Ограничено время
Пример: первичная настройка, эксперименты

КОМБИНИРОВАННЫЙ ПОДХОД:
1. RandomizedSearch - грубая настройка
2. GridSearch - точная настройка вокруг найденного
""")

# ============================================
# РЕЗЮМЕ
# ============================================

print("\n" + "="*60)
print("РЕЗЮМЕ:")
print("="*60)

print(f"""
RANDOMIZED SEARCH = случайный поиск параметров

ПРЕИМУЩЕСТВА:
✓ Быстрее GridSearch (меньше итераций)
✓ Можно задать широкие диапазоны
✓ Часто находит хорошие параметры
✓ Хорош для начальной настройки

НЕДОСТАТКИ:
✗ Может пропустить лучшую комбинацию
✗ Результаты немного случайны

КОД:
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

param_distributions = {{
    'n_estimators': randint(50, 300),
    'max_depth': randint(5, 30),
    'max_features': uniform(0.1, 0.9)
}}

random_search = RandomizedSearchCV(
    estimator=model,
    param_distributions=param_distributions,
    n_iter=50,              # ← сколько попыток
    cv=5,
    random_state=42,
    n_jobs=-1
)

random_search.fit(X_train, y_train)
best_params = random_search.best_params_

РЕЗУЛЬТАТЫ СЕГОДНЯ:
RandomizedSearch: {random_score:.4f} за {elapsed_random:.1f}с
GridSearch:       {grid_score:.4f} за {elapsed_grid:.1f}с

Скорость: RandomizedSearch в {elapsed_grid/elapsed_random:.1f}x быстрее
Качество: {'Примерно равно' if abs(random_score - grid_score) < 0.01 else 'Разное'}
""")

print("\n RandomizedSearchCV освоен!")
print("="*60)
