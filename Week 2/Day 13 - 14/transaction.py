from datetime import datetime

class Transaction:
     def __init__(self, amount, category, description="", transaction_type="expense"):
          
        if not isinstance(amount, (int, float)):
               raise ValueError(f"Сумма должна быть числом, получено {type(amount)}")
        if amount <= 0:
            raise ValueError("Сумма должна быть больше нуля")
        
        # Проверяем тип транзакции
        # Разрешены только "income" или "expense"
        if transaction_type not in ["income", "expense"]:
            raise ValueError("Тип должен быть 'income' или 'expense'")
        
        self.amount = amount
        self.category = category
        self.description = description
        self.transaction_type = transaction_type

        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.id = int(datetime.now().timestamp() * 1000) # Уникальный ID

     def to_dict(self):    
         return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "transaction_type": self.transaction_type,
            "date": self.date
        }
     

     @staticmethod
     def from_dict(data):
        # Создаём транзакцию
        # data["amount"] берёт значение по ключу "amount" из словаря
        transaction = Transaction(
            amount=data["amount"],
            category=data["category"],
            description=data.get("description", ""),  # .get с дефолтом на случай если ключа нет
            transaction_type=data["transaction_type"]
        )

        # Восстанавливаем сохранённые дату и ID
        # Перезаписываем те что __init__ создал автоматически
        transaction.date = data["date"]
        transaction.id = data["id"]
        
        return transaction
     
     def __str__(self):
        symbol = "+" if self.transaction_type == "income" else "-"

        return f"{symbol}{self.amount} руб | {self.category} | {self.description}"
     
     def __repr__(self): 
         return f"Transaction(id={self.id}, amount={self.amount}, type={self.transaction_type})"
     

         
    


if __name__ == "__main__":
    print("=== Примеры Transaction ===\n")

    print("--- Пример 1: Расход ---")
    # Когда пишем Transaction(...), вызывается __init__
    expense = Transaction(
        amount=150,
        category="Еда",
        description="Купил хлеб",
        transaction_type="expense"
    )

    print(expense)  # Вызывает __str__
    print(f"ID: {expense.id}")
    print(f"Дата: {expense.date}")
    print()

    print("--- Пример 2: Доход ---")
    income = Transaction(
        amount=50000,
        category="Зарплата",
        description="Зарплата за ноябрь",
        transaction_type="income"
    )
    print(income)
    print()
    
    # ПРИМЕР 3: Превращение в словарь
    print("--- Пример 3: to_dict ---")
    data = expense.to_dict()
    print("Словарь:", data)
    print()    




    print("--- Пример 4: from_dict ---")
    # Представим что этот словарь мы загрузили из JSON
    saved_data = {
        "id": 1234567890,
        "amount": 200,
        "category": "Транспорт",
        "description": "Метро",
        "transaction_type": "expense",
        "date": "2025-11-15 10:00:00"
    }
    
    # Transaction.from_dict - вызываем через класс, не через объект
    restored = Transaction.from_dict(saved_data)
    print("Восстановлено:", restored)
    print()
    
    # ПРИМЕР 5: Ошибки валидации
    print("--- Пример 5: Валидация ---")
    try:
        # Попытка создать с отрицательной суммой
        bad_transaction = Transaction(-100, "Еда")
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    try:
        # Попытка создать с неверным типом
        bad_transaction = Transaction(100, "Еда", transaction_type="wrong")
    except ValueError as e:
        print(f"Ошибка: {e}") 


          


          
        
        

        
          
