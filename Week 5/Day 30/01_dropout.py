import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import warnings
warnings.filterwarnings('ignore')

sns.set_theme()
np.random.seed(42)

print("="*60)
print("DROPOUT - Borba s pereobucheniem")
print("="*60)


print("\n" + "="*60)
print("Создаём данные (специально сложные)")
print("="*60)

# Создаём сложную задачу
X, y = make_classification(
    n_samples=1000,
    n_features=20,
    n_informative=15,
    n_redundant=5,
    random_state=42
)


"""
make_classification - создаёт данные для классификации

n_samples=1000 - 1000 примеров
n_features=20 - 20 признаков
n_informative=15 - 15 полезных
n_redundant=5 - 5 лишних (шум)

Специально создаём сложную задачу чтобы показать переобучение!
"""

print(f"Данных: {len(X)}")
print(f"Признаков: {X.shape[1]}")
print(f"Классов: {len(np.unique(y))}")

# Масштабирование
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

print(f"Train: {len(X_train)}")
print(f"Test: {len(X_test)}")


print("\n" + "="*60)
print("МОДЕЛЬ 1: БЕЗ Dropout (переобучится!)")
print("="*60)

model_no_dropout = Sequential([
    Dense(64, activation='relu', input_shape=(20,)),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])
"""
Архитектура: 20 → 64 → 32 → 16 → 1

Много нейронов = легко переобучится!
Специально делаем большую сеть
"""

model_no_dropout.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("Обучаем модель БЕЗ dropout...")
print("(специально много эпох чтобы показать переобучение)")

history_no_dropout = model_no_dropout.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    verbose=0
)

# Оценка
train_acc_no = model_no_dropout.evaluate(X_train, y_train, verbose=0)[1]
test_acc_no = model_no_dropout.evaluate(X_test, y_test, verbose=0)[1]

print(f"\nРезультаты БЕЗ Dropout:")
print(f"  Train accuracy: {train_acc_no:.2%}")
print(f"  Test accuracy: {test_acc_no:.2%}")
print(f"  Разница: {(train_acc_no - test_acc_no)*100:.1f}%")
"""
Разница большая (>5-10%) = ПЕРЕОБУЧЕНИЕ!

Train: 95%, Test: 85% → модель запомнила train
но плохо обобщает на новые данные
"""

print("\n" + "="*60)
print("МОДЕЛЬ 2: С Dropout (НЕ переобучится!)")
print("="*60)

model_with_dropout = Sequential([
    Dense(64, activation='relu', input_shape=(20,)),
    Dropout(0.5),
    Dense(32, activation='relu'),
    Dropout(0.5),
    Dense(16, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])
"""
НОВОЕ: Dropout слои!

Dropout(0.5) - выключить 50% нейронов
Dropout(0.3) - выключить 30% нейронов

КУДА СТАВИТЬ:
После Dense слоёв (перед или после активации - работает)
НЕ ставим после последнего слоя!

СКОЛЬКО ВЫКЛЮЧАТЬ:
0.3 - 0.5 - стандартно (30-50%)
0.2 - слабый dropout
0.7 - сильный dropout (может недообучить)

ЛОГИКА:
Первые слои: больше dropout (0.5)
Последние слои: меньше dropout (0.3)
"""

model_with_dropout.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("Обучаем модель С dropout...")

history_with_dropout = model_with_dropout.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    verbose=0
)

# Оценка
train_acc_with = model_with_dropout.evaluate(X_train, y_train, verbose=0)[1]
test_acc_with = model_with_dropout.evaluate(X_test, y_test, verbose=0)[1]

print(f"\nРезультаты С Dropout:")
print(f"  Train accuracy: {train_acc_with:.2%}")
print(f"  Test accuracy: {test_acc_with:.2%}")
print(f"  Разница: {(train_acc_with - test_acc_with)*100:.1f}%")
"""
Разница маленькая (<5%) = НЕТ переобучения!

Train: 88%, Test: 87% → модель обобщает хорошо!
Train чуть ниже чем без dropout - это НОРМАЛЬНО
Зато Test лучше!
"""

print("\n" + "="*60)
print("СРАВНЕНИЕ:")
print("="*60)

comparison = pd.DataFrame({
    'Модель': ['БЕЗ Dropout', 'С Dropout'],
    'Train Acc': [train_acc_no, train_acc_with],
    'Test Acc': [test_acc_no, test_acc_with],
    'Разница': [
        (train_acc_no - test_acc_no)*100,
        (train_acc_with - test_acc_with)*100
    ]
})

