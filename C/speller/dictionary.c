// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <strings.h>
#include <string.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 65536;

//New variables
unsigned int word_count = 0;
unsigned int hash_value;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hash_word = hash(word);
    node *n = table[hash_word];

    while (n != NULL)
    {
        if (strcasecmp(n->word, word) == 0)
        {
            return true;
        }
        n = n->next;
    }
    return false;
}

// Hashes word to a number
// A modified Hash function djb2 by Dan Bernstein
// Link https://www.reddit.com/r/cs50/comments/eo4zro/good_hash_function_for_speller/
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;
    int c = *word;
    c = tolower(c);
    while (*word != 0)
    {
        hash = ((hash << 5) + hash) + c;
        c = *word++;
        c = tolower(c);
    }
    return hash % N;;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    //Open the file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    //Declare buffer variable word
    char *word = malloc((LENGTH + 1) * sizeof(char));

    //Scann the dictionary till the EOF
    while (fscanf(file, "%s", word) != EOF)
    {
        //Allocate memory for a node
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            fclose(file);
            free(word);
            return false;
        }

        //Copy the ford into node
        strcpy(n->word, word);
        n->next = NULL;

        hash_value = hash(word);
        if (table[hash_value] == NULL)
        {
            table[hash_value] = n;
        }
        else
        {
            n->next = table[hash_value];
            table[hash_value] = n;
        }

        word_count++;
    }
    fclose(file);
    free(word);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    if (word_count > 0)
    {
        return word_count;
    }
    return 0;
}

void freenode(node *n)
{
    if (n->next != NULL)
    {
        freenode(n->next);
    }
    free(n);
}
// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            freenode(table[i]);
        }
    }
    return true;
}

