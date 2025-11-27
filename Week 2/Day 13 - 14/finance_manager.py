import json
from datetime import datetime
from transaction import Transaction

class FinanceManager:
    def __init__(self, filename="transactions.json"):
        self.transactions = []  # Список всех Transaction объектов
        self.filename = filename
        self.load_from_file()  # Загружаем если файл существует

    def add_transaction(self, amount, category, description="", transaction_type="expense"):    
        transaction = Transaction(amount, category, description, transaction_type)
        self.transactions.append(transaction)
        
        # Сохраняем изменения в файл
        self.save_to_file()
        
        return transaction
    
    def remove_transaction(self, transaction_id): 
        # Проходим по всем транзакциям
        for transaction in self.transactions:
            # Проверяем ID
            if transaction.id == transaction_id:
                self.transactions.remove(transaction)
                self.save_to_file()
                return True
        return False
    
    def  get_all_transactions(self):
         return self.transactions
    
    def get_transactions_by_type(self, transaction_type):

        # List comprehension - короткий способ фильтрации
        # Читается: "дай мне t для каждого t в self.transactions, 
        # где t.transaction_type равен transaction_type"
        return [t for t in self.transactions if t.transaction_type == transaction_type]
    
    def get_transactions_by_category(self, category):
        return [t for t in self.transactions if t.category == category]
    
    def get_balance(self):
        # Считаем доходы
        # sum() складывает числа
        # [t.amount for t in ... if ...] создаёт список сумм
        # sum([100, 200, 300]) = 600
        income = sum([t.amount for t in self.transactions if t.transaction_type == "income"])

        # Считаем расходы
        expenses = sum([t.amount for t in self.transactions if t.transaction_type == "expense"])
        
        # Возвращаем разницу
        return income - expenses
    
    def get_total_income(self):
        """Общая сумма доходов"""
        return sum([t.amount for t in self.transactions if t.transaction_type == "income"])
    
    def get_total_expenses(self):
        """Общая сумма расходов"""
        return sum([t.amount for t in self.transactions if t.transaction_type == "expense"])
    
    def get_statistics(self):
        categories = {}

        for t in self.transactions:                        # Проходим по всем транзакциям
            category = t.category

            if category in categories:                     # Если категория уже есть в словаре
                categories[category] += t.amount           # Добавляем сумму к существующей
            else:
                categories[category] = t.amount            # Добавляем сумму к существующей  

        # Формируем итоговый словарь
        return {
            "total_transactions": len(self.transactions),
            "total_income": self.get_total_income(),
            "total_expenses": self.get_total_expenses(),
            "balance": self.get_balance(),
            "categories": categories
        }        
    
    def save_to_file(self):
        try:
            # Превращаем каждую транзакцию в словарь
            # [t.to_dict() for t in self.transactions]
            # Это list comprehension
            data = [t.to_dict() for t in self.transactions]
            
            # Открываем файл на запись
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)


        except Exception as e:        
            print(f"Ошибка сохранения: {e}")


    def load_from_file(self):

        try:
             with open(self.filename, "r", encoding="utf-8") as f:
                 # json.load() читает JSON из файла
                # Возвращает то что было сохранено (список словарей)
                data = json.load(f)
                
                self.transactions = [Transaction.from_dict(t) for t in data]
                print(f"Загружено {len(self.transactions)} транзакций")

        except FileNotFoundError:
            # Файла нет - это нормально при первом запуске
            print("Файл не найден, создаём новый")
            self.transactions = []
        
        except json.JSONDecodeError:
            # Файл есть но повреждён
            print("Файл повреждён, создаём новый")
            self.transactions = []
        
        except Exception as e:
            # Любая другая ошибка
            print(f"Ошибка загрузки: {e}")
            self.transactions = []


    def export_to_csv(self, filename="export.csv"):    
        """
        
        ЧТО ТАКОЕ CSV:
        CSV = Comma Separated Values (значения разделённые запятыми)
        Формат: каждая строка = одна запись, столбцы разделены запятыми
        
        """

        try:
            with open(filename, "w", encoding="utf-8") as f:
                # Записываем заголовок (первая строка)
                f.write("ID,Дата,Тип,Сумма,Категория,Описание\n")
                
                # Записываем каждую транзакцию
                for t in self.transactions:
                    # Форматируем строку
                    # {t.id},{t.date},...
                    # f.write() записывает строку в файл
                    line = f"{t.id},{t.date},{t.transaction_type},{t.amount},{t.category},{t.description}\n"
                    f.write(line)
            
            print(f"Экспортировано в {filename}")
            return True
        
        except Exception as e:
            print(f"Ошибка экспорта: {e}")
            return False
        




if __name__ == "__main__":
    print("=== Примеры FinanceManager ===\n")

    print("--- Создание менеджера ---")
    # При создании автоматически загружаются данные из файла (если есть)
    manager = FinanceManager("test_finances.json")
    print()

    print("--- Добавление транзакций ---")
    manager.add_transaction(50000, "Зарплата", "Зарплата за ноябрь", "income")
    manager.add_transaction(500, "Еда", "Продукты", "expense")
    manager.add_transaction(1000, "Транспорт", "Проездной", "expense")
    manager.add_transaction(2000, "Развлечения", "Кино", "expense")
    print("Добавлено 4 транзакции")
    print()

    # ПРИМЕР 3: Просмотр всех транзакций
    print("--- Все транзакции ---")
    for t in manager.get_all_transactions():
        print(t)  # Вызывает t.__str__()
    print()
    
    # ПРИМЕР 4: Фильтрация по типу
    print("--- Только расходы ---")
    expenses = manager.get_transactions_by_type("expense")
    for t in expenses:
        print(t)
    print()

    # ПРИМЕР 5: Статистика
    print("--- Статистика ---")
    stats = manager.get_statistics()
    print(f"Всего транзакций: {stats['total_transactions']}")
    print(f"Доходы: {stats['total_income']} руб")
    print(f"Расходы: {stats['total_expenses']} руб")
    print(f"Баланс: {stats['balance']} руб")
    print("\nПо категориям:")
    for category, amount in stats['categories'].items():
        print(f"  {category}: {amount} руб")
    print()

    # ПРИМЕР 6: Экспорт в CSV
    print("--- Экспорт в CSV ---")
    manager.export_to_csv("test_export.csv")
    print()
    
    # ПРИМЕР 7: Удаление транзакции
    print("--- Удаление транзакции ---")
    if manager.transactions:
        first_id = manager.transactions[0].id
        print(f"Удаляем транзакцию ID: {first_id}")
        result = manager.remove_transaction(first_id)
        print(f"Результат: {'Успешно' if result else 'Не найдено'}")





















    

    








    








          
