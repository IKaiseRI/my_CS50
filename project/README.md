# DISH MANAGER
### Video Demo:  <https://youtu.be/vs2p-poqQZ0>
## Description:

This is a simple web application developed in educational purpose

### What is this app?

Dish Manager is a web aplication where you can manage your foot stocks.
Basing on the food stocks that you have you can create your own recepies that can further be added to a menue.
In order to have a better looks on the dishes that you create and menues that you would like to use in your daylife, the aplication
supports images and the nutrient qualityes of the ingredients.

### Who can use it?

It can be used by anybody who wants to know what is the actual status of the stocks that he has at home and to create a daily or weekely menue directly from the aplication.

---
## Implementation

### Technologies
- Python
- HTML
- CSS
- JS
- Jinja
- Flask framework

### Components

The aplication consists of the following files and folders:
- file [app.py](app.py)
- folder static
    - [styles.css](styles.css)
    - images
- folder templates
    - HTML files
- folder flask_session
- file [project.db](project.db)
    - dishes table
    - groceryStock table
    - ingredients table
    - menues table
    - users table


---
### 1. File [app.py](app.py)

This is the core file that contains the whole logic of the aplication.
It contains all functions and rendering requests.

### 2. Folder [static](static)

As by default development rules it contains the [styles.css](styles.css) CSS file and for my aplication it is the folder where all uploaded images are stored.
The folder does not contain any script file for JS as they were used __directly in the HTML file__ where was needed.

### 3. Folder [templates](templates)

As by default development rules it contains all HTML files that are being used in the aplication.

### 4. Folder [Flask_session](Flask_session)

Contains users sessions

### 5. File [project.db](project.db)
####    - dishes table contains all information about dishes : (id, name, user_id, ingredients, weight, quantity).
####    - groceryStock table contains all products that are present in users account and the expiration date of the product : (name, quantity, weight, user_id, id).
####    - ingredients table contains all products that were inserted by all users. This way the table of the total products will increase fast and users will have acces to a larger amount of products : (id, name, carbohydrates, proteins, fats, calories)
####    - menues table contains all menues that a user created, in fact the menus are a compilation of dishes : (id, name, dish_total, user_id).
####    - users table contains all information about users : (id, username, hash)


---


## Why the aplication is needed ?

It is needed for simpler monitoring of products and to simplify the decision of cooking. When you already have a menu for the whole day or even for the whole week, you already know what you will cook in the evening or tomorrow.

## Who will need the application ?
It can be used by anyone, from the average person who wants to be able to streamline their diet and be able to easily monitor the food they have at home, to the restaurant manager who needs to always know what is and what is not in stock.

---

## Improvements

As this is a Demo application, it can be improved with numerous features:
- Categorisation of products;
- Extend the number of available products;
- Interactive stylization;
- Calculation of the total nutrition quantities in one dish and in one menu etc;



