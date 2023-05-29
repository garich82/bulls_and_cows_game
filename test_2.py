digits = [5,1,9,0]
guesses = {5910: 103}

for guess in guesses.keys():
    print(set(digits))
    print(set(str(guess)))
    if set(digits) == set(map(int, str(guess))):
        print("True")
        continue
print("False")

