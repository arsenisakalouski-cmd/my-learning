# 02_missing_full.py - Полная версия с визуализацией

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer

sns.set_theme()
np.random.seed(42)

print("="*60)
print("ОБРАБОТКА ПРОПУСКОВ - Полная версия")
print("="*60)

# Создание данных
n = 100
data = {
    'возраст': np.random.randint(20, 60, n),
    'зарплата': np.random.randint(30000, 150000, n),
    'опыт': np.random.randint(0, 30, n),
    'балл': np.random.randint(50, 100, n)
}

df = pd.DataFrame(data)

# Добавляем пропуски
df.loc[np.random.random(n) < 0.2, 'зарплата'] = np.nan
df.loc[np.random.random(n) < 0.1, 'возраст'] = np.nan
df.loc[np.random.random(n) < 0.3, 'балл'] = np.nan

print("\nПропуски:")
print(df.isnull().sum())
print("\nПроцент:")
print((df.isnull().sum() / len(df) * 100).round(1))

# Разные методы
df_dropped = df.dropna()
df_mean = df.copy()
df_mean['зарплата'] = df_mean['зарплата'].fillna(df_mean['зарплата'].mean())
df_mean['возраст'] = df_mean['возраст'].fillna(df_mean['возраст'].mean())
df_mean['балл'] = df_mean['балл'].fillna(df_mean['балл'].mean())

df_median = df.copy()
df_median['зарплата'] = df_median['зарплата'].fillna(df_median['зарплата'].median())
df_median['возраст'] = df_median['возраст'].fillna(df_median['возраст'].median())
df_median['балл'] = df_median['балл'].fillna(df_median['балл'].median())

imputer = SimpleImputer(strategy='median')
df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

# Сравнение
print("\n" + "="*60)
print("СРАВНЕНИЕ МЕТОДОВ:")
print("="*60)

comparison = pd.DataFrame({
    'Метод': ['Оригинал', 'Удаление', 'Среднее', 'Медиана', 'Imputer'],
    'Строк': [len(df), len(df_dropped), len(df_mean), len(df_median), len(df_imputed)],
    'Пропусков': [
        df.isnull().sum().sum(),
        df_dropped.isnull().sum().sum(),
        df_mean.isnull().sum().sum(),
        df_median.isnull().sum().sum(),
        df_imputed.isnull().sum().sum()
    ]
})

print("\n" + comparison.to_string(index=False))

# Визуализация
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

axes[0, 0].hist(df['зарплата'].dropna(), bins=20, color='gray', edgecolor='black', alpha=0.7)
axes[0, 0].set_title('Оригинал (с пропусками)', fontweight='bold')
axes[0, 0].set_xlabel('Зарплата')
axes[0, 0].grid(True, alpha=0.3, axis='y')

axes[0, 1].hist(df_mean['зарплата'], bins=20, color='blue', edgecolor='black', alpha=0.7)
axes[0, 1].axvline(df['зарплата'].mean(), color='red', linestyle='--', linewidth=2)
axes[0, 1].set_title('Заполнено средним', fontweight='bold')
axes[0, 1].set_xlabel('Зарплата')
axes[0, 1].grid(True, alpha=0.3, axis='y')

axes[1, 0].hist(df_median['зарплата'], bins=20, color='green', edgecolor='black', alpha=0.7)
axes[1, 0].axvline(df['зарплата'].median(), color='red', linestyle='--', linewidth=2)
axes[1, 0].set_title('Заполнено медианой', fontweight='bold')
axes[1, 0].set_xlabel('Зарплата')
axes[1, 0].grid(True, alpha=0.3, axis='y')

axes[1, 1].boxplot([df['зарплата'].dropna(), df_mean['зарплата'], df_median['зарплата']], 
                    labels=['Оригинал', 'Mean', 'Median'])
axes[1, 1].set_title('Сравнение', fontweight='bold')
axes[1, 1].set_ylabel('Зарплата')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("\n✅ Визуализация показана!")