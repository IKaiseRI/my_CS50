# TODO
from cs50 import get_int


def main():
    # Get a card number
    while True:
        number = get_int("Number: ")
        if len(str(number)) in (13, 15, 16):
            break
        else:
            # Exit if it don't corespond the condition
            print("INVALID")
            exit(0)
    # Call checksum
    checksum(number)


# Implementation of Luh's algorithm
def counter(x):
    multiplied = 0
    nonmultiplied = 0
    checker = 0
    while x != 0:
        nonmultiplied += x % 10
        x = x // 10
        checker = 2 * (x % 10)
        if checker < 10:
            multiplied += checker
        else:
            multiplied += (checker % 10 + checker // 10)
        x = x // 10
    # If card is valide, continue: Else exit
    if (multiplied + nonmultiplied) % 10 == 0:
        return True
    else:
        print("INVALID")
        exit(0)


# Cheking the card type
def checksum(x):
    length = len(str(x))
    if counter(x):
        if int(str(x)[:2]) in (34, 37) and length == 15:
            print("AMEX")
        elif int(str(x)[:2]) in (51, 52, 53, 54, 55) and length == 16:
            print("MASTERCARD")
        elif int(str(x)[:1]) == 4 and length in (13, 16):
            print("VISA")
        else:
            print("INVALID")


# Call the main method
main()