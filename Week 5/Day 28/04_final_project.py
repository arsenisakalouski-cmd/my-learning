
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.metrics import r2_score, mean_absolute_error

sns.set_theme()
np.random.seed(42)

print("="*60)
print("FINALNYY PROEKT: Polnyy Feature Engineering")
print("="*60)

print("""
Задача: Предсказать цену дома

Этапы:
1. Базовая модель (без feature engineering)
2. Создание новых признаков
3. Polynomial features
4. Scaling
5. Сравнение результатов
""")

print("\n" + "="*60)
print("Шаг 1: Создаём данные")
print("="*60)

n = 500

data = {
    'ploshchad': np.random.randint(30, 200, n),
    'komnat': np.random.randint(1, 6, n),
    'etazh': np.random.randint(1, 25, n),
    'god_postroyki': np.random.randint(1970, 2024, n),
    'rasstoyanie_metro': np.random.uniform(0.1, 10, n),
    'rasstoyanie_tsentr': np.random.uniform(1, 30, n)
}

df = pd.DataFrame(data)

# Реальная зависимость (сложная)
tsena = (
    df['ploshchad'] * 150 +
    df['komnat'] * 8000 +
    (df['ploshchad'] / df['komnat']) * 1000 +
    df['etazh'] * 300 +
    (2024 - df['god_postroyki']) * (-500) +
    df['rasstoyanie_metro'] * (-2000) +
    df['rasstoyanie_tsentr'] * (-800) +
    (df['ploshchad'] ** 2) * 0.5 +
    np.random.normal(0, 5000, n)
)

df['tsena'] = tsena

print(f"Создано {len(df)} домов")
print("\nПервые строки:")
print(df.head())


print("\n" + "="*60)
print("Шаг 2: Базовая модель (БЕЗ feature engineering)")
print("="*60)

features_base = ['ploshchad', 'komnat', 'etazh', 'god_postroyki', 
                 'rasstoyanie_metro', 'rasstoyanie_tsentr']

X_base = df[features_base].values
y = df['tsena'].values

X_train_base, X_test_base, y_train, y_test = train_test_split(
    X_base, y, test_size=0.2, random_state=42
)

model_base = RandomForestRegressor(n_estimators=100, random_state=42)
model_base.fit(X_train_base, y_train)

y_pred_base = model_base.predict(X_test_base)
r2_base = r2_score(y_test, y_pred_base)
mae_base = mean_absolute_error(y_test, y_pred_base)

print(f"Базовая модель:")
print(f"  Признаков: {len(features_base)}")
print(f"  R²: {r2_base:.4f}")
print(f"  MAE: {mae_base:.0f}")



print("\n" + "="*60)
print("Шаг 3: Создаём новые признаки")
print("="*60)

df_eng = df.copy()

# 1. Комбинации
df_eng['ploshchad_na_komnatu'] = df_eng['ploshchad'] / df_eng['komnat']
df_eng['ploshchad_x_komnat'] = df_eng['ploshchad'] * df_eng['komnat']

# 2. Возраст
df_eng['vozrast_doma'] = 2024 - df_eng['god_postroyki']

# 3. Логарифмы
df_eng['log_ploshchad'] = np.log1p(df_eng['ploshchad'])
df_eng['log_rasstoyanie_metro'] = np.log1p(df_eng['rasstoyanie_metro'])

# 4. Степени
df_eng['ploshchad_kvadrat'] = df_eng['ploshchad'] ** 2

# 5. Бинарные
df_eng['bolshaya_ploshchad'] = (df_eng['ploshchad'] > 100).astype(int)
df_eng['novostroyka'] = (df_eng['vozrast_doma'] <= 5).astype(int)
df_eng['vysok_etazh'] = (df_eng['etazh'] > 15).astype(int)
df_eng['blizko_metro'] = (df_eng['rasstoyanie_metro'] < 1).astype(int)

# 6. Взаимодействия
df_eng['metro_x_tsentr'] = df_eng['rasstoyanie_metro'] * df_eng['rasstoyanie_tsentr']
df_eng['vozrast_x_etazh'] = df_eng['vozrast_doma'] * df_eng['etazh']

print("Создано новых признаков:")
novye = [col for col in df_eng.columns if col not in df.columns and col != 'tsena']
for i, col in enumerate(novye, 1):
    print(f"  {i}. {col}")

print(f"\nВсего признаков: {len(novye) + len(features_base)}")

print(f"\nВсего признаков: {len(novye) + len(features_base)}")


print("\n" + "="*60)
print("Шаг 4: Модель с новыми признаками")
print("="*60)

features_eng = features_base + novye
X_eng = df_eng[features_eng].values

X_train_eng, X_test_eng, _, _ = train_test_split(
    X_eng, y, test_size=0.2, random_state=42
)

model_eng = RandomForestRegressor(n_estimators=100, random_state=42)
model_eng.fit(X_train_eng, y_train)

y_pred_eng = model_eng.predict(X_test_eng)
r2_eng = r2_score(y_test, y_pred_eng)
mae_eng = mean_absolute_error(y_test, y_pred_eng)

print(f"С новыми признаками:")
print(f"  Признаков: {len(features_eng)}")
print(f"  R²: {r2_eng:.4f}")
print(f"  MAE: {mae_eng:.0f}")



print("\n" + "="*60)
print("Шаг 5: Добавляем Polynomial Features")
print("="*60)

# Берём только важные признаки для polynomial
important_features = ['ploshchad', 'komnat', 'ploshchad_na_komnatu']
X_for_poly = df_eng[important_features].values

poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X_for_poly)

# Объединяем с остальными признаками
other_features = [f for f in features_eng if f not in important_features]
X_other = df_eng[other_features].values

