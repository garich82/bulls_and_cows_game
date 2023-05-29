import random


def has_repeated_digits(digits, guesses):
    for guess in guesses.keys():
        guess_digits = list(guess)
        if all(guess_digits.count(digit) == digits.count(digit) for digit in digits):
            return True
    return False


def compare_positions(digits, all_cows_numbers):
    for cow_number in all_cows_numbers:
        for i in range(4):
            if digits[i] == cow_number[i]:
                return True
    return False


def get_computer_guess(possible_digits, sure_digits, guesses):
    if len(guesses) == 1:
        first_guess = list(guesses.keys())[0]
        digits = [digit for digit in possible_digits if digit not in first_guess]
        random.shuffle(digits)
        while digits[0] == 0:
            random.shuffle(digits)
        digits = digits[:4]
    elif len(possible_digits) == 4 and 4 in guesses.values():
        all_cows_numbers = []
        for key, value in guesses.items():
            if value == 4:
                all_cows_numbers.append(key)
        digits = random.sample(possible_digits, k=4)
        while digits[0] == 0 or tuple(digits) in guesses or compare_positions(digits, all_cows_numbers):
            digits = random.sample(possible_digits, k=4)
    elif len(possible_digits) == 4:
        digits = random.sample(possible_digits, k=4)
        while digits[0] == 0 or tuple(digits) in guesses:
            digits = random.sample(possible_digits, k=4)
    elif sure_digits:
        remaining_digits = random.sample([digit for digit in possible_digits if digit not in sure_digits], k=2)
        digits = sure_digits + remaining_digits
        random.shuffle(digits)
        while digits[0] == 0 or tuple(digits) in guesses or has_repeated_digits(digits, guesses):
            remaining_digits = random.sample([digit for digit in possible_digits if digit not in sure_digits], k=2)
            digits = sure_digits + remaining_digits
            random.shuffle(digits)
    else:
        digits = random.sample(possible_digits, k=4)
        while digits[0] == 0 or int(''.join(map(str, digits))) in guesses:
            digits = random.sample(possible_digits, k=4)
    return digits


def check_last_two(possible_digits, guesses):
    total_guessed_digits = sum(value % 10 + value // 10 for value in guesses.values())
    sure_digits = []
    if total_guessed_digits == 2:
        sure_digits = [digit for digit in possible_digits if digit not in sum(guesses.keys(), ())]
    return sure_digits


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


def generate_secret_number():
    """Generate a random 4-digit secret number for the computer"""
    return random.sample(range(10), 4)


def play_game():
    player_number = [1, 2, 3, 4]
    computer_guesses = {}
    possible_digits = list(range(10))
    sure_digits = []
    counter = 0

    while True:
        counter += 1

        computer_guess = get_computer_guess(possible_digits, sure_digits, computer_guesses)
        comp_bulls, comp_cows = calculate_bulls_and_cows(player_number, computer_guess)
        computer_guesses[tuple(computer_guess)] = comp_bulls * 10 + comp_cows
        guessed_digits = comp_bulls + comp_cows

        if guessed_digits == 0:
            digits_to_remove = computer_guess
            possible_digits = [digit for digit in possible_digits if digit not in digits_to_remove]
        elif guessed_digits == 4:
            if comp_bulls == 4:
                print(f"Computer guessed the secret number {player_number} in {counter} attempts! Game Over!")
                break
            possible_digits = computer_guess
        elif guessed_digits == 2 and len(possible_digits) == 6 and not sure_digits:
            digits_to_remove = computer_guess
            sure_digits = [digit for digit in possible_digits if digit not in digits_to_remove]

        if len(computer_guesses) == 2:
            sure_digits = check_last_two(possible_digits, computer_guesses)

        computer_guess_int = computer_guess[0] * 1000 + computer_guess[1] * 100\
                                                  + computer_guess[2] * 10 + computer_guess[3]
        print(f"Computer guessed {computer_guess_int} and got {comp_bulls} bulls and {comp_cows} cows")

    return counter + 1


play_game()
