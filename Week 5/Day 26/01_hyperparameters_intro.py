import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

sns.set_theme()
np.random.seed(42)

print("="*60)
print("ГИПЕРПАРАМЕТРЫ - Что это и зачем?")
print("="*60)

print("""
      
      ДВА ТИПА НАСТРОЕК МОДЕЛИ:

1. ПАРАМЕТРЫ (автоматические):
   - Модель находит САМА при обучении
   - model.coef_, model.intercept_
   - Мы их НЕ трогаем

2. ГИПЕРПАРАМЕТРЫ (ручные):
   - МЫ задаём ДО обучения
   - max_depth, n_estimators, learning_rate
   - Мы их ВЫБИРАЕМ

АНАЛОГИЯ - Приготовление пирога:

Рецепт (гиперпараметры):
- Температура духовки: 180°C    ← МЫ выбираем
- Время выпечки: 40 минут       ← МЫ выбираем

Процесс (параметры):
- Как поднимается тесто         ← происходит САМО
- Как образуется корочка        ← происходит САМО

ПРИМЕРЫ Random Forest:
n_estimators - сколько деревьев (50? 100? 200?)
max_depth - глубина деревьев (5? 10? 20?)
min_samples_split - минимум для разделения (2? 5? 10?)

ОТ ВЫБОРА ЗАВИСИТ КАЧЕСТВО МОДЕЛИ!
""")

print("\n" + "="*60)
print("Создаём тестовые данные")
print("="*60)

X, y = make_regression(
    n_samples=500,      # 500 примеров
    n_features=10,      # 10 признаков
    noise=20,           # шум
    random_state=42
)
"""
make_regression - создаёт искусственные данные для регрессии

n_samples - количество примеров
n_features - количество признаков
noise - уровень шума (чем больше, тем сложнее задача)
"""

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"✓ Train: {len(X_train)} примеров")
print(f"✓ Test: {len(X_test)} примеров")


print("\n" + "="*60)
print("ЭКСПЕРИМЕНТ 1: Влияние количества деревьев")
print("="*60)

n_estimators_values = [10, 50, 100, 200, 300]


"""
n_estimators = количество деревьев в лесу

Мало деревьев (10) = быстро, но неточно
Много деревьев (300) = медленно, но точнее
"""

scores_estimators = []

print("\nТестируем разное количество деревьев:")

for n in n_estimators_values:
    model = RandomForestRegressor(
        n_estimators = n,
        max_depth=10,
        random_state=42
    )

    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    scores_estimators.append(score)
    
    print(f"  n_estimators={n:3d} → R² = {score:.4f}")


print("\n" + "="*60)
print("ЭКСПЕРИМЕНТ 2: Влияние глубины деревьев")
print("="*60)

max_depth_values = [3, 5, 10, 15, 20, None]
"""
max_depth = максимальная глубина деревьев

Маленькая (3) = простые деревья, может недообучиться
Большая (20) = сложные деревья, может переобучиться
None = без ограничений (опасно - переобучение!)
"""

scores_depth = []

print("\nТестируем разную глубину:")
for depth in max_depth_values:
    model = RandomForestRegressor(
        n_estimators=100,     # ← фиксируем этот параметр
        max_depth=depth,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    scores_depth.append(score)
    
    depth_str = str(depth) if depth is not None else "None"
    print(f"  max_depth={depth_str:5s} → R² = {score:.4f}")




print("\n" + "="*60)
print("ЭКСПЕРИМЕНТ 3: Влияние min_samples_split")
print("="*60)

min_samples_values = [2, 5, 10, 20, 50]
"""
min_samples_split = минимум примеров для разделения узла

Маленькое (2) = дерево делится всегда → переобучение
Большое (50) = дерево делится редко → недообучение

По умолчанию = 2
"""

scores_samples = []

print("\nТестируем разные min_samples_split:")
for min_s in min_samples_values:
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=min_s,    # ← изменяем этот параметр
        random_state=42
    )
    
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    scores_samples.append(score)
    
    print(f"  min_samples_split={min_s:2d} → R² = {score:.4f}")    


print("\n" + "="*60)
print("Визуализируем влияние гиперпараметров")
print("="*60)

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# График 1: n_estimators
axes[0].plot(n_estimators_values, scores_estimators, 
             'bo-', linewidth=2, markersize=10)
