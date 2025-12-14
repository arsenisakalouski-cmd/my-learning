import pandas as pd
import numpy as np

print("="*60)
print("ОБЪЕДИНЕНИЕ ДАННЫХ В Pandas")
print("="*60)


print("\n1. Тестовые таблицы:")

# Таблица сотрудников
employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5],
    'name': ['Иван', 'Мария', 'Пётр', 'Анна', 'Сергей'],
    'dept_id': [10, 20, 10, 30, 20]
})

# Таблица отделов
departments = pd.DataFrame({
    'dept_id': [10, 20, 30],
    'dept_name': ['IT', 'HR', 'Sales'],
    'location': ['Москва', 'СПб', 'Казань']
})

print(f"\nСотрудники:\n{employees}")
print(f"\nОтделы:\n{departments}")


print("\n" + "="*60)
print("2. Merge - Inner Join:")
print("="*60)

# Inner join (пересечение)
inner = pd.merge(employees, departments, on='dept_id')
print(f"\nInner join:\n{inner}")
"""
Оставляет только строки где есть совпадение в обеих таблицах
"""

# Указать явно тип join
inner2 = pd.merge(employees, departments, on='dept_id', how='inner')
print(f"\nТо же самое (how='inner'):\n{inner2}")


print("\n" + "="*60)
print("3. Left Join:")
print("="*60)

# Добавить сотрудника без отдела
employees_extended = pd.concat([
    employees,
    pd.DataFrame({'emp_id': [6], 'name': ['Ольга'], 'dept_id': [99]})
], ignore_index=True)

print(f"\nСотрудники (с Ольгой):\n{employees_extended}")

# Left join (все из левой + совпадения из правой)
left = pd.merge(employees_extended, departments, on='dept_id', how='left')
print(f"\nLeft join:\n{left}")
"""
Все сотрудники + информация об отделе где есть
Ольга: dept_name = NaN (отдела 99 нет)
"""

print("\n" + "="*60)
print("4. Right Join:")
print("="*60)

# Добавить отдел без сотрудников
departments_extended = pd.concat([
    departments,
    pd.DataFrame({'dept_id': [40], 'dept_name': ['Finance'], 'location': ['Москва']})
], ignore_index=True)

print(f"\nОтделы (с Finance):\n{departments_extended}")

# Right join (все из правой + совпадения из левой)
right = pd.merge(employees, departments_extended, on='dept_id', how='right')
print(f"\nRight join:\n{right}")
"""
Все отделы + сотрудники где есть
Finance: name = NaN (нет сотрудников)
"""


print("\n" + "="*60)
print("5. Outer Join (Full):")
print("="*60)

# Outer join (всё из обеих таблиц)
outer = pd.merge(employees_extended, departments_extended, on='dept_id', how='outer')
print(f"\nOuter join:\n{outer}")
"""
Все сотрудники + все отделы
NaN где нет совпадения
"""


print("\n" + "="*60)
print("6. Merge с разными именами столбцов:")
print("="*60)

# Таблицы с разными именами ключей
orders = pd.DataFrame({
    'order_id': [101, 102, 103],
    'customer_id': [1, 2, 1],
    'amount': [1000, 1500, 2000]
})

customers = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Компания А', 'Компания Б', 'Компания В']
})

print(f"\nЗаказы:\n{orders}")
print(f"\nКлиенты:\n{customers}")

# Merge с указанием разных столбцов
merged = pd.merge(orders, customers, left_on='customer_id', right_on='id')
print(f"\nMerge (left_on, right_on):\n{merged}")

# Удалить дублирующийся столбец
merged_clean = merged.drop('id', axis=1)
print(f"\nБез дублирования:\n{merged_clean}")


print("\n" + "="*60)
print("7. Merge по индексу:")
print("="*60)

# Таблицы с индексом
df1 = pd.DataFrame({
    'A': [1, 2, 3]
}, index=['a', 'b', 'c'])

df2 = pd.DataFrame({
    'B': [10, 20, 30]
}, index=['a', 'b', 'd'])

print(f"\ndf1:\n{df1}")
print(f"\ndf2:\n{df2}")

# Merge по индексу
merged_idx = pd.merge(df1, df2, left_index=True, right_index=True, how='outer')
print(f"\nMerge по индексу:\n{merged_idx}")



print("\n" + "="*60)
print("8. Concat - вертикальное объединение:")
print("="*60)

# Данные за разные периоды
jan = pd.DataFrame({
    'month': ['Январь'] * 3,
    'sales': [1000, 1500, 2000]
})

feb = pd.DataFrame({
    'month': ['Февраль'] * 3,
    'sales': [1200, 1800, 2200]
})

print(f"\nЯнварь:\n{jan}")
print(f"\nФевраль:\n{feb}")

# Concat
combined = pd.concat([jan, feb])
print(f"\nОбъединённые данные:\n{combined}")

# Сбросить индекс
combined_reset = pd.concat([jan, feb], ignore_index=True)
print(f"\nС новым индексом:\n{combined_reset}")

# Concat с метками
combined_keys = pd.concat([jan, feb], keys=['Q1', 'Q1'])
print(f"\nС метками:\n{combined_keys}")




