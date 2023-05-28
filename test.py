import random


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



possible_digits = [0, 1, 2, 3, 4, 5, 6]
guessed_numbers = {1234: 102, 5678: 111}
print(get_computer_guess(possible_digits, guessed_numbers))
