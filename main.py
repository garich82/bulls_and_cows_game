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


def has_repeated_digits(digits, guesses):
    for guess in guesses.keys():
        guess_digits = [int(digit) for digit in str(guess)]
        if all(guess_digits.count(digit) == digits.count(digit) for digit in digits):
            return True
    return False


def compare_positions(digits, all_cows_numbers):
    for cow_number in all_cows_numbers:
        cow_number = str(cow_number)
        for i in range(4):
            if str(digits[i]) == cow_number[i]:
                return True
    return False


def get_computer_guess(possible_digits, sure_digits, guesses):
    if len(possible_digits) == 4 and 4 in guesses.values():
        all_cows_numbers = []
        for key, value in guesses.items():
            if value == 4:
                all_cows_numbers.append(key)
        digits = random.sample(possible_digits, k=4)
        while digits[0] == 0 or int(''.join(map(str, digits))) in guesses or compare_positions(digits, all_cows_numbers):
            digits = random.sample(possible_digits, k=4)
    elif len(possible_digits) == 4:
        digits = random.sample(possible_digits, k=4)
        while digits[0] == 0 or int(''.join(map(str, digits))) in guesses:
            digits = random.sample(possible_digits, k=4)
    elif sure_digits:
        remaining_digits = random.sample([digit for digit in possible_digits if digit not in sure_digits], k=2)
        digits = sure_digits + remaining_digits
        random.shuffle(digits)
        while digits[0] == 0 or int(''.join(map(str, digits))) in guesses or has_repeated_digits(digits, guesses):
            remaining_digits = random.sample([digit for digit in possible_digits if digit not in sure_digits], k=2)
            digits = sure_digits + remaining_digits
            random.shuffle(digits)
    else:
        digits = random.sample(possible_digits, k=4)
        while digits[0] == 0 or int(''.join(map(str, digits))) in guesses:
            digits = random.sample(possible_digits, k=4)
    return int(''.join(map(str, digits)))


def calculate_score(secret_number, guess):
    score = 0
    secret_digits = [int(digit) for digit in str(secret_number)]
    guess_digits = [int(digit) for digit in str(guess)]
    for i in range(len(guess_digits)):
        if guess_digits[i] == secret_digits[i]:
            score += 10
        elif guess_digits[i] in secret_digits:
            score += 1
    return score


def calculate_bulls_and_cows(secret_number, guess):
    """Calculate the number of bulls and cows in the guess."""
    if isinstance(secret_number, int):
        secret_digits = [int(digit) for digit in str(secret_number)]
    else:
        secret_digits = secret_number

    if isinstance(guess, int):
        guess_digits = [int(digit) for digit in str(guess)]
    else:
        guess_digits = guess

    bulls = sum(guess_digits[i] == secret_digits[i] for i in range(len(guess_digits)))
    cows = sum(
        guess_digits[i] in secret_digits and guess_digits[i] != secret_digits[i] for i in range(len(guess_digits)))

    return bulls, cows


def play_game():
    computer_number = generate_secret_number()
    player_number = player_secret_number()
    computer_guesses = {}
    possible_digits = list(range(10))
    sure_digits = []
    counter = 0

    while True:
        counter += 1
        guess = get_user_guess()

        bulls, cows = calculate_bulls_and_cows(computer_number, guess)

        if bulls == 4:
            print(f"Congratulations! You guessed computer's number with {counter} attempts")
            break

        print(f"You have {bulls} bulls and {cows} cows")

        computer_guess = get_computer_guess(possible_digits, sure_digits, computer_guesses)
        score = calculate_score(int(''.join(map(str, player_number))), computer_guess)
        computer_guesses[computer_guess] = score
        if score == 0:
            digits_to_remove = computer_guess
            possible_digits = [digit for digit in possible_digits if digit not in digits_to_remove]
        elif sum(map(int, str(score))) == 4:  # Specific scenario: 4 out of 4 digits are correct
            possible_digits = computer_guess
        elif sum(map(int, str(score))) == 2 and len(possible_digits) == 6 and not sure_digits:
            digits_to_remove = computer_guess
            sure_digits = [digit for digit in possible_digits if digit not in digits_to_remove]
        elif score == 40:
            print(f"Computer guessed your number in {counter} attempts! Game Over!")

        comp_bulls, comp_cows = calculate_bulls_and_cows(player_number, computer_guess)

        print(f"Computer got {comp_bulls} bulls and {comp_cows} cows")


# Start the game
print("Welcome to Bulls and Cows!")
print("I have generated a 4-digit secret number. You will also have to think of a number.")
print("Try to guess my number while I'm trying to guess yours.")
print("For every digit in each guess that matches the secret number in the correct position, that's a bull.")
print("For every digit in each guess that matches the secret number but in the wrong position, that's a cow.")
print("Let's start!")

play_game()
