import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

import warnings
warnings.filterwarnings('ignore')

sns.set_theme()
np.random.seed(42)

print("="*60)
print("ПЕРВАЯ CNN НА KERAS")
print("Распознавание рукописных цифр MNIST")
print("="*60)



print("\n" + "="*60)
print("ШАГ 1: Загрузка данных MNIST")
print("="*60)

# Загружаем MNIST
(X_train, y_train), (X_test, y_test) = mnist.load_data()
"""
mnist.load_data() - встроенный датасет в Keras

Автоматически скачивает и загружает данные
Возвращает:
- X_train: картинки для обучения
- y_train: метки (цифры) для обучения
- X_test: картинки для теста
- y_test: метки для теста
"""

print(f"✓ Данные загружены!")
print(f"  Train картинок: {len(X_train)}")
print(f"  Test картинок: {len(X_test)}")
print(f"  Размер одной картинки: {X_train[0].shape}")

# Посмотрим на примеры
print("\nПримеры картинок:")

plt.figure(figsize=(12, 3))
for i in range(10):
    plt.subplot(2, 5, i+1)
    plt.imshow(X_train[i], cmap='gray')
    plt.title(f'Метка: {y_train[i]}', fontsize=10)
    plt.axis('off')
plt.tight_layout()
plt.show()

print("""
Что мы видим:
- Размытые рукописные цифры
- Разные стили написания
- Задача: научить компьютер их различать!
""")


print("\n" + "="*60)
print("ШАГ 2: Подготовка данных")
print("="*60)

# Добавляем канал (для CNN нужен формат 4D)
X_train = X_train.reshape(-1, 28, 28, 1)
X_test = X_test.reshape(-1, 28, 28, 1)
"""
ВАЖНО! Формат данных для CNN:

Было: (60000, 28, 28) 
  60000 картинок
  28x28 пикселей

Стало: (60000, 28, 28, 1)
  60000 картинок
  28x28 пикселей
  1 канал (чёрно-белое)

Формат для CNN: (количество, высота, ширина, каналы)

-1 в reshape означает "вычисли сам"
Берёт всё что есть (60000)
"""

print(f"Форма после reshape:")
print(f"  X_train: {X_train.shape}")
print(f"  X_test: {X_test.shape}")

# Нормализация (0-255 → 0-1)
X_train = X_train.astype('float32') / 255.0
X_test = X_test.astype('float32') / 255.0
"""
ЗАЧЕМ НОРМАЛИЗАЦИЯ:

Было: значения от 0 до 255 (яркость пикселя)
Стало: значения от 0 до 1

ПОЧЕМУ:
1. Нейросети лучше работают с маленькими числами
2. Все признаки в одном масштабе
3. Обучение быстрее и стабильнее
"""

print(f"\nДиапазон значений после нормализации:")
print(f"  Min: {X_train.min()}")
print(f"  Max: {X_train.max()}")

# One-hot encoding для меток
y_train_cat = to_categorical(y_train, 10)
y_test_cat = to_categorical(y_test, 10)
"""
ONE-HOT ENCODING для классов

Было (метка): 3
Стало (one-hot): [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
                           ↑
                        позиция 3

Цифра 0: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Цифра 5: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]

ЗАЧЕМ:
Для многоклассовой классификации
Выход сети = вероятности для каждого класса
"""

print(f"\nПример one-hot encoding:")
print(f"  Цифра (метка): {y_train[0]}")
print(f"  One-hot: {y_train_cat[0]}")

print("\n✓ Данные готовы!")


print("\n" + "="*60)
print("ШАГ 3: Создание CNN")
print("="*60)

print("""
АРХИТЕКТУРА НАШЕЙ CNN:

Вход: 28x28x1 (картинка)
  ↓
Conv2D (32 фильтра 3x3) + ReLU
  ↓ находит простые паттерны (линии, углы)
MaxPooling 2x2
  ↓ уменьшает 28x28 → 14x14
Conv2D (64 фильтра 3x3) + ReLU
  ↓ находит сложные паттерны (формы цифр)
MaxPooling 2x2
  ↓ уменьшает 14x14 → 7x7
Flatten
  ↓ превращает 7x7x64 в одномерный вектор
Dense(128) + ReLU + Dropout
  ↓ обычный слой для обработки
Dense(10) + Softmax
  ↓ финальное решение: вероятность каждой цифры

Выход: [вероятности 10 цифр]
""")

