import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# TensorFlow i Keras
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Otklyuchaem preduprezhdeniya
import warnings
warnings.filterwarnings('ignore')

sns.set_theme()
np.random.seed(42)
tf.random.set_seed(42)

print("="*60)
print("KERAS - Prostoe sozdanie neyrosetey")
print("="*60)


print("""
KERAS - библиотека для создания нейросетей

ПРОСТЫМИ СЛОВАМИ:
Вместо того чтобы писать MLP с нуля (как в файле 02)
Используем готовые блоки!

БЫЛО (сложно):
class MLP:
    def __init__...
    def forward...
    def backward...
    100+ строк кода

СТАЛО (просто):
model = Sequential([
    Dense(4, activation='sigmoid'),
    Dense(1, activation='sigmoid')
])
3 строки кода!

KERAS = КОНСТРУКТОР LEGO
Берёшь готовые блоки (слои)
Складываешь в нужном порядке
Нажимаешь "обучить"
Готово!
""")

# ============================================
# PRIMER 1: XOR NA KERAS
# ============================================

print("\n" + "="*60)
print("Пример 1: XOR на Keras")
print("="*60)

# Данные (те же что раньше)
X_xor = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

y_xor = np.array([0, 1, 1, 0])

print("Данные XOR:")
for x, y in zip(X_xor, y_xor):
    print(f"  {x} → {y}")

# Создание модели
print("\nСоздаём модель...")

model = Sequential([
    Dense(4, activation='sigmoid', input_shape=(2,)),
    Dense(1, activation='sigmoid')
])
"""
Sequential - модель где слои идут ПОСЛЕДОВАТЕЛЬНО
один за другим

Dense - ПОЛНОСВЯЗНЫЙ слой
каждый нейрон соединён со всеми из предыдущего

Разбор:
1. Dense(4, ...) - слой из 4 нейронов (скрытый)
   activation='sigmoid' - используем sigmoid
   input_shape=(2,) - входов 2 (X1, X2)

2. Dense(1, ...) - слой из 1 нейрона (выход)
   activation='sigmoid' - выход 0-1

ИТОГО: 2 входа → 4 скрытых → 1 выход
Точно как мы делали вручную!
"""

print("\nАрхитектура:")
model.summary()
"""
summary() показывает:
- Слои
- Количество параметров (весов)
- Форму данных

Параметры = веса которые надо обучить
Чем больше - тем мощнее сеть (но медленнее)
"""

# Компиляция
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)
"""
compile - настройка обучения

optimizer='adam' - АЛГОРИТМ обновления весов
  Adam = улучшенная версия gradient descent
  Самый популярный!
  Автоматически подбирает learning rate

loss='binary_crossentropy' - ФУНКЦИЯ ОШИБКИ
  Для бинарной классификации (0 или 1)
  Измеряет насколько плохо предсказание

metrics=['accuracy'] - ЧТО СМОТРЕТЬ
  Accuracy = процент правильных ответов
  Удобно для оценки
"""

# Обучение
print("\nОбучение модели...")

history = model.fit(
    X_xor, y_xor,
    epochs=500,
    verbose=0
)
"""
fit - ОБУЧЕНИЕ!

X_xor, y_xor - данные
epochs=500 - сколько раз пройти по данным
verbose=0 - не печатать прогресс (тихо)
  verbose=1 - показывать прогресс
  verbose=2 - показывать только эпохи

history - история обучения
  Сохраняет loss, accuracy на каждой эпохе
"""

print("✓ Обучение завершено!")

# Тестирование
print("\nРезультаты:")
predictions = model.predict(X_xor, verbose=0)
predictions_binary = (predictions > 0.5).astype(int)

for x, y_true, y_pred, y_prob in zip(X_xor, y_xor, predictions_binary, predictions):
    correct = "✓" if y_pred[0] == y_true else "✗"
    print(f"  {x} → предсказано: {y_pred[0]}, вероятность: {y_prob[0]:.3f}, правильно: {y_true} {correct}")

print("""
ВИДитЕ?
- Вероятность близка к 0 или 1
- Бинарное предсказание правильное
- Keras решил XOR!

И это всего в несколько строк кода!
""")

# ============================================
# VIZUALIZATSIYA OBUCHENIYA
# ============================================

print("\nВизуализация обучения...")

plt.figure(figsize=(12, 5))

# График 1: Loss
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], linewidth=2)
plt.title('Изменение ошибки (Loss)', fontweight='bold', fontsize=14)
plt.xlabel('Эпоха')
plt.ylabel('Loss')
plt.grid(True, alpha=0.3)

# График 2: Accuracy
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], linewidth=2, color='green')
plt.title('Точность (Accuracy)', fontweight='bold', fontsize=14)
plt.xlabel('Эпоха')
plt.ylabel('Accuracy')
plt.ylim(0, 1.1)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("""
График показывает:
- Loss падает → сеть учится!
- Accuracy растёт → всё лучше предсказывает!

Если Loss перестал падать → можно остановить
""")

# ============================================
# SOHRANENIE I ZAGRUZKA
# ============================================

print("\n" + "="*60)
print("Сохранение и загрузка модели")
print("="*60)

# Сохранить
model.save('xor_model.h5')
print("✓ Модель сохранена в xor_model.h5")

# Загрузить
loaded_model = keras.models.load_model('xor_model.h5')
print("✓ Модель загружена")

# Проверить что работает
test_pred = loaded_model.predict(np.array([[1, 0]]), verbose=0)
print(f"\nТест загруженной модели:")
print(f"  Вход [1, 0] → {test_pred[0][0]:.3f} (должно быть ~1)")

print("""
Сохранение модели нужно чтобы:
- Не обучать заново каждый раз
- Поделиться с другими
- Использовать в production

Формат .h5 - стандартный для Keras
""")

# ============================================
# REZYUME
# ============================================

print("\n" + "="*60)
print("РЕЗЮМЕ:")
print("="*60)

print("""
KERAS - ПРОСТОЕ СОЗДАНИЕ НЕЙРОСЕТЕЙ

ТРИ ШАГА:

1. СОЗДАТЬ МОДЕЛЬ
   model = Sequential([...слои...])

2. КОМПИЛИРОВАТЬ
   model.compile(optimizer, loss, metrics)

3. ОБУЧИТЬ
   model.fit(X, y, epochs)

ГЛАВНЫЕ КОМПОНЕНТЫ:

Sequential - последовательная модель
Dense - полносвязный слой
activation - функция активации
optimizer - алгоритм обучения
loss - функция ошибки

ПРЕИМУЩЕСТВА:
✓ Просто (3 строки вместо 100)
✓ Быстро
✓ Много готовых функций
✓ Автоматическое дифференцирование

НЕДОСТАТКИ:
✗ "Чёрный ящик" (не видно что внутри)
✗ Тяжелее понять ошибки

НО: Знание основ (файл 02) помогает
понять ЧТО делает Keras внутри!
""")

print("\n Keras освоен!")
print("="*60)