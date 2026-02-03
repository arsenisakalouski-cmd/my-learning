import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
np.random.seed(42)

print("="*60)
print("MULTILAYER PERCEPTRON (MLP)")
print("="*60)


print("""
MLP = Multi-Layer Perceptron (многослойный перцептрон)

STRUKTURA:

Vkhodnoй sloy    Skrytyy sloy    Vykhodnoй sloy
    X1 ───┐         H1 ───┐
          ├────────┤       ├────> Y
    X2 ───┘         H2 ───┘

Sloi:
1. INPUT (входной) - получает данные
2. HIDDEN (скрытые) - обрабатывают
3. OUTPUT (выходной) - результат

POCHEMU RABOTAET?

Один слой: только линейные границы
Два слоя: ЛЮБЫЕ нелинейные границы!

Теорема о универсальной аппроксимации:
MLP с одним скрытым слоем может приблизить
ЛЮБУЮ функцию!
""")


print("\n" + "="*60)
print("Функции активации")
print("="*60)

def sigmoid(z):
    """
    Sigmoid (сигмоида)
    
    Формула: σ(z) = 1 / (1 + e^(-z))
    
    Свойства:
    - Выход: (0, 1)
    - Гладкая S-образная кривая
    - Используется для вероятностей
    """
    return 1 / (1 + np.exp(-z))

def sigmoid_derivative(z):
    """
    Производная sigmoid
    
    Нужна для обратного распространения!
    σ'(z) = σ(z) * (1 - σ(z))
    """
    s = sigmoid(z)
    return s * (1 - s)

def relu(z):
    """
    ReLU (Rectified Linear Unit)
    
    Формула: f(z) = max(0, z)
    
    Свойства:
    - Если z < 0 → 0
    - Если z >= 0 → z
    - Очень популярна!
    - Быстрая в вычислениях
    """
    return np.maximum(0, z)

def relu_derivative(z):
    """
    Производная ReLU
    
    f'(z) = 1 если z > 0
    f'(z) = 0 если z <= 0
    """
    return np.where(z > 0, 1, 0)

def tanh(z):
    """
    Tanh (гиперболический тангенс)
    
    Формула: tanh(z) = (e^z - e^(-z)) / (e^z + e^(-z))
    
    Свойства:
    - Выход: (-1, 1)
    - Похож на sigmoid, но центрирован в 0
    """
    return np.tanh(z)

def tanh_derivative(z):
    """
    Производная tanh
    
    tanh'(z) = 1 - tanh²(z)
    """
    return 1 - np.tanh(z)**2

# Визуализация функций активации
print("\nВизуализируем функции активации...")


z = np.linspace(-5, 5, 100)

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.plot(z, sigmoid(z), linewidth=2, label='Sigmoid')
plt.title('Sigmoid σ(z)', fontweight='bold', fontsize=14)
plt.xlabel('z')
plt.ylabel('σ(z)')
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='k', linewidth=0.5)
plt.axhline(y=1, color='k', linewidth=0.5, linestyle='--')
plt.axvline(x=0, color='k', linewidth=0.5)
plt.legend()

plt.subplot(1, 3, 2)
plt.plot(z, relu(z), linewidth=2, label='ReLU', color='green')
plt.title('ReLU f(z)', fontweight='bold', fontsize=14)
plt.xlabel('z')
plt.ylabel('f(z)')
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='k', linewidth=0.5)
plt.axvline(x=0, color='k', linewidth=0.5)
plt.legend()

plt.subplot(1, 3, 3)
plt.plot(z, tanh(z), linewidth=2, label='Tanh', color='red')
plt.title('Tanh f(z)', fontweight='bold', fontsize=14)
plt.xlabel('z')
plt.ylabel('f(z)')
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='k', linewidth=0.5)
plt.axhline(y=1, color='k', linewidth=0.5, linestyle='--')
plt.axhline(y=-1, color='k', linewidth=0.5, linestyle='--')
plt.axvline(x=0, color='k', linewidth=0.5)
plt.legend()

plt.tight_layout()
plt.show()

print("""
Когда что использовать:

SIGMOID:
- Выходной слой для бинарной классификации
- Когда нужны вероятности (0-1)

RELU:
- Скрытые слои (ОЧЕНЬ популярна!)
- Быстрая, эффективная
- По умолчанию в большинстве сетей

TANH:
- Скрытые слои
- Когда данные центрированы вокруг 0
- Лучше чем sigmoid для скрытых слоёв
""")

