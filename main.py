import random


def generate_secret_number():
    while True:
        digits = random.sample(range(10), 4)
        if digits[0] != 0:
            return digits


def player_secret_number():
    while True:
        player_number = input("Enter your secret number (4 unique digits): ")
        if len(player_number) != 4 or not player_number.isdigit():
            print("Input is invalid. Please enter a 4-digit number!")
            continue

        digits = [int(i) for i in player_number]
        if len(set(digits)) != 4 or digits[0] == 0:
            print("Number should not start with 0 and digits must not repeat!")
            continue

        return digits


def get_user_guess():
    while True:
        guess = input("Enter your guess (4 digits): ")
        if len(set(guess)) != 4 or not guess.isdigit() or guess[0] == '0':
            print("Invalid guess. Please enter a 4-digit number without leading zero.")
        else:
            return list(map(int, guess))


def compare_positions(digits, guesses):
    all_cows_numbers = [key for key, value in guesses.items() if value == "0B4C"]
    for cow_number in all_cows_numbers:
        for i in range(4):
            if digits[i] == cow_number[i]:
                return True
    return False


def get_computer_guess(possible_digits, sure_digits, guesses):
    if len(possible_digits) == 4 and "0B4C" in guesses.values():
        #  Special scenario where there are only 4 numbers left with 4 cows already found
        digits = random.sample(possible_digits, k=4)
        while digits[0] == 0 or tuple(digits) in guesses or compare_positions(digits, guesses):
            digits = random.sample(possible_digits, k=4)
    elif sure_digits:
        #  Special scenario where the sure digits are always used
        remaining_digits = random.sample([digit for digit in possible_digits if digit not in sure_digits], k=2)
        digits = sure_digits + remaining_digits
        random.shuffle(digits)
        while digits[0] == 0 or tuple(digits) in guesses:
            remaining_digits = random.sample([digit for digit in possible_digits if digit not in sure_digits], k=2)
            digits = sure_digits + remaining_digits
            random.shuffle(digits)
    else:
        #  All other scenarios
        digits = random.sample(possible_digits, k=4)
        while digits[0] == 0 or tuple(digits) in guesses:
            digits = random.sample(possible_digits, k=4)
    return digits


def calculate_bulls_and_cows(secret_number, guess):
    bulls = cows = 0

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
            return [0, 1]

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

        computer_guess_int = computer_guess[0] * 1000 + computer_guess[1] * 100 \
                             + computer_guess[2] * 10 + computer_guess[3]
        print(f"Computer guessed {computer_guess_int} and got {comp_bulls} bulls and {comp_cows} cows")


# Start the game
print("Welcome to Bulls and Cows!")
print("I have generated a 4-digit secret number. You will also have to think of a number.")
print("Try to guess my number while I'm trying to guess yours.")
print("For every digit in each guess that matches the secret number in the correct position, that's a bull.")
print("For every digit in each guess that matches the secret number but in the wrong position, that's a cow.")
print("Let's start!")

computer_wins = player_wins = 0

while True:
    computer_win, player_win = play_game()
    computer_wins += computer_win
    player_wins += player_win

    print("Current result is:")
    print(f"Computer: {computer_wins} - Player: {player_wins}\n")

    end_of_game = False
    while True:
        user_input = input("Do you want to continue? (Y)es or (N)o: ").lower()

        if user_input in ['y', 'yes']:
            print("You chose to continue.\n")
            break
        elif user_input in ['n', 'no']:
            print("You chose to stop. This is tne end of the game!")
            end_of_game = True
            break
        else:
            print("Invalid input. Please enter either 'Y' to continue or 'N' to stop playing.")

    if end_of_game:
        break
