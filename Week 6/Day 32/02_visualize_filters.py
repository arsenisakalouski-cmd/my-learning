import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow import keras
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.datasets import mnist

import warnings
warnings.filterwarnings('ignore')

sns.set_theme()
np.random.seed(42)

# Загружаем MNIST
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Подготовка
X_train = X_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0
X_test = X_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0

from tensorflow.keras.utils import to_categorical
y_train_cat = to_categorical(y_train, 10)
y_test_cat = to_categorical(y_test, 10)

# Простая модель
model = Sequential([
    Conv2D(8, (3, 3), activation='relu', input_shape=(28, 28, 1), name='conv1'),
    MaxPooling2D((2, 2), name='pool1'),
    Conv2D(16, (3, 3), activation='relu', name='conv2'),
    MaxPooling2D((2, 2), name='pool2'),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(10, activation='softmax')
])
"""
Специально делаем МЕНЬШЕ фильтров (8 и 16)
Чтобы было легче визуализировать

name='conv1' - даём имена слоям
Потом сможем обратиться к ним
"""

model.compile(optimizer='adam', 
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Берём только часть данных для скорости
history = model.fit(
    X_train[:10000], y_train_cat[:10000],
    epochs=3,
    batch_size=128,
    validation_split=0.1,
    verbose=0
)

test_acc = model.evaluate(X_test, y_test_cat, verbose=0)[1]
print(f"Test Accuracy: {test_acc:.2%}")


first_layer = model.get_layer('conv1')
filters, biases = first_layer.get_weights()
"""
get_weights() возвращает:
- filters: веса фильтров
- biases: смещения (bias)

Форма filters: (3, 3, 1, 8)
  3x3 - размер фильтра
  1 - входных каналов (чёрно-белое)
  8 - количество фильтров
"""

print(f"Форма фильтров: {filters.shape}")
print(f"Это: {filters.shape[3]} фильтров размером {filters.shape[0]}x{filters.shape[1]}")


# Визуализация фильтров
fig, axes = plt.subplots(2, 4, figsize=(12, 6))
fig.suptitle('Фильтры 1-го слоя (что ищет CNN)', fontweight='bold', fontsize=14)

for i, ax in enumerate(axes.flat):
    # i-й фильтр
    f = filters[:, :, 0, i]
    
    ax.imshow(f, cmap='gray')
    ax.set_title(f'Фильтр {i+1}', fontsize=10)
    ax.axis('off')

plt.tight_layout()
plt.show()

# Берём одну цифру (например 7)
sample_idx = 0
sample_image = X_test[sample_idx:sample_idx+1]
sample_label = y_test[sample_idx]

print(f"Взяли цифру: {sample_label}")

# Показываем картинку
plt.figure(figsize=(4, 4))
plt.imshow(sample_image.reshape(28, 28), cmap='gray')
plt.title(f'Входная картинка: цифра {sample_label}', fontweight='bold')
plt.axis('off')
plt.show()

# Создаём модель которая выдаёт активации 1-го слоя
layer_outputs = [model.get_layer('conv1').output]
activation_model = Model(inputs=model.input, outputs=layer_outputs)
"""
Model(inputs=..., outputs=...)
Создаём модель с теми же входами
Но выход = активации conv1 слоя

Это позволяет "заглянуть внутрь"
"""

# Получаем активации
activations = activation_model.predict(sample_image, verbose=0)
first_layer_activation = activations[0]

print(f"Форма активаций: {first_layer_activation.shape}")
print(f"Это: {first_layer_activation.shape[3]} карт признаков (по одной на фильтр)")

# Визуализация активаций
fig, axes = plt.subplots(2, 4, figsize=(12, 6))
fig.suptitle(f'Активации 1-го слоя для цифры {sample_label}', 
             fontweight='bold', fontsize=14)

for i, ax in enumerate(axes.flat):
    # i-я карта признаков
    activation = first_layer_activation[0, :, :, i]
    
    ax.imshow(activation, cmap='viridis')
    ax.set_title(f'Фильтр {i+1} нашёл', fontsize=10)
    ax.axis('off')

plt.tight_layout()
plt.show()


# Получаем все слои
layer_names = ['conv1', 'pool1', 'conv2', 'pool2']
layer_outputs = [model.get_layer(name).output for name in layer_names]

activation_model_all = Model(inputs=model.input, outputs=layer_outputs)

# Активации
activations_all = activation_model_all.predict(sample_image, verbose=0)

print(f"Получили активации {len(activations_all)} слоёв")

# Визуализация по слоям
images_per_row = 8

for layer_name, layer_activation in zip(layer_names, activations_all):
    n_features = layer_activation.shape[-1]
    size = layer_activation.shape[1]
    
    n_cols = min(n_features, images_per_row)
    n_rows = (n_features + images_per_row - 1) // images_per_row
    
    display_grid = np.zeros((size * n_rows, size * n_cols))
    
    for row in range(n_rows):
        for col in range(n_cols):
            idx = row * images_per_row + col
            if idx < n_features:
                channel_image = layer_activation[0, :, :, idx]
                # Нормализация для визуализации
                channel_image -= channel_image.mean()
                if channel_image.std() > 0:
                    channel_image /= channel_image.std()
                channel_image = np.clip(channel_image, 0, 1)
                
                display_grid[row * size : (row + 1) * size,
                            col * size : (col + 1) * size] = channel_image
    
    scale = 1.5
    plt.figure(figsize=(scale * n_cols, scale * n_rows))
    plt.title(f'{layer_name} - {n_features} карт признаков', fontweight='bold')
    plt.grid(False)
    plt.imshow(display_grid, aspect='auto', cmap='viridis')
    plt.axis('off')
    plt.show()

print("""
ЧТО ВИДИМ ПО СЛОЯМ:

CONV1 (первый):
- Простые паттерны (линии, углы)
- 8 карт признаков
- Размер большой

POOL1:
- Те же паттерны
- Размер уменьшился (pooling!)

CONV2 (второй):
- Более сложные формы
- 16 карт признаков
- Комбинирует паттерны из CONV1

POOL2:
- Финальное уменьшение
- Компактное представление

ВЫВОД:
Слои постепенно находят всё более сложные паттерны!
Линии → Углы → Формы → Цифра
""")