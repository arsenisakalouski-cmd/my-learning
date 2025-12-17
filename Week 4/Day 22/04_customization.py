import matplotlib.pyplot as plt
import numpy as np

print("="*60)
print("НАСТРОЙКА ГРАФИКОВ В Matplotlib")
print("="*60)

print("\n1. Встроенные стили:")

# Доступные стили
print(f"Доступные стили: {plt.style.available}")

# Данные
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Попробовать разные стили
styles_to_try = ['default', 'seaborn-v0_8', 'ggplot', 'fivethirtyeight']

for style in styles_to_try:
    if style in plt.style.available:
        plt.style.use(style)
        
        plt.figure(figsize=(10, 6))
        plt.plot(x, y1, label='sin(x)', linewidth=2)
        plt.plot(x, y2, label='cos(x)', linewidth=2)
        
        plt.title(f'Стиль: {style}', fontsize=16, fontweight='bold')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()

# Вернуть default
plt.style.use('default')

print("✓ Стили показаны")

# ==========================================
# 2. ЦВЕТОВЫЕ ПАЛИТРЫ
# ==========================================

print("\n2. Цветовые палитры:")

# Создать данные
categories = ['A', 'B', 'C', 'D', 'E', 'F']
values = [23, 45, 56, 78, 32, 67]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Палитра 1 - Пастельные
colors1 = ['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE1FF', '#E0BBE4']
axes[0, 0].bar(categories, values, color=colors1)
axes[0, 0].set_title('Пастельные цвета', fontweight='bold')

# Палитра 2 - Яркие
colors2 = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
axes[0, 1].bar(categories, values, color=colors2)
axes[0, 1].set_title('Яркие цвета', fontweight='bold')

# Палитра 3 - Монохромная
colors3 = ['#08519c', '#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#eff3ff']
axes[1, 0].bar(categories, values, color=colors3)
axes[1, 0].set_title('Монохромная (синяя)', fontweight='bold')

# Палитра 4 - Градиент
cmap = plt.cm.viridis
colors4 = [cmap(i/len(values)) for i in range(len(values))]
axes[1, 1].bar(categories, values, color=colors4)
axes[1, 1].set_title('Градиент (viridis)', fontweight='bold')

plt.tight_layout()
plt.show()

print("✓ Палитры показаны")



print("\n3. Настройка шрифтов:")

fig, ax = plt.subplots(figsize=(10, 6))

x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), linewidth=2)

# Разные шрифты и размеры
ax.set_title('Большой жирный заголовок', 
             fontsize=20, 
             fontweight='bold',
             fontstyle='italic',
             color='darkblue')

ax.set_xlabel('Ось X (средний размер)', 
              fontsize=14,
              fontweight='normal',
              color='darkgreen')

ax.set_ylabel('Ось Y (средний размер)',
              fontsize=14,
              fontweight='normal',
              color='darkred')

