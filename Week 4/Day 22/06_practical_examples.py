# 06_practical_examples.py - Практические примеры

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

print("="*60)
print("ПРАКТИЧЕСКИЕ ПРИМЕРЫ")
print("="*60)

# ==========================================
# ПРИМЕР 1: ДАШБОРД ПРОДАЖ
# ==========================================

print("\n1. Дашборд продаж:")

# Данные
np.random.seed(42)
months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
sales = np.random.randint(100, 300, 12)
costs = sales * 0.7 + np.random.randint(-20, 20, 12)
profit = sales - costs

# Создать дашборд
fig = plt.figure(figsize=(16, 10))
fig.suptitle('Дашборд продаж за 2025 год', fontsize=20, fontweight='bold', y=0.98)

# График 1 - Динамика продаж (большой, вверху)
ax1 = plt.subplot(2, 3, (1, 3))
ax1.plot(months, sales, 'bo-', linewidth=2, markersize=8, label='Продажи')
ax1.plot(months, costs, 'ro-', linewidth=2, markersize=8, label='Расходы')
ax1.fill_between(range(len(months)), sales, costs, alpha=0.3, color='green')
ax1.set_title('Продажи vs Расходы', fontsize=14, fontweight='bold')
ax1.set_ylabel('Сумма (тыс. руб)')
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)

# График 2 - Прибыль по месяцам
ax2 = plt.subplot(2, 3, 4)
colors = ['green' if p > 0 else 'red' for p in profit]
ax2.bar(months, profit, color=colors, alpha=0.7)
ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
ax2.set_title('Прибыль по месяцам', fontweight='bold')
ax2.set_ylabel('Прибыль (тыс. руб)')
ax2.grid(True, alpha=0.3, axis='y')
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

# График 3 - Распределение продаж
ax3 = plt.subplot(2, 3, 5)
ax3.hist(sales, bins=10, color='skyblue', edgecolor='black', alpha=0.7)
ax3.axvline(sales.mean(), color='red', linestyle='--', linewidth=2, label=f'Среднее: {sales.mean():.0f}')
ax3.set_title('Распределение продаж', fontweight='bold')
ax3.set_xlabel('Продажи (тыс. руб)')
ax3.set_ylabel('Частота')
ax3.legend()
ax3.grid(True, alpha=0.3, axis='y')

# График 4 - Доля кварталов
ax4 = plt.subplot(2, 3, 6)
q1 = sales[:3].sum()
q2 = sales[3:6].sum()
q3 = sales[6:9].sum()
q4 = sales[9:].sum()
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
quarter_sales = [q1, q2, q3, q4]
colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
ax4.pie(quarter_sales, labels=quarters, colors=colors_pie, autopct='%1.1f%%', startangle=90)
ax4.set_title('Доля кварталов', fontweight='bold')

plt.tight_layout()
plt.savefig('plots/dashboard_sales.png', dpi=150, bbox_inches='tight')
plt.show()

print("✓ Дашборд продаж создан")

# ==========================================
# ПРИМЕР 2: СРАВНЕНИЕ ПРОДУКТОВ
# ==========================================

print("\n2. Сравнение продуктов:")

products = ['Продукт A', 'Продукт B', 'Продукт C', 'Продукт D', 'Продукт E']
metrics = ['Продажи', 'Прибыль', 'Удовл.\nклиентов', 'Доля\nрынка']

# Данные (нормализованные 0-100)
data = np.array([
    [85, 75, 90, 70],  # A
    [70, 80, 85, 60],  # B
    [90, 85, 88, 75],  # C
    [65, 70, 80, 55],  # D
    [80, 90, 92, 68]   # E
])

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# График 1 - Сгруппированная столбчатая
x = np.arange(len(products))
width = 0.2

for i, metric in enumerate(metrics):
    offset = width * (i - len(metrics)/2 + 0.5)
    axes[0].bar(x + offset, data[:, i], width, label=metric, alpha=0.8)

