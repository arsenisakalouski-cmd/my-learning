import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

sns.set_theme()
np.random.seed(42)

print("="*60)
print("POLYNOMIAL FEATURES - Polinomialnye priznaki")
print("="*60)

print("""

ПРИМЕР:

Исходные признаки: X1, X2

При степени полинома (degree) = 2 будут созданы:
1 (константа), X1, X2, X1², X1 × X2, X2²

При степени полинома (degree) = 3 создастся ещё больше признаков!
      
""")


print("\n" + "="*60)
print("Sozdaem dannye s nelineynoy zavisimostyu")
print("="*60)

n = 100
X = np.random.uniform(-3, 3, (n, 1))
y = 0.5 * X.ravel()**2 + X.ravel() + np.random.normal(0, 0.5, n)
"""
Realnaya zavisimost: y = 0.5*X² + X + shum

Eto KVADRATICHNAYA zavisimost!
Lineynaya model ne spravitsya
Nuzhny polinomialnye priznaki
"""

df = pd.DataFrame({'X': X.ravel(), 'y': y})

print(f"Sozdano {len(df)} tochek")
print("Zavisimost: y = 0.5*X² + X + shum")



print("\n" + "="*60)
print("MODEL 1: Lineynaya (bez polynomial)")
print("="*60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model_linear = LinearRegression()
model_linear.fit(X_train, y_train)
y_pred_linear = model_linear.predict(X_test)
r2_linear = r2_score(y_test, y_pred_linear)

print(f"R² lineynoy modeli: {r2_linear:.4f}")
"""
Lineynaya model pytaetsya nayti: y = a*X + b
No realnaya zavisimost: y = 0.5*X² + X
Lineynaya ne mozhet nayti X² → ploho rabotaet!
"""


# ============================================
# MODEL 2: S POLYNOMIAL FEATURES
# ============================================

print("\n" + "="*60)
print("MODEL 2: S Polynomial Features (degree=2)")
print("="*60)

poly = PolynomialFeatures(degree=2, include_bias=False)
"""
PolynomialFeatures - sozdaet vse kombinatsii

degree=2 → vklyuchaet X²
degree=3 → vklyuchaet X², X³

include_bias=False - ne dobavlyat stolbets iz 1
  (LinearRegression sam dobavlyaet intercept)

PRIMER:
X = [2, 3]

degree=2 →
[2, 3, 4, 6, 9]
 ↑  ↑  ↑  ↑  ↑
 X1 X2 X1² X1×X2 X2²
"""

X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)
"""
fit_transform() - obuchit i primenit
  Zapomit kakiye priznaki sozdavat
  Sozdat ikh

transform() - primenit k novym dannym
  Ispolzovat te zhe pravila
"""

print(f"Priznakov bylo: {X_train.shape[1]}")
print(f"Priznakov stalo: {X_train_poly.shape[1]}")

model_poly = LinearRegression()
model_poly.fit(X_train_poly, y_train)
y_pred_poly = model_poly.predict(X_test_poly)
r2_poly = r2_score(y_test, y_pred_poly)

print(f"\nR² s polynomial: {r2_poly:.4f}")


print("\n" + "="*60)
print("SRAVNENIE:")
print("="*60)

print(f"Lineynaya model:  R² = {r2_linear:.4f}")
print(f"Polynomial model: R² = {r2_poly:.4f}")

uluchshenie = ((r2_poly - r2_linear) / abs(r2_linear)) * 100
print(f"\nUluchshenie: {uluchshenie:.1f}%")

print("\nVizualiziruem...")

plt.figure(figsize=(14, 6))

# Graf 1: Lineynaya model
plt.subplot(1, 2, 1)
plt.scatter(X, y, alpha=0.5, s=50, label='Dannye')

X_line = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_line_linear = model_linear.predict(X_line)

plt.plot(X_line, y_line_linear, 'r-', linewidth=2, 
         label=f'Lineynaya (R²={r2_linear:.3f})')
plt.title('Lineynaya model', fontweight='bold', fontsize=14)
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.grid(True, alpha=0.3)

# Graf 2: Polynomial model
plt.subplot(1, 2, 2)
plt.scatter(X, y, alpha=0.5, s=50, label='Dannye')

X_line_poly = poly.transform(X_line)
y_line_poly = model_poly.predict(X_line_poly)

plt.plot(X_line, y_line_poly, 'g-', linewidth=2, 
         label=f'Polynomial (R²={r2_poly:.3f})')
plt.title('Polynomial model', fontweight='bold', fontsize=14)
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show() 


print("\n" + "="*60)
print("Mnogomernye polynomial (2 priznaka)")
print("="*60)

# Sozdaem dannye s 2 priznakami
n = 100
X1 = np.random.uniform(-2, 2, n)
X2 = np.random.uniform(-2, 2, n)
y_multi = X1**2 + X2**2 + X1*X2 + np.random.normal(0, 0.3, n)

X_multi = np.column_stack([X1, X2])

print(f"Priznakov: {X_multi.shape[1]}")

# Polynomial degree=2
poly_multi = PolynomialFeatures(degree=2, include_bias=False)
X_multi_poly = poly_multi.fit_transform(X_multi)

print(f"Posle polynomial: {X_multi_poly.shape[1]} priznakov")
print("\nSozdannye priznaki:")
print(poly_multi.get_feature_names_out(['X1', 'X2']))
"""
get_feature_names_out() - pokazat nazvaniya priznakov

Vyvod:
['X1', 'X2', 'X1^2', 'X1 X2', 'X2^2']

Sozdal:
- Originalnye: X1, X2
- Kvadraty: X1², X2²
- Vzaimodeystvie: X1×X2
"""

# ============================================
# VLIYANIE DEGREE
# ============================================

print("\n" + "="*60)
print("Vliyanie degree na kolichestvo priznakov")
print("="*60)

X_test_size = np.random.rand(10, 3)  # 3 priznaka

for deg in [1, 2, 3, 4]:
    poly_test = PolynomialFeatures(degree=deg, include_bias=False)
    X_transformed = poly_test.fit_transform(X_test_size)
    print(f"degree={deg}: {X_test_size.shape[1]} → {X_transformed.shape[1]} priznakov")
"""
VNIMANIE:
degree bolshe → MNOGO priznakov!

3 priznaka:
degree=1 → 3
degree=2 → 9
degree=3 → 19
degree=4 → 34

Mnogo priznakov → pereobuchenie!
Obychno ispolzuem degree=2, redko 3
"""

# ============================================
# REZYUME
# ============================================

print("\n" + "="*60)
print("REZYUME:")
print("="*60)

print("""
POLYNOMIAL FEATURES:

ZACHEM:
- Nelineynye zavisimosti
- Kvadratichnye, kubicheskie svyazi

KAK:
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

DEGREE:
2 - obychno (kvadraty + vzaimodeystviya)
3 - redko (slishkom mnogo priznakov)

OPASNOST:
Mnogo priznakov → pereobuchenie!
Ispolzuyte s ostorozhnostyu
""")

print("\n Polynomial Features osvoeny!")
print("="*60)