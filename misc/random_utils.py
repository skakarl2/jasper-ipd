#!/usr/bin/env python3
"""
Random utility functions for various tasks.
"""

import hashlib
import json
from typing import List, Dict, Any, Callable
from datetime import datetime, timedelta
import random


class TextAnalyzer:
    """Analyze and manipulate text in interesting ways."""
    
    @staticmethod
    def reverse_words(text: str) -> str:
        """Reverse the order of words in a string."""
        return " ".join(reversed(text.split()))
    
    @staticmethod
    def count_vowels(text: str) -> Dict[str, int]:
        """Count occurrences of each vowel."""
        vowels = "aeiouAEIOU"
        return {v: text.count(v) for v in "aeiou"}
    
    @staticmethod
    def is_palindrome(text: str) -> bool:
        """Check if text is a palindrome (ignoring spaces and case)."""
        cleaned = ''.join(c.lower() for c in text if c.isalnum())
        return cleaned == cleaned[::-1]


class DataGenerator:
    """Generate various types of data."""
    
    @staticmethod
    def fibonacci(n: int) -> List[int]:
        """Generate first n Fibonacci numbers."""
        if n <= 0:
            return []
        elif n == 1:
            return [0]
        fib = [0, 1]
        for _ in range(n - 2):
            fib.append(fib[-1] + fib[-2])
        return fib[:n]
    
    @staticmethod
    def random_schedule(days: int = 7) -> Dict[str, str]:
        """Generate a random daily schedule."""
        activities = ["Exercise", "Study", "Work", "Relax", "Cook", "Read", "Code"]
        schedule = {}
        base_date = datetime.now()
        for i in range(days):
            date_str = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
            schedule[date_str] = random.choice(activities)
        return schedule
    
    @staticmethod
    def hash_data(data: Any) -> str:
        """Create a SHA256 hash of JSON-serialized data."""
        json_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(json_str.encode()).hexdigest()


class NumberCruncher:
    """Perform mathematical operations."""
    
    @staticmethod
    def prime_factors(n: int) -> List[int]:
        """Return prime factors of n."""
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Euclidean algorithm for greatest common divisor."""
        while b:
            a, b = b, a % b
        return a
    
    @staticmethod
    def lcm(a: int, b: int) -> int:
        """Least common multiple."""
        return abs(a * b) // NumberCruncher.gcd(a, b)


def pipeline(*functions: Callable) -> Callable:
    """Create a function pipeline: chain multiple functions together."""
    def pipe(value):
        for func in functions:
            value = func(value)
        return value
    return pipe


def memoize(func: Callable) -> Callable:
    """Simple memoization decorator."""
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper


@memoize
def fibonacci_memo(n: int) -> int:
    """Fibonacci with memoization."""
    if n <= 1:
        return n
    return fibonacci_memo(n - 1) + fibonacci_memo(n - 2)


if __name__ == "__main__":
    # Demo the utilities
    print("=== Text Analyzer ===")
    text = "A man, a plan, a canal: Panama"
    print(f"Original: {text}")
    print(f"Palindrome: {TextAnalyzer.is_palindrome(text)}")
    print(f"Vowels: {TextAnalyzer.count_vowels(text)}")
    print(f"Reversed: {TextAnalyzer.reverse_words(text)}\n")
    
    print("=== Data Generator ===")
    print(f"Fibonacci(10): {DataGenerator.fibonacci(10)}")
    print(f"Schedule: {DataGenerator.random_schedule(3)}\n")
    
    print("=== Number Cruncher ===")
    print(f"Prime factors of 84: {NumberCruncher.prime_factors(84)}")
    print(f"GCD(48, 18): {NumberCruncher.gcd(48, 18)}")
    print(f"LCM(12, 18): {NumberCruncher.lcm(12, 18)}\n")
    
    print("=== Pipeline Example ===")
    double = lambda x: x * 2
    add_ten = lambda x: x + 10
    square = lambda x: x ** 2
    
    my_pipe = pipeline(double, add_ten, square)
    print(f"Pipeline (double → +10 → square) of 5: {my_pipe(5)}")
    
    print("\n=== Memoized Fibonacci ===")
    print(f"Fib(35): {fibonacci_memo(35)}")
