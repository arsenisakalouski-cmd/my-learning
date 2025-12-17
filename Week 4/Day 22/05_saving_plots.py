# 05_saving_plots.py - Сохранение графиков

import matplotlib.pyplot as plt
import numpy as np
import os

print("="*60)
print("СОХРАНЕНИЕ ГРАФИКОВ")
print("="*60)

# Создать папку для графиков
if not os.path.exists('plots'):
    os.makedirs('plots')
    print("✓ Папка 'plots' создана")

# ==========================================
# 1. БАЗОВОЕ СОХРАНЕНИЕ
# ==========================================

print("\n1. Базовое сохранение:")

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, linewidth=2)
plt.title('Синус', fontsize=16, fontweight='bold')
plt.xlabel('X')
plt.ylabel('sin(X)')
plt.grid(True, alpha=0.3)

# Сохранить
plt.savefig('plots/01_basic.png')
"""
savefig(filename) - сохранить график в файл
Поддерживаемые форматы: png, jpg, pdf, svg, eps
"""
print("✓ Сохранено: plots/01_basic.png")

plt.close()  # Закрыть фигуру (не показывать)

# ==========================================
# 2. РАЗНЫЕ ФОРМАТЫ
# ==========================================

print("\n2. Разные форматы:")

plt.figure(figsize=(10, 6))
plt.plot(x, y, linewidth=2)
plt.title('График в разных форматах', fontsize=16, fontweight='bold')
plt.grid(True, alpha=0.3)

# PNG - растровый (для веба)
plt.savefig('plots/02_format.png')
print("✓ PNG сохранён")

# PDF - векторный (для печати)
plt.savefig('plots/02_format.pdf')
print("✓ PDF сохранён")

# SVG - векторный (для редактирования)
plt.savefig('plots/02_format.svg')
print("✓ SVG сохранён")

# JPEG - растровый (меньше размер)
plt.savefig('plots/02_format.jpg')
print("✓ JPEG сохранён")

plt.close()

# ==========================================
# 3. DPI (РАЗРЕШЕНИЕ)
# ==========================================

print("\n3. Разрешение (DPI):")

plt.figure(figsize=(10, 6))
plt.plot(x, y, linewidth=2)
plt.title('Разное разрешение', fontsize=16, fontweight='bold')
plt.grid(True, alpha=0.3)

# Низкое разрешение (для веба)
plt.savefig('plots/03_dpi_72.png', dpi=72)
print("✓ 72 DPI (веб)")

# Среднее (стандарт)
plt.savefig('plots/03_dpi_150.png', dpi=150)
print("✓ 150 DPI (стандарт)")

# Высокое (для печати)
plt.savefig('plots/03_dpi_300.png', dpi=300)
print("✓ 300 DPI (печать)")

plt.close()

"""
DPI (Dots Per Inch):
- 72 - веб, экран
- 150 - средний
- 300 - печать, публикации
Больше DPI = больше размер файла
"""

# ==========================================
# 4. ОБРЕЗКА ПОЛЕЙ
# ==========================================

print("\n4. Обрезка полей:")

plt.figure(figsize=(10, 6))
plt.plot(x, y, linewidth=2)
plt.title('Обрезка полей', fontsize=16, fontweight='bold')
plt.grid(True, alpha=0.3)

# С полями (по умолчанию)
plt.savefig('plots/04_with_padding.png')
print("✓ С полями")

# Без лишних полей
plt.savefig('plots/04_tight.png', bbox_inches='tight')
"""
bbox_inches='tight' - убрать лишние поля
Полезно для вставки в документы
"""
print("✓ Без полей (tight)")

plt.close()

# ==========================================
# 5. ПРОЗРАЧНЫЙ ФОН
# ==========================================

print("\n5. Прозрачный фон:")

plt.figure(figsize=(10, 6))
plt.plot(x, y, linewidth=2)
plt.title('Прозрачный фон', fontsize=16, fontweight='bold')
plt.grid(True, alpha=0.3)

# Белый фон
plt.savefig('plots/05_white_bg.png')
print("✓ Белый фон")

# Прозрачный фон
plt.savefig('plots/05_transparent.png', transparent=True)
"""
transparent=True - прозрачный фон
Полезно для презентаций, наложения на другие изображения
"""
print("✓ Прозрачный фон")

plt.close()

# ==========================================
# 6. КАЧЕСТВО JPEG
# ==========================================

print("\n6. Качество JPEG:")

plt.figure(figsize=(10, 6))
plt.plot(x, y, linewidth=2)
plt.title('Качество JPEG', fontsize=16, fontweight='bold')
plt.grid(True, alpha=0.3)

# В новых версиях Matplotlib качество JPEG настраивается через pil_kwargs
# Низкое качество (маленький файл)
plt.savefig('plots/06_quality_low.jpg', pil_kwargs={'quality': 30})
print("✓ Низкое качество (30)")

