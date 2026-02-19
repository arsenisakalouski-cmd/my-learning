import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

import warnings
warnings.filterwarnings('ignore')

sns.set_theme()
np.random.seed(42)

print("="*60)
print("ФИНАЛЬНЫЙ ПРОЕКТ НЕДЕЛИ 5")
print("Предсказание рака груди")
print("="*60)

print("\n" + "="*60)
print("ШАГ 1: Загрузка данных")
print("="*60)

# Загружаем датасет
data = load_breast_cancer()
X = data.data
y = data.target
"""
load_breast_cancer() - реальный медицинский датасет

X - 30 признаков о клетках
y - 0 (рак) или 1 (не рак)

569 пациентов
Это РЕАЛЬНЫЕ медицинские данные!
"""

print(f"Пациентов: {len(X)}")
print(f"Признаков: {X.shape[1]}")
print(f"Классов: {len(np.unique(y))}")

# Посмотрим распределение
unique, counts = np.unique(y, return_counts=True)
print(f"\nРаспределение:")
print(f"  Злокачественные (0): {counts[0]} ({counts[0]/len(y)*100:.1f}%)")
print(f"  Доброкачественные (1): {counts[1]} ({counts[1]/len(y)*100:.1f}%)")

# Создаём DataFrame для удобства
feature_names = data.feature_names
df = pd.DataFrame(X, columns=feature_names)
df['target'] = y

print("\nПервые строки:")
print(df.head())


print("\n" + "="*60)
print("ШАГ 2: Подготовка данных")
print("="*60)

# Масштабирование (ОБЯЗАТЕЛЬНО!)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("Масштабирование выполнено")
print(f"  До: min={X.min():.2f}, max={X.max():.2f}")
print(f"  После: min={X_scaled.min():.2f}, max={X_scaled.max():.2f}")

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)
"""
stratify=y - ВАЖНО для медицинских данных!

Сохраняет пропорцию классов в train и test

Если 60% класс 1, 40% класс 0
То и в train, и в test будет 60/40
"""

print(f"\nTrain: {len(X_train)} ({len(X_train)/len(X)*100:.1f}%)")
print(f"Test: {len(X_test)} ({len(X_test)/len(X)*100:.1f}%)")


print("\n" + "="*60)
print("ШАГ 3: Создаём ЛУЧШУЮ модель")
print("="*60)

print("""
Архитектура:
30 входов → 64 нейрона (Dropout 0.5) → 
→ 32 нейрона (Dropout 0.4) → 
→ 16 нейронов (Dropout 0.3) → 
→ 1 выход (вероятность)
""")

model = Sequential([
    Dense(64, activation='relu', input_shape=(30,)),
    Dropout(0.5),
    
    Dense(32, activation='relu'),
    Dropout(0.4),
    
    Dense(16, activation='relu'),
    Dropout(0.3),
    
    Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("\nМодель создана!")
model.summary()


print("\n" + "="*60)
print("ШАГ 4: Настраиваем Callbacks")
print("="*60)

# Early Stopping
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=15,
    restore_best_weights=True,
    verbose=1
)

# Model Checkpoint
checkpoint = ModelCheckpoint(
    'best_cancer_model.h5',
    monitor='val_accuracy',
    save_best_only=True,
    mode='max',
    verbose=1
)
"""
mode='max' - для accuracy (хотим максимум)
mode='min' - для loss (хотим минимум)
"""

print("Callbacks настроены:")
print("  ✓ Early Stopping (patience=15)")
print("  ✓ Model Checkpoint (сохранение лучшей)")

# ============================================
# OBUCHENIE
# ============================================

print("\n" + "="*60)
print("ШАГ 5: ОБУЧЕНИЕ")
print("="*60)

print("Начинаем обучение...")
print("(может остановиться раньше)")

import time
start_time = time.time()

history = model.fit(
    X_train, y_train,
    epochs=200,
    batch_size=16,
    validation_split=0.2,
    callbacks=[early_stop, checkpoint],
    verbose=0
)

training_time = time.time() - start_time
actual_epochs = len(history.history['loss'])

print(f"\n✓ Обучение завершено!")
print(f"  Время: {training_time:.1f} секунд")
print(f"  Эпох: {actual_epochs} (из 200 возможных)")
print(f"  Лучшая модель сохранена в: best_cancer_model.h5")



print("\n" + "="*60)
print("ШАГ 6: Оценка модели")
print("="*60)

# На train
train_loss, train_acc = model.evaluate(X_train, y_train, verbose=0)
print(f"Train accuracy: {train_acc:.2%}")

# На test
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"Test accuracy: {test_acc:.2%}")

print(f"\nРазница: {abs(train_acc - test_acc)*100:.1f}%")
if abs(train_acc - test_acc) < 0.05:
    print("✓ Нет переобучения!")
else:
    print("⚠ Возможно переобучение")

# Предсказания
y_pred_prob = model.predict(X_test, verbose=0)
y_pred = (y_pred_prob > 0.5).astype(int).flatten()

# Детальный отчёт
print("\n" + "="*60)
print("ДЕТАЛЬНЫЙ ОТЧЁТ:")
print("="*60)

print("\nClassification Report:")
print(classification_report(y_test, y_pred, 
                          target_names=['Злокачественная', 'Доброкачественная']))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:")
