### День 27 (файл 02): Обработка пропусков ⭐⭐⭐

**Главная идея:** Модели не работают с NaN - нужно обработать!

**3 способа:**

1. **dropna()** - удалить строки
   - Когда: < 5% пропусков
   
2. **fillna(mean/median)** - заполнить
   - mean - среднее (простое)
   - median - медиана (лучше при выбросах)
   - Когда: 5-30% пропусков

3. **SimpleImputer** - для ML
   - Запоминает значения
   - Применяем к test

**Код-шаблон:**
```python
# Удаление
df_clean = df.dropna()

# Заполнение
df['col'] = df['col'].fillna(df['col'].median())

# Для ML
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='median')
X_filled = imputer.fit_transform(X_train)  # train
X_test_filled = imputer.transform(X_test)  # test
```

**Важно:** 
- На train: fit_transform()
- На test: transform()