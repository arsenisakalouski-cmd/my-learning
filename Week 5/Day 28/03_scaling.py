
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

sns.set_theme()
np.random.seed(42)

print("="*60)
print("FEATURE SCALING - Masshtabirovanie")
print("="*60)


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

sns.set_theme()
np.random.seed(42)

print("="*60)
print("FEATURE SCALING - Masshtabirovanie")
print("="*60)


print("""
PROBLEMA: Raznye masshtaby priznakov

Primer:
- Vozrast: 20-60 (desyatki)
- Zarplata: 30000-200000 (desyatki tysyach)
- Rost: 150-190 (sotni)

Model uvidit chto zarplata MENSHAETSYA silnee
I reshit chto ona vazhnee!
No eto ne tak - prosto drugoy masshtab!

RESHENIE: Privesti vse k odnomu masshtabu
""")

print("\n" + "="*60)
print("Sozdaem dannye s raznymi masshtabami")
print("="*60)

n = 100

data = {
    'vozrast': np.random.randint(20, 60, n),
    'zarplata': np.random.randint(30000, 200000, n),
    'opyt': np.random.randint(0, 30, n),
    'rost': np.random.randint(150, 190, n)
}

df = pd.DataFrame(data)

# Tsena zavisit ot vseh priznakov
tsena = (
    df['vozrast'] * 100 +
    df['zarplata'] * 0.01 +
    df['opyt'] * 500 +
    df['rost'] * 50 +
    np.random.normal(0, 1000, n)
)

df['tsena'] = tsena

print("Statistika (raznye masshtaby!):")
print(df.describe())

print("\nMin-Max dlya kazhdogo:")
for col in ['vozrast', 'zarplata', 'opyt', 'rost']:
    print(f"  {col}: [{df[col].min()}, {df[col].max()}]")


print("\n" + "="*60)
print("METOD 1: StandardScaler (standartizatsiya)")
print("="*60)

scaler_standard = StandardScaler()
"""
StandardScaler - standartizatsiya (Z-score)

Formula: z = (x - mean) / std

Rezultat:
- Srednee = 0
- Std = 1
- Raspredelenie sohranitsya

Primer:
Vozrast: [20, 30, 40, 50, 60]
mean = 40, std = 14.14
20 → (20-40)/14.14 = -1.41
40 → (40-40)/14.14 = 0
60 → (60-40)/14.14 = 1.41

KOGDA ISPOLZOVAT:
- Dannye normalno raspredeleny
- Vazhno sohranit formu raspredeleniya
- Dlya modeley kak LogisticRegression, SVM
"""

X = df[['vozrast', 'zarplata', 'opyt', 'rost']].values
X_scaled_standard = scaler_standard.fit_transform(X)

print("Do StandardScaler:")
print(f"  Mean: {X.mean(axis=0)}")
print(f"  Std: {X.std(axis=0)}")

print("\nPosle StandardScaler:")
print(f"  Mean: {X_scaled_standard.mean(axis=0)}")
print(f"  Std: {X_scaled_standard.std(axis=0)}")

print("\n" + "="*60)
print("METOD 2: MinMaxScaler (normalizatsiya)")
print("="*60)

scaler_minmax = MinMaxScaler()
"""
MinMaxScaler - normalizatsiya v diapazon [0, 1]

Formula: x_scaled = (x - min) / (max - min)

Rezultat:
- Min → 0
- Max → 1
- Vse mezh 0 i 1

Primer:
Zarplata: [30000, 50000, 100000, 200000]
min = 30000, max = 200000
30000 → (30000-30000)/(200000-30000) = 0
200000 → (200000-30000)/(200000-30000) = 1
100000 → (100000-30000)/(200000-30000) = 0.41

KOGDA ISPOLZOVAT:
- Nuzhny znacheniya v [0, 1]
- Dlya neyronnykh setey
- Net silnykh vybrosov
"""

X_scaled_minmax = scaler_minmax.fit_transform(X)

print("Do MinMaxScaler:")
print(f"  Min: {X.min(axis=0)}")
print(f"  Max: {X.max(axis=0)}")

print("\nPosle MinMaxScaler:")
print(f"  Min: {X_scaled_minmax.min(axis=0)}")
print(f"  Max: {X_scaled_minmax.max(axis=0)}")

print("\n" + "="*60)
print("METOD 3: RobustScaler (ustoychivyy)")
print("="*60)

# Dobavim vybrosy
X_with_outliers = X.copy()
X_with_outliers[5, 1] = 5000000  # gigantskaya zarplata

