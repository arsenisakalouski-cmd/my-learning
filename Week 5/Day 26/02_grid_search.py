import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

sns.set_theme()
np.random.seed(42)

print("="*60)
print("GRID SEARCH - Автоматический поиск параметров")
print("="*60)

print("\n" + "="*60)
print("Создаём данные")
print("="*60)

X, y = make_regression(
    n_samples=300,      # меньше данных для скорости
    n_features=10,
    noise=20,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"✓ Train: {len(X_train)}")
print(f"✓ Test: {len(X_test)}")

print("\n" + "="*60)
print("БАЗОВАЯ МОДЕЛЬ (параметры по умолчанию)")
print("="*60)

base_model = RandomForestRegressor(random_state=42)
base_model.fit(X_train, y_train)
base_score = base_model.score(X_test, y_test)

print(f"R² базовой модели: {base_score:.4f}")

# ============================================
# GRID SEARCH - ПРОСТОЙ ПРИМЕР
# ============================================

print("\n" + "="*60)
print("GRID SEARCH - Простой пример")
print("="*60)

# Шаг 1: Создаём сетку параметров
param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [5, 10, 15]
}
"""
param_grid - словарь с параметрами

Ключ = название параметра
Значение = список возможных значений

GridSearch попробует ВСЕ комбинации:
n_estimators=50,  max_depth=5
n_estimators=50,  max_depth=10
n_estimators=50,  max_depth=15
n_estimators=100, max_depth=5
...и так далее
= 3 × 3 = 9 комбинаций
"""

print("\nСетка параметров:")
print(f"  n_estimators: {param_grid['n_estimators']}")
print(f"  max_depth: {param_grid['max_depth']}")
print(f"  Всего комбинаций: {len(param_grid['n_estimators']) * len(param_grid['max_depth'])}")

# Шаг 2: Создаём GridSearchCV
grid_search = GridSearchCV(
    estimator=RandomForestRegressor(random_state=42),  # ← базовая модель
    param_grid=param_grid,                             # ← сетка параметров
    cv=5,                                              # ← кросс-валидация (5 fold)
    scoring='r2',                                      # ← метрика оценки
    verbose=1,                                         # ← показывать прогресс
    n_jobs=-1                                          # ← использовать все процессоры
)
"""
GridSearchCV - главный класс для поиска

estimator - базовая модель (без параметров)
param_grid - что перебирать
cv=5 - для каждой комбинации делает 5-fold CV
scoring - метрика для выбора лучшей
verbose - уровень детализации вывода (0, 1, 2, 3)
n_jobs=-1 - параллельные вычисления (быстрее!)

ВАЖНО:
GridSearch САМ делит данные на train/val внутри!
Мы даём ему только тренировочные данные!
"""

# Шаг 3: Запускаем поиск
print("\nЗапускаем GridSearch...")
print("(это может занять время)")

start_time = time.time()
grid_search.fit(X_train, y_train)
elapsed = time.time() - start_time

print(f"\n✓ Поиск завершён за {elapsed:.1f} секунд")


print("\n" + "="*60)
print("РЕЗУЛЬТАТЫ GRID SEARCH:")
print("="*60)

# Лучшие параметры
best_params = grid_search.best_params_
"""
best_params_ - лучшие найденные параметры
Это словарь: {'n_estimators': 100, 'max_depth': 10}
"""

print("\nЛучшие параметры:")
for param, value in best_params.items():
    print(f"  {param}: {value}")

# Лучший score (на валидации внутри CV)
best_cv_score = grid_search.best_score_
"""
best_score_ - лучший результат на кросс-валидации
Это среднее R² по 5 fold'ам
"""

print(f"\nЛучший CV R²: {best_cv_score:.4f}")

# Лучшая модель
best_model = grid_search.best_estimator_
"""
best_estimator_ - готовая модель с лучшими параметрами
Уже обучена на ВСЕХ тренировочных данных!
Можно сразу использовать для предсказаний!
"""

# Проверить на тестовых данных
test_score = best_model.score(X_test, y_test)
print(f"R² на тесте: {test_score:.4f}")

# Сравнение
print("\n" + "="*60)
print("СРАВНЕНИЕ:")
print("="*60)
print(f"Базовая модель:      {base_score:.4f}")
print(f"После GridSearch:    {test_score:.4f}")

улучшение = ((test_score - base_score) / abs(base_score)) * 100
print(f"Улучшение:           {улучшение:.2f}%")






print("\n" + "="*60)
print("ВСЕ ПРОТЕСТИРОВАННЫЕ КОМБИНАЦИИ:")
print("="*60)

# cv_results_ содержит ВСЮ информацию о поиске
results_df = pd.DataFrame(grid_search.cv_results_)
"""
cv_results_ - детальная информация о ВСЕХ комбинациях

Содержит:
- params - комбинация параметров
- mean_test_score - средний score
- std_test_score - разброс
- rank_test_score - ранг (1 = лучший)
- mean_fit_time - время обучения
"""

# Выбираем важные столбцы
important_cols = [
    'param_n_estimators',
    'param_max_depth',
    'mean_test_score',
    'std_test_score',
    'rank_test_score'
]

