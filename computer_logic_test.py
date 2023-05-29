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
    if len(possible_digits) == 4 and "0B4C" in guesses.values():
        all_cows_numbers = []
        for key, value in guesses.items():
            if value == "0B4C":
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


def play_game(secret_number):
    # player_number = generate_secret_number()
    player_number = [int(i) for i in str(secret_number)]
    computer_guesses = {}
    possible_digits = list(range(10))
    sure_digits = []
    counter = 0

    while True:
        counter += 1

        computer_guess = get_computer_guess(possible_digits, sure_digits, computer_guesses)
        comp_bulls, comp_cows = calculate_bulls_and_cows(player_number, computer_guess)
        computer_guesses[tuple(computer_guess)] = f"{comp_bulls}B{comp_cows}C"
        guessed_digits = comp_bulls + comp_cows

        if guessed_digits == 0:
            digits_to_remove = computer_guess
            possible_digits = [digit for digit in possible_digits if digit not in digits_to_remove]
        elif guessed_digits == 4:
            if comp_bulls == 4:
                # print(f"Computer guessed your number in {counter} attempts! Game Over!")
                break
            possible_digits = computer_guess
        elif guessed_digits == 2 and len(possible_digits) == 6 and not sure_digits:
            digits_to_remove = computer_guess
            sure_digits = [digit for digit in possible_digits if digit not in digits_to_remove]

        # computer_guess_int = computer_guess[0] * 1000 + computer_guess[1] * 100\
        #                                           + computer_guess[2] * 10 + computer_guess[3]
        # print(f"Computer guessed {computer_guess_int} and got {comp_bulls} bulls and {comp_cows} cows")

    return counter + 1


def run_multiple_games(num_games):
    secret_number = int(input("Enter a secret 4-digit number with unique digits (excluding leading 0): "))
    total_guesses = 0
    for _ in range(num_games):
        guesses = play_game(secret_number)
        total_guesses += guesses
    average_guesses = total_guesses / num_games
    print(f"Average number of guesses across {num_games} games: {average_guesses}")


run_multiple_games(10000)  # Change the number of games as needed
