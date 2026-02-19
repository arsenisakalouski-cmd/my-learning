### День 30 (файл 01): Dropout ⭐⭐⭐

**Идея:** Случайно выключать нейроны во время обучения

**Зачем:** Борьба с переобучением

**Аналогия:**
- Тренировка с завязанными глазами → потом лучше видишь
- Футболист тренируется в разном составе → становится универсальнее

**Как работает:**
```
Эпоха 1: [N1, ✗, N3, ✗, N5] (случайно выключили)
Эпоха 2: [✗, N2, ✗, N4, ✗] (другие выключили)
→ Каждый нейрон учится работать независимо
```

**Код:**
```python
from tensorflow.keras.layers import Dropout

model = Sequential([
    Dense(64, activation='relu'),
    Dropout(0.5),  # 50% нейронов выключить
    Dense(32, activation='relu'),
    Dropout(0.3),  # 30% нейронов выключить
    Dense(1, activation='sigmoid')
])
```

**Параметры:**
- `0.3-0.5` - стандартно (30-50%)
- Больше dropout в начале, меньше в конце
- НЕ ставим после последнего слоя

**Когда использовать:**
- Большая сеть
- Мало данных
- Видно переобучение (Train >> Test)

**Важно:** При предсказании dropout ОТКЛЮЧАЕТСЯ автоматически!


### День 30 (файл 02): Early Stopping ⭐⭐⭐

**Идея:** Остановить обучение когда перестало улучшаться

**Зачем:** 
- Экономить время
- Не переобучаться
- Автоматически находить лучший момент

**Как работает:**
```
Эпоха 50: val_loss = 0.25 ← лучший!
Эпоха 51: val_loss = 0.26 ← хуже
Эпоха 52: val_loss = 0.27 ← хуже
...
Эпоха 60: не улучшается 10 эпох → СТОП!
Возвращаемся к эпохе 50!
```

**Код:**
```python
from tensorflow.keras.callbacks import EarlyStopping

early_stop = EarlyStopping(
    monitor='val_loss',           # что смотреть
    patience=10,                  # сколько эпох ждать
    restore_best_weights=True,    # вернуть лучшие веса
    verbose=1                     # печатать
)

model.fit(X, y, callbacks=[early_stop])
```

**Параметры:**
- `monitor='val_loss'` - обычно это
- `patience=10` - стандартно (5-20)
- `restore_best_weights=True` - ВАЖНО! всегда True

**Бонус - ModelCheckpoint:**
```python
from tensorflow.keras.callbacks import ModelCheckpoint

checkpoint = ModelCheckpoint(
    'best_model.h5',
    monitor='val_loss',
    save_best_only=True
)

model.fit(X, y, callbacks=[early_stop, checkpoint])
```

**Результаты:**
- Без: 200 эпох, долго
- С Early Stop: ~60 эпох, быстро
- Экономия: 70% времени!



---

## День 30: Улучшение нейросетей - ИТОГИ ⭐⭐⭐

**Главные техники:**

### 1. Dropout
```python
from tensorflow.keras.layers import Dropout

model = Sequential([
    Dense(64, activation='relu'),
    Dropout(0.5),  # выключить 50%
    Dense(32, activation='relu'),
    Dropout(0.3),  # выключить 30%
    Dense(1, activation='sigmoid')
])
```

**Зачем:** Борьба с переобучением
**Как:** Случайно выключает нейроны
**Сколько:** 0.3-0.5 (30-50%)

### 2. Early Stopping
```python
from tensorflow.keras.callbacks import EarlyStopping

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

model.fit(X, y, callbacks=[early_stop])
```

**Зачем:** Экономия времени, предотвращение переобучения
**Как:** Останавливается если не улучшается
**Параметры:**
- `monitor='val_loss'` - что смотреть
- `patience=10` - сколько эпох ждать
- `restore_best_weights=True` - вернуть лучшие

### 3. Model Checkpoint
```python
from tensorflow.keras.callbacks import ModelCheckpoint

checkpoint = ModelCheckpoint(
    'best_model.h5',
    monitor='val_accuracy',
    save_best_only=True,
    mode='max'
)

model.fit(X, y, callbacks=[early_stop, checkpoint])
```

**Зачем:** Автоматическое сохранение лучшей модели
**mode='max'** - для accuracy
**mode='min'** - для loss

### Полный пример (медицинский датасет):
```python
# Подготовка
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y)

# Модель
model = Sequential([
    Dense(64, activation='relu', input_shape=(30,)),
    Dropout(0.5),
    Dense(32, activation='relu'),
    Dropout(0.4),
    Dense(16, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Callbacks
early_stop = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)
checkpoint = ModelCheckpoint('best.h5', monitor='val_accuracy', save_best_only=True)

# Обучение
history = model.fit(
    X_train, y_train,
    epochs=200,
    callbacks=[early_stop, checkpoint],
    validation_split=0.2
)

# Результат: остановилось на эпохе ~60, accuracy 97%
```

### Результаты финального проекта:
- Датасет: Breast Cancer (569 пациентов)
- Accuracy: 97%+
- Sensitivity: 98% (находит рак)
- Specificity: 96% (не пугает здоровых)
- Экономия времени: 70% (early stopping)

### Когда что использовать:

**Dropout:**
- Большая сеть
- Мало данных
- Есть переобучение

**Early Stopping:**
- ВСЕГДА! (экономит время)
- patience=10-20 обычно

**Model Checkpoint:**
- Долгое обучение
- Важно не потерять лучший результат

### Неделя 5 - пройдено:
- День 26: Hyperparameter Tuning ✓
- День 27: Реальные данные ✓
- День 28: Feature Engineering ✓
- День 29: Нейронные сети ✓
- День 30: Улучшение нейросетей ✓
```

---