model = Sequential([
    # БЛОК 1: Свёртка + Pooling
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    
    # БЛОК 2: Свёртка + Pooling
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    # ВЫРАВНИВАНИЕ
    Flatten(),
    
    # ПОЛНОСВЯЗНЫЕ СЛОИ
    Dense(128, activation='relu'),
    Dropout(0.5),
    
    # ВЫХОД
    Dense(10, activation='softmax')
])
"""
ПОДРОБНО О КАЖДОМ СЛОЕ:

Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1))
  32 - количество фильтров
    Каждый фильтр ищет свой паттерн
    32 фильтра = 32 разных паттерна
  (3, 3) - размер фильтра
    Окошко 3x3 скользит по картинке
  activation='relu' - функция активации
    Убирает отрицательные значения
  input_shape=(28, 28, 1) - размер входа
    Только для ПЕРВОГО слоя!

MaxPooling2D((2, 2))
  (2, 2) - размер окна pooling
    Берём квадрат 2x2, выбираем максимум
    Уменьшает размер в 2 раза

Conv2D(64, (3, 3), activation='relu')
  64 фильтра - больше чем в первом слое
    Ищет более сложные паттерны
  Размер фильтра тот же (3x3)

Flatten()
  Превращает 3D в 1D
  Пример: (7, 7, 64) → (3136,)
  Нужно для Dense слоёв

Dense(128, activation='relu')
  Обычный полносвязный слой
  128 нейронов
  Обрабатывает найденные паттерны

Dropout(0.5)
  Выключает 50% нейронов при обучении
  Против переобучения!

Dense(10, activation='softmax')
  10 нейронов = 10 цифр (0-9)
  softmax даёт вероятности
  Сумма вероятностей = 1.0
"""

print("\n✓ Модель создана!")
print("\nАрхитектура:")
model.summary()

print("""
ЧТО ВИДИМ В SUMMARY:

Output Shape - размер после каждого слоя:
  (None, 26, 26, 32) - после 1-й свёртки
    None = количество примеров (любое)
    26x26 = размер (было 28x28, стало меньше из-за фильтра 3x3)
    32 = количество фильтров

Param # - количество обучаемых параметров:
  Больше параметров = мощнее модель
  Но больше риск переобучения

Total params - всего параметров для обучения
""")


print("\n" + "="*60)
print("ШАГ 4: Компиляция")
print("="*60)

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
"""
optimizer='adam'
  Умный алгоритм обучения
  Автоматически подбирает скорость

loss='categorical_crossentropy'
  Функция ошибки для многоклассовой классификации
  Измеряет: насколько плохо предсказание

metrics=['accuracy']
  Процент правильных ответов
  Удобно для оценки
"""


print("✓ Модель скомпилирована!")




print("\n" + "="*60)
print("ШАГ 5: ОБУЧЕНИЕ")
print("="*60)

print("Начинаем обучение...")
print("(это займёт 1-2 минуты)")

import time
start_time = time.time()

history = model.fit(
    X_train, y_train_cat,
    epochs=5,
    batch_size=128,
    validation_split=0.1,
    verbose=1
)
"""
epochs=5
  Пройти по данным 5 раз
  Больше эпох = дольше, но лучше
  5 достаточно для MNIST

batch_size=128
  Обновлять веса после каждых 128 картинок
  Баланс скорости и стабильности

validation_split=0.1
  10% train → для проверки
  Смотрим не переобучается ли

verbose=1
  Показывать прогресс
  Видим loss и accuracy на каждой эпохе
"""

training_time = time.time() - start_time

print(f"\n✓ Обучение завершено за {training_time:.1f} секунд!")


print("\n" + "="*60)
print("ШАГ 6: Оценка на тестовых данных")
print("="*60)

test_loss, test_accuracy = model.evaluate(X_test, y_test_cat, verbose=0)

print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")

print("""
ЧТО ОЗНАЧАЕТ ACCURACY:

98% accuracy = правильно распознал 98 из 100 цифр!

ЭТО ОТЛИЧНО для первой CNN!
Человек делает ошибки в ~2-3%

CNN научилась распознавать рукописные цифры!
""")