# Текст на графике
ax.text(5, 0.5, 'Аннотация',
        fontsize=16,
        fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("✓ Шрифты показаны")


print("\n4. Настройка легенд:")

fig, ax = plt.subplots(figsize=(10, 6))

x = np.linspace(0, 10, 100)

ax.plot(x, np.sin(x), 'b-', linewidth=2, label='Синус')
ax.plot(x, np.cos(x), 'r-', linewidth=2, label='Косинус')
ax.plot(x, np.sin(x) * np.cos(x), 'g-', linewidth=2, label='Произведение')

# Легенда с настройками
ax.legend(loc='upper right',           # Позиция
          fontsize=12,                 # Размер шрифта
          frameon=True,                # Рамка
          fancybox=True,               # Скруглённые углы
          shadow=True,                 # Тень
          ncol=1,                      # Количество столбцов
          title='Функции',             # Заголовок легенды
          title_fontsize=14)

ax.set_title('График с легендой', fontsize=16, fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Разные позиции легенды
positions = ['upper left', 'upper right', 'lower left', 'lower right', 
             'center', 'center left', 'center right']

print(f"\nДоступные позиции: {positions}")

print("✓ Легенды показаны")




print("\n5. Настройка сетки:")

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

x = np.linspace(0, 10, 100)
y = np.sin(x)

# Простая сетка
axes[0, 0].plot(x, y)
axes[0, 0].grid(True)
axes[0, 0].set_title('Простая сетка')

# Только по Y
axes[0, 1].plot(x, y)
axes[0, 1].grid(True, axis='y')
axes[0, 1].set_title('Только по Y')

# Настроенная сетка
axes[1, 0].plot(x, y)
axes[1, 0].grid(True, 
                linestyle='--',      # Стиль
                linewidth=1,         # Толщина
                color='red',         # Цвет
                alpha=0.5)           # Прозрачность
axes[1, 0].set_title('Настроенная сетка')

# Две сетки (основная + вспомогательная)
axes[1, 1].plot(x, y)
axes[1, 1].grid(True, which='major', linestyle='-', linewidth=1.5, alpha=0.7)
axes[1, 1].grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.5)
axes[1, 1].minorticks_on()  # Включить мелкие деления
axes[1, 1].set_title('Двойная сетка')

plt.tight_layout()
plt.show()

print("✓ Сетки показаны")



print("\n6. Аннотации и стрелки:")

fig, ax = plt.subplots(figsize=(10, 6))

x = np.linspace(0, 10, 100)
y = np.sin(x)

ax.plot(x, y, 'b-', linewidth=2)

# Простая аннотация
ax.text(5, 0.5, 'Простой текст', fontsize=12)

# Аннотация со стрелкой
ax.annotate('Максимум',
            xy=(np.pi/2, 1),           # Точка на графике
            xytext=(3, 0.5),           # Позиция текста
            fontsize=12,
            arrowprops=dict(
                arrowstyle='->',       # Стиль стрелки
                connectionstyle='arc3,rad=0.3',  # Изгиб
                color='red',
                lw=2
            ),
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

# Ещё аннотация
ax.annotate('Минимум',
            xy=(3*np.pi/2, -1),
            xytext=(6, -0.5),
            fontsize=12,
            arrowprops=dict(arrowstyle='->', color='green', lw=2),
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

ax.set_title('Аннотации и стрелки', fontsize=16, fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("✓ Аннотации показаны")


# ==========================================
# 7. ЗАПОЛНЕНИЕ ОБЛАСТИ
# ==========================================

print("\n7. Заполнение области:")

fig, ax = plt.subplots(figsize=(10, 6))

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Линии
ax.plot(x, y1, 'b-', linewidth=2, label='sin(x)')
ax.plot(x, y2, 'r-', linewidth=2, label='cos(x)')

# Заполнить область между линиями
ax.fill_between(x, y1, y2, 
                where=(y1 >= y2),     # Условие
                alpha=0.3,            # Прозрачность
                color='blue',
                label='sin > cos')

ax.fill_between(x, y1, y2,
                where=(y1 < y2),
                alpha=0.3,
                color='red',
                label='cos > sin')

ax.set_title('Заполнение области', fontsize=16, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("✓ Заполнение показано")

# ==========================================
# 8. ЛОГАРИФМИЧЕСКИЕ ШКАЛЫ
# ==========================================

print("\n8. Логарифмические шкалы:")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

x = np.linspace(1, 100, 100)
y = np.exp(x / 10)

# Обычная шкала
axes[0].plot(x, y)
axes[0].set_title('Обычная шкала')
axes[0].grid(True, alpha=0.3)

# Логарифмическая Y
axes[1].semilogy(x, y)
axes[1].set_title('Log Y')
axes[1].grid(True, alpha=0.3)

# Логарифмическая X и Y
axes[2].loglog(x, y)
axes[2].set_title('Log X и Log Y')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("✓ Логарифмические шкалы показаны")

print("\n" + "="*60)
print("ИТОГИ:")
print("="*60)
print("""
Настройка графиков:

Стили:
- plt.style.use('seaborn')
- Встроенные стили: plt.style.available

Цвета:
- Hex: '#FF6B6B'
- Названия: 'red', 'blue'
- Палитры: plt.cm.viridis

Шрифты:
- fontsize - размер
- fontweight - жирность ('normal', 'bold')
- fontstyle - стиль ('normal', 'italic')

Легенда:
- loc - позиция
- frameon - рамка
- shadow - тень
- ncol - столбцов

Сетка:
- grid(True, axis='y')
- linestyle, linewidth, color, alpha

Аннотации:
- text() - простой текст
- annotate() - со стрелкой
- bbox - рамка вокруг текста

Специальное:
- fill_between() - заполнение
- semilogy(), loglog() - лог шкалы
""")