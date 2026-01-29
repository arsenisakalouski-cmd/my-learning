import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

sns.set_theme()
np.random.seed(42)

print("="*60)
print("ПРОЕКТ: Очистка грязных данных и ML")
print("="*60)


print("\n" + "="*60)
print("ШАГ 1: Создаём грязный датасет")
print("="*60)

n = 200

data = {
    'age': np.random.randint(20, 60, n),
    'experience': np.random.randint(0, 30, n),
    'education': np.random.choice(['High', 'Bachelor', 'Master'], n),
    'city': np.random.choice(['Moscow', 'SPb', 'Kazan'], n),
    'score': np.random.randint(50, 100, n)
}

# Формула зарплаты (реальная зависимость)
salary = (
    data['age'] * 500 +
    data['experience'] * 2000 +
    data['score'] * 300 +
    np.random.normal(0, 5000, n)
)

data['salary'] = salary

df = pd.DataFrame(data)

# ДОБАВЛЯЕМ ПРОБЛЕМЫ:

# 1. Пропуски (20%)
mask = np.random.random(n) < 0.2
df.loc[mask, 'salary'] = np.nan

mask = np.random.random(n) < 0.1
df.loc[mask, 'age'] = np.nan

mask = np.random.random(n) < 0.15
df.loc[mask, 'education'] = np.nan

# 2. Выбросы
df.loc[5, 'salary'] = 5000000   # миллионер
df.loc[10, 'age'] = 5           # ошибка
df.loc[15, 'experience'] = 100  # ошибка
df.loc[20, 'score'] = 200       # невозможно

# 3. Дубликаты
df = pd.concat([df, df.iloc[:5]], ignore_index=True)

print(f"Создано {len(df)} строк (с дубликатами)")
print("\nПроблемы в данных:")
print(f"  Пропусков: {df.isnull().sum().sum()}")
print(f"  Дубликатов: {df.duplicated().sum()}")

print("\nПропуски по столбцам:")
print(df.isnull().sum())


print("\n" + "="*60)
print("ШАГ 2: Базовая модель (НА ГРЯЗНЫХ ДАННЫХ)")
print("="*60)

print("Попробуем обучить на грязных данных...")

# Удалим только строки с NaN в salary (цель)
df_baseline = df.dropna(subset=['salary'])

# Категории в числа (простейший способ)
le_education = LabelEncoder()
le_city = LabelEncoder()

df_baseline['education_encoded'] = le_education.fit_transform(
    df_baseline['education'].fillna('Unknown')
)
df_baseline['city_encoded'] = le_city.fit_transform(df_baseline['city'])

# Заполним пропуски нулями (плохой способ!)
df_baseline = df_baseline.fillna(0)

# Признаки и цель
features = ['age', 'experience', 'score', 'education_encoded', 'city_encoded']
X_baseline = df_baseline[features].values
y_baseline = df_baseline['salary'].values

# Разделение
X_train_base, X_test_base, y_train_base, y_test_base = train_test_split(
    X_baseline, y_baseline, test_size=0.2, random_state=42
)

# Модель
model_baseline = RandomForestRegressor(n_estimators=100, random_state=42)
model_baseline.fit(X_train_base, y_train_base)

# Оценка
y_pred_base = model_baseline.predict(X_test_base)
r2_baseline = r2_score(y_test_base, y_pred_base)
mae_baseline = mean_absolute_error(y_test_base, y_pred_base)

print(f"\n📊 Результаты на грязных данных:")
print(f"  R²: {r2_baseline:.4f}")
print(f"  MAE: {mae_baseline:.0f}")




print("\n" + "="*60)
print("ШАГ 3: ОЧИСТКА ДАННЫХ")
print("="*60)

df_clean = df.copy()

# 3.1 Удалить дубликаты
print("\n3.1 Удаление дубликатов...")
before_dup = len(df_clean)
df_clean = df_clean.drop_duplicates()
print(f"  Было: {before_dup}, Стало: {len(df_clean)}")

# 3.2 Обработать выбросы (IQR метод)
print("\n3.2 Обработка выбросов...")

for col in ['age', 'experience', 'salary', 'score']:
    if df_clean[col].notna().sum() > 0:  # если есть значения
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        
        # Capping (обрезка)
        df_clean[col] = df_clean[col].clip(lower=lower, upper=upper)
        
        print(f"  {col}: границы [{lower:.0f}, {upper:.0f}]")

# 3.3 Обработать пропуски
print("\n3.3 Обработка пропусков...")

# Числовые - медиана
imputer_num = SimpleImputer(strategy='median')
numeric_cols = ['age', 'experience', 'salary', 'score']
df_clean[numeric_cols] = imputer_num.fit_transform(df_clean[numeric_cols])

# Категориальные - мода
imputer_cat = SimpleImputer(strategy='most_frequent')
df_clean['education'] = imputer_cat.fit_transform(df_clean[['education']])

print(f"  Пропусков осталось: {df_clean.isnull().sum().sum()}")

# 3.4 Кодирование категорий
print("\n3.4 Кодирование категорий...")

df_clean['education_encoded'] = le_education.fit_transform(df_clean['education'])
df_clean['city_encoded'] = le_city.fit_transform(df_clean['city'])

print("  ✓ Категории закодированы")

print("\n Данные очищены!")


print("\n" + "="*60)
print("ШАГ 4: Модель на ЧИСТЫХ данных")
print("="*60)