print("\n" + "="*60)
print("Создаём MLP с нуля")
print("="*60)


class MLP:

    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.1):
        """
        input_size - количество входов
        hidden_size - нейронов в скрытом слое
        output_size - количество выходов
        """
        # Веса слоя 1 (вход → скрытый)
        self.W1 = np.random.randn(input_size, hidden_size) * 0.5
        self.b1 = np.zeros(hidden_size)
        
        # Веса слоя 2 (скрытый → выход)
        self.W2 = np.random.randn(hidden_size, output_size) * 0.5
        self.b2 = np.zeros(output_size)
        
        self.learning_rate = learning_rate

    def forward(self, X):
        """
        Прямое распространение (forward propagation)
        
        Шаг 1: Вход → Скрытый слой
        Шаг 2: Скрытый → Выход
        """
        # Слой 1
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = sigmoid(self.z1)
        """
        z1 - взвешенная сумма
        a1 - активация (выход скрытого слоя)
        """
        
        # Слой 2
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = sigmoid(self.z2)
        """
        a2 - финальный выход сети
        """
        
        return self.a2    
    

  def backward(self, X, y, output):
        """
        Обратное распространение (backpropagation)
        
        Вычисляем градиенты и обновляем веса
        """
        m = X.shape[0]  # количество примеров
        
        # Ошибка выходного слоя
        self.output_error = output - y
        self.output_delta = self.output_error * sigmoid_derivative(self.z2)
        """
        output_delta - насколько нужно изменить выход
        
        Умножаем на производную активации!
        Это говорит: насколько чувствителен выход к изменению z
        """
        
        # Ошибка скрытого слоя
        self.hidden_error = np.dot(self.output_delta, self.W2.T)
        self.hidden_delta = self.hidden_error * sigmoid_derivative(self.z1)
        """
        Распространяем ошибку назад через веса!
        
        .T - транспонирование матрицы
        Нужно для правильных размерностей
        """
        
        # Обновление весов
        self.W2 -= self.learning_rate * np.dot(self.a1.T, self.output_delta) / m
        self.b2 -= self.learning_rate * np.sum(self.output_delta, axis=0) / m
        
        self.W1 -= self.learning_rate * np.dot(X.T, self.hidden_delta) / m
        self.b1 -= self.learning_rate * np.sum(self.hidden_delta, axis=0) / m
        
    def train(self, X, y, epochs=1000):
        """
        Обучение сети
        """
        losses = []
        
        for epoch in range(epochs):
            # Прямое распространение
            output = self.forward(X)
            
            # Ошибка (MSE)
            loss = np.mean((output - y)**2)
            losses.append(loss)
            
            # Обратное распространение
            self.backward(X, y, output)
            
            if epoch % 100 == 0:
                print(f"  Эпоха {epoch}: Loss = {loss:.4f}")
        
        return losses
    
    def predict(self, X):
        """
        Предсказание
        """
        output = self.forward(X)
        return (output > 0.5).astype(int)

# ============================================
# ZADACHA: XOR
# ============================================

print("\n" + "="*60)
print("Решаем XOR с помощью MLP!")
print("="*60)

# Данные XOR
X_xor = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

y_xor = np.array([[0], [1], [1], [0]])

# Создаём MLP
mlp = MLP(input_size=2, hidden_size=4, output_size=1, learning_rate=0.5)
"""
Архитектура:
2 входа → 4 скрытых нейрона → 1 выход

Почему 4 скрытых?
Эмпирическое правило: между количеством входов и выходов
Можно экспериментировать!
"""

print("\nОбучение MLP...")
print("Архитектура: 2 → 4 → 1")

losses = mlp.train(X_xor, y_xor, epochs=1000)

# Тестирование
print("\nРезультаты на XOR:")
predictions = mlp.predict(X_xor)

for x, y_true, y_pred in zip(X_xor, y_xor, predictions):
    correct = "✓" if y_pred[0] == y_true[0] else "✗"
    print(f"  {x} → предсказано: {y_pred[0]}, правильно: {y_true[0]} {correct}")

print("""
УСПЕХ! MLP решил XOR!
Перцептрон не мог, а MLP смог!
""")

# ============================================
# VIZUALIZATSIYA
# ============================================

