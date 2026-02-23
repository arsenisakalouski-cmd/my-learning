import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

sns.set_theme()

print("="*60)
print("КАК КОМПЬЮТЕР ВИДИТ ИЗОБРАЖЕНИЯ")
print("="*60)


print("\n" + "="*60)
print("Создаём простую картинку вручную")
print("="*60)

# Создаём чёрно-белый смайлик 10x10
smiley = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 1, 0],  # глаза
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 1, 0],  # рот
    [0, 1, 0, 0, 1, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
], dtype=np.float32)
"""
Создали массив 10x10

0 = чёрный (фон)
1 = белый (смайлик)

dtype=np.float32 - тип данных (числа с плавающей точкой)
Нужно для нейросетей
"""

print(f"Размер: {smiley.shape}")
print(f"Минимум: {smiley.min()}")
print(f"Максимум: {smiley.max()}")

print("\nКак выглядит для компьютера (числа):")
print(smiley)

# Визуализация
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(smiley, cmap='gray')
plt.title('Как видит ЧЕЛОВЕК', fontweight='bold', fontsize=14)
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(smiley, cmap='gray')
for i in range(10):
    for j in range(10):
        plt.text(j, i, f'{smiley[i,j]:.0f}', 
                ha='center', va='center', color='red', fontsize=8)
plt.title('Как видит КОМПЬЮТЕР (числа)', fontweight='bold', fontsize=14)
plt.axis('off')

plt.tight_layout()
plt.show()

print("""
ВИДИТЕ?
Человек: смайлик 😊
Компьютер: таблица из 0 и 1
""")



print("\n" + "="*60)
print("Цветное изображение (RGB)")
print("="*60)

# Создаём маленькую цветную картинку 5x5
# 3 канала: Red, Green, Blue
color_image = np.zeros((5, 5, 3), dtype=np.float32)
"""
Shape: (5, 5, 3)
5x5 - размер
3 - каналы (R, G, B)
"""

# Рисуем красный квадрат слева
color_image[1:4, 1:2, 0] = 1.0  # Red канал
"""
[1:4, 1:2, 0] означает:
[1:4] - строки с 1 по 3
[1:2] - столбец 1
0 - первый канал (Red)
"""

# Рисуем зелёный квадрат в центре
color_image[1:4, 2:3, 1] = 1.0  # Green канал

# Рисуем синий квадрат справа
color_image[1:4, 3:4, 2] = 1.0  # Blue канал

print(f"Размер цветной картинки: {color_image.shape}")
print(f"Это: {color_image.shape[0]}x{color_image.shape[1]} пикселей")
print(f"Каналов: {color_image.shape[2]} (RGB)")

# Визуализация
fig, axes = plt.subplots(1, 4, figsize=(16, 4))

# Полная картинка
axes[0].imshow(color_image)
axes[0].set_title('Полная картинка (RGB)', fontweight='bold')
axes[0].axis('off')

# Отдельные каналы
axes[1].imshow(color_image[:,:,0], cmap='Reds')
axes[1].set_title('Red канал', fontweight='bold')
axes[1].axis('off')

axes[2].imshow(color_image[:,:,1], cmap='Greens')
axes[2].set_title('Green канал', fontweight='bold')
axes[2].axis('off')

axes[3].imshow(color_image[:,:,2], cmap='Blues')
axes[3].set_title('Blue канал', fontweight='bold')
axes[3].axis('off')

plt.tight_layout()
plt.show()

print("""
ЦВЕТНАЯ КАРТИНКА:
- 3 канала (R, G, B)
- Каждый канал - отдельная таблица чисел
- Комбинация даёт цвет!
""")




print("\n" + "="*60)
print("Работа с реальным изображением")
print("="*60)

# Создаём простую картинку программно
real_image = np.random.rand(28, 28, 3)
"""
random.rand создаёт случайные числа от 0 до 1

28x28 - размер (как в MNIST)
3 - каналы (RGB)

Это просто пример, не настоящее фото
"""

print(f"Размер: {real_image.shape}")
print(f"Тип данных: {real_image.dtype}")
print(f"Диапазон значений: {real_image.min():.2f} - {real_image.max():.2f}")

# Для нейросетей часто нужно [0, 1] или [0, 255]
print("""
ВАЖНО ДЛЯ НЕЙРОСЕТЕЙ:

Нормализация - приведение к диапазону [0, 1]:
image = image / 255.0

ЗАЧЕМ:
- Нейросети лучше работают с маленькими числами
- Стандартизация входов
- Быстрее обучение
""")

# Визуализация
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(real_image)
plt.title('Случайное изображение 28x28', fontweight='bold', fontsize=14)
plt.axis('off')

plt.subplot(1, 2, 2)
plt.hist(real_image.flatten(), bins=50, color='skyblue', edgecolor='black')
plt.title('Распределение значений пикселей', fontweight='bold', fontsize=14)
plt.xlabel('Значение')
plt.ylabel('Частота')
plt.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()








print("""
КАК КОМПЬЮТЕР ВИДИТ ИЗОБРАЖЕНИЯ:

1. ЧЁРНО-БЕЛОЕ (GRAYSCALE):
   - Одна таблица чисел
   - Размер: (высота, ширина)
   - Значения: 0 (чёрный) - 255 (белый)
   - Для нейросетей: делим на 255 → [0, 1]

2. ЦВЕТНОЕ (RGB):
   - Три таблицы (R, G, B)
   - Размер: (высота, ширина, 3)
   - Каждый канал: 0-255
   - Для нейросетей: делим на 255 → [0, 1]

3. ВАЖНЫЕ ОПЕРАЦИИ:
   shape - размер (высота, ширина, каналы)
   dtype - тип данных
   min/max - диапазон значений
   /255.0 - нормализация

4. ДЛЯ CNN:
   Входной формат: (высота, ширина, каналы)
   Пример: (28, 28, 1) - чёрно-белое 28x28
           (224, 224, 3) - цветное 224x224

СЛЕДУЮЩИЙ ШАГ:
Как CNN обрабатывает эти числа!
""")

print("\n Основы изображений освоены!")
print("="*60)