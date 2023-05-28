import random


def generate_secret_number(possible_digits, sure_digits, guesses):
    if sure_digits:
        remaining_digits = random.sample([digit for digit in possible_digits if digit not in sure_digits], k=2)
        digits = sure_digits + remaining_digits
        while digits[0] == 0 or int(''.join(map(str, digits))) in guesses:
            random.shuffle(digits)
    else:
        digits = random.sample(possible_digits, k=4)
        while digits[0] == 0 or int(''.join(map(str, digits))) in guesses:
            digits = random.sample(possible_digits, k=4)
    return int(''.join(map(str, digits)))


def calculate_score(secret_number, guess):
    score = 100
    secret_digits = [int(digit) for digit in str(secret_number)]
    guess_digits = [int(digit) for digit in str(guess)]
    for i in range(len(guess_digits)):
        if guess_digits[i] == secret_digits[i]:
            score += 10
        elif guess_digits[i] in secret_digits:
            score += 1
    return score

def play_game():
    secret_number = int(input("Enter a secret 4-digit number with unique digits (excluding leading 0): "))
    possible_digits = list(range(10))  # List of possible digits for the secret number
    sure_digits = []  # List of digits for which we know that are in the secret number
    guesses = {}
    counter = 0  # Counter for the number of computer's guesses
    computer_guess = generate_secret_number(possible_digits, sure_digits, guesses)
    while computer_guess != secret_number:
        score = calculate_score(secret_number, computer_guess)
        if (computer_guess, score) not in guesses.items():  # Check if the guess with the same score is already present
            counter += 1
        guesses[computer_guess] = score
        print(f"Computer guess {counter}: {computer_guess} | Score: {score}")
        if score == 100:
            digits_to_remove = [int(digit) for digit in str(computer_guess)]
            possible_digits = [digit for digit in possible_digits if digit not in digits_to_remove]
        elif sum(map(int, str(score))) == 5:  # Specific scenario: 4 out of 4 digits are correct
            possible_digits = [int(digit) for digit in str(computer_guess)]
        elif sum(map(int, str(score))) == 3 and len(possible_digits) == 6 and not sure_digits:
            digits_to_remove = [int(digit) for digit in str(computer_guess)]
            sure_digits = [digit for digit in possible_digits if digit not in digits_to_remove]

        computer_guess = generate_secret_number(possible_digits, sure_digits, guesses)

    print(f"Computer guessed the secret number {secret_number} in {counter+1} guesses!")

play_game()








# import random
#
#
# def generate_secret_number(possible_digits, sure_digits, guesses):
#     if sure_digits:
#         remaining_digits = random.sample([digit for digit in possible_digits if digit not in sure_digits], k=2)
#         digits = sure_digits + remaining_digits
#         while digits[0] == 0 or int(''.join(map(str, digits))) in guesses:
#             random.shuffle(digits)
#     else:
#         digits = random.sample(possible_digits, k=4)
#         while digits[0] == 0 or int(''.join(map(str, digits))) in guesses:
#             digits = random.sample(possible_digits, k=4)
#     return int(''.join(map(str, digits)))
#
#
# def calculate_score(secret_number, guess):
#     score = 100
#     secret_digits = [int(digit) for digit in str(secret_number)]
#     guess_digits = [int(digit) for digit in str(guess)]
#     for i in range(len(guess_digits)):
#         if guess_digits[i] == secret_digits[i]:
#             score += 10
#         elif guess_digits[i] in secret_digits:
#             score += 1
#     return score
#
#
# def play_game(secret_number):
#     possible_digits = list(range(10))  # List of possible digits for the secret number
#     sure_digits = []  # List of digits for which we know that are in the secret number
#     guesses = {}
#     counter = 0  # Counter for the number of computer's guesses
#     computer_guess = generate_secret_number(possible_digits, sure_digits, guesses)
#     while computer_guess != secret_number:
#         score = calculate_score(secret_number, computer_guess)
#         if (computer_guess, score) not in guesses.items():  # Check if the guess with the same score is already present
#             counter += 1
#         guesses[computer_guess] = score
#         if score == 100:
#             digits_to_remove = [int(digit) for digit in str(computer_guess)]
#             possible_digits = [digit for digit in possible_digits if digit not in digits_to_remove]
#         elif sum(map(int, str(score))) == 5:  # Specific scenario: 4 out of 4 digits are correct
#             possible_digits = [int(digit) for digit in str(computer_guess)]
#         elif sum(map(int, str(score))) == 3 and len(possible_digits) == 6 and not sure_digits:
#             digits_to_remove = [int(digit) for digit in str(computer_guess)]
#             sure_digits = [digit for digit in possible_digits if digit not in digits_to_remove]
#
#         computer_guess = generate_secret_number(possible_digits, sure_digits, guesses)
#
#     return counter + 1
#
#
# def run_multiple_games(num_games):
#     secret_number = int(input("Enter a secret 4-digit number with unique digits (excluding leading 0): "))
#     total_guesses = 0
#     for _ in range(num_games):
#         guesses = play_game(secret_number)
#         total_guesses += guesses
#     average_guesses = total_guesses / num_games
#     print(f"Average number of guesses across {num_games} games: {average_guesses}")
#
#
# run_multiple_games(20000)  # Change the number of games as needed
