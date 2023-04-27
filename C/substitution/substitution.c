#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int validation(string x);  //Declaring validation
void encipher(string x, string y); //Declaring enchipher

int main(int argc, string argv[])
{
    string plaintext;
    if (argc != 2) //checking parameter
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    if (validation(argv[1]) == 0)
    {
        plaintext = get_string("plaintext: "); //get the plain text
    }
    else
    {
        return 1;
    }
    encipher(argv[1], plaintext); //calling the enchipher function
    return 0;
}
void encipher(string x, string y)
{
    string abc = "abcdefghijklmnopqrstuvwxyz"; //lowercase alphabet
    string ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; //uppercase alphabet
    printf("ciphertext: ");
    for (int i = 0; i < strlen(y); i++)
    {
        for (int j = 0; j < strlen(x); j ++)
        {
            if (isalpha(y[i])) //if it's a diggit
            {
                if (y[i] == ABC[j]) //if it's uppercase
                {
                    printf("%c", toupper(x[j]));
                }
                else if (y[i] == abc[j]) //if it's lowercase
                {
                    printf("%c", tolower(x[j]));
                }
            }
            else
            {
                printf("%c", y[i]); //print nondigits
                break;
            }
        }
    }
    printf("\n");
}
int validation(string x)
{
    bool checknumber = false; //boolean value to identify digits
    bool checkdupletter = false; //boolean value to identify duplicates
    for (int i = 0; i < strlen(x); i++)
    {
        if (isdigit(x[i]))
        {
            checknumber = true; //case a digit, will give true
            break;
        }
    }
    for (int i = 0; i < strlen(x); i++)
    {
        for (int j = 0; j < strlen(x); j++)
        {
            if (x[i] == x[j] && i != j)
            {
                checkdupletter = true; //case a duplicate, will give true
            }
        }
    }
    if (checknumber) //check the digit
    {
        printf("Key must only contain alphabetic characters.\n");
        return 1;
    }
    else if (strlen(x) != 26) //check the length
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    else if (checkdupletter) //check the duplicate
    {
        printf("Key must not contain repeated characters.\n");
        return 1;
    }
    else
    {
        return 0;
    }
}

