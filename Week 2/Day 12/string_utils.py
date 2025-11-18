def reverse_string(s):
    return s[::-1]

def is_palindrome(s):
    """
    Проверить палиндром ли строка
    (читается одинаково в обе стороны)
    
    ПРИМЕР:
    is_palindrome("radar") -> True
    is_palindrome("hello") -> False
    """
    s = s.lower().replace(" ", "")
    return s == s[::-1]

def count_vowels(s):
    """
    Подсчитать гласные буквы
    """
    vowels = "aeiouаеёиоуыэюя"
    count = 0
    for char in s.lower():
        if char in vowels:
            count += 1
    return count

def capitalize_words(s):
    words = s.split()
    capitalized = []
    for word in words:
        if word:
            capitalized.append(word[0].upper() + word[1:])
    return " ".join(capitalized)

def remove_duplicates(s):
    result = []
    seen = set()
    
    for char in s:
        if char not in seen:
            result.append(char)
            seen.add(char)
    
    return "".join(result)