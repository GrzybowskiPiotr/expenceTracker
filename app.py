import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from helpers import login_required
load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "GET":
    return render_template("login.html")

  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
      flash("Username and password are required!", "error")
      return redirect("/login")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Log user in"""

#     # Forget any user_id
#     session.clear()

#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":
#         # Ensure username was submitted
#         if not request.form.get("username"):
#             return apology("must provide username", 403)

#         # Ensure password was submitted
#         elif not request.form.get("password"):
#             return apology("must provide password", 403)

#         # Query database for username
#         rows = db.execute(
#             "SELECT * FROM users WHERE username = ?", request.form.get("username")
#         )

#         # Ensure username exists and password is correct
#         if len(rows) != 1 or not check_password_hash(
#             rows[0]["hash"], request.form.get("password")
#         ):
#             return apology("invalid username and/or password", 403)

#         # Remember which user has logged in
#         session["user_id"] = rows[0]["id"]

#         # Redirect user to home page
#         return redirect("/")

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("Username is required!", "error")
            return redirect("/register")

        if not password:
            flash("Password is required!", "error")
            return redirect("/register")

        if password != confirmation:
            flash("Passwords do not match!", "error")
            return redirect("/register")

        # Check if username already exists
        # existing_user = db.execute(
        #     text("SELECT * FROM users WHERE username = :username"),
        #     {"username": username}
        # ).fetchone()

        # if existing_user:
        #     flash("Username already taken!", "error")
        #     return redirect("/register")

        # Insert new user into the database
        # db.execute(
        #     text("INSERT INTO users (username, hash) VALUES (:username, :hash)"),
        #     {"username": username, "hash": password}  # Hash the password in production
        # )
        # db.commit()

        flash("Registered successfully! Please log in.", "success")
        return redirect("/login")

    return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)