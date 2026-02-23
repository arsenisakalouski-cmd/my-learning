import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()


print("\n" + "="*60)
print("Делаем свёртку ВРУЧНУЮ (чтобы понять)")
print("="*60)

# Простая картинка 5x5
image = np.array([
    [1, 1, 1, 0, 0],
    [1, 1, 1, 0, 0],
    [1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
], dtype=np.float32)
"""
Картинка:
Белый квадрат 3x3 слева вверху
Остальное чёрное
"""

# Фильтр для обнаружения вертикального края
filter_vertical = np.array([
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1]
], dtype=np.float32)
"""
Этот фильтр находит ВЕРТИКАЛЬНЫЕ линии

Почему?
Слева -1 (тёмное)
Справа +1 (светлое)
→ Обнаруживает переход тёмное→светлое
"""

print("Картинка (5x5):")
print(image)

print("\nФильтр (вертикальный край):")
print(filter_vertical)

# Делаем свёртку вручную (одна позиция)
print("\n--- СВЁРТКА В ОДНОЙ ПОЗИЦИИ ---")
print("\nБерём левый верхний кусок 3x3:")
patch = image[0:3, 0:3]
print(patch)

print("\nУмножаем поэлементно с фильтром:")
result = patch * filter_vertical
print(result)

print("\nСуммируем все элементы:")
conv_value = np.sum(result)
print(f"Результат: {conv_value}")

print("""
Объяснение:
Левый верх картинки - белый квадрат
Вертикального края там нет
→ Результат близок к 0
""")

# Делаем свёртку для другой позиции
print("\n--- СВЁРТКА В ДРУГОЙ ПОЗИЦИИ ---")
print("\nБерём кусок где есть граница (столбец 2):")
patch2 = image[0:3, 1:4]
print(patch2)

print("\nУмножаем с фильтром:")
result2 = patch2 * filter_vertical
print(result2)

conv_value2 = np.sum(result2)
print(f"\nРезультат: {conv_value2}")

print("""
Объяснение:
Здесь есть граница белое→чёрное!
Фильтр обнаружил её
→ Результат большой (3.0)
""")



print("\n" + "="*60)
print("Полная свёртка по всей картинке")
print("="*60)

def manual_conv2d(image, filter_kernel):
    """
    Свёртка вручную
    
    Проходим фильтром по всей картинке
    Возвращаем карту признаков
    """
    # Размеры
    img_h, img_w = image.shape
    filt_h, filt_w = filter_kernel.shape
    
    # Размер выхода
    out_h = img_h - filt_h + 1
    out_w = img_w - filt_w + 1
    """
    Почему размер уменьшается?
    
    Картинка 5x5, фильтр 3x3
    Фильтр может встать:
    - По высоте: 5 - 3 + 1 = 3 позиции
    - По ширине: 5 - 3 + 1 = 3 позиции
    
    Результат: 3x3
    """
    
    # Создаём выход
    output = np.zeros((out_h, out_w))
    
    # Проходим по всем позициям
    for i in range(out_h):
        for j in range(out_w):
            # Вырезаем кусок
            patch = image[i:i+filt_h, j:j+filt_w]
            
            # Умножаем поэлементно и суммируем
            output[i, j] = np.sum(patch * filter_kernel)
    
    return output

# Применяем свёртку
feature_map = manual_conv2d(image, filter_vertical)

print(f"Размер картинки: {image.shape}")
print(f"Размер фильтра: {filter_vertical.shape}")
print(f"Размер результата: {feature_map.shape}")

print("\nРезультат свёртки (feature map):")
print(feature_map)

print("""
ЧТО ПОЛУЧИЛИ:

Карта признаков (feature map) показывает
ГДЕ на картинке есть вертикальные линии!

Большие значения = есть вертикальная линия
Маленькие = нет линии
""")



print("\nВизуализация...")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Исходная картинка
axes[0].imshow(image, cmap='gray', vmin=0, vmax=1)
axes[0].set_title('Исходная картинка', fontweight='bold', fontsize=14)
axes[0].axis('off')

# Фильтр
im = axes[1].imshow(filter_vertical, cmap='seismic', vmin=-1, vmax=1)
axes[1].set_title('Фильтр (вертикальный край)', fontweight='bold', fontsize=14)
axes[1].axis('off')
plt.colorbar(im, ax=axes[1])

