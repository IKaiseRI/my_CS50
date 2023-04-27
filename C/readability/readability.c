#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>
#include <string.h>

//Declaring functions
int letters(string text);
int words(string text);
int sentences(string text);

int main(void)
{
    string text = get_string("Text: "); //Get string
    float L = 0, W = 0, S = 0; //Calculation variables
    W = words(text);
    L = (letters(text) / W) * 100;
    S = (sentences(text) / W) * 100;

    float calculation = 0.0588 * L - 0.296 * S - 15.8; //Caclucating formula
    int index = round(calculation);

    //Resunt conditions
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
    return 0;
}

//Count the letters
int letters(string text)
{
    int count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            count ++;
        }
    }
    return count;
}

//Count the words
int words(string text)
{
    int count = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            count ++;
        }
    }
    return count;
}

//Count the sentences
int sentences(string text)
{
    int count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            count ++;
        }
    }
    return count;
}