#include <cs50.h>
#include <stdio.h>

long input()
{
    long x = get_long("Number: "); //inserting a long value

    return x; //returning a long value
}
int numberLength(long x) //function to check the length of the card
{
    int length = 0;
    do
    {
        x = x / 10;
        length++;
    }
    while (x != 0);
    return length; //returns the length
}
int counter(long x) //Luhn's Algorithm
{
    int multiplied = 0, nonmultiplied = 0; //falues for doubled and not doubled sums
    int checker = 0; //in case the value that is doubled is higher than 10
    do
    {
        nonmultiplied += x % 10;
        x = x / 10;
        checker = 2 * (x % 10);
        if (checker < 10)
        {
            multiplied = multiplied + checker;
        }
        else
        {
            multiplied = multiplied + (checker % 10 + checker / 10);
        }
        x = x / 10;
    }
    while (x != 0);
    return multiplied + nonmultiplied; //returns the final result of the Algorithm
}
void checksum(long x) // final function that cheks if the card is a valid one
{
    int keyvalue = 0; //value that will hold the first digits
    int length = numberLength(x);
    switch (length)
    {
        case 15:
            keyvalue = x / 10000000000000;
            if (keyvalue == 37 || keyvalue == 34) // in case the digits correspond the algoright will be cheked
            {
                if (counter(x) % 10 == 0)
                {
                    printf("AMEX\n");
                }
                else
                {
                    printf("INVALID\n");
                }
            }
            else
            {
                printf("INVALID\n");
            }
            break;
        case 16:
            keyvalue = x / 100000000000000;
            if (keyvalue == 51 || keyvalue == 52 || keyvalue == 53 || keyvalue == 54
                || keyvalue == 55) // in case the digits correspond the algoright will be cheked
            {
                if (counter(x) % 10 == 0)
                {
                    printf("MASTERCARD\n");
                }
                else
                {
                    printf("INVALID\n");
                }
            }
            else if (keyvalue >= 40 && keyvalue <= 49) // in case the digits correspond the algoright will be cheked
            {
                if (counter(x) % 10 == 0)
                {
                    printf("VISA\n");
                }
                else
                {
                    printf("INVALID\n");
                }
            }
            else
            {
                printf("INVALID\n");
            }
            break;
        case 13:
            keyvalue = x / 1000000000000;
            if (keyvalue == 4) // in case the digits correspond the algoright will be cheked
            {
                if (counter(x) % 10 == 0)
                {
                    printf("VISA\n");
                }
                else
                {
                    printf("INVALID\n");
                }
            }
            else
            {
                printf("INVALID\n");
            }
            break;
        default:
            printf("INVALID\n");
            break;
    }
}
int main(void)
{
    long number = input(); // creating a variable of type long and associate with the input function
    checksum(number); //declaring the function
}