print("\nВизуализация обучения...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# График 1: Loss
axes[0].plot(losses, linewidth=2)
axes[0].set_title('Обучение MLP (XOR)', fontweight='bold', fontsize=14)
axes[0].set_xlabel('Эпоха')
axes[0].set_ylabel('Loss (MSE)')
axes[0].grid(True, alpha=0.3)

# График 2: Граница решения
x_min, x_max = -0.5, 1.5
y_min, y_max = -0.5, 1.5

xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                     np.linspace(y_min, y_max, 100))

Z = mlp.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

axes[1].contourf(xx, yy, Z, alpha=0.3, levels=1, colors=['blue', 'red'])
axes[1].scatter(X_xor[:, 0], X_xor[:, 1], c=y_xor.ravel(), 
                s=200, edgecolors='black', linewidth=2, cmap='coolwarm')
axes[1].set_title('Граница решения XOR', fontweight='bold', fontsize=14)
axes[1].set_xlabel('X1')
axes[1].set_ylabel('X2')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================
# REZYUME
# ============================================

print("\n" + "="*60)
print("РЕЗЮМЕ:")
print("="*60)

print("""
MULTILAYER PERCEPTRON (MLP):

АРХИТЕКТУРА:
Input → Hidden → Output
(вход)  (скрытый) (выход)

ОБУЧЕНИЕ:
1. Forward Pass - прямое распространение
   Вычисляем выход сети
   
2. Backward Pass - обратное распространение
   Вычисляем градиенты
   Обновляем веса

ФУНКЦИИ АКТИВАЦИИ:
- Sigmoid: для выхода (вероятности)
- ReLU: для скрытых слоёв (популярна!)
- Tanh: для скрытых слоёв

ВОЗМОЖНОСТИ:
✓ Нелинейные задачи (XOR!)
✓ Универсальный аппроксиматор
✓ Основа глубокого обучения

СЛЕДУЮЩИЙ ШАГ:
Использовать готовые библиотеки (Keras)!
""")

print("\n MLP освоен!")
print("="*60)    




# ============================================
# PROSTOE OBYASNENIE (dlya ponimaniya)
# ============================================

print("\n" + "="*60)
print("ПРОСТЫМИ СЛОВАМИ:")
print("="*60)

