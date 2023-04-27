#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float gray;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j ++)
        {
            gray = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.00);
            image[i][j].rgbtRed = gray;
            image[i][j].rgbtGreen = gray;
            image[i][j].rgbtBlue = gray;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int *temp = malloc(3 * sizeof(int));
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            temp[0] = image[i][j].rgbtBlue;
            temp[1] = image[i][j].rgbtGreen;
            temp[2] = image[i][j].rgbtRed;

            image[i][j].rgbtBlue = image[i][width - j - 1].rgbtBlue;
            image[i][j].rgbtGreen = image[i][width - j - 1].rgbtGreen;
            image[i][j].rgbtRed = image[i][width - j - 1].rgbtRed;

            image[i][width - j - 1].rgbtBlue = temp[0];
            image[i][width - j - 1].rgbtGreen = temp[1];
            image[i][width - j - 1].rgbtRed = temp[2];
        }
    }
    free(temp);
    return;
}
//additional function that will be calculating the average of R G B
int average_blur(int i, int j, int rgb, int height, int width, RGBTRIPLE image[height][width])
{
    int sum = 0;
    float count = 0;
    for (int x = i - 1; x < i + 2; x++)
    {
        for (int y = j - 1; y < j + 2; y++)
        {
            if (x < 0 || y < 0 || x >= height || y >= width)
            {
                continue; // continue if the pixel is out of the image
            }

            if (rgb == 0)
            {
                sum += image[x][y].rgbtRed; //sum of red
            }
            else if (rgb == 1)
            {
                sum += image[x][y].rgbtGreen; //sum of green
            }
            else if (rgb == 2)
            {
                sum += image[x][y].rgbtBlue; //sum of blue
            }
            count ++;
        }
    }
    //return the average
    return round(sum / count);
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE duplicate[height][width]; //a duplicate image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            duplicate[i][j] = image[i][j];
        }
    }
    //updating the output
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = average_blur(i, j, 0, height, width, duplicate);
            image[i][j].rgbtGreen = average_blur(i, j, 1, height, width, duplicate);
            image[i][j].rgbtBlue = average_blur(i, j, 2, height, width, duplicate);
        }
    }
    return;
}

int boarders(int i, int j, int rgb, int height, int width, RGBTRIPLE image[height][width])
{
    float sumX = 0;
    float sumY = 0;
    int coeficient = 0;
    // Gx and GY
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int k = i - 1, x = 0; k < i + 2; k++, x++)
    {
        for (int l = j - 1, y = 0; l < j + 2; l++, y++)
        {
            if (k < 0 || l < 0 || k >= height || l >= width)
            {
                continue; // continue if the pixel is out of the image
            }
            if (rgb == 0)
            {
                //sum of red
                sumX += image[k][l].rgbtRed * gx[x][y];
                sumY += image[k][l].rgbtRed * gy[x][y];
            }
            else if (rgb == 1)
            {
                //sum of Green
                sumX += image[k][l].rgbtGreen * gx[x][y];
                sumY += image[k][l].rgbtGreen * gy[x][y];
            }
            else if (rgb == 2)
            {
                //sum of Blue
                sumX += image[k][l].rgbtBlue * gx[x][y];
                sumY += image[k][l].rgbtBlue * gy[x][y];
            }

        }
    }

    //calcutating the formula of Gx^2 + Gy^2
    coeficient = round(sqrt((sumX * sumX) + (sumY * sumY)));

    return coeficient < 255 ? coeficient : 255;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE duplicate[height][width]; //a duplicate image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            duplicate[i][j] = image[i][j];
        }
    }
    //updating the output
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = boarders(i, j, 0, height, width, duplicate);
            image[i][j].rgbtGreen = boarders(i, j, 1, height, width, duplicate);
            image[i][j].rgbtBlue = boarders(i, j, 2, height, width, duplicate);
        }
    }
    return;
}
