import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
np.random.seed(42)

print("="*60)
print("PERCEPTRON - Prosteyshaya neyroset")
print("="*60)

print("""
PERCEPTRON - eto ODIN neyron

Struktura:
         X1 ──┐
         X2 ──┤
         X3 ──┼──> Σ ──> Aktivatsiya ──> Vykhod
         ... ─┤
         Xn ──┘
         
         W1, W2, W3... (vesa)

Shag 1: Vychislit summu
  z = X1*W1 + X2*W2 + ... + Xn*Wn + b
  (b - bias, sdvig)

Shag 2: Primenit aktivatsiyu
  y = activation(z)

PRIMER:
X = [2, 3]
W = [0.5, 0.3]
b = 1

z = 2*0.5 + 3*0.3 + 1 = 1 + 0.9 + 1 = 2.9
y = step(2.9) = 1 (esli z > 0)
""")

print("\n" + "="*60)
print("Sozdaem perceptron s nulya")
print("="*60)

class Perceptron:
    def __init__(self, n_inputs, learning_rate = 0.01):
         """
        n_inputs - количество входов
        learning_rate - скорость обучения
        """
         self.weights = np.random.randn(n_inputs)
         self.bias = np.random.randn()
         self.learning_rate = learning_rate
    
    def activation(self, z):
        """
        Функция активации: Step (ступенька)
        Если z >= 0 → 1
        Если z < 0  → 0
        """
        return np.where(z >= 0, 1, 0)
    
    def predict(self, X):
        """
        Предсказание для одного или нескольких примеров
        """
        z = np.dot(X, self.weights) + self.bias
        """
        np.dot(X, W) - скалярное произведение
        X = [x1, x2], W = [w1, w2]
        dot(X, W) = x1*w1 + x2*w2
        """
        return self.activation(z)

def train(self, X, y, epochs=100):
        """
        Обучение перцептрона
        
        X - входы (n_samples, n_features)
        y - цели (n_samples,)
        epochs - количество эпох
        """
        errors_history = []
        
        for epoch in range(epochs):
            total_error = 0
            
            for xi, yi in zip(X, y):
                """
                Для каждого примера:
                1. Предсказать
                2. Вычислить ошибку
                3. Обновить веса
                """
                # Предсказание
                prediction = self.predict(xi)
                
                # Ошибка
                error = yi - prediction
                
                # Обновление весов (правило перцептрона)
                self.weights += self.learning_rate * error * xi
                self.bias += self.learning_rate * error
                """
                Правило обучения:
                W_new = W_old + lr * error * X
                
                Если ошибка = 0 (правильно) → веса не меняются
                Если ошибка > 0 (надо больше) → увеличиваем веса
                Если ошибка < 0 (надо меньше) → уменьшаем веса
                """
                
                total_error += abs(error)
            
            errors_history.append(total_error)
            
            if epoch % 10 == 0:
                print(f"  Эпоха {epoch}: ошибок = {total_error}")
        
        return errors_history

print("\n" + "="*60)
print("Задача: Логическое AND")
print("="*60)

print("""
AND (И):
X1  X2  → Y
0   0   → 0
0   1   → 0
1   0   → 0
1   1   → 1

Только когда ОБА входа = 1, результат = 1
""")

# Данные
X_and = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

y_and = np.array([0, 0, 0, 1])

# Создание и обучение
perceptron_and = Perceptron(n_inputs=2, learning_rate=0.1)

print("\nОбучение перцептрона...")
errors_and = perceptron_and.train(X_and, y_and, epochs=50)

# Тестирование
print("\nРезультаты:")
for x, y_true in zip(X_and, y_and):
    y_pred = perceptron_and.predict(x)
    print(f"  {x} → предсказано: {y_pred}, правильно: {y_true}")

# ============================================
# ZADACHA: LOGICHESKOE OR
# ============================================

print("\n" + "="*60)
print("Задача: Логическое OR")
print("="*60)

print("""
OR (ИЛИ):
X1  X2  → Y
0   0   → 0
0   1   → 1
1   0   → 1
1   1   → 1

Если ХОТЬ ОДИН вход = 1, результат = 1
""")

y_or = np.array([0, 1, 1, 1])

perceptron_or = Perceptron(n_inputs=2, learning_rate=0.1)