# Среднее
plt.savefig('plots/06_quality_medium.jpg', pil_kwargs={'quality': 70})
print("✓ Среднее качество (70)")

# Высокое
plt.savefig('plots/06_quality_high.jpg', pil_kwargs={'quality': 95})
print("✓ Высокое качество (95)")

plt.close()

"""
pil_kwargs={'quality': N} для JPEG:
1-100, где 100 = лучшее качество
Меньше = больше артефактов, но меньше размер

Работает в Matplotlib 3.x+
"""

# ==========================================
# 7. ЦВЕТ ФОНА
# ==========================================

print("\n7. Цвет фона:")

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(x, y, linewidth=2, color='white')
ax.set_title('Тёмный фон', fontsize=16, fontweight='bold', color='white')
ax.set_xlabel('X', color='white')
ax.set_ylabel('Y', color='white')

# Изменить цвет фона
fig.patch.set_facecolor('#2C3E50')  # Фон фигуры
ax.set_facecolor('#34495E')         # Фон графика
ax.grid(True, alpha=0.3, color='white')
ax.tick_params(colors='white')      # Цвет делений

plt.savefig('plots/07_dark_theme.png', facecolor='#2C3E50')
print("✓ Тёмная тема")

plt.close()

# ==========================================
# 8. ПАКЕТНОЕ СОХРАНЕНИЕ
# ==========================================

print("\n8. Пакетное сохранение:")

functions = {
    'sin': np.sin,
    'cos': np.cos,
    'tan': np.tan
}

for name, func in functions.items():
    plt.figure(figsize=(10, 6))
    
    try:
        y = func(x)
        plt.plot(x, y, linewidth=2)
        plt.title(f'Функция {name}(x)', fontsize=16, fontweight='bold')
        plt.xlabel('X')
        plt.ylabel(f'{name}(X)')
        plt.grid(True, alpha=0.3)
        
        if name == 'tan':
            plt.ylim(-5, 5)
        
        # Сохранить
        filename = f'plots/08_{name}.png'
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"✓ Сохранён: {filename}")
        
    finally:
        plt.close()

# ==========================================
# 9. СУБПЛОТЫ
# ==========================================

print("\n9. Сохранение субплотов:")

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# График 1
axes[0, 0].plot(x, np.sin(x))
axes[0, 0].set_title('sin(x)')
axes[0, 0].grid(True, alpha=0.3)

# График 2
axes[0, 1].plot(x, np.cos(x))
axes[0, 1].set_title('cos(x)')
axes[0, 1].grid(True, alpha=0.3)

# График 3
axes[1, 0].plot(x, np.tan(x))
axes[1, 0].set_title('tan(x)')
axes[1, 0].set_ylim(-5, 5)
axes[1, 0].grid(True, alpha=0.3)

# График 4
axes[1, 1].plot(x, np.exp(x/5))
axes[1, 1].set_title('exp(x/5)')
axes[1, 1].grid(True, alpha=0.3)

fig.suptitle('Тригонометрические функции', fontsize=18, fontweight='bold')

plt.tight_layout()
plt.savefig('plots/09_subplots.png', dpi=150, bbox_inches='tight')
print("✓ Субплоты сохранены")

plt.close()

# ==========================================
# 10. ИНФОРМАЦИЯ О ФАЙЛАХ
# ==========================================

print("\n" + "="*60)
print("ИНФОРМАЦИЯ О СОХРАНЁННЫХ ФАЙЛАХ:")
print("="*60)

import os

for filename in sorted(os.listdir('plots')):
    filepath = os.path.join('plots', filename)
    size = os.path.getsize(filepath)
    
    # Размер в KB
    size_kb = size / 1024
    
    print(f"{filename:30s} - {size_kb:8.2f} KB")

print("\n" + "="*60)
print("ИТОГИ:")
print("="*60)
print("""
Сохранение графиков:

Базовое:
- plt.savefig('filename.png')
- Форматы: png, jpg, pdf, svg, eps

Параметры:
- dpi=300 - разрешение
- bbox_inches='tight' - без полей
- transparent=True - прозрачный фон
- quality=95 - качество JPEG (1-100)
- facecolor='color' - цвет фона

DPI:
- 72 - веб
- 150 - стандарт
- 300 - печать

Форматы:
- PNG - универсальный, поддерживает прозрачность
- JPEG - меньший размер, без прозрачности
- PDF - векторный, для печати
- SVG - векторный, для редактирования

Важно:
- plt.close() после сохранения
- bbox_inches='tight' для экономии места
- Высокий DPI только для печати
- Проверяйте размер файлов
""")

print(f"\n✅ Все графики сохранены в папке 'plots/'")