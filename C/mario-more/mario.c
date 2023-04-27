#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;  // the height of the piramid
    int difference = 1;  // a value that fixez the difference of characters
    do
    {
        height = get_int("Height:"); //inserting the height of the piramid
    }
    while (height < 1 || height > 8); //keep trying until the value will be between [1...8]
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height - difference; j++) // prints number of spaces in value of height -1
        {
            printf(" ");
        }
        for (int j = 0; j < difference; j++) // prints the hashtags on the left side
        {
            printf("#");
        }
        printf("  "); // 2 spaces
        for (int j = 0; j < difference; j++) // prints hashtags on the right side
        {
            printf("#");
        }
        difference++; //increment the diference as on the next line the number of spaces deacreasez and the number of hashtrags increasez
        printf("\n");
    }
}