print("\nОбучение...")
errors_or = perceptron_or.train(X_and, y_or, epochs=50)

print("\nРезультаты:")
for x, y_true in zip(X_and, y_or):
    y_pred = perceptron_or.predict(x)
    print(f"  {x} → предсказано: {y_pred}, правильно: {y_true}")

# ============================================
# PROBLEMA: XOR
# ============================================

print("\n" + "="*60)
print("ПРОБЛЕМА: Логическое XOR")
print("="*60)

print("""
XOR (исключающее ИЛИ):
X1  X2  → Y
0   0   → 0
0   1   → 1
1   0   → 1
1   1   → 0

Результат = 1 только если входы РАЗНЫЕ

ЭТО ПРОБЛЕМА!
Один перцептрон НЕ МОЖЕТ решить XOR!
Нужна многослойная сеть!
""")

y_xor = np.array([0, 1, 1, 0])

perceptron_xor = Perceptron(n_inputs=2, learning_rate=0.1)

print("\nПопытка обучить...")
errors_xor = perceptron_xor.train(X_and, y_xor, epochs=100)

print("\nРезультаты (будут неправильные!):")
for x, y_true in zip(X_and, y_xor):
    y_pred = perceptron_xor.predict(x)
    correct = "✓" if y_pred == y_true else "✗"
    print(f"  {x} → предсказано: {y_pred}, правильно: {y_true} {correct}")

print("""
Видите? Перцептрон не справился с XOR!
Причина: XOR нелинейно разделим
Нужна многослойная сеть!
""")

# ============================================
# VIZUALIZATSIYA
# ============================================

print("\nВизуализация...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# График 1: Обучение AND
axes[0, 0].plot(errors_and, linewidth=2)
axes[0, 0].set_title('Обучение AND', fontweight='bold', fontsize=14)
axes[0, 0].set_xlabel('Эпоха')
axes[0, 0].set_ylabel('Количество ошибок')
axes[0, 0].grid(True, alpha=0.3)

# График 2: Обучение OR
axes[0, 1].plot(errors_or, linewidth=2, color='green')
axes[0, 1].set_title('Обучение OR', fontweight='bold', fontsize=14)
axes[0, 1].set_xlabel('Эпоха')
axes[0, 1].set_ylabel('Количество ошибок')
axes[0, 1].grid(True, alpha=0.3)

# График 3: Обучение XOR (не сходится!)
axes[1, 0].plot(errors_xor, linewidth=2, color='red')
axes[1, 0].set_title('Обучение XOR (НЕ работает!)', fontweight='bold', fontsize=14)
axes[1, 0].set_xlabel('Эпоха')
axes[1, 0].set_ylabel('Количество ошибок')
axes[1, 0].grid(True, alpha=0.3)

# График 4: Сравнение задач
axes[1, 1].bar(['AND', 'OR', 'XOR'], 
               [errors_and[-1], errors_or[-1], errors_xor[-1]],
               color=['blue', 'green', 'red'], alpha=0.7)
axes[1, 1].set_title('Финальные ошибки', fontweight='bold', fontsize=14)
axes[1, 1].set_ylabel('Ошибок')
axes[1, 1].grid(True, alpha=0.3, axis='y')

for i, v in enumerate([errors_and[-1], errors_or[-1], errors_xor[-1]]):
    axes[1, 1].text(i, v + 0.1, f'{int(v)}', ha='center', fontweight='bold')

plt.tight_layout()
plt.show()

# ============================================
# REZYUME
# ============================================

print("\n" + "="*60)
print("РЕЗЮМЕ:")
print("="*60)

print("""
PERCEPTRON:

ЧТО ЭТО:
- Простейшая нейросеть (1 нейрон)
- Линейный классификатор

КАК РАБОТАЕТ:
1. z = Σ(Xi * Wi) + b
2. y = activation(z)

ОБУЧЕНИЕ:
W_new = W_old + lr * error * X

ЧТО МОЖЕТ:
✓ AND, OR (линейно разделимые)

ЧТО НЕ МОЖЕТ:
✗ XOR (нелинейная задача)

РЕШЕНИЕ:
Многослойные сети! (следующий файл)
""")

print("\n Перцептрон освоен!")
print("="*60)