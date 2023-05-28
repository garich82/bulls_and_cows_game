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


def get_computer_guess(possible_digits, guessed_numbers):
    impossible_digits = [n for n in range(0, 10) if n not in possible_digits]
    if possible_digits == 4:
        while True:
            random.shuffle(possible_digits)
            computer_guess = int(''.join(map(str, possible_digits)))
            if computer_guess not in guessed_numbers:
                return computer_guess
    else:
        while True:
            random.shuffle(impossible_digits)
            random.shuffle(possible_digits)
            computer_guess = possible_digits[0] * 1000 + possible_digits[1] * 100 + \
                             possible_digits[2] * 10 + impossible_digits[0]
            if computer_guess not in guessed_numbers:
                return computer_guess



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
    computer_guessed_numbers = {}
    players_possible_digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    while True:
        guess = get_user_guess()
        bulls, cows = calculate_bulls_and_cows(computer_number, guess)

        print(f"You have {bulls} bulls and {cows} cows")

        if bulls == 4:
            print("Congratulations! You guessed computer's number.")
            break

        comp_guess = get_computer_guess(players_possible_digits, computer_guessed_numbers)
        comp_bulls, comp_cows = calculate_bulls_and_cows(player_number, comp_guess)


# Start the game
print("Welcome to Bulls and Cows!")
print("I have generated a 4-digit secret number. You will also have to think of a number.")
print("Try to guess my number while I'm trying to guess yours.")
print("For every digit in each guess that matches the secret number in the correct position, that's a bull.")
print("For every digit in each guess that matches the secret number but in the wrong position, that's a cow.")
print("Let's start!")

play_game()