X_combined = np.concatenate([X_poly, X_other], axis=1)

X_train_poly, X_test_poly, _, _ = train_test_split(
    X_combined, y, test_size=0.2, random_state=42
)

model_poly = RandomForestRegressor(n_estimators=100, random_state=42)
model_poly.fit(X_train_poly, y_train)

y_pred_poly = model_poly.predict(X_test_poly)
r2_poly = r2_score(y_test, y_pred_poly)
mae_poly = mean_absolute_error(y_test, y_pred_poly)

print(f"С Polynomial:")
print(f"  Признаков: {X_combined.shape[1]}")
print(f"  R²: {r2_poly:.4f}")
print(f"  MAE: {mae_poly:.0f}")



print("\n" + "="*60)
print("Шаг 6: Добавляем Scaling")
print("="*60)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_poly)
X_test_scaled = scaler.transform(X_test_poly)

model_scaled = RandomForestRegressor(n_estimators=100, random_state=42)
model_scaled.fit(X_train_scaled, y_train)

y_pred_scaled = model_scaled.predict(X_test_scaled)
r2_scaled = r2_score(y_test, y_pred_scaled)
mae_scaled = mean_absolute_error(y_test, y_pred_scaled)

print(f"С Scaling:")
print(f"  R²: {r2_scaled:.4f}")
print(f"  MAE: {mae_scaled:.0f}")

print("""
Примечание: Для Random Forest scaling обычно не улучшает,
но для других моделей (SVM, Neural Networks) критичен!
""")



# ============================================
# SRAVNENIE
# ============================================

print("\n" + "="*60)
print("ИТОГОВОЕ СРАВНЕНИЕ:")
print("="*60)

comparison = pd.DataFrame({
    'Модель': ['Базовая', 'С новыми признаками', 'С Polynomial', 'С Scaling'],
    'Признаков': [len(features_base), len(features_eng), 
                  X_combined.shape[1], X_combined.shape[1]],
    'R²': [r2_base, r2_eng, r2_poly, r2_scaled],
    'MAE': [mae_base, mae_eng, mae_poly, mae_scaled]
})

print("\n" + comparison.to_string(index=False))

uluchshenie = ((r2_poly - r2_base) / abs(r2_base)) * 100
print(f"\nУлучшение от Feature Engineering: {uluchshenie:.1f}%")

# ============================================
# VAZHNOST PRIZNAKOV
# ============================================

print("\n" + "="*60)
print("Важность признаков (топ-10):")
print("="*60)

importances = model_eng.feature_importances_
indices = np.argsort(importances)[::-1][:10]

print("\nТоп-10 самых важных:")
for i, idx in enumerate(indices, 1):
    print(f"  {i}. {features_eng[idx]:30s}: {importances[idx]:.4f}")

# ============================================
# VIZUALIZATSIYA
# ============================================


print("\nВизуализация результатов...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# График 1: Сравнение R²
models = ['Базовая', 'Новые\nпризнаки', 'Polynomial', 'Scaling']
r2_scores = [r2_base, r2_eng, r2_poly, r2_scaled]
colors = ['red', 'orange', 'lightgreen', 'green']

bars = axes[0, 0].bar(range(len(models)), r2_scores, color=colors, alpha=0.7)
axes[0, 0].set_xticks(range(len(models)))
axes[0, 0].set_xticklabels(models)
axes[0, 0].set_title('Сравнение R² Score', fontweight='bold', fontsize=14)
axes[0, 0].set_ylabel('R²')
axes[0, 0].set_ylim(0, 1)
axes[0, 0].grid(True, alpha=0.3, axis='y')

for bar, score in zip(bars, r2_scores):
    height = bar.get_height()
    axes[0, 0].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{score:.3f}', ha='center', fontweight='bold')

# График 2: MAE
mae_scores = [mae_base, mae_eng, mae_poly, mae_scaled]
bars = axes[0, 1].bar(range(len(models)), mae_scores, color=colors, alpha=0.7)
axes[0, 1].set_xticks(range(len(models)))
axes[0, 1].set_xticklabels(models)
axes[0, 1].set_title('Сравнение MAE', fontweight='bold', fontsize=14)
axes[0, 1].set_ylabel('MAE (руб)')
axes[0, 1].grid(True, alpha=0.3, axis='y')

for bar, mae in zip(bars, mae_scores):
    height = bar.get_height()
    axes[0, 1].text(bar.get_x() + bar.get_width()/2., height + 200,
                    f'{mae:.0f}', ha='center', fontweight='bold')

# График 3: Важность признаков (топ-10)
top_features = [features_eng[i] for i in indices]
top_importances = [importances[i] for i in indices]

axes[1, 0].barh(range(10), top_importances, color='skyblue')
axes[1, 0].set_yticks(range(10))
axes[1, 0].set_yticklabels(top_features, fontsize=9)
axes[1, 0].set_title('Топ-10 важных признаков', fontweight='bold', fontsize=14)
axes[1, 0].set_xlabel('Важность')
axes[1, 0].invert_yaxis()
axes[1, 0].grid(True, alpha=0.3, axis='x')

# График 4: Предсказания vs Реальность (лучшая модель)
axes[1, 1].scatter(y_test, y_pred_poly, alpha=0.5, s=30, color='green')
axes[1, 1].plot([y_test.min(), y_test.max()],
                [y_test.min(), y_test.max()],
                'r--', linewidth=2)
axes[1, 1].set_title(f'Лучшая модель (R²={r2_poly:.3f})', 
                     fontweight='bold', fontsize=14)
axes[1, 1].set_xlabel('Реальная цена')
axes[1, 1].set_ylabel('Предсказанная цена')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()