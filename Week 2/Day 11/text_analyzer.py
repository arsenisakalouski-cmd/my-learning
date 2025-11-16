import re
import json 
from datetime import datetime

class TextAnalyzer:
    def __init__(self, text):
        self.text = text
        self.results = {}

    def find_emails(self):
        pattern = r'[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails =  re.findall(pattern, self.text)   
        self.results['emails'] = list(set(emails))
        return self.results['emails']
    
    def find_phones(self):
        """Найти все телефоны"""
        # Российские форматы
        pattern = r'(\+7|8)[\s\-\(]?\d{3}[\s\-\)]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
        phones = re.findall(pattern, self.text)
        self.results['phones'] = list(set(phones))
        return self.results['phones']
    
    def find_urls(self):
        """Найти все URL"""
        pattern = r'https?://[^\s]+'
        urls = re.findall(pattern, self.text)
        self.results['urls'] = list(set(urls))
        return self.results['urls']
    
    def find_dates(self):
        ""
        patterns = [
            r'\d{2}\.\d{2}\.\d{4}',  # 01.01.2025
            r'\d{4}-\d{2}-\d{2}',    # 2025-01-01
            r'\d{2}/\d{2}/\d{4}',    # 01/01/2025
        ]
        
        dates = []
        for pattern in patterns:
            dates.extend(re.findall(pattern, self.text))
        
        self.results['dates'] = list(set(dates))
        return self.results['dates']
    
    def count_words(self):
        """Подсчитать слова"""
        # \b\w+\b - слово (граница слова)
        words = re.findall(r'\b\w+\b', self.text.lower())
        self.results['word_count'] = len(words)
        return len(words)
    
    def get_statistics(self):
        """Получить статистику"""
        stats = {
            'chars': len(self.text),
            'lines': len(self.text.split('\n')),
            'words': self.count_words(),
            'emails': len(self.find_emails()),
            'phones': len(self.find_phones()),
            'urls': len(self.find_urls()),
            'dates': len(self.find_dates()),
        }
        return stats
    

    def clean_text(self): 
         # Заменить множественные пробелы на один
        cleaned = re.sub(r'\s+', ' ', self.text)
        
        # Убрать пробелы в начале/конце строк
        cleaned = cleaned.strip()
        
        return cleaned
    
    def generate_report(self):
        """Создать отчёт"""
        stats = self.get_statistics()
        
        report = "\n" + "="*60 + "\n"
        report += "АНАЛИЗ ТЕКСТА\n"
        report += "="*60 + "\n"
        
        report += f"\nСИМВОЛОВ: {stats['chars']}\n"
        report += f"СТРОК: {stats['lines']}\n"
        report += f"СЛОВ: {stats['words']}\n"
        
        if stats['emails'] > 0:
            report += f"\nEMAIL: {stats['emails']}\n"
            for email in self.results['emails']:
                report += f"  - {email}\n"
        
        if stats['phones'] > 0:
            report += f"\nТЕЛЕФОНЫ: {stats['phones']}\n"
            for phone in self.results['phones']:
                report += f"  - {phone}\n"
        
        if stats['urls'] > 0:
            report += f"\nURL: {stats['urls']}\n"
            for url in self.results['urls']:
                report += f"  - {url}\n"
        
        if stats['dates'] > 0:
            report += f"\nДАТЫ: {stats['dates']}\n"
            for date in self.results['dates']:
                report += f"  - {date}\n"
        
        report += "\n" + "="*60 + "\n"
        
        return report
    

def analyze_file(filename):
    """Анализировать файл"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        
        analyzer = TextAnalyzer(text)
        report = analyzer.generate_report()
        
        print(report)
        
        # Сохранить отчёт
        report_filename = filename.replace('.txt', '_report.txt')
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Отчёт сохранён: {report_filename}\n")
        
        return analyzer
    
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None
def analyze_text_input():
    """Анализировать введённый текст"""
    print("\n--- Ввод текста ---")
    print("Введите текст (Enter дважды для завершения):\n")
    
    lines = []
    while True:
        line = input()
        if line == "" and len(lines) > 0 and lines[-1] == "":
            break
        lines.append(line)
    
    # Убираем последнюю пустую строку
    if lines and lines[-1] == "":
        lines.pop()
    
    text = "\n".join(lines)
    
    if not text:
        print("Текст пустой")
        return None
    
    analyzer = TextAnalyzer(text)
    report = analyzer.generate_report()
    
    print(report)
    
    return analyzer

def validate_data():
    """Проверить корректность данных"""
    print("\n--- Валидатор ---")
    print("1. Email")
    print("2. Телефон")
    print("3. URL")
    
    choice = input("\nЧто проверить? (1-3): ").strip()
    
    if choice == "1":
        email = input("Email: ").strip()
        pattern = r'^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            print("OK - Корректный email")
        else:
            print("Плохой - Некорректный email")
    
    elif choice == "2":
        phone = input("Телефон: ").strip()
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        patterns = [
            r'^\+7\d{10}$',
            r'^8\d{10}$',
        ]
        
        valid = any(re.match(p, cleaned) for p in patterns)
        
        if valid:
            print("OK - Корректный телефон")
        else:
            print("Плохой - Некорректный телефон")
    
    elif choice == "3":
        url = input("URL: ").strip()
        pattern = r'^https?://[^\s]+$'
        
        if re.match(pattern, url):
            print("OK - Корректный URL")
        else:
            print("Плохой - Некорректный URL")

def find_replace():
    """Найти и заменить в тексте"""
    print("\n--- Поиск и замена ---")
    
    text = input("Введите текст: ")
    pattern = input("Что искать (regex): ")
    replacement = input("На что заменить: ")
    
    try:
        result = re.sub(pattern, replacement, text)
        print(f"\nРезультат:\n{result}")
    except re.error as e:
        print(f"Ошибка в паттерне: {e}")

def main():
    """Главная функция"""
    
    print("\n" + "="*60)
    print("АНАЛИЗАТОР ТЕКСТА")
    print("="*60)
    
    while True:
        print("\n--- МЕНЮ ---")
        print("1. Анализ файла")
        print("2. Анализ введённого текста")
        print("3. Валидатор данных")
        print("4. Поиск и замена")
        print("5. Выход")
        
        choice = input("\nВыбор (1-5): ").strip()
        
        if choice == "1":
            filename = input("\nИмя файла: ").strip()
            analyze_file(filename)
        
        elif choice == "2":
            analyze_text_input()
        
        elif choice == "3":
            validate_data()
        
        elif choice == "4":
            find_replace()
        
        elif choice == "5":
            print("\nДо встречи!")
            break
        
        else:
            print("Выберите 1-5")


if __name__ == "__main__":
    main()