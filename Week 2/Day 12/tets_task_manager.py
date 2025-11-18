import pytest
from task_manager import Task, TaskManager

@pytest.fixture
def empty_manager():
    """
    Фикстура: пустой менеджер задач
    
    КАК РАБОТАЕТ:
    1. Функция с декоратором @pytest.fixture
    2. Возвращает объект
    3. pytest автоматически вызывает её и передаёт результат в тест
    
    ИСПОЛЬЗОВАНИЕ:
    def test_something(empty_manager):
        # empty_manager это результат этой функции
    """
    return TaskManager()

@pytest.fixture
def manager_with_tasks():
    """
    Фикстура: менеджер с готовыми задачами
    
    ЗАЧЕМ:
    Много тестов проверяют операции с существующими задачами
    Вместо создания задач в каждом тесте - делаем один раз здесь
    """
    manager = TaskManager()
    manager.add_task("Купить молоко")
    manager.add_task("Сделать уроки")
    manager.add_task("Позвонить другу")
    return manager

@pytest.fixture
def manager_with_completed():
    """Фикстура: менеджер с выполненными и невыполненными задачами"""
    manager = TaskManager()
    
    # Добавляем задачи
    task1 = manager.add_task("Задача 1")
    task2 = manager.add_task("Задача 2")
    task3 = manager.add_task("Задача 3")
    
    # Отмечаем первую как выполненную
    task1.mark_completed()
    
    return manager

def test_add_task(empty_manager):
    """
    Тест добавления задачи
    
    ПАРАМЕТР empty_manager:
    pytest автоматически вызовет фикстуру empty_manager()
    и передаст результат в этот параметр
    """
    # empty_manager это объект TaskManager из фикстуры
    task = empty_manager.add_task("Новая задача")
    
    assert task is not None
    assert task.title == "Новая задача"
    assert task.completed == False
    assert empty_manager.count_tasks() == 1




def test_remove_task(manager_with_tasks):
    """Тест удаления задачи"""
    # В manager_with_tasks уже есть 3 задачи
    assert manager_with_tasks.count_tasks() == 3
    
    result = manager_with_tasks.remowe_task("Купить молоко")
    
    assert result == True
    assert manager_with_tasks.count_tasks() == 2

def test_remove_nonexistent_task(manager_with_tasks):
    """Тест удаления несуществующей задачи"""
    result = manager_with_tasks.remowe_task("Несуществующая задача")
    
    assert result == False
    assert manager_with_tasks.count_tasks() == 3  # Ничего не удалилось




def test_mark_task_completed(manager_with_tasks):
    """Тест отметки задачи как выполненной"""
    task = manager_with_tasks.get_task("Купить молоко")
    
    assert task.completed == False
    
    task.mark_completed()
    
    assert task.completed == True





def test_get_completed_tasks(manager_with_completed):
    """Тест получения выполненных задач"""
    completed = manager_with_completed.get_completed_tasks()
    
    assert len(completed) == 1
    assert completed[0].title == "Задача 1"

def test_get_incomplete_tasks(manager_with_completed):
    """Тест получения невыполненных задач"""
    incomplete = manager_with_completed.get_incomplete_tasks()
    
    assert len(incomplete) == 2

def test_count_completed(manager_with_completed):
    """Тест подсчёта выполненных"""
    assert manager_with_completed.count_completed() == 1



def test_clear_completed(manager_with_completed):
    """Тест удаления всех выполненных задач"""
    assert manager_with_completed.count_tasks() == 3
    
    manager_with_completed.clear_completed()
    
    assert manager_with_completed.count_tasks() == 2
    assert manager_with_completed.count_completed() == 0





def test_multiple_fixtures(empty_manager, manager_with_tasks):
    """
    Можно использовать несколько фикстур в одном тесте
    
    pytest создаст оба объекта и передаст в параметры
    """
    assert empty_manager.count_tasks() == 0
    assert manager_with_tasks.count_tasks() == 3



@pytest.fixture(scope="module")
def shared_manager():
    """
    Фикстура с scope="module"
    
    РАЗНИЦА:
    - Обычная фикстура создаётся для КАЖДОГО теста заново
    - scope="module" создаётся ОДИН РАЗ для всех тестов в файле
    
    ЗАЧЕМ:
    Если создание объекта дорогое (подключение к БД, загрузка файла)
    """
    print("\n>>> Создание shared_manager")
    manager = TaskManager()
    manager.add_task("Общая задача")
    return manager


def test_shared_1(shared_manager):
    """Первый тест с shared_manager"""
    assert shared_manager.count_tasks() >= 1


def test_shared_2(shared_manager):
    """Второй тест с тем же shared_manager"""
    assert shared_manager.count_tasks() >= 1


@pytest.fixture
def manager_with_cleanup():
    """
    Фикстура с очисткой после теста
    
    КАК РАБОТАЕТ:
    1. Код до yield выполняется ДО теста (setup)
    2. yield возвращает объект в тест
    3. Код после yield выполняется ПОСЛЕ теста (teardown)
    """
    print("\n>>> Setup: создаём менеджер")
    manager = TaskManager()
    manager.add_task("Тестовая задача")
    
    yield manager  # Передаём в тест
    
    # Этот код выполнится ПОСЛЕ теста
    print("\n>>> Teardown: очищаем менеджер")
    manager.tasks.clear()


def test_with_cleanup(manager_with_cleanup):
    """Тест с очисткой"""
    assert manager_with_cleanup.count_tasks() == 1
    # После этого теста выполнится код после yield