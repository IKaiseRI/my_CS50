# TODO

# Def the main function
def main():
    # Get height
    height = get_height()
    # Decrementor value for spaces
    difference = 1
    for i in range(height):
        for j in range(height - difference):
            print(" ", end="")
        for k in range(difference):
            print("#", end="")
        print("  ", end="")
        for m in range(difference):
            print("#", end="")
        difference += 1
        print()


# Method to get height
def get_height():
    while True:
        try:
            height = int(input("Height: "))
            if 0 < height < 9:
                break
        except ValueError:
            print("Please insert max value of 8")
    return height


# Calling the main function
main()