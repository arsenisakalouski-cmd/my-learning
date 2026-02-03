import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

import warnings
warnings.filterwarnings('ignore')

sns.set_theme()
np.random.seed(42)

print("="*60)
print("PROSTOY PRIMER: Predkazanie pokupki tovara")
print("="*60)

print("""
╔════════════════════════════════════════════════╗
║                  ЗАДАЧА                       ║
╚════════════════════════════════════════════════╝

МАГАЗИН хочет предсказать: купит ли человек товар?

ДАННЫЕ О КЛИЕНТЕ:
1. Возраст (18-70 лет)
2. Доход (тысяч рублей в месяц)
3. Время на сайте (минут)

РЕЗУЛЬТАТ:
0 = НЕ купил
1 = КУПИЛ

ПРИМЕР:
Человек: возраст=25, доход=50, время=10
Купил? 1 (да)

Человек: возраст=60, доход=30, время=2  
Купил? 0 (нет)

Создадим нейросеть которая это предскажет!
""")


print("\n" + "="*60)
print("Шаг 1: Создаём данные")
print("="*60)


n = 200 

vozrast = np.random.randint(18 , 70 , n)
dokhod = np.random.randint(20, 150, n)
vremya = np.random.randint(1, 60, n)

# Формула покупки (упрощённая)
"""
Логика покупки:
- Молодые с высоким доходом → обычно покупают
- Много времени на сайте → интересуются → покупают
- Низкий доход и мало времени → не покупают

Делаем формулу:
"""

kupil = []
for v, d, vr in zip(vozrast, dokhod, vremya):
    # Считаем "склонность к покупке"
    sklonnost = (
        (70 - v) * 0.01 +      # молодые лучше
        d * 0.02 +              # богатые лучше  
        vr * 0.03               # долго на сайте лучше
    )
    
    # Добавляем случайность
    sklonnost += np.random.normal(0, 0.5)
    
    # Если склонность > порога → купил
    if sklonnost > 2:
        kupil.append(1)
    else:
        kupil.append(0)

kupil = np.array(kupil)

df = pd.DataFrame({
    'vozrast': vozrast,
    'dokhod': dokhod,
    'vremya': vremya,
    'kupil': kupil
})

print(f"Создано {len(df)} клиентов")
print(f"Купили: {kupil.sum()} ({kupil.sum()/len(kupil)*100:.1f}%)")
print(f"Не купили: {len(kupil) - kupil.sum()} ({(len(kupil)-kupil.sum())/len(kupil)*100:.1f}%)")

print("\nПервые 5 клиентов:")
print(df.head())


print("\n" + "="*60)
print("Шаг 2: Подготовка данных")
print("="*60)

# Признаки (X) и цель (y)
X = df[['vozrast', 'dokhod', 'vremya']].values
y = df['kupil'].values

print(f"X shape: {X.shape}")
"""
(200, 3) означает:
200 - примеров (клиентов)
3 - признака (возраст, доход, время)
"""

print(f"y shape: {y.shape}")
"""
(200,) означает:
200 - ответов (купил/не купил)
"""

# Масштабирование (ВАЖНО для нейросетей!)
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
"""
Зачем масштабирование?

БЕЗ масштабирования:
Возраст: 20-70 (десятки)
Доход: 20-150 (сотни)
Время: 1-60 (десятки)

Нейросеть подумает что доход НАМНОГО важнее!
(большие числа)

С масштабированием:
Все признаки: примерно от -2 до 2
Нейросеть видит все равными
"""

print("\nДо масштабирования:")
print(f"  Возраст: {X[:, 0].min():.0f} - {X[:, 0].max():.0f}")
print(f"  Доход: {X[:, 1].min():.0f} - {X[:, 1].max():.0f}")
print(f"  Время: {X[:, 2].min():.0f} - {X[:, 2].max():.0f}")

print("\nПосле масштабирования:")
print(f"  Возраст: {X_scaled[:, 0].min():.2f} - {X_scaled[:, 0].max():.2f}")
print(f"  Доход: {X_scaled[:, 1].min():.2f} - {X_scaled[:, 1].max():.2f}")
print(f"  Время: {X_scaled[:, 2].min():.2f} - {X_scaled[:, 2].max():.2f}")

# Разделение на train/test
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

print(f"\nTrain: {len(X_train)} примеров")
print(f"Test: {len(X_test)} примеров")


print("\n" + "="*60)
print("Шаг 3: Создаём нейросеть")
print("="*60)

print("""
Архитектура (рисунок):

    Вход (3)      Скрытый (8)    Скрытый (4)    Выход (1)
    
    vozrast ──┐      N1 ──┐        N1 ──┐
              │      N2   │        N2   │
    dokhod ───┼──►   N3   ├───►    N3   ├───► kupil?
              │      N4   │        N4   │
    vremya ──┘       ...  ┘             ┘
                     N8

Логика:
- 3 входа (наши признаки)
- 8 нейронов в первом скрытом (ищут паттерны)
- 4 нейрона во втором скрытом (комбинируют паттерны)
- 1 выход (вероятность покупки)
""")

model = Sequential([
    Dense(8, activation='relu', input_shape=(3,)),
    Dense(4, activation='relu'),
    Dense(1, activation='sigmoid')
])
"""
Разбор по частям:

Dense(8, activation='relu', input_shape=(3,))
  8 - нейронов в слое
  relu - функция активации (популярная!)
  input_shape=(3,) - входов 3 (возраст, доход, время)

Dense(4, activation='relu')
  4 - нейрона
  relu - снова relu (хорошо работает)

Dense(1, activation='sigmoid')
  1 - выход
  sigmoid - даёт вероятность 0-1

Почему ReLU в скрытых?
- Быстрая
- Хорошо работает
- Стандарт в индустрии

Почему sigmoid в выходе?
- Нужна вероятность (0-1)
- 0.8 = 80% шанс что купит
"""

