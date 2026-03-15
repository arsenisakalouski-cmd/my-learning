### День 32 (файл 01): Data Augmentation 

**Идея:** Создать больше данных из того что есть

**Как работает:**
- Поворот картинки (±15°)
- Сдвиг влево/вправо (±10%)
- Zoom (±10%)
- Отражение (для некоторых задач)

**Зачем:**
- Больше данных → лучше обучение
- Меньше переобучение
- Модель устойчивее

**Код:**
```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1
)

train_gen = datagen.flow(X_train, y_train, batch_size=32)

model.fit(train_gen, 
          steps_per_epoch=len(X_train)//32,
          epochs=10)
```

**Важно:**
- Только на train!
- Test не трогаем
- Разумные параметры



### День 32 (файл 02): Визуализация CNN ⭐⭐⭐

**Идея:** Увидеть что CNN видит внутри

**Что смотрим:**

1. **Фильтры (веса)** - что модель выучила
2. **Активации** - что фильтры нашли на картинке
3. **Все слои** - как картинка превращается в решение

**Код (фильтры):**
```python
# Получить веса слоя
layer = model.get_layer('conv1')
filters, biases = layer.get_weights()

# Визуализировать i-й фильтр
filter_i = filters[:, :, 0, i]
plt.imshow(filter_i, cmap='gray')
```

**Код (активации):**
```python
from tensorflow.keras.models import Model

# Создать модель для активаций
activation_model = Model(
    inputs=model.input,
    outputs=model.get_layer('conv1').output
)

# Получить активации
activations = activation_model.predict(image)
```

**Что видим:**
- 1-й слой: линии, углы (простое)
- 2-й слой: формы, части цифр (сложнее)
- Последние слои: целые объекты

**Зачем:**
- Отладка (почему ошибка)
- Проверка (учит ли правильно)
- Понимание (что внутри)

### День 32 (файл 03): CIFAR-10 - цветные изображения 

**Задача:** Классификация 10 типов объектов (самолёты, машины, животные)

**Датасет:**
- 60,000 цветных фото 32x32x3
- 10 классов
- Сложнее чем MNIST!

**Архитектура (более глубокая):**
```python
model = Sequential([
    # БЛОК 1
    Conv2D(32, (3,3), padding='same', activation='relu'),
    Conv2D(32, (3,3), activation='relu'),
    MaxPooling2D((2,2)),
    Dropout(0.25),
    
    # БЛОК 2
    Conv2D(64, (3,3), padding='same', activation='relu'),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D((2,2)),
    Dropout(0.25),
    
    # КЛАССИФИКАТОР
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(10, activation='softmax')
])
```

**Новые техники:**

1. **padding='same'** - сохраняет размер
   - Без: 32x32 → 30x30
   - С: 32x32 → 32x32

2. **ReduceLROnPlateau** - адаптивный learning rate
```python
   reduce_lr = ReduceLROnPlateau(
       monitor='val_loss',
       factor=0.5,
       patience=3
   )
```
   - Не улучшается 3 эпохи → LR уменьшается в 2 раза
   - Помогает точнее настроить модель

3. **Два Conv слоя подряд**
   - Больше паттернов
   - Глубже сеть
   - Лучше для сложных данных

**Результаты:**
- Accuracy: 70-75% (хорошо для CIFAR-10!)
- Confusion Matrix показывает частые ошибки
- Кошек путают с собаками (похожи!)

**Важно:**
- Цветные: (32, 32, 3) - 3 канала
- Нормализация: /255.0
- Больше эпох чем для MNIST (25 vs 5)
```
