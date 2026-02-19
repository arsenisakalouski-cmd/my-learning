import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import warnings
warnings.filterwarnings('ignore')

sns.set_theme()
np.random.seed(42)

print("\n" + "="*60)
print("Создаём данные")
print("="*60)

X, y = make_classification(
    n_samples=1000,
    n_features=20,
    n_informative=15,
    n_redundant=5,
    random_state=42
)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

print(f"Train: {len(X_train)}")
print(f"Test: {len(X_test)}")




print("\n" + "="*60)
print("МОДЕЛЬ 1: БЕЗ Early Stopping")
print("="*60)

model_no_early = Sequential([
    Dense(64, activation='relu', input_shape=(20,)),
    Dropout(0.5),
    Dense(32, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])

model_no_early.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("Обучаем 200 эпох (много!)...")

import time
start = time.time()

history_no_early = model_no_early.fit(
    X_train, y_train,
    epochs=200,
    batch_size=32,
    validation_split=0.2,
    verbose=0
)

time_no_early = time.time() - start

print(f"✓ Завершено за {time_no_early:.1f} секунд")
print(f"  Прошло 200 эпох")

# Найти лучшую эпоху вручную
best_epoch_no_early = np.argmin(history_no_early.history['val_loss'])
best_val_loss_no_early = history_no_early.history['val_loss'][best_epoch_no_early]

print(f"  Лучшая эпоха: {best_epoch_no_early + 1}")
print(f"  Лучший val_loss: {best_val_loss_no_early:.4f}")
print(f"  Последний val_loss: {history_no_early.history['val_loss'][-1]:.4f}")

print("""
ПРОБЛЕМА:
- Лучшая модель была на эпохе ~50
- Но мы продолжали до 200!
- Зря потратили время
- Возможно переобучились
""")

print("\n" + "="*60)
print("МОДЕЛЬ 2: С Early Stopping")
print("="*60)

model_with_early = Sequential([
    Dense(64, activation='relu', input_shape=(20,)),
    Dropout(0.5),
    Dense(32, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])

model_with_early.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# СОЗДАЁМ EARLY STOPPING
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)
"""
EarlyStopping - callback (автоматическое действие)

monitor='val_loss' - ЧТО смотреть
  val_loss - ошибка на валидации
  val_accuracy - точность на валидации
  loss - ошибка на train (не рекомендуется)

patience=10 - СКОЛЬКО ЖДАТЬ
  Если 10 эпох подряд не улучшается → СТОП
  patience=5 - остановится быстрее
  patience=20 - будет ждать дольше

restore_best_weights=True - ВАЖНО!
  Вернуть веса с лучшей эпохи
  Если False - останется с последней эпохи

verbose=1 - печатать когда останавливается
"""

print("Обучаем максимум 200 эпох (но остановится раньше!)...")

start = time.time()

history_with_early = model_with_early.fit(
    X_train, y_train,
    epochs=200,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stop],  # ← ПЕРЕДАЁМ CALLBACK!
    verbose=0
)

time_with_early = time.time() - start

actual_epochs = len(history_with_early.history['loss'])

print(f"\n✓ Завершено за {time_with_early:.1f} секунд")
print(f"  Остановилось на эпохе: {actual_epochs}")
print(f"  Лучший val_loss: {min(history_with_early.history['val_loss']):.4f}")

print("""
РЕЗУЛЬТАТ:
- Остановилось автоматически!
- Не тратили время на бесполезные эпохи
- Вернулись к лучшим весам
""")

# ============================================
# SRAVNENIE
# ============================================

print("\n" + "="*60)
print("СРАВНЕНИЕ:")
print("="*60)

comparison = pd.DataFrame({
    'Модель': ['БЕЗ Early Stop', 'С Early Stop'],
    'Эпох': [200, actual_epochs],
    'Время (сек)': [time_no_early, time_with_early],
    'Лучший val_loss': [
        best_val_loss_no_early,
        min(history_with_early.history['val_loss'])
    ]
})

print("\n" + comparison.to_string(index=False))

print(f"""
ЭКОНОМИЯ ВРЕМЕНИ: {time_no_early - time_with_early:.1f} секунд
ЭТО: {(time_no_early - time_with_early) / time_no_early * 100:.0f}% быстрее!

КАЧЕСТВО: Одинаковое или лучше!

ВЫВОД: Early Stopping = умно и быстро! ✓
""")

