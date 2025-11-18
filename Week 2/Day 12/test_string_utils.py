import pytest
from string_utils import (
    reverse_string, 
    is_palindrome, 
    count_vowels,
    capitalize_words,
    remove_duplicates
)
def test_reverse_string():
    """Тест переворота строки"""
    assert reverse_string("hello") == "olleh"
    assert reverse_string("python") == "nohtyp"
    assert reverse_string("") == ""
    assert reverse_string("a") == "a"

@pytest.mark.parametrize("input_str, expected", [
        ("hello", "olleh"),
        ("12345", "54321"),
        ("", ""),
        ("a", "a"),
    ])


def test_reverse_string_parametrized(input_str, expected):
    assert reverse_string(input_str) == expected


def test_is_palindrome():
    """Тест проверки палиндрома"""
    # Палиндромы
    assert is_palindrome("radar") == True
    assert is_palindrome("level") == True
    assert is_palindrome("a") == True
    
    # Не палиндромы
    assert is_palindrome("hello") == False
    assert is_palindrome("python") == False

@pytest.mark.parametrize("text, expected", [
    ("hello", 2),      # e, o
    ("python", 1),     # o
    ("aeiou", 5),      # все гласные
    ("bcdfg", 0),      # нет гласных
    ("", 0),           # пустая строка
])
def test_count_vowels(text, expected):
    assert count_vowels(text) == expected

def test_capitalize_words():
    """Тест капитализации слов"""
    assert capitalize_words("hello world") == "Hello World"
    assert capitalize_words("python programming") == "Python Programming"
    assert capitalize_words("a b c") == "A B C"

@pytest.mark.parametrize("text, expected", [
    ("hello", "helo"),
    ("aabbcc", "abc"),
    ("", ""),
    ("abc", "abc"),
    ("aaaa", "a"),
])
def test_remove_duplicates(text, expected):
    assert remove_duplicates(text) == expected

class TestStringUtils:
    """
    Класс для группировки тестов
    
    ЗАЧЕМ:
    Удобно организовать связанные тесты
    pytest автоматически найдёт все методы начинающиеся с test_
    """
    
    def test_reverse(self):
        assert reverse_string("test") == "tset"
    
    def test_palindrome(self):
        assert is_palindrome("mom") == True
    
    def test_vowels(self):
        assert count_vowels("test") == 1