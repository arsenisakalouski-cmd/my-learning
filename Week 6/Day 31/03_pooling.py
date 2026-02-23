import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

print("="*60)
print("POOLING - Уменьшение размера")
print("="*60)


print("\n" + "="*60)
print("Max Pooling вручную")
print("="*60)

# Простая картинка 4x4
image = np.array([
    [1, 3, 2, 4],
    [5, 6, 7, 8],
    [9, 2, 1, 3],
    [4, 5, 6, 7]
], dtype=np.float32)

print("Исходная картинка 4x4:")
print(image)

def max_pooling_manual(image, pool_size=2):
    """
    Max Pooling вручную
    
    Берём окно pool_size x pool_size
    Заменяем максимумом
    """
    h, w = image.shape
    new_h = h // pool_size  # // = целочисленное деление
    new_w = w // pool_size
    """
    Размер выхода:
    4 // 2 = 2
    Картинка 4x4 → станет 2x2
    """
    
    output = np.zeros((new_h, new_w))
    
    # Проходим по блокам
    for i in range(new_h):
        for j in range(new_w):
            # Вырезаем блок 2x2
            start_i = i * pool_size
            start_j = j * pool_size
            
            block = image[start_i:start_i+pool_size, 
                         start_j:start_j+pool_size]
            
            # Берём максимум
            output[i, j] = np.max(block)
    
    return output

# Применяем Max Pooling
pooled = max_pooling_manual(image, pool_size=2)

print(f"\nРазмер до: {image.shape}")
print(f"Размер после: {pooled.shape}")

print("\nРезультат Max Pooling 2x2:")
print(pooled)

print("""
ЧТО ПРОИЗОШЛО:

Блок 1 (левый верх):  Блок 2 (правый верх):
[1, 3]                [2, 4]
[5, 6]  → max = 6     [7, 8]  → max = 8

Блок 3 (левый низ):   Блок 4 (правый низ):
[9, 2]                [1, 3]
[4, 5]  → max = 9     [6, 7]  → max = 7

Результат:
[6, 8]
[9, 7]

Размер уменьшился 4x4 → 2x2 (в 2 раза по каждой стороне)
Осталось самое яркое (важное)!
""")


print("\nВизуализация...")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# До pooling
axes[0].imshow(image, cmap='hot', interpolation='nearest')
axes[0].set_title('ДО Max Pooling (4x4)', fontweight='bold', fontsize=14)
axes[0].axis('off')

# После pooling
axes[1].imshow(pooled, cmap='hot', interpolation='nearest')
axes[1].set_title('ПОСЛЕ Max Pooling (2x2)', fontweight='bold', fontsize=14)
axes[1].axis('off')

plt.tight_layout()
plt.show()


print("\n" + "="*60)
print("Пример с более реальной картинкой")
print("="*60)

# Создаём картинку посложнее 8x8
big_image = np.random.rand(8, 8) * 100
big_image = big_image.astype(np.float32)

print(f"Большая картинка: {big_image.shape}")

# Применяем pooling несколько раз
pooled_1 = max_pooling_manual(big_image, 2)  # 8x8 → 4x4
pooled_2 = max_pooling_manual(pooled_1, 2)   # 4x4 → 2x2

print(f"После 1-го pooling: {pooled_1.shape}")
print(f"После 2-го pooling: {pooled_2.shape}")

# Визуализация
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(big_image, cmap='viridis')
axes[0].set_title('Исходная (8x8)', fontweight='bold', fontsize=14)
axes[0].axis('off')

axes[1].imshow(pooled_1, cmap='viridis')
axes[1].set_title('1-й Pooling (4x4)', fontweight='bold', fontsize=14)
axes[1].axis('off')

axes[2].imshow(pooled_2, cmap='viridis')
axes[2].set_title('2-й Pooling (2x2)', fontweight='bold', fontsize=14)
axes[2].axis('off')

plt.tight_layout()
plt.show()

print("""
ЧТО ВИДИМ:

Каждый pooling уменьшает размер в 2 раза
8x8 → 4x4 → 2x2

Картинка становится меньше
Но важные паттерны сохраняются!
""")




def average_pooling_manual(image, pool_size=2):
    """
    Average Pooling - берём СРЕДНЕЕ вместо максимума
    """
    h, w = image.shape
    new_h = h // pool_size
    new_w = w // pool_size
    
    output = np.zeros((new_h, new_w))
    
    for i in range(new_h):
        for j in range(new_w):
            start_i = i * pool_size
            start_j = j * pool_size
            
            block = image[start_i:start_i+pool_size, 
                         start_j:start_j+pool_size]
            
            # Берём СРЕДНЕЕ вместо максимума
            output[i, j] = np.mean(block)
    
    return output

# Тестируем
test_image = np.array([
    [1, 3, 2, 4],
    [5, 6, 7, 8],
    [9, 2, 1, 3],
    [4, 5, 6, 7]
], dtype=np.float32)

max_result = max_pooling_manual(test_image, 2)
avg_result = average_pooling_manual(test_image, 2)

print("Исходная картинка:")
print(test_image)

print("\nMax Pooling (максимум):")
print(max_result)

print("\nAverage Pooling (среднее):")
print(avg_result)

print("""
РАЗНИЦА:

Max Pooling - берёт САМОЕ ЯРКОЕ (максимум)
Average Pooling - берёт СРЕДНЕЕ

Max популярнее!
Лучше сохраняет важные детали
""")

# ============================================
# REZYUME
# ============================================

print("\n" + "="*60)
print("РЕЗЮМЕ:")
print("="*60)

print("""
POOLING - уменьшение размера картинки

MAX POOLING (популярный):
- Окно 2x2 скользит по картинке
- Из 4 чисел берём МАКСИМУМ
- Размер уменьшается в 2 раза

ПРИМЕР:
[1, 3]
[5, 6]  → max = 6

ЗАЧЕМ:
✓ Меньше вычислений (размер ↓)
✓ Оставляет важное
✓ Устойчивость к сдвигам

РАЗМЕРЫ:
Вход: 4x4
Max Pooling 2x2
Выход: 2x2

В CNN:
После свёртки обычно идёт pooling
Conv → Pooling → Conv → Pooling → ...

AVERAGE POOLING:
Берёт среднее вместо максимума
Реже используется

СЛЕДУЮЩИЙ ШАГ:
Собираем всё в CNN на Keras!
""")

print("\n Pooling освоен!")
print("="*60)