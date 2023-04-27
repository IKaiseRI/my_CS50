import os
import datetime

from datetime import timedelta, date
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps

UPLOAD_FOLDER = '/workspaces/71149359/project/static/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    if request.method == "GET":
        return render_template("index.html")
    return redirect("/")

@app.route("/my_products", methods=["GET", "POST"])
@login_required
def my_products():
    user_id = session["user_id"]
    if request.method == "GET":
        products = db.execute("SELECT * FROM groceryStock where user_id = ?", user_id)
        return render_template("my_products.html", ingredients=products)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    """Get ingredient quote."""
    if request.method == "POST":
        name = request.form.get("name")
        carbohydrates = request.form.get("carbohydrates")
        proteins = request.form.get("proteins")
        fats = request.form.get("fats")
        calories = request.form.get("calories")

        if not name:
            flash("Oops you missed name field")
        if not carbohydrates:
            flash("Oops you missed carbs")
        if not proteins:
            flash("Oops you missed proteins")
        if not fats:
            flash("Oops you missed fats")
        if not calories:
            flash("Oops you missed calories")

        try:
            db.execute("INSERT INTO ingredients (name,carbohydrates,proteins,fats,calories) VALUES (?,?,?,?,?)",
                                    name, carbohydrates, proteins, fats, calories)
        except:
            flash("Product already exists")

        return render_template("add_product.html")

    else:
        return render_template("add_product.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Get the date from fields
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if the fields are completed
        if not username:
            flash("Please write your username")

        if not password:
            flash("Please write your password")

        if not confirmation:
            flash("Please confirm your password")

        if password != confirmation:
            flash("Passwords don't match")

        # Create the hash
        hash = generate_password_hash(password)

        try:
            # Insert the new user
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            flash("User already exists")

        session["user_id"] = new_user

        return redirect("/")

    else:
        return render_template("register.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/add_recipes", methods=["GET", "POST"])
@login_required
def recepies():
    user_id = session["user_id"]
    if request.method == "GET":
        ingredients_db = db.execute("SELECT * FROM ingredients")
        return render_template("add_recipes.html", ingredients=ingredients_db)
    else:
        dish_ingredients_id = request.form.getlist("check")
        name = request.form.get("recipe")
        if not name:
            flash("Please name your dish")

        if not dish_ingredients_id:
            flash("Please select some ingredients")

        ing = [str(i) for i in dish_ingredients_id]
        res = " ".join(ing)
        ids = []
        db.execute("INSERT INTO dishes (name,ingredients,user_id) VALUES (?,?,?)", name, res, user_id)
        for i in dish_ingredients_id:
            ids.append(int(i))
        dish_ingredients = db.execute("SELECT * FROM ingredients WHERE id in (?)", ids)
        dish_id = db.execute("SELECT id FROM dishes WHERE name = ? and ingredients in (?) and user_id = ?", name, res, user_id)
        return render_template("recipes_quantities.html", dish_name=name, ingredients = dish_ingredients, dish_id=dish_id)



@app.route("/recipes_quantities", methods=["GET", "POST"])
@login_required
def recipes_quantities():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        name = request.values.get("dish")
        quantity = request.form.getlist("quantity")
        weight = request.form.getlist("weight")
        total_q = " ".join(quantity)
        total_w = " ".join(weight)
        db.execute("UPDATE dishes SET weight = ?, quantity = ? where name = ?", total_w, total_q, name)
        return redirect("add_recipes")


@app.route("/my_recipes", methods=["GET", "POST"])
@login_required
def my_recipes():
    user_id = session["user_id"]
    recipes_db=db.execute("SELECT name, id FROM dishes")
    recipes_id_db=db.execute("SELECT ingredients FROM dishes")
    recipes_q_db=db.execute("SELECT quantity FROM dishes")
    recipes_we_db=db.execute("SELECT weight FROM dishes")
    stoks_db=db.execute("SELECT * FROM groceryStock where user_id = ?", user_id)

        #Converting text weights into Int weights
    total_we_list = []
    for i in recipes_we_db:
        list_values = list(i.values())
        total_we_list.append(list_values)

    total_we_integers = []
    for lists in total_we_list:
        for elements in lists:
            x = elements.split()
            integers = [int(val) for val in x]
            total_we_integers.append(integers)

        #Converting text IDs into Int IDs
    total_id_list = []
    for i in recipes_id_db:
        list_values = list(i.values())
        total_id_list.append(list_values)

    total_id_integers = []
    for lists in total_id_list:
        for elements in lists:
            x = elements.split()
            integers = [int(val) for val in x]
            total_id_integers.append(integers)

        #Converting text Quant into Int Quant
    total_q_list = []
    for i in recipes_q_db:
        list_values = list(i.values())
        total_q_list.append(list_values)

    total_q_integers = []
    for lists in total_q_list:
        for elements in lists:
            x = elements.split()
            integers = [int(val) for val in x]
            total_q_integers.append(integers)

        #Updating data to the table
    total_ingredients = []
    for i in total_id_integers:
        ingredients_line=db.execute("SELECT name as ingredient FROM ingredients where id in (?)", i)
        total_ingredients.append(ingredients_line)

    qianities_totals = []
    for i in range(len(total_id_integers)):
        ingredients_line[i]=db.execute("SELECT name as ingredient FROM ingredients where id in (?)", total_id_integers[i])
        total_ingredients[i]=db.execute("SELECT id FROM ingredients where id in (?)", total_id_integers[i])
        for j in range(len(ingredients_line[i])):
            ingredients_line[i][j].update({"quantity": total_q_integers[i][j]})
            ingredients_line[i][j].update({"weight": total_we_integers[i][j]})
            ingredients_line[i][j].update({"id": total_id_integers[i][j]})
            for y in range(len(stoks_db)):
                if total_ingredients[i][j]["id"] == stoks_db[y]["id"]:
                    ingredients_line[i][j].update({"qstock": stoks_db[y]["quantity"]})
                    ingredients_line[i][j].update({"wstock": stoks_db[y]["weight"]})
        qianities_totals.append(ingredients_line[i])

        #Inserting the name into tables
    ingredients_qianities_totals = []
    counter = 0
    for i in qianities_totals:
        i.insert(0,recipes_db[counter])
        counter += 1
        ingredients_qianities_totals.append(i)

    if request.method == "GET":
        return render_template("my_recipes.html", dishes=ingredients_qianities_totals)

    else:
        if request.form["action"] == "add":
            menue = request.form.get("menue")
            ids = request.form.getlist("check")
            ing = [str(i) for i in ids]
            res = " ".join(ing)
            db.execute("INSERT INTO menues (name,dish_total,user_id) VALUES(?,?,?)", menue, res, user_id)
            return redirect("my_recipes")

        elif request.form["action"] == "prepare":
            check = request.form.get("check")

            id = 0
            if check is None:
                flash("Choose a dish first")
            else:
                id = int(check)

            dish = []
            for i in ingredients_qianities_totals:
                for j in i:
                    if id == j["id"]:
                        dish = i
            counter = 0
            for i in range(len(dish)):
                if dish[i].get("ingredient") is not None:
                    if dish[i].get("qstock") is None and dish[i].get("wstock") is  None:
                        counter += 1

            if counter != 0:
                flash("You don't have enough stock")

            for i in range(len(dish)):
                if dish[i].get("ingredient") is not None:
                    if (dish[i].get("qstock") - dish[i].get("quantity")) == 0 and (dish[i].get("wstock") - dish[i].get("weight")) != 0:
                        quant = 1
                        db.execute("UPDATE groceryStock SET quantity=?, weight=? where user_id = ? and id = ?",
                        quant, dish[i].get("wstock") - dish[i].get("weight"), user_id, dish[i].get("id"))
                    else:
                        db.execute("UPDATE groceryStock SET quantity=?, weight=? where user_id = ? and id = ?",
                        dish[i].get("qstock") - dish[i].get("quantity"), dish[i].get("wstock") - dish[i].get("weight"), user_id, dish[i].get("id"))

            return redirect("my_recipes")


@app.route("/my_menues", methods=["GET", "POST"])
@login_required
def my_menues():
    user_id = session["user_id"]
    if request.method == "GET":
        names = db.execute("SELECT name as Menu FROM menues WHERE user_id = ?", user_id)
        manue_dishes = db.execute("SELECT dish_total FROM menues WHERE user_id = ?", user_id)

        total_dish_list = []
        for i in manue_dishes:
            list_values = list(i.values())
            total_dish_list.append(list_values)

        total_dish_integers = []
        for lists in total_dish_list:
            for elements in lists:
                x = elements.split()
                integers = [int(val) for val in x]
                total_dish_integers.append(integers)

        total_dishes = []
        for i in total_dish_integers:
            dish_names=db.execute("SELECT name from dishes WHERE id in (?)", i)
            total_dishes.append(dish_names)

        total_menue = []
        counter = 0
        for i in total_dishes:
            i.insert(0,names[counter])
            counter += 1
            total_menue.append(i)

        return render_template("my_menues.html", menues=total_menue)

    return redirect("my_menues")

@app.route("/search_products", methods=["GET", "POST"])
@login_required
def search_products():
    user_id = session["user_id"]
    if request.method == "GET":
        ingredients_db = db.execute("SELECT * FROM ingredients")
        return render_template("search_products.html", ingredients=ingredients_db)
    if request.method == "POST":
        if request.form["action"] == "add":
            name = request.values.get("check")
            quantity = request.form.get("quantity")
            weight = request.form.get("weight")
            exp_days = int(request.form.get("days"))
            id_db = db.execute("SELECT id FROM ingredients where name = ?", name)
            date = datetime.date.today()
            exp_date = date + timedelta(days=exp_days)
            if not quantity:
                quantity = 1

            if not weight:
                flash("Please insert the weight")
            id = 0
            for i in id_db:
                id = list(i.values())

            db.execute("INSERT INTO groceryStock (id,name,expire,quantity,weight,user_id) VALUES (?,?,?,?,?,?)", id ,name, exp_date, quantity, weight, user_id)

        elif request.form["action"] == "delete":
            name = request.values.get("check")
            db.execute("DELETE FROM ingredients where name = ?", name)

        elif request.form["action"] == "edit":
            name = request.values.get("check")
            edit_db = db.execute("SELECT * FROM ingredients where name = ?", name)
            return render_template("edit_product.html", db=edit_db)


    return redirect("search_products")

@app.route("/edit_product", methods=["GET", "POST"])
@login_required
def edit_product():
    if request.method == "POST":
        name = request.form.get("name")
        modify_name = request.form.get("modify_name")
        carbohydrates = request.form.get("carbohydrates")
        proteins = request.form.get("proteins")
        fats = request.form.get("fats")
        calories = request.form.get("calories")

        if not name:
            flash("Oops you missed name field")
        if not carbohydrates:
            flash("Oops you missed carbs")
        if not proteins:
            flash("Oops you missed proteins")
        if not fats:
            flash("Oops you missed fats")
        if not calories:
            flash("Oops you missed calories")
        db.execute("UPDATE ingredients SET name=?, carbohydrates=?, proteins=?, fats=?, calories=? where name=?", name, carbohydrates, proteins, fats, calories, modify_name)

    else:
        return render_template("register.html")

    return redirect("search_products")



@app.route("/products", methods=["GET", "POST"])
@login_required
def products():
    q = request.args.get("q")
    if q:
        ingredients_db = db.execute("SELECT * FROM ingredients where name LIKE ?", "%" + q + "%")
    else:
        ingredients_db = ingredients_db = db.execute("SELECT * FROM ingredients")
    return render_template("products.html", ingredients=ingredients_db)


@app.route("/own_products", methods=["GET", "POST"])
@login_required
def own_products():
    q = request.args.get("q")
    if q:
        ingredients_db = db.execute("SELECT * FROM groceryStock where name LIKE ?", "%" + q + "%")
    else:
        ingredients_db = ingredients_db = db.execute("SELECT * FROM groceryStock")
    return render_template("own_products.html", ingredients=ingredients_db)