print("""
╔════════════════════════════════════════════════╗
║     КАК РАБОТАЕТ НЕЙРОСЕТЬ - ПРОСТАЯ АНАЛОГИЯ ║
╚════════════════════════════════════════════════╝

ПРЕДСТАВЬТЕ ФАБРИКУ:

1. ВХОДНОЙ КОНВЕЙЕР (Input Layer)
   Сюда приходят сырые материалы: X1, X2
   Например: [0, 1] - два числа

2. РАБОЧИЕ (Hidden Layer - скрытый слой)
   Каждый рабочий:
   - Берёт ВСЕ материалы (X1 и X2)
   - Умножает на свой коэффициент (вес)
   - Складывает результаты
   - Решает: передавать дальше или нет (активация)
   
   Пример для Рабочего #1:
   Получил: X1=0, X2=1
   Его веса: W1=0.5, W2=0.3
   Считает: 0*0.5 + 1*0.3 = 0.3
   Активация sigmoid(0.3) ≈ 0.57
   Передаёт дальше: 0.57

3. НАЧАЛЬНИК (Output Layer - выходной слой)
   Получает результаты от ВСЕХ рабочих
   Делает финальное решение: 0 или 1

ОБУЧЕНИЕ:

Сначала веса случайные (рабочие не знают что делать)
Показываем примеры:
[0,1] должно дать 1 → сеть дала 0.3 → ОШИБКА!

Обратное распространение = "разбор полётов":
Начальник говорит: "Я ошибся, надо было больше"
Рабочие спрашивают: "А нам как изменить коэффициенты?"
Математика вычисляет: насколько изменить каждый вес

После 1000 таких разборов - все научились!

╔════════════════════════════════════════════════╗
║           BACKPROPAGATION БЕЗ МАТЕМАТИКИ      ║
╚════════════════════════════════════════════════╝

Обычное объяснение (сложное):
"Вычисляем градиент функции потерь..."

ПРОСТОЕ ОБЪЯСНЕНИЕ:

1. Получили ошибку на выходе
   Ожидали: 1, Получили: 0.3
   Ошибка = 1 - 0.3 = 0.7 (надо увеличить!)

2. Спрашиваем выходной нейрон:
   "Насколько чувствителен твой выход к входу?"
   Производная sigmoid говорит: "Очень чувствителен!"
   
3. Распространяем "вину" на скрытый слой:
   Каждый скрытый нейрон получает часть ошибки
   Пропорционально его вкладу (весу связи)
   
4. Обновляем веса:
   Если нейрон способствовал ошибке → уменьшаем его вес
   Если помогал → увеличиваем вес

╔════════════════════════════════════════════════╗
║              ЗАЧЕМ ПРОИЗВОДНЫЕ?               ║
╚════════════════════════════════════════════════╝

Производная = "чувствительность"

Представьте руль автомобиля:
- Маленький поворот руля → большой поворот машины = высокая производная
- Большой поворот руля → малый поворот машины = низкая производная

В нейросетях:
sigmoid_derivative говорит:
"Если я изменю ВХОД на 0.1, насколько изменится ВЫХОД?"

Это нужно, чтобы понять:
- Стоит ли менять этот вес? (если производная большая - да!)
- На сколько менять? (пропорционально производной)

╔════════════════════════════════════════════════╗
║                ПОЧЕМУ MLP ЛУЧШЕ?              ║
╚════════════════════════════════════════════════╝

ПЕРЦЕПТРОН (1 слой):
Может провести только ОДНУ прямую линию
Разделить данные на 2 части

Пример: может разделить это ✓
   O O O | X X X
   
Не может разделить это ✗ (XOR):
   X O O X
   O X X O
   
MLP (2+ слоя):
Первый слой проводит несколько линий
Второй слой комбинирует их
Может создать ЛЮБУЮ границу!

Пример: может разделить XOR ✓
   Использует 2 линии, которые пересекаются

╔════════════════════════════════════════════════╗
║            ЧАСТЫЕ ВОПРОСЫ                     ║
╚════════════════════════════════════════════════╝

Q: Почему веса случайные вначале?
A: Если все одинаковые - все нейроны будут учиться одинаково!
   Случайность = разнообразие = лучше обучение

Q: Что если убрать функцию активации?
A: Сеть станет линейной! Слои схлопнутся в один
   10 слоёв без активации = 1 слой
   С активацией - каждый слой добавляет нелинейность

Q: Почему learning_rate маленький?
A: Большой = быстро, но перескакиваем минимум
   Маленький = медленно, но точно
   Как спуск с горы: большие шаги - можно упасть!

Q: Сколько нужно скрытых нейронов?
A: Эмпирическое правило:
   - Между количеством входов и выходов
   - Для XOR: 2 входа, 1 выход → 2-4 скрытых
   - Экспериментируйте!

Q: Почему 1000 эпох?
A: Одна эпоха = 1 проход по всем данным
   Нужно много проходов чтобы веса "устоялись"
   Следите за loss - если перестал падать, хватит!
""")

# ============================================
# NAGLYADNYY PRIMER
# ============================================

print("\n" + "="*60)
print("НАГЛЯДНЫЙ ПРИМЕР:")
print("="*60)

print("""
Давайте посмотрим что происходит ВНУТРИ:

Задача: XOR, вход [1, 0]
Правильный ответ: 1

ДО ОБУЧЕНИЯ:
""")

mlp_demo = MLP(input_size=2, hidden_size=2, output_size=1)
output_before = mlp_demo.forward(np.array([[1, 0]]))

print(f"Вход: [1, 0]")
print(f"Скрытый слой активации: {mlp_demo.a1[0]}")
print(f"Выход сети: {output_before[0][0]:.4f}")
print(f"Правильный ответ: 1")
print(f"Ошибка: {abs(1 - output_before[0][0]):.4f}")

print("""
ПОСЛЕ ОБУЧЕНИЯ:
""")

mlp_demo.train(X_xor, y_xor, epochs=1000)
output_after = mlp_demo.forward(np.array([[1, 0]]))

print(f"Вход: [1, 0]")
print(f"Скрытый слой активации: {mlp_demo.a1[0]}")
print(f"Выход сети: {output_after[0][0]:.4f}")
print(f"Правильный ответ: 1")
print(f"Ошибка: {abs(1 - output_after[0][0]):.4f}")

print("""
ВИДИТЕ?
- Скрытый слой изменился (научился находить паттерны)
- Выход стал ближе к 1
- Ошибка уменьшилась!

Это и есть обучение - подбор весов!
""")