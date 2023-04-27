# TODO

# Import getstring
from cs50 import get_string


# Main function
def main():
    # Declare variables
    letters = 0
    words = 1
    sentences = 0
    # Get the string
    text = get_string("Text: ")
    # Count counters
    for i in range(len(text)):
        if text[i].isalpha():
            letters += 1
        elif text[i] == ' ' and letters > 0 and i != (len(text) - 1):
            words += 1
        elif text[i] in ['!', '?', '.']:
            sentences += 1

    # Apply the formula
    L = letters / words * 100
    S = sentences / words * 100
    calculation = 0.0588 * L - 0.296 * S - 15.8
    index = round(calculation)
    # Print
    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print("Grade ", index)


main()
