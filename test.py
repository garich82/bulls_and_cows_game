import random

def get_computer_guess(possible_digits):
    impossible_digits = [n for n in range(0,10) if n not in possible_digits]
    if possible_digits == 4:
        pass
    else:
        random.shuffle(impossible_digits)
        random.shuffle(possible_digits)
        

print(get_computer_guess([0,1,2,3,4,5,6]))