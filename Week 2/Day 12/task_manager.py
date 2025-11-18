class Task:
    def __init__(self, title , completed = False):
        self.title = title
        self.completed  = completed

    def mark_completed(self):
        self.completed = True

    def mark_incomolete(self):
        self.completed = False

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title):
        task = Task(title)
        self.tasks.append(task)
        return task

    def remowe_task(self, title):
        for task in self.tasks:
            if task.title == title:
                self.tasks.remove(task)
                return True
        return False

    def get_task(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None
    
    def get_all_tasks(self):
        return self.tasks

    
    def get_completed_tasks(self):
        """Получить только выполненные"""
        return [task for task in self.tasks if task.completed]
    
    def get_incomplete_tasks(self):
        """Получить только невыполненные"""
        return [task for task in self.tasks if not task.completed]
    
    def count_tasks(self):
        """Подсчитать все задачи"""
        return len(self.tasks)
    
    def count_completed(self):
        """Подсчитать выполненные"""
        return len(self.get_completed_tasks())
    
    def clear_completed(self):
        """Удалить все выполненные задачи"""
        self.tasks = [task for task in self.tasks if not task.completed]

