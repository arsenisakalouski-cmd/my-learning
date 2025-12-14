import pandas as pd
import numpy as np

print("="*60)
print("ГРУППИРОВКА И АГРЕГАЦИЯ В Pandas")
print("="*60)

# ==========================================
# СОЗДАНИЕ ДАННЫХ
# ==========================================

print("\n1. Тестовые данные:")

np.random.seed(42)

data = {
    'Сотрудник': ['Иван', 'Мария', 'Пётр', 'Анна', 'Сергей', 'Ольга', 
                  'Дмитрий', 'Елена', 'Алексей', 'Наталья'] * 3,
    'Отдел': ['IT', 'HR', 'IT', 'Sales', 'IT', 'HR', 'Sales', 'IT', 'Sales', 'HR'] * 3,
    'Город': ['Москва', 'СПб', 'Москва', 'Казань', 'СПб', 'Москва', 
              'Казань', 'СПб', 'Москва', 'Казань'] * 3,
    'Месяц': ['Январь']*10 + ['Февраль']*10 + ['Март']*10,
    'Продажи': np.random.randint(10000, 50000, 30),
    'Расходы': np.random.randint(5000, 20000, 30)
}

df = pd.DataFrame(data)
print(f"\nDataFrame ({df.shape[0]} строк):\n{df.head(10)}")

print("\n" + "="*60)
print("2. Простая группировка:")
print("="*60)

# Группировать по одному столбцу
grouped = df.groupby('Отдел')
print(f"\nТип: {type(grouped)}")
"""
GroupBy объект - ещё не результат!
Нужно применить агрегирующую функцию
"""

# Посчитать среднее
mean_by_dept = df.groupby('Отдел')['Продажи'].mean()
print(f"\nСредние продажи по отделам:\n{mean_by_dept}")

# Несколько агрегаций
print(f"\nРазные агрегации:")
print(f"Сумма:\n{df.groupby('Отдел')['Продажи'].sum()}")
print(f"\nМинимум:\n{df.groupby('Отдел')['Продажи'].min()}")
print(f"\nМаксимум:\n{df.groupby('Отдел')['Продажи'].max()}")
print(f"\nКоличество:\n{df.groupby('Отдел')['Продажи'].count()}")

# Для всех числовых столбцов
all_stats = df.groupby('Отдел').mean(numeric_only=True)
print(f"\nСредние для всех числовых:\n{all_stats}")

print("\n" + "="*60)
print("3. Множественные агрегации (agg):")
print("="*60)

# Разные функции к одному столбцу
sales_agg = df.groupby('Отдел')['Продажи'].agg(['sum', 'mean', 'min', 'max', 'count'])
print(f"\nМножественные агрегации продаж:\n{sales_agg}")

# Разные функции к разным столбцам
multi_agg = df.groupby('Отдел').agg({
    'Продажи': ['sum', 'mean'],
    'Расходы': ['sum', 'mean']
})
print(f"\nРазные агрегации для разных столбцов:\n{multi_agg}")

named_agg = df.groupby('Отдел').agg(
    Всего_продаж=('Продажи', 'sum'),
    Средние_продажи=('Продажи', 'mean'),
    Всего_расходов=('Расходы', 'sum'),
    Средние_расходы=('Расходы', 'mean')
    )
print(f"\nС переименованием:\n{named_agg}")

# Кастомная функция
def range_values(x):
    """Размах (max - min)"""
    return x.max() - x.min()

custom_agg = df.groupby('Отдел')['Продажи'].agg(['mean', range_values])
print(f"\nС кастомной функцией:\n{custom_agg}")

print("\n" + "="*60)
print("4. Группировка по нескольким столбцам:")
print("="*60)

# По двум столбцам
multi_group = df.groupby(['Отдел', 'Город'])['Продажи'].mean()
print(f"\nПо отделу и городу:\n{multi_group}")
"""
Результат - Series с многоуровневым индексом:
Отдел  Город
HR     Казань    ...
       Москва    ...
       СПб       ...
IT     Москва    ...
"""
# Преобразовать в таблицу
multi_table = df.groupby(['Отдел', 'Город'])['Продажи'].mean().unstack()
print(f"\nВ виде таблицы (unstack):\n{multi_table}")
"""
unstack() - из многоуровневого индекса в столбцы

         Казань   Москва     СПб
Отдел
HR      ...      ...        ...
IT      ...      ...        ...
Sales   ...      ...        ...
"""

# С заполнением пропусков
multi_table_filled = multi_table.fillna(0)
print(f"\nС заполнением NaN:\n{multi_table_filled}")

print("\n" + "="*60)
print("5. Pivot Table (сводная таблица):")
print("="*60)

# Простая pivot table
pivot = pd.pivot_table(
    df,
    values='Продажи',
    index='Отдел',
    columns='Город',
    aggfunc='mean'
)
print(f"\nPivot table:\n{pivot}")