print("\n" + "="*60)
print("9. Concat - горизонтальное объединение:")
print("="*60)

# Разные показатели
sales = pd.DataFrame({
    'sales': [1000, 1500, 2000]
})

costs = pd.DataFrame({
    'costs': [800, 1200, 1600]
})

print(f"\nПродажи:\n{sales}")
print(f"\nРасходы:\n{costs}")

# Concat по столбцам
metrics = pd.concat([sales, costs], axis=1)
print(f"\nОбъединённые метрики:\n{metrics}")

# Добавить вычисляемый столбец
metrics['profit'] = metrics['sales'] - metrics['costs']
print(f"\nС прибылью:\n{metrics}")



print("\n" + "="*60)
print("10. Join (упрощённый merge):")
print("="*60)

# DataFrames с индексом
left_df = pd.DataFrame({
    'A': [1, 2, 3]
}, index=['a', 'b', 'c'])

right_df = pd.DataFrame({
    'B': [10, 20, 30]
}, index=['a', 'b', 'd'])

print(f"\nLeft:\n{left_df}")
print(f"\nRight:\n{right_df}")

# Join (по умолчанию left join по индексу)
joined = left_df.join(right_df)
print(f"\nJoin:\n{joined}")

# Другие типы join
joined_inner = left_df.join(right_df, how='inner')
print(f"\nInner join:\n{joined_inner}")



print("\n" + "="*60)
print("11. Практический пример - анализ продаж:")
print("="*60)

# Транзакции
transactions = pd.DataFrame({
    'trans_id': [1, 2, 3, 4, 5],
    'product_id': [101, 102, 101, 103, 102],
    'customer_id': [1, 2, 1, 3, 2],
    'quantity': [2, 1, 3, 1, 2],
    'date': pd.date_range('2025-01-01', periods=5)
})

# Продукты
products = pd.DataFrame({
    'product_id': [101, 102, 103],
    'product_name': ['Ноутбук', 'Мышь', 'Клавиатура'],
    'price': [50000, 1000, 3000]
})

# Клиенты
customers = pd.DataFrame({
    'customer_id': [1, 2, 3],
    'customer_name': ['ООО "Рога"', 'ИП Копыта', 'ООО "Хвосты"'],
    'city': ['Москва', 'СПб', 'Казань']
})

print(f"\nТранзакции:\n{transactions}")
print(f"\nПродукты:\n{products}")
print(f"\nКлиенты:\n{customers}")

# Объединить все данные
# 1. Добавить информацию о продуктах
sales = pd.merge(transactions, products, on='product_id')
print(f"\nС продуктами:\n{sales}")

# 2. Добавить информацию о клиентах
sales = pd.merge(sales, customers, on='customer_id')
print(f"\nПолные данные:\n{sales}")

# 3. Вычислить сумму
sales['total'] = sales['quantity'] * sales['price']
print(f"\nС суммами:\n{sales[['trans_id', 'product_name', 'customer_name', 'quantity', 'price', 'total']]}")

# Анализ
print(f"\n--- АНАЛИЗ ---")
print(f"Всего транзакций: {len(sales)}")
print(f"Общая сумма: {sales['total'].sum():,.0f} руб")
print(f"\nПо продуктам:")
print(sales.groupby('product_name')['total'].sum().sort_values(ascending=False))
print(f"\nПо городам:")
print(sales.groupby('city')['total'].sum().sort_values(ascending=False))
print(f"\nПо клиентам:")
print(sales.groupby('customer_name')['total'].sum().sort_values(ascending=False))

# ==========================================
# APPEND (УСТАРЕВШИЙ, НО ПОЛЕЗНО ЗНАТЬ)
# ==========================================

print("\n" + "="*60)
print("12. Альтернативы append (устарел в Pandas 2.0):")
print("="*60)

df1 = pd.DataFrame({'A': [1, 2]})
df2 = pd.DataFrame({'A': [3, 4]})

# Старый способ (deprecated)
# df_appended = df1.append(df2)

# Новый способ
df_concat = pd.concat([df1, df2], ignore_index=True)
print(f"\nИспользуйте concat вместо append:\n{df_concat}")

print("\n" + "="*60)
print("ИТОГИ:")
print("="*60)
print("""
Объединение данных:

Merge (SQL-стиль):
- pd.merge(df1, df2, on='key') - inner join
- how='left' - left join (все из левой)
- how='right' - right join (все из правой)
- how='outer' - outer join (все из обеих)
- left_on='A', right_on='B' - разные имена

Join (по индексу):
- df1.join(df2) - left join по индексу
- df1.join(df2, how='inner')

Concat (склейка):
- pd.concat([df1, df2]) - вертикально
- pd.concat([df1, df2], axis=1) - горизонтально
- ignore_index=True - новый индекс

Типы join:
- inner - пересечение (только совпадения)
- left - все из левой + совпадения справа
- right - все из правой + совпадения слева
- outer - всё из обеих (union)

Применение:
- Объединение связанных таблиц
- Добавление справочной информации
- Комбинирование данных из разных источников
""")