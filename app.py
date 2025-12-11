import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash
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

    user_id = session.get("user_id")

    if user_id:
       return render_template("dashboard.html")

    return render_template("index.html")

@app.route("/dashboard")
@login_required
def dashboard():
  return render_template("dashboard.html")


@app.route("/login", methods=["GET", "POST"])
def login():

  # Forget any user_id
  session.clear()

  if request.method == "GET":
    return render_template("login.html")

  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
      flash("Username and password are required!", "error")
      return redirect("/login")

    user_data_from_db = db.session.execute(text("SELECT * FROM users WHERE username = username"),{"username": username})

    user = [dict(row._mapping) for row in user_data_from_db]

#Ensure username exists and password is correct
    if len(user) != 1 or not check_password_hash(
            user[0]["hash"], request.form.get("password")
        ):
          flash("Invalid Username or Password!", "error")
          return redirect("/")

# Remember which user has logged in
    session["user_id"] = user[0]["id"]
    flash("Login sucessfull", "info")
  return redirect("/")

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
        existing_user = db.session.execute(
            text("SELECT * FROM users WHERE username = :username"),
            {"username": username}
        ).fetchone()

        if existing_user:
            flash("Username already taken!", "error")
            return redirect("/register")

        hash = generate_password_hash(password)

        # Insert new user into the database
        db.session.execute(
            text("INSERT INTO users (username, hash) VALUES (:username, :hash)"),
            {"username": username, "hash": hash}
        )
        db.session.commit()

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