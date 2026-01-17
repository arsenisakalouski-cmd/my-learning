# 04_cross_validation.py - Кросс-валидация

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

sns.set_theme()
np.random.seed(42)

print("="*60)
print("CROSS-VALIDATION - Кросс-валидация")
print("="*60)

# ============================================
# ЧТО ТАКОЕ CROSS-VALIDATION?
# ============================================

print("""
╔════════════════════════════════════════════════╗
║       ЧТО ТАКОЕ CROSS-VALIDATION?             ║
╚════════════════════════════════════════════════╝

ПРОБЛЕМА обычного train/test:

Данные: [1,2,3,4,5,6,7,8,9,10]
Train: [1,2,3,4,5,6,7,8]  ← учимся
Test:  [9,10]              ← проверяем

❌ Что если 9,10 случайно "лёгкие"?
❌ Что если 9,10 случайно "сложные"?
   → Оценка качества НЕТОЧНАЯ!

РЕШЕНИЕ - Cross-Validation (K-Fold):

Делим данные на K частей (обычно K=5)

Fold 1: [TEST][train][train][train][train]
Fold 2: [train][TEST][train][train][train]
Fold 3: [train][train][TEST][train][train]
Fold 4: [train][train][train][TEST][train]
Fold 5: [train][train][train][train][TEST]

Каждый раз:
- Обучаем на 4 частях
- Тестируем на 1 части
→ Получаем 5 оценок
→ Усредняем = ТОЧНАЯ оценка!

ПРЕИМУЩЕСТВА:
✓ Более надёжная оценка качества
✓ Используем ВСЕ данные для теста
✓ Видим стабильность модели
""")

# ============================================
# СОЗДАНИЕ ДАННЫХ
# ============================================

print("\n" + "="*60)
print("Создаём данные")
print("="*60)

# Простые данные
X = np.random.rand(100, 1) * 10
y = 2 * X.ravel() + 1 + np.random.normal(0, 1, 100)

print(f"Данных: {len(X)} примеров")

# ============================================
# МЕТОД 1: Обычный train/test
# ============================================

print("\n" + "="*60)
print("МЕТОД 1: Обычный train/test split")
print("="*60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
"""
Обычное разделение:
80% train + 20% test = ОДНА оценка
"""

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
score_simple = model.score(X_test, y_test)

print(f"R² (один тест): {score_simple:.3f}")
print("⚠️ Это ОДНА оценка - может быть неточной!")

# ============================================
# МЕТОД 2: Cross-Validation
# ============================================

print("\n" + "="*60)
print("МЕТОД 2: Cross-Validation (5-Fold)")
print("="*60)

model = RandomForestRegressor(n_estimators=100, random_state=42)

scores_cv = cross_val_score(
    model,           # ← модель
    X, y,            # ← ВСЕ данные (не делим заранее!)
    cv=5,            # ← количество fold'ов (обычно 5 или 10)
    scoring='r2'     # ← метрика ('r2', 'neg_mean_squared_error', 'accuracy')                                                 
)
"""
cross_val_score делает всё автоматически:
1. Делит данные на 5 частей
2. Обучает 5 раз (каждый раз на 4 частях)
3. Тестирует 5 раз (каждый раз на 1 части)
4. Возвращает 5 оценок

cv=5 означает:
Каждая часть = 20% данных
Train = 80%, Test = 20% (но каждый раз разные части!)

scoring='r2':
- Для регрессии: 'r2', 'neg_mean_squared_error'
- Для классификации: 'accuracy', 'f1', 'precision', 'recall'
"""

print("\nРезультаты 5 тестов:")
for i, score in enumerate(scores_cv, 1):
    print(f"  Fold {i}: R² = {score:.3f}")

print(f"\nСреднее: {scores_cv.mean():.3f}")
print(f"Разброс (std): {scores_cv.std():.3f}")
"""
mean() - среднее всех оценок = финальная оценка
std() - стандартное отклонение = насколько стабильна модель

std маленький = стабильная модель
std большой = нестабильная модель
"""

print(f"\n✓ Более надёжная оценка: {scores_cv.mean():.3f} ± {scores_cv.std():.3f}")

# ============================================
# СРАВНЕНИЕ МОДЕЛЕЙ с CV
# ============================================

print("\n" + "="*60)
print("СРАВНЕНИЕ МОДЕЛЕЙ через Cross-Validation")
print("="*60)

# Тестируем 3 модели
models = {
    'Linear Regression': LinearRegression(),
    'Decision Tree': DecisionTreeRegressor(max_depth=5, random_state=42),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
}

results = {}

for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5, scoring='r2')
    results[name] = {
        'scores': scores,
        'mean': scores.mean(),
        'std': scores.std()
    }
    
    print(f"\n{name}:")
    print(f"  Среднее R²: {scores.mean():.3f}")
    print(f"  Разброс:    {scores.std():.3f}")
    print(f"  Все fold'ы: {[f'{s:.3f}' for s in scores]}")

