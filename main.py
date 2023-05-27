import random


def generate_secret_number():
    """Generate a random 4-digit secret number for computer"""
    digits = list(range(10))
    random.shuffle(digits)
    return digits[:4]


def player_secret_number():
    """Validate player's number"""
    while True:
        player_number = input("Enter your secret number (4 unique digits): ")
        if len(player_number) != 4 or not player_number.isdigit():
            print("Invalid guess. Please enter a 4-digit number.")
            continue

        digits = list(player_number)
        if len(set(digits)) != 4:
            print("Invalid guess. Digits must not repeat.")
            continue

        return list(map(int, digits))


def get_user_guess():
    """Get a 4-digit guess from the user."""
    while True:
        guess = input("Enter your guess (4 digits): ")
        if len(guess) != 4 or not guess.isdigit():
            print("Invalid guess. Please enter a 4-digit number.")
        else:
            return list(map(int, guess))


def get_computer_guess():



def calculate_bulls_and_cows(secret_number, guess):
    """Calculate the number of bulls and cows in the guess."""
    bulls = 0
    cows = 0
    for i in range(len(guess)):
        if guess[i] == secret_number[i]:
            bulls += 1
        elif guess[i] in secret_number:
            cows += 1
    return bulls, cows


def play_game():
    computer_number = generate_secret_number()
    player_number = player_secret_number()
    attempts = 0

    while True:
        guess = get_user_guess()
        bulls, cows = calculate_bulls_and_cows(computer_number, guess)
        attempts += 1

        print("Bulls: ", bulls)
        print("Cows: ", cows)

        if bulls == 4:
            print("Congratulations! You guessed the number in", attempts, "attempts.")
            break


# Start the game
print("Welcome to Bulls and Cows!")
print("I have generated a 4-digit secret number. You will also have to think of a number.")
print("Try to guess my number while I'm trying to guess yours.")
print("For every digit in each guess that matches the secret number in the correct position, that's a bull.")
print("For every digit in each guess that matches the secret number but in the wrong position, that's a cow.")
print("Let's start!")

play_game()