import random

def guess_number_game():
    print("Welcome to the Number Guessing Game!")
    number_to_guess = random.randint(1, 100)
    attempts = 0

    while True:
        try:
            user_guess = int(input("Guess a number between 1 and 100: "))
            attempts += 1

            if user_guess < 1 or user_guess > 100:
                print("Please guess a number within the range!")
            elif user_guess < number_to_guess:
                print("Too low! Try again.")
            elif user_guess > number_to_guess:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts.")
                break
        except ValueError:
            print("Invalid input! Please enter a number.")

if __name__ == "__main__":
    guess_number_game()    import unittest
    from unittest.mock import patch
    from commit_test import guess_number_game
    
    class TestGuessNumberGame(unittest.TestCase):
        @patch('builtins.input', side_effect=['50', '75', '25', '100'])
        @patch('builtins.print')
        @patch('commit_test.random.randint', return_value=75)
        def test_game(self, mock_randint, mock_print, mock_input):
            guess_number_game()
            mock_randint.assert_called_once_with(1, 100)
            self.assertIn("Congratulations! You guessed the number in", str(mock_print.call_args_list))
    
    if __name__ == "__main__":
        unittest.main()