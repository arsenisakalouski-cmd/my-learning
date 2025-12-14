# 06_pandas_practice.py - Практические задачи

import pandas as pd
import numpy as np

print("="*60)
print("ПРАКТИЧЕСКИЕ ЗАДАЧИ Pandas")
print("="*60)

# ==========================================
# ЗАДАЧА 1: АНАЛИЗ ПРОДАЖ МАГАЗИНА
# ==========================================

print("\n" + "="*60)
print("ЗАДАЧА 1: Анализ продаж магазина")
print("="*60)

# Создать данные
np.random.seed(42)

dates = pd.date_range('2025-01-01', periods=100)
categories = ['Электроника', 'Одежда', 'Продукты', 'Книги']
cities = ['Москва', 'СПб', 'Казань']

sales_data = pd.DataFrame({
    'date': np.random.choice(dates, 200),
    'category': np.random.choice(categories, 200),
    'city': np.random.choice(cities, 200),
    'amount': np.random.randint(100, 10000, 200),
    'quantity': np.random.randint(1, 10, 200)
})

print(f"Данные о продажах:\n{sales_data.head(10)}")

# 1. Общая статистика
print(f"\n--- Общая статистика ---")
print(f"Всего транзакций: {len(sales_data)}")
print(f"Общая сумма: {sales_data['amount'].sum():,.0f} руб")
print(f"Средний чек: {sales_data['amount'].mean():.0f} руб")
print(f"Медианный чек: {sales_data['amount'].median():.0f} руб")

# 2. По категориям
print(f"\n--- По категориям ---")
by_category = sales_data.groupby('category').agg({
    'amount': ['sum', 'mean', 'count']
}).round(0)
print(by_category.sort_values(('amount', 'sum'), ascending=False))

# 3. По городам
print(f"\n--- По городам ---")
by_city = sales_data.groupby('city')['amount'].sum().sort_values(ascending=False)
print(by_city)

# 4. Топ-5 дней по продажам
print(f"\n--- Топ-5 дней ---")
by_date = sales_data.groupby('date')['amount'].sum().sort_values(ascending=False).head(5)
print(by_date)

# 5. Сводная таблица
print(f"\n--- Сводная таблица: категория × город ---")
pivot = pd.pivot_table(
    sales_data,
    values='amount',
    index='category',
    columns='city',
    aggfunc='sum',
    fill_value=0
)
print(pivot)

# ==========================================
# ЗАДАЧА 2: ОБРАБОТКА ДАННЫХ СОТРУДНИКОВ
# ==========================================

print("\n" + "="*60)
print("ЗАДАЧА 2: Обработка данных сотрудников")
print("="*60)

# Грязные данные
employee_data = pd.DataFrame({
    'id': [1, 2, 3, 4, 5, 6, 7, 8],
    'name': ['иван иванов', 'МАРИЯ ПЕТРОВА', None, 'Пётр Сидоров', 
             'анна', 'Сергей', 'Ольга Смирнова', ''],
    'age': [25, 30, 35, -5, 150, 28, np.nan, 33],
    'salary': [50000, 60000, np.nan, 45000, 70000, 0, 55000, 48000],
    'department': ['IT', 'hr', 'IT', 'sales', 'IT', 'HR', 'Sales', None],
    'email': ['ivan@company.com', 'maria@', 'petr@company.com', 
              'anna@company.com', None, 'sergey@company.com', 
              'olga@company.com', 'alex']
})

print(f"Грязные данные:\n{employee_data}")

# Очистка
cleaned = employee_data.copy()

# 1. Очистка имён
# Удалить пустые
cleaned = cleaned[cleaned['name'].notna()]
cleaned = cleaned[cleaned['name'] != '']

# Привести к Title Case
cleaned['name'] = cleaned['name'].str.title()

# 2. Очистка возраста
# Убрать невалидные
cleaned = cleaned[(cleaned['age'] >= 18) & (cleaned['age'] <= 100)]

# 3. Очистка зарплаты
# 0 → NaN, затем заполнить средним
cleaned.loc[cleaned['salary'] == 0, 'salary'] = np.nan
cleaned['salary'] = cleaned['salary'].fillna(cleaned['salary'].mean())

# 4. Очистка отдела
# Привести к единому формату
cleaned['department'] = cleaned['department'].str.title()

# 5. Очистка email
# Удалить невалидные
cleaned = cleaned[cleaned['email'].str.contains('@', na=False)]
cleaned = cleaned[cleaned['email'].str.contains(r'@.*\.', na=False, regex=True)]

print(f"\n--- Результат очистки ---")
print(f"Было строк: {len(employee_data)}")
print(f"Стало строк: {len(cleaned)}")
print(f"\nОчищенные данные:\n{cleaned}")

# Статистика
print(f"\n--- Статистика по отделам ---")
dept_stats = cleaned.groupby('department').agg({
    'age': 'mean',
    'salary': ['mean', 'min', 'max']
}).round(0)
print(dept_stats)

# ==========================================
# ЗАДАЧА 3: АНАЛИЗ ВРЕМЕННОГО РЯДА
# ==========================================

print("\n" + "="*60)
print("ЗАДАЧА 3: Анализ временного ряда")
print("="*60)

# Дневные данные за 3 месяца
dates = pd.date_range('2025-01-01', periods=90)
temperature = 20 + np.random.randn(90) * 5
temperature = temperature + np.sin(np.arange(90) / 10) * 3  # Волна

ts = pd.DataFrame({
    'date': dates,
    'temperature': temperature
})