print("\n" + comparison.to_string(index=False))

print("""
ВЫВОДЫ:

БЕЗ DROPOUT:
- Train выше (модель "умнее" на обучающих данных)
- Test ниже (плохо обобщает)
- Большая разница = ПЕРЕОБУЧЕНИЕ

С DROPOUT:
- Train чуть ниже (это нормально!)
- Test выше! (лучше обобщает!)
- Маленькая разница = НЕТ переобучения

ГЛАВНОЕ: Test accuracy ВЫШЕ → Dropout работает! ✓
""")


print("\nВизуализация обучения...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# График 1: Loss БЕЗ dropout
axes[0, 0].plot(history_no_dropout.history['loss'], label='Train', linewidth=2)
axes[0, 0].plot(history_no_dropout.history['val_loss'], label='Validation', linewidth=2)
axes[0, 0].set_title('Loss БЕЗ Dropout', fontweight='bold', fontsize=14)
axes[0, 0].set_xlabel('Эпоха')
axes[0, 0].set_ylabel('Loss')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# График 2: Loss С dropout
axes[0, 1].plot(history_with_dropout.history['loss'], label='Train', linewidth=2)
axes[0, 1].plot(history_with_dropout.history['val_loss'], label='Validation', linewidth=2)
axes[0, 1].set_title('Loss С Dropout', fontweight='bold', fontsize=14)
axes[0, 1].set_xlabel('Эпоха')
axes[0, 1].set_ylabel('Loss')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# График 3: Accuracy БЕЗ dropout
axes[1, 0].plot(history_no_dropout.history['accuracy'], label='Train', linewidth=2)
axes[1, 0].plot(history_no_dropout.history['val_accuracy'], label='Validation', linewidth=2)
axes[1, 0].set_title('Accuracy БЕЗ Dropout', fontweight='bold', fontsize=14)
axes[1, 0].set_xlabel('Эпоха')
axes[1, 0].set_ylabel('Accuracy')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# График 4: Accuracy С dropout
axes[1, 1].plot(history_with_dropout.history['accuracy'], label='Train', linewidth=2)
axes[1, 1].plot(history_with_dropout.history['val_accuracy'], label='Validation', linewidth=2)
axes[1, 1].set_title('Accuracy С Dropout', fontweight='bold', fontsize=14)
axes[1, 1].set_xlabel('Эпоха')
axes[1, 1].set_ylabel('Accuracy')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("""
ЧТО ВИДНО НА ГРАФИКАХ:

БЕЗ DROPOUT (слева):
- Train и Validation расходятся
- Train растёт, Validation останавливается
- Признак ПЕРЕОБУЧЕНИЯ!

С DROPOUT (справа):
- Train и Validation идут вместе
- Обе растут примерно одинаково
- НЕТ переобучения!
""")

# ============================================
# REZYUME
# ============================================

print("\n" + "="*60)
print("РЕЗЮМЕ:")
print("="*60)

print(f"""
DROPOUT - простой способ борьбы с переобучением

КАК РАБОТАЕТ:
1. Случайно выключает нейроны во время обучения
2. Каждый нейрон учится работать независимо
3. При предсказании все нейроны работают

КОД:
from tensorflow.keras.layers import Dropout

model = Sequential([
    Dense(64, activation='relu'),
    Dropout(0.5),  # ← 50% нейронов выключить
    Dense(32, activation='relu'),
    Dropout(0.3),  # ← 30% нейронов выключить
    Dense(1, activation='sigmoid')
])

КОГДА ИСПОЛЬЗОВАТЬ:
✓ Большая сеть (много нейронов)
✓ Мало данных
✓ Видно переобучение (Train >> Test)

СКОЛЬКО ВЫКЛЮЧАТЬ:
- 0.3-0.5 (30-50%) - стандартно
- Больше в первых слоях, меньше в последних

РЕЗУЛЬТАТЫ СЕГОДНЯ:
БЕЗ Dropout: Train {train_acc_no:.1%}, Test {test_acc_no:.1%}
С Dropout:   Train {train_acc_with:.1%}, Test {test_acc_with:.1%}

Test accuracy ВЫШЕ с Dropout → РАБОТАЕТ! ✓
""")

print("\n Dropout освоен!")
print("="*60)