# С несколькими значениями
pivot_multi = pd.pivot_table(
    df,
    values=['Продажи', 'Расходы'],
    index='Отдел',
    columns='Город',
    aggfunc='mean'
)
print(f"\nС несколькими значениями:\n{pivot_multi}")

# С итогами (margins)
pivot_margins = pd.pivot_table(
    df,
    values='Продажи',
    index='Отдел',
    columns='Город',
    aggfunc='mean',
    margins=True,
    margins_name='Итого'
)
print(f"\nС итогами:\n{pivot_margins}")



print("\n" + "="*60)
print("6. Применение функций к группам (transform, apply):")
print("="*60)

# transform - возвращает тот же размер
df['Средние_продажи_отдела'] = df.groupby('Отдел')['Продажи'].transform('mean')
print(f"\nС добавленным столбцом (transform):\n{df[['Отдел', 'Продажи', 'Средние_продажи_отдела']].head(10)}")
"""
transform добавляет значение группы к каждой строке
Размер не меняется
"""

# Отклонение от среднего по отделу
df['Отклонение_от_среднего'] = df['Продажи'] - df['Средние_продажи_отдела']
print(f"\nОтклонение от среднего:\n{df[['Отдел', 'Продажи', 'Отклонение_от_среднего']].head(10)}")

# apply - кастомная логика
def top_2(group):
    """Вернуть топ-2 по продажам в группе"""
    return group.nlargest(2, 'Продажи')

top_sales = df.groupby('Отдел').apply(top_2, include_groups=False)
print(f"\nТоп-2 продаж в каждом отделе:\n{top_sales}")


print("\n" + "="*60)
print("7. Фильтрация групп:")
print("="*60)

# Оставить только группы где > 5 записей
filtered = df.groupby('Отдел').filter(lambda x: len(x) > 5)
print(f"\nГруппы с > 5 записей:\n{filtered.groupby('Отдел').size()}")

# Группы где средние продажи > 25000
high_sales = df.groupby('Отдел').filter(lambda x: x['Продажи'].mean() > 25000)
print(f"\nОтделы со средними продажами > 25000:\n{high_sales['Отдел'].unique()}")


print("\n" + "="*60)
print("8. Размер групп:")
print("="*60)

# Количество строк в каждой группе
group_sizes = df.groupby('Отдел').size()
print(f"\nРазмер групп:\n{group_sizes}")

# То же через count (для каждого столбца)
group_counts = df.groupby('Отдел').count()
print(f"\nCount для каждого столбца:\n{group_counts}")

# Количество уникальных значений
unique_cities = df.groupby('Отдел')['Город'].nunique()
print(f"\nУникальных городов в отделе:\n{unique_cities}")


print("\n" + "="*60)
print("9. Итерация по группам:")
print("="*60)

print("\nОбработка каждой группы:")
for dept, group in df.groupby('Отдел'):
    print(f"\nОтдел: {dept}")
    print(f"  Строк: {len(group)}")
    print(f"  Средние продажи: {group['Продажи'].mean():.0f}")
    print(f"  Всего продаж: {group['Продажи'].sum():.0f}")




print("\n" + "="*60)
print("10. Практический пример - ежемесячный отчёт:")
print("="*60)

monthly_report = df.groupby(['Месяц', 'Отдел']).agg(
    Всего_продаж=('Продажи', 'sum'),
    Средние_продажи=('Продажи', 'mean'),
    Всего_расходов=('Расходы', 'sum'),
    Количество_транзакций=('Продажи', 'count')
).round(0)

print(f"\nЕжемесячный отчёт:\n{monthly_report}")

# Прибыль
monthly_report['Прибыль'] = monthly_report['Всего_продаж'] - monthly_report['Всего_расходов']
print(f"\nС прибылью:\n{monthly_report}")

# Рентабельность
monthly_report['Рентабельность_%'] = (
    monthly_report['Прибыль'] / monthly_report['Всего_продаж'] * 100
).round(1)

print(f"\nПолный отчёт:\n{monthly_report}")

print("\n" + "="*60)
print("ИТОГИ:")
print("="*60)
print("""
Группировка и агрегация:

Простая группировка:
- df.groupby('column')['value'].mean()
- df.groupby('column')['value'].sum()

Множественные агрегации:
- df.groupby('col').agg(['sum', 'mean', 'max'])
- df.groupby('col').agg({'A': 'sum', 'B': 'mean'})

По нескольким столбцам:
- df.groupby(['col1', 'col2']).mean()
- .unstack() - в таблицу

Pivot Table:
- pd.pivot_table(df, values='A', index='B', columns='C')

Transform/Apply:
- .transform('mean') - сохраняет размер
- .apply(func) - кастомная логика
- .filter(lambda x: ...) - фильтрация групп

Размеры:
- .size() - количество строк
- .count() - не-NaN значений
- .nunique() - уникальных значений
""")