# Результат
im2 = axes[2].imshow(feature_map, cmap='hot')
axes[2].set_title('Feature Map\n(где есть вертикальные края)', fontweight='bold', fontsize=14)
axes[2].axis('off')
plt.colorbar(im2, ax=axes[2])

plt.tight_layout()
plt.show()

# ============================================
# RAZNYE FILTRY
# ============================================

print("\n" + "="*60)
print("Разные фильтры находят разное")
print("="*60)

# Создаём более интересную картинку
complex_image = np.array([
    [0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0]
], dtype=np.float32)

# Горизонтальный фильтр
filter_horizontal = np.array([
    [-1, -1, -1],
    [ 0,  0,  0],
    [ 1,  1,  1]
], dtype=np.float32)

# Применяем оба фильтра
vertical_edges = manual_conv2d(complex_image, filter_vertical)
horizontal_edges = manual_conv2d(complex_image, filter_horizontal)

# Визуализация
fig, axes = plt.subplots(2, 2, figsize=(12, 12))

axes[0, 0].imshow(complex_image, cmap='gray')
axes[0, 0].set_title('Исходная картинка\n(крест)', fontweight='bold', fontsize=12)
axes[0, 0].axis('off')

axes[0, 1].imshow(filter_vertical, cmap='seismic', vmin=-1, vmax=1)
axes[0, 1].set_title('Вертикальный фильтр', fontweight='bold', fontsize=12)
axes[0, 1].axis('off')

axes[1, 0].imshow(vertical_edges, cmap='hot')
axes[1, 0].set_title('Вертикальные края\n(найдены!)', fontweight='bold', fontsize=12)
axes[1, 0].axis('off')

axes[1, 1].imshow(horizontal_edges, cmap='hot')
axes[1, 1].set_title('Горизонтальные края\n(найдены!)', fontweight='bold', fontsize=12)
axes[1, 1].axis('off')

plt.tight_layout()
plt.show()



print("\n" + "="*60)
print("ПРОСТОЙ ЭКСПЕРИМЕНТ")
print("="*60)

# Создайте букву "T"
letter_t = np.array([
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]
], dtype=np.float32)

# Найдите вертикальные линии
t_vertical = manual_conv2d(letter_t, filter_vertical)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(letter_t, cmap='gray')
plt.title('Буква T', fontweight='bold')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(t_vertical, cmap='hot')
plt.title('Найденные вертикальные линии', fontweight='bold')
plt.axis('off')

plt.tight_layout()
plt.show()

print("✓ Фильтр нашёл вертикальную палочку буквы T!")












print("""


Разные фильтры находят разные паттерны:
- Вертикальный фильтр → вертикальные линии
- Горизонтальный фильтр → горизонтальные линии

CNN АВТОМАТИЧЕСКИ учит фильтры!
Мы не говорим "ищи вертикальные линии"
Сеть САМА понимает что искать!
""")

# ============================================
# REZYUME
# ============================================

print("\n" + "="*60)
print("РЕЗЮМЕ:")
print("="*60)

print("""
СВЁРТКА (CONVOLUTION):

ЧТО ЭТО:
Фильтр скользит по картинке
Умножает и суммирует значения
Результат = feature map (карта признаков)

КАК РАБОТАЕТ:
1. Берём кусок картинки (3x3)
2. Умножаем поэлементно с фильтром
3. Суммируем → одно число
4. Сдвигаем фильтр
5. Повторяем

ЗАЧЕМ:
Находит паттерны:
- Линии (вертикальные, горизонтальные)
- Углы
- Текстуры
- Формы

РАЗМЕРЫ:
Вход: (H, W)
Фильтр: (F, F)
Выход: (H-F+1, W-W+1)

Пример:
Картинка 5x5, фильтр 3x3
→ Результат 3x3

В CNN:
- Десятки/сотни фильтров
- Каждый находит свой паттерн
- Фильтры ОБУЧАЮТСЯ автоматически!

СЛЕДУЮЩИЙ ШАГ:
Pooling - уменьшение размера
""")

print("\n Свёртка освоена!")
print("="*60)