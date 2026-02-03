# 05_final_test.py - Itogovyy test po neyrosetyam

import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("ИТОГОВЫЙ ТЕСТ: Проверка понимания")
print("="*60)

print("""
Сейчас вы создадите нейросеть САМИ!

ЗАДАЧА: Классификация цветов Iris

У вас есть данные о цветках:
- sepal_length (длина чашелистика)
- sepal_width (ширина чашелистика)
- petal_length (длина лепестка)
- petal_width (ширина лепестка)

Надо предсказать вид:
- 0 = setosa
- 1 = versicolor
- 2 = virginica

Попробуйте сделать сами!
""")

# Загрузка данных
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

iris = load_iris()
X = iris.data
y = iris.target

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

print(f"\nTrain: {len(X_train)}")
print(f"Test: {len(X_test)}")

# ============================================
# VASH KOD ZDES!
# ============================================

print("\n" + "="*60)
print("Создаём модель...")
print("="*60)

# ПОДСКАЗКА: Это задача с 3 классами!
# Выходной слой должен быть Dense(3, activation='softmax')
# softmax - для многоклассовой классификации

model = Sequential([
    Dense(8, activation='relu', input_shape=(4,)),
    Dense(6, activation='relu'),
    Dense(3, activation='softmax')  # 3 класса!
])
"""
НОВОЕ: softmax вместо sigmoid!

sigmoid - для 2 классов (0 или 1)
softmax - для 3+ классов (0, 1, 2, ...)

softmax даёт вероятности для КАЖДОГО класса:
[0.1, 0.7, 0.2] = 10% что класс 0, 70% что класс 1, 20% что класс 2
Сумма = 1.0
"""

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',  # для 3+ классов
    metrics=['accuracy']
)
"""
НОВОЕ: sparse_categorical_crossentropy

binary_crossentropy - для 2 классов
sparse_categorical_crossentropy - для 3+ классов

'sparse' означает что y = [0, 1, 2]
(без sparse надо y = [[1,0,0], [0,1,0], [0,0,1]])
"""

print("Обучаем...")
history = model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=16,
    validation_split=0.2,
    verbose=0
)

# Оценка
test_acc = model.evaluate(X_test, y_test, verbose=0)[1]

print(f"\n✓ Обучение завершено!")
print(f"Test Accuracy: {test_acc:.2%}")

if test_acc > 0.90:
    print("🎉 ОТЛИЧНО! Модель работает хорошо!")
elif test_acc > 0.80:
    print("👍 Хорошо! Попробуйте улучшить!")
else:
    print("🤔 Можно лучше. Попробуйте:")
    print("  - Больше эпох")
    print("  - Больше нейронов")
    print("  - Другую архитектуру")

# Предсказание
print("\nПример предсказания:")
sample = X_test[:3]
predictions = model.predict(sample, verbose=0)

for i, (x, pred) in enumerate(zip(sample, predictions)):
    pred_class = np.argmax(pred)  # класс с максимальной вероятностью
    true_class = y_test[i]
    
    print(f"\nЦветок {i+1}:")
    print(f"  Вероятности: {pred}")
    print(f"  Предсказан класс: {pred_class} ({iris.target_names[pred_class]})")
    print(f"  Правильный класс: {true_class} ({iris.target_names[true_class]})")
    print(f"  {'✓ Верно!' if pred_class == true_class else '✗ Ошибка'}")

print("\n" + "="*60)
print("РЕЗЮМЕ ТЕСТА:")
print("="*60)

print(f"""
ВЫ СОЗДАЛИ НЕЙРОСЕТЬ ДЛЯ 3 КЛАССОВ!

НОВОЕ что узнали:
- softmax для многоклассовой классификации
- sparse_categorical_crossentropy для 3+ классов
- np.argmax() для выбора класса с максимальной вероятностью

АРХИТЕКТУРА:
4 входа → 8 нейронов → 6 нейронов → 3 выхода

РЕЗУЛЬТАТ:
Accuracy: {test_acc:.2%}

Iris - классическая задача в ML!
Вы её решили нейросетью! 🎉
""")

print("\n✅ Итоговый тест пройден!")
print("="*60)