print(f"Временной ряд:\n{ts.head(10)}")

# Добавить временные признаки
ts['year'] = ts['date'].dt.year
ts['month'] = ts['date'].dt.month
ts['day'] = ts['date'].dt.day
ts['weekday'] = ts['date'].dt.day_name()
ts['week'] = ts['date'].dt.isocalendar().week

print(f"\nС временными признаками:\n{ts.head()}")

# Статистика по месяцам
monthly = ts.groupby('month')['temperature'].agg(['mean', 'min', 'max']).round(1)
print(f"\n--- По месяцам ---")
print(monthly)

# По дням недели
weekly = ts.groupby('weekday')['temperature'].mean().round(1)
print(f"\n--- По дням недели ---")
print(weekly)

# Скользящее среднее (7 дней)
ts['moving_avg_7'] = ts['temperature'].rolling(window=7).mean()
print(f"\nСо скользящим средним:\n{ts[['date', 'temperature', 'moving_avg_7']].head(10)}")

# Аномалии (> 2 стандартных отклонений)
mean = ts['temperature'].mean()
std = ts['temperature'].std()
ts['is_anomaly'] = (ts['temperature'] - mean).abs() > 2 * std

anomalies = ts[ts['is_anomaly']]
print(f"\nАномалии ({len(anomalies)} дней):")
print(anomalies[['date', 'temperature']])

# ==========================================
# ЗАДАЧА 4: ОБЪЕДИНЕНИЕ ДАННЫХ
# ==========================================

print("\n" + "="*60)
print("ЗАДАЧА 4: Объединение данных из разных источников")
print("="*60)

# Данные из разных источников
orders = pd.DataFrame({
    'order_id': [1, 2, 3, 4, 5],
    'customer_id': [101, 102, 101, 103, 102],
    'product_id': [501, 502, 503, 501, 502],
    'quantity': [2, 1, 3, 1, 2],
    'date': pd.date_range('2025-01-01', periods=5)
})

customers = pd.DataFrame({
    'customer_id': [101, 102, 103],
    'name': ['ООО "Альфа"', 'ИП Бета', 'ООО "Гамма"'],
    'city': ['Москва', 'СПб', 'Казань'],
    'segment': ['VIP', 'Regular', 'VIP']
})

products = pd.DataFrame({
    'product_id': [501, 502, 503],
    'name': ['Товар А', 'Товар Б', 'Товар В'],
    'price': [1000, 1500, 2000],
    'category': ['Категория 1', 'Категория 2', 'Категория 1']
})

print(f"Заказы:\n{orders}")
print(f"\nКлиенты:\n{customers}")
print(f"\nПродукты:\n{products}")

# Объединить
full_data = orders.merge(customers, on='customer_id')
full_data = full_data.merge(products, on='product_id')
full_data['total'] = full_data['quantity'] * full_data['price']

print(f"\nПолные данные:\n{full_data}")

# Анализ
print(f"\n--- Анализ ---")
print(f"Всего заказов: {len(full_data)}")
print(f"Общая сумма: {full_data['total'].sum():,.0f} руб")

print(f"\nПо клиентам:")
by_customer = full_data.groupby('name')['total'].sum().sort_values(ascending=False)
print(by_customer)

print(f"\nПо категориям:")
by_category = full_data.groupby('category')['total'].sum().sort_values(ascending=False)
print(by_category)

print(f"\nПо сегментам:")
by_segment = full_data.groupby('segment')['total'].agg(['sum', 'mean', 'count'])
print(by_segment)

# VIP vs Regular
vip_sales = full_data[full_data['segment'] == 'VIP']['total'].sum()
regular_sales = full_data[full_data['segment'] == 'Regular']['total'].sum()
print(f"\nVIP: {vip_sales:,.0f} руб ({vip_sales/(vip_sales+regular_sales)*100:.1f}%)")
print(f"Regular: {regular_sales:,.0f} руб ({regular_sales/(vip_sales+regular_sales)*100:.1f}%)")

# ==========================================
# ЗАДАЧА 5: ТОП ПРОДУКТОВ
# ==========================================

print("\n" + "="*60)
print("ЗАДАЧА 5: Топ продуктов по продажам")
print("="*60)

# Данные продаж
np.random.seed(42)
product_sales = pd.DataFrame({
    'product': [f'Товар {i}' for i in range(1, 21)] * 10,
    'month': np.repeat(range(1, 11), 20),
    'sales': np.random.randint(100, 1000, 200)
})

print(f"Данные:\n{product_sales.head(10)}")

# Общие продажи по продуктам
total_sales = product_sales.groupby('product')['sales'].sum().sort_values(ascending=False)

# Топ-5
top5 = total_sales.head(5)
print(f"\nТоп-5 продуктов:\n{top5}")

# Худшие 5
bottom5 = total_sales.tail(5)
print(f"\nХудшие 5 продуктов:\n{bottom5}")

# Динамика топ-3 по месяцам
top3_products = top5.head(3).index.tolist()
top3_dynamics = product_sales[product_sales['product'].isin(top3_products)]
top3_pivot = top3_dynamics.pivot_table(
    values='sales',
    index='month',
    columns='product',
    aggfunc='sum'
)
print(f"\nДинамика топ-3:\n{top3_pivot}")

# Рост по месяцам
growth = top3_pivot.pct_change() * 100
print(f"\nПроцентный рост:\n{growth.round(1)}")

print("\n" + "="*60)
print("✅ ВСЕ ЗАДАЧИ РЕШЕНЫ!")
print("="*60)