results_view = results_df[important_cols].copy()
results_view.columns = ['n_estimators', 'max_depth', 'Mean R²', 'Std R²', 'Rank']

# Сортировать по рангу
results_view = results_view.sort_values('Rank')

print("\nТоп-5 комбинаций:")
print(results_view.head().to_string(index=False))

# ============================================
# GRID SEARCH - РАСШИРЕННЫЙ ПРИМЕР
# ============================================

print("\n" + "="*60)
print("GRID SEARCH - Расширенный (больше параметров)")
print("="*60)

# Более детальная сетка
param_grid_extended = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
"""
Добавили 2 новых параметра:
- min_samples_split - минимум примеров для разделения
- min_samples_leaf - минимум примеров в листе

Комбинаций: 3 × 4 × 3 × 3 = 108 !
С CV=5: 108 × 5 = 540 обучений!
"""

print("\nРасширенная сетка:")
for param, values in param_grid_extended.items():
    print(f"  {param}: {values}")

total_combinations = 1
for values in param_grid_extended.values():
    total_combinations *= len(values)

print(f"\nВсего комбинаций: {total_combinations}")
print(f"С CV=5: {total_combinations * 5} обучений")
print("\nЭто займёт больше времени...")

# Запуск расширенного поиска
grid_search_ext = GridSearchCV(
    estimator=RandomForestRegressor(random_state=42),
    param_grid=param_grid_extended,
    cv=5,
    scoring='r2',
    verbose=1,
    n_jobs=-1
)

start_time = time.time()
grid_search_ext.fit(X_train, y_train)
elapsed = time.time() - start_time

print(f"\n✓ Расширенный поиск завершён за {elapsed:.1f} секунд")

# Результаты
print("\nЛучшие параметры (расширенный поиск):")
for param, value in grid_search_ext.best_params_.items():
    print(f"  {param}: {value}")

ext_test_score = grid_search_ext.best_estimator_.score(X_test, y_test)
print(f"\nR² на тесте: {ext_test_score:.4f}")



# ============================================
# ВИЗУАЛИЗАЦИЯ
# ============================================

print("\n" + "="*60)
print("Визуализируем результаты")
print("="*60)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# График 1: Сравнение подходов
approaches = ['Базовая\nмодель', 'Simple\nGridSearch', 'Extended\nGridSearch']
scores = [base_score, test_score, ext_test_score]
colors = ['gray', 'orange', 'green']

bars = axes[0].bar(approaches, scores, color=colors, alpha=0.7)
axes[0].set_title('📊 Сравнение подходов', fontweight='bold', fontsize=14)
axes[0].set_ylabel('R² Score')
axes[0].set_ylim(min(scores) - 0.05, max(scores) + 0.05)
axes[0].grid(True, alpha=0.3, axis='y')

for bar, score in zip(bars, scores):
    height = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2., height,
                 f'{score:.4f}', ha='center', va='bottom', fontweight='bold')

# График 2: Тепловая карта (простой GridSearch)
pivot_data = results_view.pivot_table(
    values='Mean R²',
    index='max_depth',
    columns='n_estimators'
)

sns.heatmap(pivot_data, annot=True, fmt='.4f', cmap='RdYlGn',
            cbar_kws={'label': 'R² Score'}, ax=axes[1])
axes[1].set_title('🔥 Тепловая карта результатов', fontweight='bold', fontsize=14)
axes[1].set_xlabel('n_estimators')
axes[1].set_ylabel('max_depth')

plt.tight_layout()
plt.show()

# ============================================
# РЕЗЮМЕ
# ============================================

print("\n" + "="*60)
print("РЕЗЮМЕ - GRID SEARCH:")
print("="*60)

print(f"""
ЧТО ТАКОЕ:
GridSearchCV - автоматический перебор ВСЕХ комбинаций параметров

КАК РАБОТАЕТ:
1. Задаём сетку параметров (param_grid)
2. GridSearch пробует каждую комбинацию
3. Для каждой делает Cross-Validation
4. Выбирает лучшую

ПРЕИМУЩЕСТВА:
✓ Автоматически
✓ Использует Cross-Validation
✓ Находит оптимальные параметры
✓ Параллельные вычисления (n_jobs=-1)

НЕДОСТАТКИ:
✗ Медленно для больших сеток
✗ Пробует ВСЕ комбинации (даже плохие)

КОД:
from sklearn.model_selection import GridSearchCV

param_grid = {{
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15]
}}

grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=5,
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

# Лучшие параметры
best_params = grid_search.best_params_

# Лучшая модель
best_model = grid_search.best_estimator_

РЕЗУЛЬТАТЫ СЕГОДНЯ:
Базовая модель:     {base_score:.4f}
Simple GridSearch:  {test_score:.4f}
Extended GridSearch: {ext_test_score:.4f}

Улучшение: {((ext_test_score - base_score) / abs(base_score)) * 100:.2f}%

КОГДА МНОГО КОМБИНАЦИЙ:
Используйте RandomizedSearchCV (следующий файл)
""")

print("\n✅ GridSearchCV освоен!")
print("="*60)