# Лучшая модель
best_model = max(results, key=lambda x: results[x]['mean'])
print(f"\n🏆 Лучшая модель: {best_model}")

# ============================================
# ВИЗУАЛИЗАЦИЯ
# ============================================

print("\nВизуализируем результаты...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# График 1: Сравнение моделей
names = list(results.keys())
means = [results[name]['mean'] for name in names]
stds = [results[name]['std'] for name in names]

axes[0].bar(names, means, yerr=stds, capsize=10, 
            color=['red', 'orange', 'green'], alpha=0.7)
"""
yerr=stds - усы показывают разброс
capsize=10 - размер "шапочки" на усах
"""

axes[0].set_title('📊 Сравнение моделей (Cross-Validation)', 
                  fontweight='bold', fontsize=14)
axes[0].set_ylabel('R² Score')
axes[0].set_ylim(0, 1)
axes[0].grid(True, alpha=0.3, axis='y')

# Добавить значения
for i, (m, s) in enumerate(zip(means, stds)):
    axes[0].text(i, m + s + 0.05, f'{m:.3f}±{s:.3f}', 
                 ha='center', fontweight='bold')

# График 2: Детали для каждой модели
positions = []
labels = []
all_scores = []

for i, (name, data) in enumerate(results.items()):
    scores = data['scores']
    pos = np.random.normal(i, 0.04, len(scores))  # Разброс точек
    axes[1].scatter(pos, scores, alpha=0.6, s=100)
    positions.append(i)
    labels.append(name)
    all_scores.append(scores)

axes[1].boxplot(all_scores, positions=positions)
"""
boxplot - ящик с усами для каждой модели
Показывает: медиану, квартили, выбросы
"""

axes[1].set_xticks(positions)
axes[1].set_xticklabels(labels, rotation=15, ha='right')
axes[1].set_title('📈 Распределение результатов по fold\'ам', 
                  fontweight='bold', fontsize=14)
axes[1].set_ylabel('R² Score')
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# ============================================
# НАСТРОЙКА K-Fold
# ============================================

print("\n" + "="*60)
print("Влияние количества fold'ов")
print("="*60)

model = RandomForestRegressor(n_estimators=100, random_state=42)

k_values = [3, 5, 10, 20]
"""
Обычные значения K:
- K=5: стандарт (80% train, 20% test)
- K=10: более точная оценка, но медленнее
- K=3: быстрее, но менее точно
- K=len(data): Leave-One-Out (очень медленно!)

Выбор K:
- Мало данных (<100) → K=5
- Средне данных (100-1000) → K=5 или K=10
- Много данных (>1000) → K=3 или K=5
"""

print("\nТестируем разные K:")
for k in k_values:
    scores = cross_val_score(model, X, y, cv=k, scoring='r2')
    print(f"  K={k:2d}: mean={scores.mean():.3f}, std={scores.std():.3f}")

# ============================================
# РЕЗЮМЕ
# ============================================

print("\n" + "="*60)
print("РЕЗЮМЕ - CROSS-VALIDATION:")
print("="*60)

print(f"""
ЧТО ТАКОЕ:
Многократное тестирование на разных частях данных

КАК РАБОТАЕТ:
1. Делим данные на K частей
2. K раз обучаем и тестируем
3. Усредняем результаты

ПРЕИМУЩЕСТВА:
✓ Более надёжная оценка
✓ Используем все данные
✓ Видим стабильность модели

КОД:
from sklearn.model_selection import cross_val_score

scores = cross_val_score(
    model,           # модель
    X, y,            # данные
    cv=5,            # количество fold'ов
    scoring='r2'     # метрика
)

mean = scores.mean()    # средняя оценка
std = scores.std()      # разброс

КОГДА ИСПОЛЬЗОВАТЬ:
✓ Мало данных (<1000)
✓ Нужна точная оценка
✓ Сравнение моделей

СТАНДАРТНЫЕ ЗНАЧЕНИЯ:
cv=5  - обычно достаточно
cv=10 - для большей точности

РЕЗУЛЬТАТЫ СЕГОДНЯ:
Лучшая модель: {best_model}
Оценка: {results[best_model]['mean']:.3f} ± {results[best_model]['std']:.3f}
""")

print("\n Cross-Validation освоен!")
print("="*60)