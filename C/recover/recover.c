#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    char name[8];  //pointer for name of the files
    int counter = 0; //counter for number of files
    BYTE buffer[512]; //buffer to store 512 bytes
    if (argc != 2) //if there are no arguments will fail
    {
        printf("Usage: ./recover IMAGE");
        return 1;
    }

    FILE *file = fopen(argv[1], "r"); //if there is no existent file will fail
    if (file == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }
    FILE *img = NULL; //created a new FILE
    while (fread(buffer, sizeof(BYTE), 512, file) == 512) //moving trhow the card as in your hint
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0) //checking header
        {
            if (counter == 0) //in case it's the first one
            {
                sprintf(name, "%03i.jpg", counter);
                img = fopen(name, "w");
                fwrite(buffer, sizeof(BYTE), 512, img);
                counter ++;
            }
            else if (counter > 0) // in case it's not the first one
            {
                fclose(img);
                sprintf(name, "%03i.jpg", counter);
                img = fopen(name, "w");
                fwrite(buffer, sizeof(BYTE), 512, img);
                counter ++;
            }
        }
        else if (counter > 0) //if the ching ended but no headers were found
        {
            fwrite(buffer, sizeof(BYTE), 512, img);
        }
    }
    //free the memory

    //close files
    fclose(img);
    fclose(file);
    return 0;
}