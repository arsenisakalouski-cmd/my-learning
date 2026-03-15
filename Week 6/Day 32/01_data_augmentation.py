import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.datasets import mnist

import warnings
warnings.filterwarnings('ignore')

sns.set_theme()
np.random.seed(42)

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.datasets import mnist

import warnings
warnings.filterwarnings('ignore')

sns.set_theme()
np.random.seed(42)

(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Берём только первые 1000 картинок (для скорости)
X_train_small = X_train[:1000]
y_train_small = y_train[:1000]

# Reshape для CNN
X_train_small = X_train_small.reshape(-1, 28, 28, 1).astype('float32') / 255.0

print(f"Train: {len(X_train_small)} картинок")

sample_image = X_train_small[0]

print("Форма:", sample_image.shape)

plt.figure(figsize=(6, 6))
plt.imshow(sample_image.reshape(28, 28), cmap='gray')
plt.title('Оригинальная картинка', fontweight='bold', fontsize=14)
plt.axis('off')
plt.show()


datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=False
)
"""
ImageDataGenerator - создаёт augmented картинки

ПАРАМЕТРЫ (простыми словами):

rotation_range=15
  Поворачивать на ±15 градусов
  Пример: цифра 3 чуть наклонена

width_shift_range=0.1
  Сдвигать влево/вправо на 10% ширины
  Пример: цифра не по центру

height_shift_range=0.1
  Сдвигать вверх/вниз на 10% высоты

zoom_range=0.1
  Приближать/отдалять на 10%
  Пример: цифра чуть крупнее

horizontal_flip=False
  НЕ отражать горизонтально
  Почему False? 
  Цифра 3 отражённая → не цифра 3!
  Для котов можно True (кот справа = кот слева)

ДРУГИЕ ВОЗМОЖНЫЕ ПАРАМЕТРЫ:
fill_mode='nearest' - как заполнять пустоты
brightness_range=[0.8, 1.2] - менять яркость
shear_range=0.2 - наклон/искажение
"""

print("Параметры augmentation:")
print("  Поворот: ±15°")
print("  Сдвиг: ±10%")
print("  Zoom: ±10%")

# Подготовка для generator
sample_batch = sample_image.reshape(1, 28, 28, 1)
"""
Generator требует формат:
(количество, высота, ширина, каналы)

Одна картинка 28x28x1 → (1, 28, 28, 1)
"""

# Генерируем варианты
augmented_images = []
generator = datagen.flow(sample_batch, batch_size=1)

for i in range(9):
    augmented_batch = next(generator)
    augmented_images.append(augmented_batch[0])

print(f"Создано {len(augmented_images)} augmented версий")

# Визуализация
fig, axes = plt.subplots(3, 3, figsize=(10, 10))
fig.suptitle('Data Augmentation - Варианты одной картинки', 
             fontweight='bold', fontsize=16)

for i, ax in enumerate(axes.flat):
    ax.imshow(augmented_images[i].reshape(28, 28), cmap='gray')
    ax.set_title(f'Вариант {i+1}', fontsize=10)
    ax.axis('off')

plt.tight_layout()
plt.show()

print("""
ЧТО ВИДИМ:
- Одна и та же цифра
- Но в разных позициях/поворотах
- Для модели это РАЗНЫЕ примеры!
- Больше разнообразия → лучше обучение
""")

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical

# Подготовка меток
y_train_cat = to_categorical(y_train_small, 10)

# Модель (простая)
def create_model():
    model = Sequential([
        Conv2D(16, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', 
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

print("\n1. Обучение БЕЗ augmentation...")

model_no_aug = create_model()
history_no_aug = model_no_aug.fit(
    X_train_small, y_train_cat,
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    verbose=0
)

print("✓ Завершено")

print("\n2. Обучение С augmentation...")

model_with_aug = create_model()

# Создаём generator
train_generator = datagen.flow(
    X_train_small, y_train_cat,
    batch_size=32
)
"""
datagen.flow создаёт бесконечный поток augmented данных

На каждой эпохе:
- Берёт batch картинок
- Применяет случайные трансформации
- Возвращает augmented batch

Модель видит РАЗНЫЕ версии картинок каждую эпоху!
"""

# Обучение
history_with_aug = model_with_aug.fit(
    train_generator,
    steps_per_epoch=len(X_train_small) // 32,
    epochs=10,
    validation_data=(X_train_small, y_train_cat),
    verbose=0
)
"""
steps_per_epoch - сколько batch'ей за эпоху

Вычисление:
1000 картинок / 32 batch = ~31 step

Почему нужно указывать:
Generator бесконечный!
Нужно сказать когда эпоха закончилась
"""

print("Завершено")

print("\n" + "="*60)
print("РЕЗУЛЬТАТЫ:")
print("="*60)

val_acc_no_aug = history_no_aug.history['val_accuracy'][-1]
val_acc_with_aug = history_with_aug.history['val_accuracy'][-1]

print(f"БЕЗ augmentation:")
print(f"  Val Accuracy: {val_acc_no_aug:.4f} ({val_acc_no_aug*100:.2f}%)")

print(f"\nС augmentation:")
print(f"  Val Accuracy: {val_acc_with_aug:.4f} ({val_acc_with_aug*100:.2f}%)")

if val_acc_with_aug > val_acc_no_aug:
    improvement = (val_acc_with_aug - val_acc_no_aug) * 100
    print(f"\n✓ Улучшение: +{improvement:.2f}%")
    print("  Data Augmentation помогло!")
else:
    print("\n⚠ На маленьком датасете разница может быть незначительной")
    print("  Но на больших данных augmentation ВСЕГДА помогает!")

# Визуализация обучения
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Validation Accuracy
axes[0].plot(history_no_aug.history['val_accuracy'], 
             label='БЕЗ augmentation', linewidth=2)
axes[0].plot(history_with_aug.history['val_accuracy'], 
             label='С augmentation', linewidth=2)
axes[0].set_title('Validation Accuracy', fontweight='bold', fontsize=14)
axes[0].set_xlabel('Эпоха')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Validation Loss
axes[1].plot(history_no_aug.history['val_loss'], 
             label='БЕЗ augmentation', linewidth=2)
axes[1].plot(history_with_aug.history['val_loss'], 
             label='С augmentation', linewidth=2)
axes[1].set_title('Validation Loss', fontweight='bold', fontsize=14)
axes[1].set_xlabel('Эпоха')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n" + "="*60)
print("РЕЗЮМЕ:")
print("="*60)

print("""
DATA AUGMENTATION:

ЧТО ЭТО:
Создание новых данных из существующих
Повороты, сдвиги, zoom, отражения

КОД:
from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1
)

train_gen = datagen.flow(X_train, y_train, batch_size=32)
model.fit(train_gen, steps_per_epoch=len(X_train)//32, epochs=10)

ЗАЧЕМ:
✓ Больше данных → лучше обучение
✓ Меньше переобучение
✓ Модель устойчивее к изменениям

КОГДА ИСПОЛЬЗОВАТЬ:
- Мало данных (< 10,000 картинок)
- Есть переобучение
- ВСЕГДА для Computer Vision!

ВАЖНО:
- Только на train данных!
- Test не трогаем!
- Разумные параметры (не rotation_range=180)

СЛЕДУЮЩИЙ ШАГ:
Посмотрим что видит CNN внутри!
""")
