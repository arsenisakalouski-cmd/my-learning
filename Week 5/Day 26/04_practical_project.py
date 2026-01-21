import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from scipy.stats import randint

sns.set_theme()
np.random.seed(42)

print("="*60)
print("ПРАКТИЧЕСКИЙ ПРОЕКТ: Предсказание цен домов")
print("="*60)


print("\n" + "="*60)
print("ШАГ 1: Загрузка данных")
print("="*60)

# Загрузить датасет
housing = fetch_california_housing()
"""
fetch_california_housing() - загружает датасет из sklearn
20640 примеров (районов Калифорнии)
8 признаков
"""

X = housing.data
y = housing.target
feature_names = housing.feature_names

print(f"\n✓ Загружено {X.shape[0]} примеров")
print(f"✓ Признаков: {X.shape[1]}")
print(f"\nПризнаки: {', '.join(feature_names)}")

# Создать DataFrame для удобства
df = pd.DataFrame(X, columns=feature_names)
df['Price'] = y

print("\nПервые строки:")
print(df.head())

print("\nСтатистика:")
print(df.describe())

print("\n" + "="*60)
print("ШАГ 2: Разделение на train/test")
print("="*60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Train: {len(X_train)} примеров")
print(f"Test: {len(X_test)} примеров")


print("\n" + "="*60)
print("ШАГ 2: Разделение на train/test")
print("="*60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Train: {len(X_train)} примеров")
print(f"Test: {len(X_test)} примеров")

print("\n" + "="*60)
print("ШАГ 3: Базовая модель (параметры по умолчанию)")
print("="*60)

base_model = RandomForestRegressor(random_state=42)
"""
Параметры по умолчанию:
n_estimators=100
max_depth=None (без ограничений)
min_samples_split=2
min_samples_leaf=1
"""

print("Обучаем базовую модель...")
start_time = time.time()
base_model.fit(X_train, y_train)
base_time = time.time() - start_time

y_pred_base = base_model.predict(X_test)

# Метрики
r2_base = r2_score(y_test, y_pred_base)
mae_base = mean_absolute_error(y_test, y_pred_base)
rmse_base = np.sqrt(mean_squared_error(y_test, y_pred_base))

print(f"\n✓ Обучение: {base_time:.1f}с")
print(f"R²: {r2_base:.4f}")
print(f"MAE: ${mae_base:.2f} (в единицах $100k)")
print(f"RMSE: ${rmse_base:.2f}")


print("\n" + "="*60)
print("ШАГ 4: RandomizedSearch (быстрая настройка)")
print("="*60)

param_distributions = {
    'n_estimators': randint(50, 300),
    'max_depth': randint(5, 50),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'max_features': ['sqrt', 'log2', None]
}
"""
max_features - сколько признаков использовать в каждом дереве
'sqrt' - квадратный корень от количества (хорошо по умолчанию)
'log2' - логарифм от количества
None - все признаки
"""

print("\nНастройка RandomizedSearch...")
print(f"Попробуем 30 случайных комбинаций с CV=3")

random_search = RandomizedSearchCV(
    estimator=RandomForestRegressor(random_state=42),
    param_distributions=param_distributions,
    n_iter=30,          # меньше итераций для скорости
    cv=3,               # меньше fold'ов для скорости
    scoring='r2',
    verbose=1,
    random_state=42,
    n_jobs=-1
)

start_time = time.time()
random_search.fit(X_train, y_train)
random_time = time.time() - start_time

y_pred_random = random_search.best_estimator_.predict(X_test)

# Метрики
r2_random = r2_score(y_test, y_pred_random)
mae_random = mean_absolute_error(y_test, y_pred_random)
rmse_random = np.sqrt(mean_squared_error(y_test, y_pred_random))

print(f"\n✓ Поиск: {random_time:.1f}с")
print(f"\nЛучшие параметры:")
for param, value in random_search.best_params_.items():
    print(f"  {param}: {value}")

print(f"\nМетрики:")
print(f"R²: {r2_random:.4f}")
print(f"MAE: ${mae_random:.2f}")
print(f"RMSE: ${rmse_random:.2f}")



print("\n" + "="*60)
print("ШАГ 5: GridSearch (точная настройка вокруг найденного)")
print("="*60)

# Берём параметры из RandomSearch и ищем вокруг них
best_n_est = random_search.best_params_['n_estimators']
best_depth = random_search.best_params_['max_depth']

param_grid = {
    'n_estimators': [
        max(50, best_n_est - 50),
        best_n_est,
        best_n_est + 50
    ],
    'max_depth': [
        max(5, best_depth - 5),
        best_depth,
        min(50, best_depth + 5)
    ],
    'min_samples_split': [2, 5, 10],
    'max_features': ['sqrt', 'log2']
}
"""
Стратегия: точная настройка вокруг найденных параметров
Берём лучшие значения из RandomSearch ± дельта
"""

print(f"\nНастройка GridSearch вокруг:")
print(f"  n_estimators: ~{best_n_est}")
print(f"  max_depth: ~{best_depth}")
print(f"\nКомбинаций: {3 * 3 * 3 * 2} с CV=3")

grid_search = GridSearchCV(
    estimator=RandomForestRegressor(random_state=42),
    param_grid=param_grid,
    cv=3,
    scoring='r2',
    verbose=1,
    n_jobs=-1
)

start_time = time.time()
grid_search.fit(X_train, y_train)
grid_time = time.time() - start_time

y_pred_grid = grid_search.best_estimator_.predict(X_test)

# Метрики
r2_grid = r2_score(y_test, y_pred_grid)
mae_grid = mean_absolute_error(y_test, y_pred_grid)
rmse_grid = np.sqrt(mean_squared_error(y_test, y_pred_grid))

print(f"\n✓ Поиск: {grid_time:.1f}с")
print(f"\nФинальные параметры:")
for param, value in grid_search.best_params_.items():
    print(f"  {param}: {value}")

print(f"\nМетрики:")
print(f"R²: {r2_grid:.4f}")
print(f"MAE: ${mae_grid:.2f}")
print(f"RMSE: ${rmse_grid:.2f}")


print("\n" + "="*60)
print("ШАГ 6: ИТОГОВОЕ СРАВНЕНИЕ")
print("="*60)

comparison = pd.DataFrame({
    'Модель': ['Базовая', 'RandomSearch', 'GridSearch'],
    'Время обучения (с)': [base_time, random_time, grid_time],
    'R²': [r2_base, r2_random, r2_grid],
    'MAE ($100k)': [mae_base, mae_random, mae_grid],
    'RMSE ($100k)': [rmse_base, rmse_random, rmse_grid]
})

print("\n" + comparison.to_string(index=False))

# Улучшение
improve_random = ((r2_random - r2_base) / abs(r2_base)) * 100
improve_grid = ((r2_grid - r2_base) / abs(r2_base)) * 100

print(f"\nУлучшение от RandomSearch: {improve_random:.2f}%")
print(f"Улучшение от GridSearch: {improve_grid:.2f}%")


print("\n" + "="*60)
print("ШАГ 7: Важность признаков (финальная модель)")
print("="*60)

best_model = grid_search.best_estimator_
importances = best_model.feature_importances_
indices = np.argsort(importances)[::-1]

print("\nРейтинг признаков:")
for i, idx in enumerate(indices, 1):
    print(f"{i}. {feature_names[idx]:15s}: {importances[idx]:.3f}")



print("\n" + "="*60)
print("Визуализация результатов")
print("="*60)

fig = plt.figure(figsize=(16, 10))

# График 1: Сравнение R²
ax1 = plt.subplot(2, 3, 1)
models = ['Базовая', 'Random\nSearch', 'Grid\nSearch']
r2_scores = [r2_base, r2_random, r2_grid]
colors = ['gray', 'orange', 'green']

bars = ax1.bar(models, r2_scores, color=colors, alpha=0.7)
ax1.set_title('📊 Сравнение R² Score', fontweight='bold')
ax1.set_ylabel('R² Score')
ax1.grid(True, alpha=0.3, axis='y')

for bar, score in zip(bars, r2_scores):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{score:.4f}', ha='center', va='bottom', fontweight='bold')

# График 2: Время обучения
ax2 = plt.subplot(2, 3, 2)
times = [base_time, random_time, grid_time]

bars = ax2.bar(models, times, color=colors, alpha=0.7)
ax2.set_title('⏱️ Время обучения', fontweight='bold')
ax2.set_ylabel('Секунды')
ax2.grid(True, alpha=0.3, axis='y')

for bar, t in zip(bars, times):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{t:.1f}с', ha='center', va='bottom', fontweight='bold')

# График 3: MAE
ax3 = plt.subplot(2, 3, 3)
maes = [mae_base, mae_random, mae_grid]

bars = ax3.bar(models, maes, color=colors, alpha=0.7)
ax3.set_title('📏 Средняя ошибка (MAE)', fontweight='bold')
ax3.set_ylabel('MAE ($100k)')
ax3.grid(True, alpha=0.3, axis='y')

for bar, mae in zip(bars, maes):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'${mae:.2f}', ha='center', va='bottom', fontweight='bold')

# График 4: Важность признаков
ax4 = plt.subplot(2, 3, 4)
ax4.barh(range(len(feature_names)), importances[indices])
ax4.set_yticks(range(len(feature_names)))
ax4.set_yticklabels([feature_names[i] for i in indices])
ax4.set_title('🔍 Важность признаков', fontweight='bold')
ax4.set_xlabel('Важность')
ax4.grid(True, alpha=0.3, axis='x')

# График 5: Предсказания vs Реальность (лучшая модель)
ax5 = plt.subplot(2, 3, 5)
ax5.scatter(y_test, y_pred_grid, alpha=0.5, s=20)
ax5.plot([y_test.min(), y_test.max()], 
         [y_test.min(), y_test.max()], 
         'r--', linewidth=2, label='Идеал')
ax5.set_title(f'🎯 Предсказания (R²={r2_grid:.4f})', fontweight='bold')
ax5.set_xlabel('Реальная цена ($100k)')
ax5.set_ylabel('Предсказанная цена ($100k)')
ax5.legend()
ax5.grid(True, alpha=0.3)

# График 6: Распределение ошибок
ax6 = plt.subplot(2, 3, 6)
errors = y_test - y_pred_grid
ax6.hist(errors, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
ax6.axvline(x=0, color='red', linestyle='--', linewidth=2)
ax6.set_title('📊 Распределение ошибок', fontweight='bold')
ax6.set_xlabel('Ошибка ($100k)')
ax6.set_ylabel('Частота')
ax6.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