print("\nСтруктура модели:")
model.summary()
"""
Читаем summary:

Layer (type)         Output Shape    Param #
dense (Dense)        (None, 8)       32
  32 параметра = 3 входа × 8 нейронов + 8 bias = 24 + 8 = 32

dense_1 (Dense)      (None, 4)       36
  36 параметров = 8 × 4 + 4 = 32 + 4 = 36

dense_2 (Dense)      (None, 1)       5
  5 параметров = 4 × 1 + 1 = 4 + 1 = 5

Total params: 73
Все эти 73 числа нейросеть будет учить!
"""


print("\n" + "="*60)
print("Шаг 4: Компилируем (настраиваем обучение)")
print("="*60)

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("""
Что выбрали:

optimizer='adam'
  Adam = умный алгоритм обучения
  Сам подбирает скорость
  Работает лучше чем простой gradient descent

loss='binary_crossentropy'
  Для задач "да/нет" (0 или 1)
  Сильно штрафует за уверенные ошибки:
    Предсказал 0.9, а правильно 0 → большой штраф
    Предсказал 0.6, а правильно 0 → средний штраф

metrics=['accuracy']
  Accuracy = процент правильных
  Удобно понимать: 0.85 = 85% правильных
""")



print("\n" + "="*60)
print("Шаг 6: Оценка модели")
print("="*60)

# На train
train_loss, train_acc = model.evaluate(X_train, y_train, verbose=0)
print(f"Train accuracy: {train_acc:.2%}")

# На test
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"Test accuracy: {test_acc:.2%}")

print("""
Что это значит?

Train accuracy: 85% = на обучающих данных 85% правильных
Test accuracy: 82% = на новых данных 82% правильных

ХОРОШО если:
- Test близко к Train (не переобучилась)
- Оба > 70-80%

ПЛОХО если:
- Train 95%, Test 60% → переобучение!
- Оба < 60% → модель слабая
""")

print("\n" + "="*60)
print("Шаг 7: Предсказания на новых клиентах")
print("="*60)

# Новые клиенты
novye_klienty = np.array([
    [25, 80, 30],   # молодой, средний доход, долго на сайте
    [60, 150, 5],   # старый, богатый, мало времени
    [30, 40, 45],   # молодой, бедный, очень долго
])

print("Новые клиенты:")
for i, k in enumerate(novye_klienty, 1):
    print(f"  {i}. Возраст: {k[0]}, Доход: {k[1]}к, Время: {k[2]}мин")

# Масштабируем (ВАЖНО!)
novye_scaled = scaler.transform(novye_klienty)
"""
ВАЖНО использовать тот же scaler!
Нельзя создавать новый - будут другие параметры!

Используем transform (не fit_transform!)
Применяем те же правила что на train
"""

# Предсказываем
predkazaniya = model.predict(novye_scaled, verbose=0)

print("\nПредсказания:")
for i, (k, p) in enumerate(zip(novye_klienty, predkazaniya), 1):
    prob = p[0]
    reshenie = "КУПИТ" if prob > 0.5 else "НЕ КУПИТ"
    print(f"  {i}. Возраст: {k[0]}, Доход: {k[1]}к, Время: {k[2]}мин")
    print(f"     → Вероятность: {prob:.1%}, Решение: {reshenie}")


print("\nВизуализация обучения...")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# График 1: Loss
axes[0].plot(history.history['loss'], label='Train', linewidth=2)
axes[0].plot(history.history['val_loss'], label='Validation', linewidth=2)
axes[0].set_title('Ошибка (Loss)', fontweight='bold', fontsize=14)
axes[0].set_xlabel('Эпоха')
axes[0].set_ylabel('Loss')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# График 2: Accuracy
axes[1].plot(history.history['accuracy'], label='Train', linewidth=2)
axes[1].plot(history.history['val_accuracy'], label='Validation', linewidth=2)
axes[1].set_title('Точность (Accuracy)', fontweight='bold', fontsize=14)
axes[1].set_xlabel('Эпоха')
axes[1].set_ylabel('Accuracy')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("""
Графики показывают:

ХОРОШО:
✓ Loss падает
✓ Accuracy растёт
✓ Train и Validation близки

ПЛОХО:
✗ Train падает, Validation растёт → переобучение
✗ Обе линии не меняются → модель не учится
""")

# ============================================
# REZYUME
# ============================================

print("\n" + "="*60)
print("РЕЗЮМЕ:")
print("="*60)

print(f"""
ЧТО СДЕЛАЛИ:

1. Создали данные о {n} клиентах
2. Подготовили (масштабирование!)
3. Создали нейросеть: 3 → 8 → 4 → 1
4. Обучили за 100 эпох
5. Получили accuracy: {test_acc:.1%}
6. Предсказали для новых клиентов

ВАЖНЫЕ МОМЕНТЫ:

✓ Масштабирование ОБЯЗАТЕЛЬНО для нейросетей
✓ ReLU в скрытых слоях - стандарт
✓ Sigmoid в выходе для вероятностей
✓ Adam optimizer - умный и популярный
✓ Validation показывает переобучение

СЛЕДУЮЩИЙ ШАГ:
Попробуйте поменять:
- Количество нейронов
- Количество слоёв
- Функции активации

И посмотрите как изменится accuracy!
""")

print("\n Практический пример завершён!")
print("="*60)