axes[0].set_title('Влияние количества деревьев', 
                  fontweight='bold', fontsize=12)
axes[0].set_xlabel('n_estimators')
axes[0].set_ylabel('R² Score')
axes[0].grid(True, alpha=0.3)
axes[0].axhline(y=max(scores_estimators), color='r', 
                linestyle='--', alpha=0.5)

# График 2: max_depth
depth_labels = [str(d) if d is not None else "None" for d in max_depth_values]
axes[1].plot(range(len(max_depth_values)), scores_depth, 
             'go-', linewidth=2, markersize=10)
axes[1].set_xticks(range(len(max_depth_values)))
axes[1].set_xticklabels(depth_labels)
axes[1].set_title('Влияние глубины деревьев', 
                  fontweight='bold', fontsize=12)
axes[1].set_xlabel('max_depth')
axes[1].set_ylabel('R² Score')
axes[1].grid(True, alpha=0.3)
axes[1].axhline(y=max(scores_depth), color='r', 
                linestyle='--', alpha=0.5)

# График 3: min_samples_split
axes[2].plot(min_samples_values, scores_samples, 
             'mo-', linewidth=2, markersize=10)
axes[2].set_title('Влияние min_samples_split', 
                  fontweight='bold', fontsize=12)
axes[2].set_xlabel('min_samples_split')
axes[2].set_ylabel('R² Score')
axes[2].grid(True, alpha=0.3)
axes[2].axhline(y=max(scores_samples), color='r', 
                linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()


print("\n" + "="*60)
print("ЛУЧШИЕ ЗНАЧЕНИЯ:")
print("="*60)

best_n_estimators = n_estimators_values[np.argmax(scores_estimators)]
best_max_depth = max_depth_values[np.argmax(scores_depth)]
best_min_samples = min_samples_values[np.argmax(scores_samples)]

print(f"\nЛучший n_estimators: {best_n_estimators}")
print(f"Лучший max_depth: {best_max_depth}")
print(f"Лучший min_samples_split: {best_min_samples}")

# Обучить модель с лучшими параметрами
print("\nОбучаем модель с лучшими параметрами...")
best_model = RandomForestRegressor(
    n_estimators=best_n_estimators,
    max_depth=best_max_depth,
    min_samples_split=best_min_samples,
    random_state=42
)

best_model.fit(X_train, y_train)
best_score = best_model.score(X_test, y_test)

print(f"R² с лучшими параметрами: {best_score:.4f}")

# Сравнить с параметрами по умолчанию
default_model = RandomForestRegressor(random_state=42)
default_model.fit(X_train, y_train)
default_score = default_model.score(X_test, y_test)

print(f"R² с параметрами по умолчанию: {default_score:.4f}")

улучшение = ((best_score - default_score) / abs(default_score)) * 100
print(f"\nУлучшение: {улучшение:.2f}%")

# ============================================
# РЕЗЮМЕ
# ============================================

print("\n" + "="*60)
print("РЕЗЮМЕ:")
print("="*60)

print(f"""
ГИПЕРПАРАМЕТРЫ = настройки модели, которые МЫ выбираем

ОСНОВНЫЕ ДЛЯ RANDOM FOREST:
1. n_estimators - количество деревьев
   - Больше = точнее, но медленнее
   - Обычно: 100-300

2. max_depth - глубина деревьев
   - Маленькая = недообучение
   - Большая = переобучение
   - Обычно: 5-15

3. min_samples_split - минимум для разделения
   - Маленькое = переобучение
   - Большое = недообучение
   - Обычно: 2-10

РЕЗУЛЬТАТЫ ЭКСПЕРИМЕНТА:
Лучшие параметры:
- n_estimators: {best_n_estimators}
- max_depth: {best_max_depth}
- min_samples_split: {best_min_samples}

Улучшение: {улучшение:.2f}%

ПРОБЛЕМА:
Перебирать ВСЕ комбинации вручную = долго!

РЕШЕНИЕ:
GridSearchCV и RandomizedSearchCV
(изучим в следующих файлах)
""")

print("\n Введение в гиперпараметры завершено!")
print("="*60)