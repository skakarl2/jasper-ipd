import random

def number_guessing_game():
    target = random.randint(1, 100)
    attempts = 0
    print("Welcome to the Number Guessing Game!")
    print("Guess a number between 1 and 100.")
    
    while True:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1
            if guess < target:
                print("Too low! Try again.")
            elif guess > target:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts.")
                return attempts
        except ValueError:
            print("Invalid input. Please enter a number.")

import unittest
from unittest.mock import patch
from game import number_guessing_game

class TestNumberGuessingGame(unittest.TestCase):
    @patch('builtins.input', side_effect=[50, 75, 62, 68, 65])
    @patch('random.randint', return_value=65)
    def test_game_success(self, mock_randint, mock_input):
        attempts = number_guessing_game()
        self.assertEqual(attempts, 5)

    @patch('builtins.input', side_effect=[101, 'abc', 65])
    @patch('random.randint', return_value=65)
    def test_game_invalid_inputs(self, mock_randint, mock_input):
        attempts = number_guessing_game()
        self.assertEqual(attempts, 3)

if __name__ == '__main__':
    unittest.main()