# Признаки и цель
X_clean = df_clean[features].values
y_clean = df_clean['salary'].values

# Разделение
X_train_clean, X_test_clean, y_train_clean, y_test_clean = train_test_split(
    X_clean, y_clean, test_size=0.2, random_state=42
)

# Модель
model_clean = RandomForestRegressor(n_estimators=100, random_state=42)
model_clean.fit(X_train_clean, y_train_clean)

# Оценка
y_pred_clean = model_clean.predict(X_test_clean)
r2_clean = r2_score(y_test_clean, y_pred_clean)
mae_clean = mean_absolute_error(y_test_clean, y_pred_clean)

print(f"\n📊 Результаты на чистых данных:")
print(f"  R²: {r2_clean:.4f}")
print(f"  MAE: {mae_clean:.0f}")

# ============================================
# ШАГ 5: СРАВНЕНИЕ
# ============================================

print("\n" + "="*60)
print("ШАГ 5: СРАВНЕНИЕ РЕЗУЛЬТАТОВ")
print("="*60)

comparison = pd.DataFrame({
    'Данные': ['Грязные', 'Чистые'],
    'Строк': [len(X_baseline), len(X_clean)],
    'R²': [r2_baseline, r2_clean],
    'MAE': [mae_baseline, mae_clean]
})

print("\n" + comparison.to_string(index=False))

improvement = ((r2_clean - r2_baseline) / abs(r2_baseline)) * 100
print(f"\n🎯 Улучшение R²: {improvement:.1f}%")

mae_improvement = ((mae_baseline - mae_clean) / mae_baseline) * 100
print(f"🎯 Улучшение MAE: {mae_improvement:.1f}%")

# ============================================
# ШАГ 6: ВИЗУАЛИЗАЦИЯ
# ============================================

print("\n" + "="*60)
print("ШАГ 6: Визуализация")
print("="*60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# График 1: Сравнение R²
axes[0, 0].bar(['Грязные\nданные', 'Чистые\nданные'], 
               [r2_baseline, r2_clean],
               color=['red', 'green'], alpha=0.7)
axes[0, 0].set_title('📊 Сравнение R² Score', fontweight='bold', fontsize=14)
axes[0, 0].set_ylabel('R² Score')
axes[0, 0].set_ylim(0, 1)
axes[0, 0].grid(True, alpha=0.3, axis='y')

for i, v in enumerate([r2_baseline, r2_clean]):
    axes[0, 0].text(i, v + 0.02, f'{v:.3f}', 
                    ha='center', fontweight='bold')

# График 2: Сравнение MAE
axes[0, 1].bar(['Грязные\nданные', 'Чистые\nданные'], 
               [mae_baseline, mae_clean],
               color=['red', 'green'], alpha=0.7)
axes[0, 1].set_title('📏 Сравнение MAE', fontweight='bold', fontsize=14)
axes[0, 1].set_ylabel('MAE (руб)')
axes[0, 1].grid(True, alpha=0.3, axis='y')

for i, v in enumerate([mae_baseline, mae_clean]):
    axes[0, 1].text(i, v + 500, f'{v:.0f}', 
                    ha='center', fontweight='bold')

# График 3: Предсказания vs Реальность (грязные)
axes[1, 0].scatter(y_test_base, y_pred_base, alpha=0.5, s=30, color='red')
axes[1, 0].plot([y_test_base.min(), y_test_base.max()],
                [y_test_base.min(), y_test_base.max()],
                'k--', linewidth=2)
axes[1, 0].set_title(f'Грязные (R²={r2_baseline:.3f})', fontweight='bold')
axes[1, 0].set_xlabel('Реальная зарплата')
axes[1, 0].set_ylabel('Предсказанная зарплата')
axes[1, 0].grid(True, alpha=0.3)

# График 4: Предсказания vs Реальность (чистые)
axes[1, 1].scatter(y_test_clean, y_pred_clean, alpha=0.5, s=30, color='green')
axes[1, 1].plot([y_test_clean.min(), y_test_clean.max()],
                [y_test_clean.min(), y_test_clean.max()],
                'k--', linewidth=2)
axes[1, 1].set_title(f'Чистые (R²={r2_clean:.3f})', fontweight='bold')
axes[1, 1].set_xlabel('Реальная зарплата')
axes[1, 1].set_ylabel('Предсказанная зарплата')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================
# ИТОГИ
# ============================================

print("\n" + "="*60)
print("ИТОГИ ПРОЕКТА:")
print("="*60)

print(f"""
✅ ЧТО СДЕЛАЛИ:

1. Создали грязный датасет ({n} записей)
   - Пропуски
   - Выбросы
   - Дубликаты

2. Обучили модель на грязных данных
   R² = {r2_baseline:.3f}

3. Очистили данные:
   - Удалили дубликаты
   - Обработали выбросы (IQR + capping)
   - Заполнили пропуски (median/mode)
   - Закодировали категории

4. Обучили модель на чистых данных
   R² = {r2_clean:.3f}

📊 РЕЗУЛЬТАТ:
Улучшение качества на {improvement:.1f}%!

💡 ВЫВОД:
Очистка данных КРИТИЧЕСКИ ВАЖНА для ML!
Грязные данные = плохая модель
Чистые данные = хорошая модель
""")

print("\n✅ Проект завершён!")