# ============================================
# VIZUALIZATSIYA
# ============================================

print("\nВизуализация...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# График 1: БЕЗ Early Stopping
axes[0].plot(history_no_early.history['val_loss'], linewidth=2)
axes[0].axvline(x=best_epoch_no_early, color='red', linestyle='--', 
                linewidth=2, label=f'Лучшая эпоха: {best_epoch_no_early+1}')
axes[0].set_title('БЕЗ Early Stopping\n(зря продолжали)', 
                  fontweight='bold', fontsize=14)
axes[0].set_xlabel('Эпоха')
axes[0].set_ylabel('Validation Loss')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# График 2: С Early Stopping
axes[1].plot(history_with_early.history['val_loss'], linewidth=2)
axes[1].axvline(x=actual_epochs-1, color='green', linestyle='--', 
                linewidth=2, label=f'Остановились: {actual_epochs}')
axes[1].set_title('С Early Stopping\n(остановились вовремя)', 
                  fontweight='bold', fontsize=14)
axes[1].set_xlabel('Эпоха')
axes[1].set_ylabel('Validation Loss')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("""
ЧТО ВИДНО:

СЛЕВА (без Early Stop):
- После лучшей точки продолжали обучаться
- Loss перестал улучшаться или ухудшился
- Зря потратили время

СПРАВА (с Early Stop):
- Остановились когда перестало улучшаться
- Сэкономили время
- Вернулись к лучшим весам
""")

# ============================================
# MODEL CHECKPOINT
# ============================================

print("\n" + "="*60)
print("БОНУС: Model Checkpoint")
print("="*60)

print("""
ModelCheckpoint - сохраняет модель автоматически

ЧТО ДЕЛАЕТ:
Во время обучения сохраняет модель когда она улучшается

ЗАЧЕМ:
- Если обучение прервётся (свет выключили) - модель сохранена!
- Всегда имеем лучшую версию
""")

model_checkpoint = Sequential([
    Dense(64, activation='relu', input_shape=(20,)),
    Dropout(0.5),
    Dense(32, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])

model_checkpoint.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# СОЗДАЁМ CHECKPOINT
checkpoint = ModelCheckpoint(
    'best_model.h5',
    monitor='val_loss',
    save_best_only=True,
    verbose=1
)
"""
ModelCheckpoint - автоматическое сохранение

'best_model.h5' - имя файла
monitor='val_loss' - что смотреть
save_best_only=True - сохранять только когда улучшается
  False - сохранять каждую эпоху (много файлов!)
verbose=1 - печатать когда сохраняет
"""

print("\nОбучаем с checkpoint...")

history_checkpoint = model_checkpoint.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stop, checkpoint],  # ← оба callback!
    verbose=0
)

print("""
✓ Модель сохранена в best_model.h5
  Можно загрузить: keras.models.load_model('best_model.h5')
""")

# ============================================
# REZYUME
# ============================================

print("\n" + "="*60)
print("РЕЗЮМЕ:")
print("="*60)

print(f"""
EARLY STOPPING:

ЧТО ДЕЛАЕТ:
Останавливает обучение когда модель перестаёт улучшаться

КОД:
from tensorflow.keras.callbacks import EarlyStopping

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

model.fit(X, y, callbacks=[early_stop])

ПАРАМЕТРЫ:
monitor - что смотреть (val_loss обычно)
patience - сколько эпох ждать (10-20 обычно)
restore_best_weights - вернуть лучшие веса (True!)

РЕЗУЛЬТАТЫ СЕГОДНЯ:
БЕЗ: 200 эпох, {time_no_early:.1f} сек
С Early Stop: {actual_epochs} эпох, {time_with_early:.1f} сек
Экономия: {(time_no_early - time_with_early) / time_no_early * 100:.0f}%!

БОНУС: ModelCheckpoint
Автоматически сохраняет лучшую модель

ВЫВОД:
Early Stopping = умная остановка
Экономит время, предотвращает переобучение
ВСЕГДА используйте! ✓
""")

print("\n Early Stopping освоен!")
print("="*60)
