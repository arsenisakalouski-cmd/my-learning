from finance_manager import FinanceManager
from transaction import Transaction
import re


class FinanceApp:
    def __init__(self):
        self.manager = FinanceManager("transactions.json") # При создании он автоматически загрузит transactions.json
        # Списки категорий для расходов и доходов
        self.expense_categories = [
            "Еда",
            "Транспорт", 
            "Развлечения",
            "Здоровье",
            "Образование",
            "Коммунальные услуги",
            "Одежда",
            "Другое"
        ]
        
        self.income_categories = [
            "Зарплата",
            "Фриланс",
            "Инвестиции",
            "Подарки",
            "Другое"
        ]


    def validate_amount(self, amount_str):

        pattern = r'^\d+(\.\d+)?$'
        # re.match проверяет: соответствует ли строка паттерну?
        # Возвращает Match объект если да, None если нет
        if not re.match(pattern, amount_str):
            return False, "Сумма должна быть числом (например: 100 или 100.50)"
        
        try:
            amount = float(amount_str)

            if amount <= 0:
                return False , "Сумма должна быть больше нуля"
            return True, amount
        

        except ValueError:
            return False, "Некорректная сумма"
        
    def select_category(self, transaction_type):

        categories = self.expense_categories if transaction_type == "expense" else self.income_categories
        print("\nВыберите категорию:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        print("0. Ввести свою категорию")

        try:

            choice = input("\nВыбор: ").strip()

              # Проверяем что ввели число
            if not choice.isdigit():
            
                print("Введите номер категории")
                return None
            
            # Превращаем в число
            choice = int(choice)

            if choice == 0:
                # Ввести свою категорию
                custom = input("Введите название категории: ").strip()
                return custom if custom else None
            
            elif 1 <= choice <= len(categories):
                # categories[choice - 1] потому что:
                # Пользователь вводит 1, 2, 3...
                # Индексы в Python: 0, 1, 2...
                # Поэтому вычитаем 1
                return categories[choice - 1]
            
            else:
                print(f"Выберите от 0 до {len(categories)}")
                return None
        
        except KeyboardInterrupt:
            # Если нажали Ctrl+C
            print("\nОтмена")
            return None
        
        
    def add_transaction_interactive(self):
        """
        Добавить транзакцию (интерактивно)
        
        КАК РАБОТАЕТ:
        1. Спрашиваем тип (доход/расход)
        2. Спрашиваем сумму (с валидацией)
        3. Выбираем категорию
        4. Вводим описание
        5. Создаём транзакцию
        """
        print("\n" + "="*60)
        print("ДОБАВИТЬ ТРАНЗАКЦИЮ")
        print("="*60)

        # ШАГ 1: Выбрать тип
        print("\nТип транзакции:")
        print("1. Расход")
        print("2. Доход")
        
        type_choice = input("Выбор (1-2): ").strip()
        
        # Определяем тип
        if type_choice == "1":
            transaction_type = "expense"
            type_name = "расход"
        elif type_choice == "2":
            transaction_type = "income"
            type_name = "доход"
        else:
            print("Некорректный выбор")
            return
        
        # ШАГ 2: Ввести сумму
        amount_str = input(f"\nСумма {type_name}а: ").strip()
        
        # Валидация суммы
        # validate_amount возвращает кортеж (bool, значение)
        # is_valid, amount = кортеж
        # Это называется "распаковка кортежа"
        is_valid, amount = self.validate_amount(amount_str)

        is_valid, amount = self.validate_amount(amount_str)
        
        if not is_valid:
            # amount содержит сообщение об ошибке
            print(f"Ошибка: {amount}")
            return
        
        # ШАГ 3: Выбрать категорию
        category = self.select_category(transaction_type)
        
        if not category:
            print("Отмена")
            return
        

        # ШАГ 4: Ввести описание
        description = input("\nОписание (необязательно): ").strip()

        try:
            # Вызываем метод менеджера
            transaction = self.manager.add_transaction(
                amount=amount,
                category=category,
                description=description,
                transaction_type=transaction_type
            )
            
            print("\n✓ Транзакция добавлена:")
            print(transaction)
        
        except Exception as e:
            # Если что-то пошло не так
            print(f"\nОшибка: {e}")

    def view_transactions(self):
       
        print("\n" + "="*60)
        print("ТРАНЗАКЦИИ")
        print("="*60)
        
        print("\n1. Все транзакции")
        print("2. Только доходы")
        print("3. Только расходы")


        choice = input("\nВыбор (1-3): ").strip()
        
        # Получаем нужные транзакции
        if choice == "1":
            transactions = self.manager.get_all_transactions()
            title = "ВСЕ ТРАНЗАКЦИИ"
        elif choice == "2":
            transactions = self.manager.get_transactions_by_type("income")
            title = "ДОХОДЫ"
        elif choice == "3":
            transactions = self.manager.get_transactions_by_type("expense")
            title = "РАСХОДЫ"
        else:
            print("Некорректный выбор")
            return
        
        # Показываем
        print("\n" + "="*60)
        print(title)
        print("="*60)
        
        if not transactions:
            print("\nНет транзакций")
            return 
        
        # Проходим по транзакциям с номерами
        for i, t in enumerate(transactions, 1):
            # t.__str__() вызывается автоматически при print(t)
            print(f"\n{i}. {t}")
            print(f"   Дата: {t.date}")
            print(f"   ID: {t.id}")
        
        print("\n" + "="*60)




    def show_statistics(self):
        """
        Показать статистику
        
        ВЫВОДИТ:
        - Общее количество транзакций
        - Доходы
        - Расходы
        - Баланс
        - Разбивку по категориям
        """
        print("\n" + "="*60)
        print("СТАТИСТИКА")
        print("="*60)

        # Получаем статистику из менеджера
        # stats это словарь
        stats = self.manager.get_statistics()
        
        # Выводим основную информацию
        print(f"\nВсего транзакций: {stats['total_transactions']}")
        print(f"Доходы: {stats['total_income']:.2f} руб")
        print(f"Расходы: {stats['total_expenses']:.2f} руб")

        # Баланс (может быть отрицательным)
        balance = stats['balance']
        # Выбираем символ в зависимости от знака
        balance_sign = "+" if balance >= 0 else ""
        print(f"Баланс: {balance_sign}{balance:.2f} руб")

         # Показываем категории если есть
        if stats['categories']:
            print("\n" + "-"*60)
            print("ПО КАТЕГОРИЯМ:")
            print("-"*60)

             # .items() возвращает пары (ключ, значение) из словаря
            # {"Еда": 1000, "Транспорт": 500}.items() -> [("Еда", 1000), ("Транспорт", 500)]
            for category, amount in stats['categories'].items():
                print(f"{category:20} {amount:>10.2f} руб")
                # {category:20} - выровнять по левому краю, ширина 20
                # {amount:>10.2f} - выровнять по правому краю, ширина 10, 2 знака после точки
            print("\n" + "="*60)


        
    def delete_transaction(self):
        """
        Удалить транзакцию
        
        КАК РАБОТАЕТ:
        1. Показываем список с ID
        2. Спрашиваем какой ID удалить
        3. Подтверждение
        4. Удаляем
        """
        print("\n" + "="*60)
        print("УДАЛИТЬ ТРАНЗАКЦИЮ")
        print("="*60)
        
        transactions = self.manager.get_all_transactions()
        
        if not transactions:
            print("\nНет транзакций")
            return
        
        # Показываем список
        print("\nТранзакции:")
        for i, t in enumerate(transactions, 1):
            print(f"{i}. {t} (ID: {t.id})")

        try:
            # Спрашиваем ID
            id_str = input("\nВведите ID для удаления: ").strip()
            
            # Проверяем что это число
            if not id_str.isdigit():
                print("ID должен быть числом")
                return
            
            transaction_id = int(id_str)
            
            # Подтверждение
            confirm = input(f"Удалить транзакцию ID {transaction_id}? (да/нет): ").strip().lower()
            
            if confirm != "да":
                print("Отмена")
                return
            
            # Удаляем
            result = self.manager.remove_transaction(transaction_id)
            
            if result:
                print("\n✓ Транзакция удалена")
            else:
                print(f"\nТранзакция с ID {transaction_id} не найдена")
        
        except KeyboardInterrupt:
            print("\n\nОтмена")



    def export_to_csv(self):
        """Экспорт в CSV"""
        print("\n" + "="*60)
        print("ЭКСПОРТ В CSV")
        print("="*60)
        
        filename = input("\nИмя файла (Enter = export.csv): ").strip()
        
        if not filename:
            filename = "export.csv"
        
        # Добавляем расширение если забыли
        if not filename.endswith(".csv"):
            filename += ".csv"
        
        result = self.manager.export_to_csv(filename)
        
        if result:
            print(f"\n✓ Экспортировано в {filename}")
            print("Откройте файл в Excel для просмотра")






    def run(self):
        """
        Запустить приложение
        
        ГЛАВНЫЙ ЦИКЛ:
        Показывает меню → получает выбор → выполняет действие → повторяет
        """
        print("\n" + "="*60)
        print("ЛИЧНЫЙ ФИНАНСОВЫЙ ТРЕКЕР")
        print("="*60)
        
        # Бесконечный цикл
        # Выход через break
        while True:
            print("\n" + "="*60)
            print("МЕНЮ")
            print("="*60)
            print("1. Добавить транзакцию")
            print("2. Просмотр транзакций")
            print("3. Статистика")
            print("4. Удалить транзакцию")
            print("5. Экспорт в CSV")
            print("6. Выход")
            print("="*60)
            
            try:
                choice = input("\nВыбор (1-6): ").strip()
                
                if choice == "1":
                    self.add_transaction_interactive()
                
                elif choice == "2":
                    self.view_transactions()
                
                elif choice == "3":
                    self.show_statistics()
                
                elif choice == "4":
                    self.delete_transaction()
                
                elif choice == "5":
                    self.export_to_csv()
                
                elif choice == "6":
                    print("\nДо встречи!")
                    break  # Выход из цикла = завершение программы
                
                else:
                    print("\nВыберите от 1 до 6")
            
            except KeyboardInterrupt:
                # Если нажали Ctrl+C
                print("\n\nПрограмма прервана")
                print("До встречи!")
                break
            
            except Exception as e:
                # Любая другая ошибка
                print(f"\nОшибка: {e}")
                print("Попробуйте снова")


# ==========================================
# ЗАПУСК ПРОГРАММЫ
# ==========================================

if __name__ == "__main__":
    # Создаём приложение
    app = FinanceApp()
    
    # Запускаем главный цикл
    app.run()        

















        






        



        





            

            


            









        