axes[0].set_title('Сравнение продуктов по метрикам', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Продукты')
axes[0].set_ylabel('Показатель (0-100)')
axes[0].set_xticks(x)
axes[0].set_xticklabels(products)
axes[0].legend()
axes[0].grid(True, alpha=0.3, axis='y')

# График 2 - Тепловая карта
im = axes[1].imshow(data.T, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
axes[1].set_title('Тепловая карта метрик', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Продукты')
axes[1].set_ylabel('Метрики')
axes[1].set_xticks(range(len(products)))
axes[1].set_xticklabels(products)
axes[1].set_yticks(range(len(metrics)))
axes[1].set_yticklabels(metrics)

# Добавить значения
for i in range(len(metrics)):
    for j in range(len(products)):
        text = axes[1].text(j, i, f'{data[j, i]:.0f}',
                           ha="center", va="center", color="black", fontweight='bold')

# Цветовая шкала
plt.colorbar(im, ax=axes[1], label='Показатель')

plt.tight_layout()
plt.savefig('plots/product_comparison.png', dpi=150, bbox_inches='tight')
plt.show()

print("✓ Сравнение продуктов создано")

# ==========================================
# ПРИМЕР 3: ВРЕМЕННОЙ РЯД С ПРОГНОЗОМ
# ==========================================

print("\n3. Временной ряд с прогнозом:")

# Исторические данные
dates = pd.date_range('2024-01-01', periods=12, freq='M')
actual = 100 + np.cumsum(np.random.randn(12) * 10)

# Прогноз
forecast_dates = pd.date_range('2025-01-01', periods=6, freq='M')
forecast = actual[-1] + np.cumsum(np.random.randn(6) * 8)

# Доверительный интервал
upper_bound = forecast + 15
lower_bound = forecast - 15

fig, ax = plt.subplots(figsize=(14, 6))

# Исторические данные
ax.plot(dates, actual, 'bo-', linewidth=2, markersize=6, label='Фактические данные')

# Прогноз
ax.plot(forecast_dates, forecast, 'r--', linewidth=2, label='Прогноз')
ax.fill_between(forecast_dates, lower_bound, upper_bound, alpha=0.3, color='red', label='Доверительный интервал')

# Вертикальная линия разделения
ax.axvline(dates[-1], color='black', linestyle=':', linewidth=1, label='Граница прогноза')

ax.set_title('Прогноз продаж на 2025 год', fontsize=16, fontweight='bold')
ax.set_xlabel('Дата')
ax.set_ylabel('Продажи')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

# Форматирование дат
fig.autofmt_xdate()

plt.tight_layout()
plt.savefig('plots/forecast.png', dpi=150, bbox_inches='tight')
plt.show()

print("✓ Прогноз создан")

# ==========================================
# ПРИМЕР 4: ВОРОНКА ПРОДАЖ
# ==========================================

print("\n4. Воронка продаж:")

stages = ['Визиты', 'Регистрации', 'Добавили\nв корзину', 'Начали\nоформление', 'Оплатили']
values = [10000, 5000, 2500, 1500, 1000]
colors_funnel = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# График 1 - Воронка (горизонтальные столбцы)
y_pos = np.arange(len(stages))
ax1.barh(y_pos, values, color=colors_funnel, alpha=0.8)

# Добавить значения и проценты
for i, (stage, value) in enumerate(zip(stages, values)):
    pct = (value / values[0]) * 100
    ax1.text(value + 200, i, f'{value:,} ({pct:.1f}%)', va='center', fontweight='bold')

ax1.set_yticks(y_pos)
ax1.set_yticklabels(stages)
ax1.invert_yaxis()
ax1.set_xlabel('Количество')
ax1.set_title('Воронка продаж', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='x')

# График 2 - Конверсия между этапами
conversions = [(values[i+1] / values[i]) * 100 for i in range(len(values)-1)]
stage_transitions = [f'{stages[i]}\n→\n{stages[i+1]}' for i in range(len(stages)-1)]

bars = ax2.bar(range(len(conversions)), conversions, color=colors_funnel[1:], alpha=0.8)
ax2.set_xticks(range(len(conversions)))
ax2.set_xticklabels(stage_transitions, fontsize=9)
ax2.set_ylabel('Конверсия (%)')
ax2.set_title('Конверсия между этапами', fontsize=14, fontweight='bold')
ax2.axhline(y=50, color='red', linestyle='--', linewidth=1, label='Цель: 50%')
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

# Добавить значения на столбцы
for bar, conv in zip(bars, conversions):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{conv:.1f}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('plots/sales_funnel.png', dpi=150, bbox_inches='tight')
plt.show()

print("✓ Воронка продаж создана")

# ==========================================
# ПРИМЕР 5: КPI ДАШБОРД
# ==========================================

print("\n5. KPI дашборд:")

fig = plt.figure(figsize=(16, 10))
fig.suptitle('KPI Dashboard - Ноябрь 2025', fontsize=20, fontweight='bold', y=0.98)

# KPI значения
kpis = {
    'Выручка': {'value': 2_450_000, 'target': 2_000_000, 'unit': 'руб'},
    'Новые клиенты': {'value': 450, 'target': 500, 'unit': 'чел'},
    'Конверсия': {'value': 3.2, 'target': 3.0, 'unit': '%'},
    'Средний чек': {'value': 5_444, 'target': 5_000, 'unit': 'руб'}
}

# Создать карточки KPI
for i, (name, data) in enumerate(kpis.items()):
    ax = plt.subplot(2, 4, i + 1)
    ax.axis('off')
    
    # Прогресс
    progress = (data['value'] / data['target']) * 100
    color = 'green' if progress >= 100 else 'orange' if progress >= 80 else 'red'
    
    # Заголовок
    ax.text(0.5, 0.9, name, ha='center', fontsize=14, fontweight='bold', transform=ax.transAxes)
    
    # Значение
    if data['unit'] == 'руб':
        value_text = f"{data['value']:,.0f} {data['unit']}"
    else:
        value_text = f"{data['value']} {data['unit']}"
    ax.text(0.5, 0.6, value_text, ha='center', fontsize=18, fontweight='bold', color=color, transform=ax.transAxes)
    
    # Цель
    target_text = f"Цель: {data['target']:,.0f} {data['unit']}"
    ax.text(0.5, 0.4, target_text, ha='center', fontsize=10, transform=ax.transAxes)
    
    # Прогресс бар
    ax.barh([0], [progress], height=0.5, color=color, alpha=0.7)
    ax.barh([0], [100], height=0.5, color='lightgray', alpha=0.3)
    ax.set_xlim(0, 120)
    ax.set_ylim(-0.5, 0.5)
    ax.text(progress + 2, 0, f'{progress:.0f}%', va='center', fontweight='bold')

# Графики внизу
# Динамика выручки
ax5 = plt.subplot(2, 2, 3)
weeks = ['Нед 1', 'Нед 2', 'Нед 3', 'Нед 4']
weekly_revenue = [580000, 620000, 590000, 660000]
ax5.plot(weeks, weekly_revenue, 'go-', linewidth=2, markersize=8)
ax5.set_title('Динамика выручки по неделям', fontweight='bold')
ax5.set_ylabel('Выручка (руб)')
ax5.grid(True, alpha=0.3)
for i, v in enumerate(weekly_revenue):
    ax5.text(i, v + 10000, f'{v:,.0f}', ha='center', fontsize=9)

# Источники трафика
ax6 = plt.subplot(2, 2, 4)
sources = ['Поиск', 'Реклама', 'Соцсети', 'Прямой', 'Другие']
traffic = [35, 30, 20, 10, 5]
colors_traffic = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
ax6.pie(traffic, labels=sources, colors=colors_traffic, autopct='%1.1f%%', startangle=90)
ax6.set_title('Источники трафика', fontweight='bold')

plt.tight_layout()
plt.savefig('plots/kpi_dashboard.png', dpi=150, bbox_inches='tight')
plt.show()

print("✓ KPI дашборд создан")

print("\n" + "="*60)
print("✅ ВСЕ ПРИМЕРЫ СОЗДАНЫ И СОХРАНЕНЫ В 'plots/'")
print("="*60)