class MathOperations:

    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("b can't be zero")
        return a / b


class GetUser:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce_user(self):
        return f"User's name is {self.name.title()} and age is {self.age} years old."


class StringHelpers:

    @staticmethod
    def _is_empty(word): 
        return len(word) == 0 

    def reverse_name(self, name):
        if self._is_empty(name):
            raise ValueError("String input cannot be empty.") 
        return name[::-1]
    
    def palindrome(self, word):
        if self._is_empty(word):
            raise ValueError("String input cannot be empty.")
        return word == word[::-1]
    
    def check_starts_with_upper_case(self, word):
        if self._is_empty(word):
            raise ValueError("String input cannot be empty.")
        return word[0].isupper()
    

class FileOperations:
    def read(self):
        pass
    def write(self):
        pass