scaler_robust = RobustScaler()
"""
RobustScaler - ustoychiv k vybrosam

Formula: x_scaled = (x - median) / IQR
gde IQR = Q3 - Q1

Ispolzuet median vmesto mean
Ispolzuet IQR vmesto std

POCHEMU LUCHSHE PRI VYBROSAKH:
Median i IQR ne iskaiutsya vybrosami!

Mean zarplata s vybrosami: 80000 → 130000 (iskazheno!)
Median zarplata s vybrosami: 80000 → 81000 (pochti ne izmenilsya)

KOGDA ISPOLZOVAT:
- Est vybrosy
- Raspredelenie skoshennoe
"""

X_scaled_robust = scaler_robust.fit_transform(X_with_outliers)

print("S vybrosami - RobustScaler:")
print(f"  Median: {np.median(X_scaled_robust, axis=0)}")






print("\n" + "="*60)
print("SRAVNENIE: vliyanie na model")
print("="*60)

y = df['tsena'].values

# Bez scaling
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model_no_scale = LinearRegression()
model_no_scale.fit(X_train, y_train)
r2_no_scale = model_no_scale.score(X_test, y_test)

# S StandardScaler
X_train_std, X_test_std, _, _ = train_test_split(
    X_scaled_standard, y, test_size=0.2, random_state=42
)

model_scaled = LinearRegression()
model_scaled.fit(X_train_std, y_train)
r2_scaled = model_scaled.score(X_test_std, y_test)

print(f"R² bez scaling: {r2_no_scale:.4f}")
print(f"R² s scaling: {r2_scaled:.4f}")

print("""
VAZHNOE ZAMECHANIE:
Dlya LinearRegression scaling ne vsegda nuzhen
No dlya drugikh modeley (SVM, KNN, Neural Networks) - OBYAZATELEN!
""")
print("\nVizualiziruem raznye metody...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Originalnye dannye
axes[0, 0].boxplot([df['vozrast'], df['zarplata']/1000, 
                    df['opyt'], df['rost']])
axes[0, 0].set_xticklabels(['Vozrast', 'Zarplata\n(tys)', 'Opyt', 'Rost'])
axes[0, 0].set_title('Originalnye (raznye masshtaby)', fontweight='bold')
axes[0, 0].set_ylabel('Znacheniya')
axes[0, 0].grid(True, alpha=0.3, axis='y')

# StandardScaler
axes[0, 1].boxplot(X_scaled_standard)
axes[0, 1].set_xticklabels(['Vozrast', 'Zarplata', 'Opyt', 'Rost'])
axes[0, 1].set_title('StandardScaler (mean=0, std=1)', fontweight='bold')
axes[0, 1].set_ylabel('Z-score')
axes[0, 1].grid(True, alpha=0.3, axis='y')

# MinMaxScaler
axes[1, 0].boxplot(X_scaled_minmax)
axes[1, 0].set_xticklabels(['Vozrast', 'Zarplata', 'Opyt', 'Rost'])
axes[1, 0].set_title('MinMaxScaler (0-1)', fontweight='bold')
axes[1, 0].set_ylabel('Normalizovannoe znachenie')
axes[1, 0].set_ylim(-0.1, 1.1)
axes[1, 0].grid(True, alpha=0.3, axis='y')

# RobustScaler
axes[1, 1].boxplot(X_scaled_robust)
axes[1, 1].set_xticklabels(['Vozrast', 'Zarplata', 'Opyt', 'Rost'])
axes[1, 1].set_title('RobustScaler (ustoychiv k vybrosam)', fontweight='bold')
axes[1, 1].set_ylabel('Masshtabirovannoe znachenie')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()



print("\n" + "="*60)
print("REZYUME:")
print("="*60)

print("""
TRI METODA SCALING:

1. StandardScaler
   Formula: (x - mean) / std
   Rezultat: mean=0, std=1
   Kogda: normalnoe raspredelenie

2. MinMaxScaler
   Formula: (x - min) / (max - min)
   Rezultat: znacheniya v [0, 1]
   Kogda: nuzhny znacheniya 0-1

3. RobustScaler
   Formula: (x - median) / IQR
   Rezultat: ustoychiv k vybrosam
   Kogda: est vybrosy

VAZHNO:
- fit_transform() na train
- transform() na test
- Dlya LinearRegression ne obyazatelno
- Dlya SVM, KNN, Neural Networks - OBYAZATELNO!
""")