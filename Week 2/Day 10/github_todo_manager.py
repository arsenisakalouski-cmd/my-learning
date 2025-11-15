import requests
import json
from datetime import datetime

GITHUB_API = "https://api.github.com"
TASKS_FILE = "tasks.json"

class Task:
    def __init__(self, title, description ="", task_id = None):
        self.id = task_id or self.generate_id()
        self.title = title
        self.description = description
        self.status = "todo"
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_id(self):
        """Генерация уникального ID"""
        return int(datetime.now().timestamp() * 1000)
    
def to_dict(self):
        """Преобразовать в словарь"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at
        }        

@staticmethod

#@staticmethod = метод, который:
#не получает self
#не связан с конкретным объектом
#просто помогает классу выполнять какую-то задачу
#В твоём случае: создание задачи из словаря.

def from_dict(data):
        """Создать задачу из словаря"""
        task = Task(data["title"], data["description"], data["id"])
        task.status = data["status"]
        task.created_at = data["created_at"]
        return task

def __str__(self):
        status_emoji = {
            "todo": "⏳",
            "in_progress": "🔄",
            "done": "✅"
        }
        emoji = status_emoji.get(self.status, "❓")
        return f"{emoji} [{self.id}] {self.title}"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        """Загрузить задачи из файла"""
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.tasks = [Task.from_dict(task_data) for task_data in data]
            print(f" Загружено {len(self.tasks)} задач")
        
        except FileNotFoundError:
            print("ℹ Файл задач не найден, создаём новый")
            self.tasks = []
        
        except json.JSONDecodeError:
            print(" Файл задач повреждён, создаём новый")
            self.tasks = []

    def save_tasks(self):
        """Сохранить задачи в файл"""
        try:
            data = [task.to_dict() for task in self.tasks]
            with open(TASKS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(" Задачи сохранены")
        except Exception as e:
            print(f" Ошибка сохранения: {e}")       

    def add_task(self, title, description=""):
        """Добавить новую задачу"""
        task = Task(title, description)
        self.tasks.append(task)
        self.save_tasks()
        print(f" Задача добавлена: {task}")
        return task      
    
    def list_tasks(self, status=None):
        """Показать список задач"""
        # Фильтруем по статусу если нужно
        filtered = self.tasks if not status else [t for t in self.tasks if t.status == status]
        
        if not filtered:
            print("\n📋 Нет задач")
            return
        
        print("\n" + "="*70)
        print(f"📋 ЗАДАЧИ ({len(filtered)})")
        print("="*70)
        
        for task in filtered:
            print(f"\n{task}")
            if task.description:
                print(f"   {task.description}")
            print(f"   Создано: {task.created_at}")
        
        print("\n" + "="*70 + "\n")
    
    def update_status(self, task_id, new_status):
        """Изменить статус задачи"""
        for task in self.tasks:
            if task.id == task_id:
                task.status = new_status
                self.save_tasks()
                print(f"✅ Статус обновлён: {task}")
                return True
        
        print(f" Задача {task_id} не найдена")
        return False
    
    def delete_task(self, task_id):
        """Удалить задачу"""
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                print(f" Задача удалена: {task.title}")
                return True
        
        print(f" Задача {task_id} не найдена")
        return False
    

def get_statistics(self):
        """Получить статистику"""
        total = len(self.tasks)
        todo = len([t for t in self.tasks if t.status == "todo"])
        in_progress = len([t for t in self.tasks if t.status == "in_progress"])
        done = len([t for t in self.tasks if t.status == "done"])
        
        print("\n" + "="*50)
        print(" СТАТИСТИКА")
        print("="*50)
        print(f"Всего задач: {total}")
        print(f" К выполнению: {todo}")
        print(f" В работе: {in_progress}")
        print(f" Выполнено: {done}")
        
        if total > 0:
            completion = (done / total) * 100
            print(f"\n Прогресс: {completion:.1f}%")
        
        print("="*50 + "\n")  

        
class GitHubIntegration:
    """
    Интеграция с GitHub Issues
    
    ФУНКЦИИ:
    - Получить issues из репозитория
    - Импортировать как задачи
    """
    
    @staticmethod
    def get_repo_issues(owner, repo):
        """
        Получить issues из репозитория
        
        ПРИМЕР:
        get_repo_issues("python", "cpython")
        """
        url = f"{GITHUB_API}/repos/{owner}/{repo}/issues"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                issues = response.json()
                print(f" Получено {len(issues)} issues")
                return issues
            
            elif response.status_code == 404:
                print(f" Репозиторий {owner}/{repo} не найден")
                return None
            
            else:
                print(f" Ошибка {response.status_code}")
                return None
        
        except requests.Timeout:
            print(" Превышено время ожидания")
            return None
        
        except requests.RequestException as e:
            print(f" Ошибка: {e}")
            return None
        

    @staticmethod
    def import_issues(manager, issues):
        """
        Импортировать GitHub issues как задачи
        
        КАК ЭТО РАБОТАЕТ:
        1. Берём issues из GitHub
        2. Преобразуем в Task объекты
        3. Добавляем в менеджер
        """
        if not issues:
            return
        
        count = 0
        for issue in issues[:5]:  # Импортируем первые 5
            title = issue['title']
            description = f"GitHub Issue #{issue['number']}"
            
            manager.add_task(title, description)
            count += 1
        
        print(f" Импортировано {count} задач из GitHub")

def main():
    """Главная функция приложения"""
    manager = TaskManager()
    
    print("\n" + "📝"*35)
    print("       TODO МЕНЕДЖЕР С GITHUB ИНТЕГРАЦИЕЙ")
    print("📝"*35 + "\n")
    
    while True:
        print("="*70)
        print("МЕНЮ")
        print("="*70)
        print("1. ➕ Добавить задачу")
        print("2. 📋 Показать все задачи")
        print("3. 🔄 Изменить статус задачи")
        print("4. ❌ Удалить задачу")
        print("5. 📊 Статистика")
        print("6. 🌐 Импортировать из GitHub")
        print("7. 🚪 Выход")
        print("="*70)
        
        try:
            choice = input("\nВыбор (1-7): ").strip()
            
            if choice == "1":
                # Добавить задачу
                title = input("\n📝 Название задачи: ").strip()
                if title:
                    description = input("📄 Описание (необязательно): ").strip()
                    manager.add_task(title, description)
                else:
                    print("❌ Название не может быть пустым")
                print()
            
            elif choice == "2":
                # Показать задачи
                print("\nФильтр:")
                print("1. Все")
                print("2. К выполнению")
                print("3. В работе")
                print("4. Выполнено")
                
                filter_choice = input("Выбор (1-4): ").strip()
                
                status_map = {
                    "1": None,
                    "2": "todo",
                    "3": "in_progress",
                    "4": "done"
                }
                
                status = status_map.get(filter_choice)
                manager.list_tasks(status)
            
            elif choice == "3":
                # Изменить статус
                try:
                    task_id = int(input("\n🔢 ID задачи: "))
                    print("\nНовый статус:")
                    print("1. ⏳ К выполнению")
                    print("2. 🔄 В работе")
                    print("3. ✅ Выполнено")
                    
                    status_choice = input("Выбор (1-3): ").strip()
                    status_map = {
                        "1": "todo",
                        "2": "in_progress",
                        "3": "done"
                    }
                    
                    new_status = status_map.get(status_choice)
                    if new_status:
                        manager.update_status(task_id, new_status)
                    else:
                        print(" Неверный выбор")
                
                except ValueError:
                    print(" Введите число")
                print()
            
            elif choice == "4":
                # Удалить задачу
                try:
                    task_id = int(input("\n🔢 ID задачи для удаления: "))
                    confirm = input(f"⚠️ Удалить задачу {task_id}? (да/нет): ").lower()
                    if confirm == "да":
                        manager.delete_task(task_id)
                except ValueError:
                    print(" Введите число")
                print()
            
            elif choice == "5":
                # Статистика
                manager.get_statistics()
            
            elif choice == "6":
                # Импорт из GitHub
                print("\n Импорт из GitHub")
                owner = input("Owner (например python): ").strip()
                repo = input("Repo (например cpython): ").strip()
                
                if owner and repo:
                    issues = GitHubIntegration.get_repo_issues(owner, repo)
                    if issues:
                        GitHubIntegration.import_issues(manager, issues)
                print()
            
            elif choice == "7":
                # Выход
                print("\n👋 До встречи!")
                break
            
            else:
                print("\n❌ Выберите от 1 до 7\n")
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Программа прервана")
            print(" До встречи!")
            break
        
        except Exception as e:
            print(f"\n Ошибка: {e}\n")




if __name__ == "__main__":
    main()