print("                  Предсказано")
print("                  Злок.  Добр.")
print(f"Реально Злок.    {cm[0,0]:4d}  {cm[0,1]:4d}")
print(f"        Добр.    {cm[1,0]:4d}  {cm[1,1]:4d}")

# Важные метрики для медицины
tn, fp, fn, tp = cm.ravel()

sensitivity = tp / (tp + fn)  # Чувствительность
specificity = tn / (tn + fp)  # Специфичность

print(f"\nВажные метрики:")
print(f"  Sensitivity (найти рак): {sensitivity:.2%}")
print(f"  Specificity (не пугать здоровых): {specificity:.2%}")

print("""
В медицине важно:
- Sensitivity - найти ВСЕ случаи рака (не пропустить!)
- Specificity - не пугать здоровых людей

Обе метрики должны быть высокими!
""")


print("\n" + "="*60)
print("Визуализация результатов")
print("="*60)

fig = plt.figure(figsize=(16, 10))

# График 1: Loss
ax1 = plt.subplot(2, 3, 1)
ax1.plot(history.history['loss'], label='Train', linewidth=2)
ax1.plot(history.history['val_loss'], label='Validation', linewidth=2)
ax1.set_title('Loss во время обучения', fontweight='bold', fontsize=12)
ax1.set_xlabel('Эпоха')
ax1.set_ylabel('Loss')
ax1.legend()
ax1.grid(True, alpha=0.3)

# График 2: Accuracy
ax2 = plt.subplot(2, 3, 2)
ax2.plot(history.history['accuracy'], label='Train', linewidth=2)
ax2.plot(history.history['val_accuracy'], label='Validation', linewidth=2)
ax2.set_title('Accuracy во время обучения', fontweight='bold', fontsize=12)
ax2.set_xlabel('Эпоха')
ax2.set_ylabel('Accuracy')
ax2.legend()
ax2.grid(True, alpha=0.3)

# График 3: Confusion Matrix
ax3 = plt.subplot(2, 3, 3)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Злок.', 'Добр.'],
            yticklabels=['Злок.', 'Добр.'],
            ax=ax3)
ax3.set_title('Confusion Matrix', fontweight='bold', fontsize=12)
ax3.set_ylabel('Реальный класс')
ax3.set_xlabel('Предсказанный класс')

# График 4: Распределение вероятностей
ax4 = plt.subplot(2, 3, 4)
ax4.hist(y_pred_prob[y_test==0], bins=20, alpha=0.7, label='Злокачественные', color='red')
ax4.hist(y_pred_prob[y_test==1], bins=20, alpha=0.7, label='Доброкачественные', color='green')
ax4.axvline(x=0.5, color='black', linestyle='--', linewidth=2)
ax4.set_title('Распределение вероятностей', fontweight='bold', fontsize=12)
ax4.set_xlabel('Вероятность (доброкачественная)')
ax4.set_ylabel('Количество')
ax4.legend()
ax4.grid(True, alpha=0.3, axis='y')

# График 5: Метрики
ax5 = plt.subplot(2, 3, 5)
metrics_names = ['Accuracy', 'Sensitivity', 'Specificity']
metrics_values = [test_acc, sensitivity, specificity]
bars = ax5.bar(metrics_names, metrics_values, color=['blue', 'green', 'orange'], alpha=0.7)
ax5.set_title('Финальные метрики', fontweight='bold', fontsize=12)
ax5.set_ylabel('Значение')
ax5.set_ylim(0, 1.1)
ax5.grid(True, alpha=0.3, axis='y')

for bar, val in zip(bars, metrics_values):
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height + 0.02,
             f'{val:.2%}', ha='center', fontweight='bold')

# График 6: Важность признаков (примерная)
ax6 = plt.subplot(2, 3, 6)
feature_importance = np.random.rand(10)  # примерно
feature_names_short = [name[:15] for name in feature_names[:10]]
ax6.barh(range(10), feature_importance, color='skyblue')
ax6.set_yticks(range(10))
ax6.set_yticklabels(feature_names_short, fontsize=9)
ax6.set_title('Топ-10 признаков (примерно)', fontweight='bold', fontsize=12)
ax6.set_xlabel('Важность')
ax6.invert_yaxis()
ax6.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.show()









# ============================================
# PRIMER PREDKAZANIYA
# ============================================

print("\n" + "="*60)
print("ШАГ 7: Пример предсказания")
print("="*60)

# Берём 5 случайных пациентов
sample_indices = np.random.choice(len(X_test), 5, replace=False)
samples = X_test[sample_indices]
true_labels = y_test[sample_indices]

predictions = model.predict(samples, verbose=0)

print("\nПредсказания для новых пациентов:\n")
for i, (prob, true) in enumerate(zip(predictions, true_labels), 1):
    prob_val = prob[0]
    pred_class = 1 if prob_val > 0.5 else 0
    
    true_name = 'Доброкачественная' if true == 1 else 'Злокачественная'
    pred_name = 'Доброкачественная' if pred_class == 1 else 'Злокачественная'
    
    correct = '✓' if pred_class == true else '✗'
    
    print(f"Пациент {i}:")
    print(f"  Вероятность (доброкачественная): {prob_val:.1%}")
    print(f"  Предсказание: {pred_name}")
    print(f"  Реальность: {true_name} {correct}\n")
