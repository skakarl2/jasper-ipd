import random

class NumberGuessingGame:
    def __init__(self, lower_bound=1, upper_bound=100):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.target_number = random.randint(lower_bound, upper_bound)

    def guess(self, number):
        if number < self.lower_bound or number > self.upper_bound:
            return "Out of bounds!"
        if number < self.target_number:
            return "Too low!"
        elif number > self.target_number:
            return "Too high!"
        else:
            return "Correct!"

# Example usage
if __name__ == "__main__":
    game = NumberGuessingGame()
    print("Guess a number between 1 and 100!")
    while True:
        try:
            user_guess = int(input("Enter your guess: "))
            result = game.guess(user_guess)
            print(result)
            if result == "Correct!":
                break
        except ValueError:
            print("Please enter a valid number.")