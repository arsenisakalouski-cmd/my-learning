import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

import warnings
warnings.filterwarnings('ignore')

sns.set_theme()
np.random.seed(42)

(X_train, y_train), (X_test, y_test) = cifar10.load_data()

class_names = ['самолёт', 'машина', 'птица', 'кот', 'олень', 
               'собака', 'лягушка', 'лошадь', 'корабль', 'грузовик']

print("\nПримеры из датасета:")

plt.figure(figsize=(15, 6))
for i in range(20):
    plt.subplot(4, 5, i+1)
    plt.imshow(X_train[i])
    plt.title(f'{class_names[y_train[i][0]]}', fontsize=9)
    plt.axis('off')
plt.tight_layout()
plt.show()

y_train_cat = to_categorical(y_train, 10)
y_test_cat = to_categorical(y_test, 10)

model = Sequential([
    # БЛОК 1
    Conv2D(32, (3, 3), padding='same', activation='relu', 
           input_shape=(32, 32, 3)),
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    # БЛОК 2
    Conv2D(64, (3, 3), padding='same', activation='relu'),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    # КЛАССИФИКАТОР
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(10, activation='softmax')
])

model.summary()


model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Early Stopping
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True,
    verbose=1
)

# ReduceLROnPlateau - НОВОЕ!
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=3,
    min_lr=1e-6,
    verbose=1
)

import time
start_time = time.time()

history = model.fit(
    X_train, y_train_cat,
    epochs=25,
    batch_size=64,
    validation_split=0.1,
    callbacks=[early_stop, reduce_lr],
    verbose=1
)

training_time = time.time() - start_time
actual_epochs = len(history.history['loss'])

print(f"\n✓ Обучение завершено!")
print(f"  Время: {training_time/60:.1f} минут")
print(f"  Эпох: {actual_epochs}")



test_loss, test_accuracy = model.evaluate(X_test, y_test_cat, verbose=0)

print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")

if test_accuracy > 0.70:
    print("\n ОТЛИЧНО! Более 70% для CIFAR-10 - хороший результат!")
elif test_accuracy > 0.60:
    print("\n ХОРОШО! Более 60% - неплохо для начала!")
else:
    print("\n Есть куда расти. CIFAR-10 - сложный датасет!")

    

indices = np.random.choice(len(X_test), 20, replace=False)

# Предсказываем
predictions = model.predict(X_test[indices], verbose=0)
predicted_labels = np.argmax(predictions, axis=1)
true_labels = y_test[indices].flatten()    

print("\nПримеры предсказаний:\n")

plt.figure(figsize=(15, 8))
for i in range(20):
    plt.subplot(4, 5, i+1)
    plt.imshow(X_test[indices[i]])
    
    pred = predicted_labels[i]
    true = true_labels[i]
    
    color = 'green' if pred == true else 'red'
    title = f'П: {class_names[pred]}\nР: {class_names[true]}'
    plt.title(title, color=color, fontsize=8)
    plt.axis('off')
    
    correct = '✓' if pred == true else '✗'
    if i < 10:  # печатаем только первые 10
        print(f"{i+1}. Предск: {class_names[pred]:10s} | "
              f"Реал: {class_names[true]:10s} {correct}")

plt.tight_layout()
plt.show()

print("\nВизуализация обучения...")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Loss
axes[0].plot(history.history['loss'], label='Train Loss', linewidth=2)
axes[0].plot(history.history['val_loss'], label='Val Loss', linewidth=2)
axes[0].set_title('Loss во время обучения', fontweight='bold', fontsize=14)
axes[0].set_xlabel('Эпоха')
axes[0].set_ylabel('Loss')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Accuracy
axes[1].plot(history.history['accuracy'], label='Train Accuracy', linewidth=2)
axes[1].plot(history.history['val_accuracy'], label='Val Accuracy', linewidth=2)
axes[1].set_title('Accuracy во время обучения', fontweight='bold', fontsize=14)
axes[1].set_xlabel('Эпоха')
axes[1].set_ylabel('Accuracy')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================
# ANALIZ OSHIBOK
# ============================================

print("\n" + "="*60)
print("ШАГ 9: Анализ ошибок")
print("="*60)

# Все предсказания
all_predictions = model.predict(X_test, verbose=0)
all_predicted_labels = np.argmax(all_predictions, axis=1)
all_true_labels = y_test.flatten()

# Confusion Matrix (упрощённая)
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(all_true_labels, all_predicted_labels)

# Визуализация
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names, yticklabels=class_names)
plt.title('Confusion Matrix - CIFAR-10', fontweight='bold', fontsize=14)
plt.ylabel('Реальный класс')
plt.xlabel('Предсказанный класс')
plt.tight_layout()
plt.show()

print("\nЧастые ошибки:")
# Находим где больше всего ошибок (кроме диагонали)
np.fill_diagonal(cm, 0)
max_errors = np.unravel_index(cm.argmax(), cm.shape)
print(f"  Часто путает: {class_names[max_errors[0]]} с {class_names[max_errors[1]]}")
print(f"  Количество ошибок: {cm[max_errors]}")