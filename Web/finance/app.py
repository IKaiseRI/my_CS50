import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    if request.method == "GET":
        user_stock_db = db.execute(
            "SELECT symbol, company, SUM(shares) AS shares, price, grand_total FROM transactions where user_id = ? and shares != 0 GROUP BY symbol", user_id)
        cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = cash_db[0]["cash"]

        return render_template("index.html", index_data=user_stock_db, cash=cash)
    else:
        date = datetime.datetime.now()
        user_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        actual_cash = user_cash[0]["cash"]
        if request.form["action"] == "funds":
            try:
                add_fund = float(request.form.get("add_funds"))
            except ValueError:
                return apology("Unacceptable amount")

            if not add_fund:
                return apology("No amount inserted")

            updated_cash = actual_cash + add_fund
            db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)
            flash("Done!")
            db.execute("INSERT INTO transactions (user_id, shares, price, grand_total, date, company) VALUES (?, ?, ?, ?, ?, ?)",
                       user_id, 0, add_fund, add_fund, date, "ADD FUNDS")

        elif request.form["action"] == "buy":
            try:
                shares = int(request.form.get("modify_shares"))
            except ValueError:
                return apology("Unacceptable number of shares")
            symbol = request.values.get("symbol")
            stock = lookup(symbol.upper())
            transaction_sum = shares * stock["price"]

            if actual_cash < transaction_sum:
                return apology("Not enough funds")
            else:
                updated_cash = actual_cash - transaction_sum
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, grand_total, date, company) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       user_id, stock["symbol"], shares, stock["price"], transaction_sum, date, stock["name"])

        elif request.form["action"] == "sell":
            try:
                shares = int(request.form.get("modify_shares"))
            except ValueError:
                return apology("Unacceptable number of shares")
            symbol = request.values.get("symbol")
            stock = lookup(symbol.upper())
            transaction_sum = shares * stock["price"]
            updated_cash = actual_cash + transaction_sum
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, grand_total, date, company) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       user_id, stock["symbol"], (-1)*shares, stock["price"], transaction_sum, date, stock["name"])

        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)
        flash("Done!")
        return redirect("/")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Unacceptable number of shares")
        # If data is not inserted
        if not symbol:
            return apology("No symbol inserted")

        stock = lookup(symbol.upper())

        if stock == None:
            return apology("A non valid Symbol")

        if shares < 0:
            return apology("Negative shares are not allowed")
        # Total amount
        transaction_sum = shares * stock["price"]
        # Cheking the amounts for the insession user
        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        actual_cash = user_cash[0]["cash"]
        # If available amount is not enough
        if actual_cash < transaction_sum:
            return apology("Not enough funds")
        else:
            updated_cash = actual_cash - transaction_sum
        # Update the DB
        date = datetime.datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, grand_total, date, company) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], shares, stock["price"], transaction_sum, date, stock["name"])

        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

        flash("Done!")

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    user_history_db = db.execute(
        "SELECT symbol, company, shares, price, grand_total, date FROM transactions where user_id = :id", id=user_id)

    return render_template("history.html", history=user_history_db)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("No symbol inserted")

        stock = lookup(symbol.upper())

        if stock == None:
            return apology("A non valid Symbol")

        return render_template("quoted.html", name=stock["name"], price=stock["price"], symbol=stock["symbol"])

    else:
        return render_template("quote.html")


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
            return apology("Please write your username")

        if not password:
            return apology("Please write your password")

        if not confirmation:
            return apology("Please confirm your password")

        if password != confirmation:
            return apology("Passwords don't match")

        # Create the hash
        hash = generate_password_hash(password)

        try:
            # Insert the new user
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("User already exists")

        session["user_id"] = new_user

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        # If data is not inserted
        if not symbol:
            return apology("No symbol inserted")

        stock = lookup(symbol.upper())

        if stock == None:
            return apology("A non valid Symbol")

        if shares < 0:
            return apology("Negative shares are not allowed")

        user_id = session["user_id"]
        user_shares = db.execute(
            "SELECT shares FROM transactions WHERE user_id=:id AND symbol=:symbol GROUP BY symbol", id=user_id, symbol=symbol)
        actual_shares = user_shares[0]["shares"]

        if shares > actual_shares:
            return apology("Not enough shares")

        # Total amount
        transaction_sum = shares * stock["price"]
        # Cheking the amounts for the insession user
        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        actual_cash = user_cash[0]["cash"]
        updated_cash = actual_cash + transaction_sum
        # Update the DB
        date = datetime.datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, grand_total, date) VALUES (?, ?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], (-1) * shares, stock["price"], transaction_sum, date)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

        flash("Done!")

        return redirect("/")

    else:
        user_id = session["user_id"]
        user_symbols = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = :id GROUP BY symbol HAVING SUM(shares) > 0", id=user_id)
        return render_template("sell.html", symbols=[row["symbol"] for row in user_symbols])


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":
        user_id = session["user_id"]
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        new_confirmation = request.form.get("new_confirmation")

        # Check if the fields are completed
        if not old_password:
            return apology("Please write your old password")

        if not new_password:
            return apology("Please write your new password")

        if not new_confirmation:
            return apology("Please confirm your new confirmation")

        if new_password != new_confirmation:
            return apology("New passwords don't match")

        new_hash = generate_password_hash(new_password)

        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, user_id)

        return redirect("/")

    else:
        return render_template("change.html")

