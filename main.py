import random


def generate_secret_number():
    """Generate a random 4-digit secret number for the computer"""
    digits = random.sample(range(10), 4)
    while digits[0] == 0:
        digits = random.sample(range(10), 4)
    return digits


def player_secret_number():
    """Validate player's number"""
    while True:
        player_number = input("Enter your secret number (4 unique digits): ")
        if len(player_number) != 4 or not player_number.isdigit():
            print("Input is invalid. Please enter a 4-digit number!")
            continue

        digits = [int(i) for i in player_number]
        if len(set(digits)) != 4 or digits[0] == 0:
            print("Number should not start with 0 and/or digits must not repeat!")
            continue

        return digits


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
            print(f"\nCongratulations! You guessed computer's number with {counter} attempts\n")
            return[0, 1]
            break

        print(f"You have {bulls} bulls and {cows} cows")

        computer_guess = get_computer_guess(possible_digits, sure_digits, computer_guesses)
        comp_bulls, comp_cows = calculate_bulls_and_cows(player_number, computer_guess)
        computer_guesses[tuple(computer_guess)] = f"{comp_bulls}B{comp_cows}C"
        guessed_digits = comp_bulls + comp_cows

        if guessed_digits == 0:
            digits_to_remove = computer_guess
            possible_digits = [digit for digit in possible_digits if digit not in digits_to_remove]
        elif guessed_digits == 4:
            if comp_bulls == 4:
                print(f"\nComputer guessed your number in {counter} attempts! Game Over!")
                print(f"Computer number was {computer_number}\n")
                return [1, 0]
            possible_digits = computer_guess
        elif guessed_digits == 2 and len(possible_digits) == 6 and not sure_digits:
            digits_to_remove = computer_guess
            sure_digits = [digit for digit in possible_digits if digit not in digits_to_remove]

        computer_guess_int = computer_guess[0] * 1000 + computer_guess[1] * 100\
                                                  + computer_guess[2] * 10 + computer_guess[3]
        print(f"Computer guessed {computer_guess_int} and got {comp_bulls} bulls and {comp_cows} cows")


# Start the game
print("Welcome to Bulls and Cows!")
print("I have generated a 4-digit secret number. You will also have to think of a number.")
print("Try to guess my number while I'm trying to guess yours.")
print("For every digit in each guess that matches the secret number in the correct position, that's a bull.")
print("For every digit in each guess that matches the secret number but in the wrong position, that's a cow.")
print("Let's start!")

computer_wins = 0
player_wins = 0

while True:
    computer_win, player_win = play_game()
    computer_wins += computer_win
    player_wins += player_win

    print("Current result is:")
    print(f"Computer: {computer_wins} - Player: {player_wins}\n")

    end_of_game = False
    while True:
        user_input = input("Do you want to continue? (Y)es or (N)o: ")

        if user_input.lower() == 'y' or user_input.lower() == 'yes':
            print("You chose to continue.\n")
            break
        elif user_input.lower() == 'n' or user_input.lower() == 'no':
            print("You chose to stop. This is tne end of the game!")
            end_of_game = True
            break
        else:
            print("Invalid input. Please enter either 'Y' or 'N'.")

    if end_of_game:
        break
