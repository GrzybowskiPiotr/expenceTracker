import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
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

    if session.get("user_id"):
       return redirect("/dashboard")

    return render_template("index.html")

@app.route("/dashboard")
@login_required
def dashboard():

    user_id = session.get("user_id")

    row = db.session.execute(text("SELECT * FROM users WHERE id = :id"),{"id": user_id}).fetchone()

    username = row._mapping["username"].capitalize()

    totalSpend = db.session.execute(text("SELECT SUM(amount) FROM expenses WHERE user_id = :id"),{"id":user_id}).scalar() or 0
    transactionsCount = db.session.execute(text("SELECT COUNT(*) FROM expenses WHERE user_id = :id"),{"id":user_id}).scalar() or 0

    sumPerCat = db.session.execute(text("SELECT SUM(ex.amount) as sum, cat.name as name FROM expenses as ex JOIN categories as cat ON ex.category_id = cat.id WHERE user_id = :id GROUP BY cat.name"), {"id":user_id}).mappings().all()

    return render_template("dashboard.html", user=username, totalSpend=totalSpend, transactionsCount=transactionsCount, sumPerCat=sumPerCat)

@app.route("/login", methods=["GET", "POST"])
def login():

  # Forget any user_id


  if request.method == "GET":
    return render_template("login.html")

  if request.method == "POST":
    session.clear()
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
      flash("Username and password are required!", "danger")
      return redirect("/login")

    user_data_from_db = db.session.execute(text("SELECT * FROM users WHERE username = :username"),{"username": username}).fetchone()

    if user_data_from_db is None:
        flash("Invalid Username or Password!", "danger")
        return redirect("/login")

    user = user_data_from_db._mapping

    if not check_password_hash(user["hash"], password):
        flash("Invalid Username or Password!", "danger")
        return redirect("/login")

# Remember which user has logged in
    session["user_id"] = user["id"]
    flash("Login sucessfull", "success")
  return redirect("/dashboard")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("Username is required!", "danger")
            return redirect("/register")

        if not password:
            flash("Password is required!", "danger")
            return redirect("/register")

        if password != confirmation:
            flash("Passwords do not match!", "danger")
            return redirect("/register")

        # Check if username already exists
        existing_user = db.session.execute(
            text("SELECT * FROM users WHERE username = :username"),
            {"username": username}
        ).fetchone()

        if existing_user:
            flash("Username already taken!", "danger")
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

@app.route("/add_expense", methods=["GET", "POST"])
@login_required
def add_expense():
    categories = db.session.execute(text("SELECT * FROM categories")).fetchall()
    if request.method == "GET":
        return render_template("/add_expense.html", categories=categories)

    if request.method == "POST":
        user_id = session.get("user_id")
        amount = request.form.get("amount")
        category = request.form.get("category")
        description = request.form.get("description")

        if category != "0":
            try:
                category = int(category)
            except ValueError:
                flash("Select valid category for expense", "info")
                return redirect("/add_expense")
            avalable_categories = [cat.id for cat in categories]

            if category not in avalable_categories:
                flash("Select valid category for expense", "info")
                return redirect("/add_expense")
        try:
            amount = float(amount)
        except ValueError:
            flash("amount must by a valid number", "danger")
            return redirect("/add_expense")

        if amount <= 0:
                flash("Please proveide amout of expense and select category!", "danger")
                return redirect("/add_expense")
        else:

            db.session.execute(text("INSERT INTO expenses (amount, category_id, description, user_id) VALUES(:amount, :category, :description, :user_id)"),{"amount": amount, "category": category, "description":description, "user_id": user_id})
            db.session.commit()

        flash("Expense added", "success")
    return  redirect("/history")

@app.route("/delete/<int:expense_id>", methods=["POST"])
@login_required
def delete_expense(expense_id):

    if request.method == "POST":
        user_id = session.get("user_id")

        # check if expence id exsists in DB

        id_exsists = db.session.execute(text("SELECT id FROM expenses WHERE id = :id AND user_id = :user_id"), {"id": expense_id, "user_id": user_id}).fetchone()

        if id_exsists is None:
            flash("Expense don't exsists", "danger")
            return redirect("/history")
        else:
            db.session.execute(text("DELETE FROM expenses WHERE user_id = :user_id AND id = :id"), {"user_id": user_id, "id": expense_id})
            db.session.commit()
            flash("Expence deleted !","success")
            return redirect("/history")

    return redirect("/history")


@app.route("/history")
@login_required
def history():
    user_id = session.get("user_id")
    category_id = request.args.get("category_id", type=int)
    categories = db.session.execute(text("SELECT * FROM categories")).mappings().all()
    selected_category = 0
    if category_id:
        history_data = db.session.execute(text("SELECT cat.name as category, ex.amount as cost, ex.description as description, ex.created_at as date, ex.id as id FROM expenses as ex JOIN categories as cat on cat.id = ex.category_id WHERE user_id = :user_id AND cat.id = :category_id ORDER BY created_at DESC"),{"user_id":user_id, "category_id": category_id}).mappings().all()
    else:

        history_data = db.session.execute(text("SELECT cat.name as category, ex.amount as cost, ex.description as description, ex.created_at as date, ex.id as id FROM expenses as ex JOIN categories as cat on cat.id = ex.category_id WHERE user_id = :user_id ORDER BY created_at DESC"),{"user_id":user_id}).mappings().all()

    return render_template("/history.html", history=history_data, categories=categories, selected_category=category_id)

@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
@login_required
def edit(expense_id):
    user_id = session.get("user_id")
    expence_data = db.session.execute(text("SELECT id, amount, description, created_at, category_id FROM expenses as exp WHERE id = :expense_id AND user_id = :user_id" ), {"expense_id" : expense_id, "user_id" : user_id}).mappings().first()
    categories = db.session.execute(text("SELECT id, name FROM categories as cat")).mappings().all()

    if expence_data is None:
        flash("Expense not found", "danger")
        return redirect("/history")


    if request.method == "GET":
        return render_template("edit.html" , expence_data=expence_data, categories=categories)

    if request.method == "POST":
        user_id = session.get("user_id")
        amount = request.form.get("amount")
        category = request.form.get("category")
        description = request.form.get("description")

        if category != "0":
            try:
                category = int(category)
            except ValueError:
                flash("Select valid category for expense", "warning")
                return redirect(url_for("edit", expense_id=expense_id))
            avalable_categories = [cat["id"] for cat in categories]
            print(avalable_categories)

            if category not in avalable_categories:
                flash("Select valid category for expense", "warning")
                return redirect(url_for("edit", expense_id=expense_id))
        try:
            amount = float(amount)
        except ValueError:
            flash("amount must by a valid number", "danger")
            return redirect(url_for("edit", expense_id=expense_id))

        if amount <= 0:
                flash("Please proveide amout of expense and select category!", "danger")
                return redirect(url_for("edit", expense_id=expense_id))
        else:
            print(category)
            result = db.session.execute(text("UPDATE expenses SET amount = :amount, category_id = :category, description = :description WHERE user_id = :user_id AND id = :expense_id"),{"amount": amount, "category": category, "description":description, "user_id": user_id, "expense_id": expense_id})
            db.session.commit()

            if result.rowcount == 0:
                flash("Nothing was updated", "warning")

        flash("Expense modified", "success")
        return redirect("/history")

    return redirect("/history")

@app.route("/categories")
@login_required
def categories():

    categories_usage = db.session.execute(text("SELECT COUNT(exp.id) as usage, cat.name, cat.description,cat.id FROM categories as cat LEFT JOIN expenses as exp ON cat.id = exp.category_id GROUP BY cat.id ORDER BY cat.name")).mappings().all()


    return render_template("categories_overview.html", categories_usage=categories_usage)

@app.route("/categories/add", methods =["GET", "POST"])
@login_required
def categories_add():

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        if not name:
            flash("Category name is reuired!", "danger")
            return redirect("/categories/add")

        # wpis do bazy

        db.session.execute(
            text(
                "INSERT INTO categories (name, description) VALUES (:name, :description)"
            ),
            {"name": name, "description": description},
        )
        db.session.commit()

        flash("New category added", "success")
        return redirect("/categories")

    return render_template("categories_form.html",mode="add", action_url="/categories/add", category=None)

@app.route("/categories/edit/<int:id>", methods =["GET", "POST"])
@login_required
def categories_edit(id):

    if request.method == "GET":
        print("get request")

    category = db.session.execute(
        text("SELECT id, name, description FROM categories WHERE id = :id"),
        {"id": id},
    ).mappings().one_or_none()

    if not category:
        flash("Category not found", "danger")
        return redirect("/categories")

    if request.method == "POST":
        print("POST reqest")
        name = request.form.get("name")
        description = request.form.get("description")

        if not name:
            flash("Category name is required", "danger")
            return redirect(f"/categories/edit/{id}")

        db.session.execute(
            text(
                """
                UPDATE categories
                SET name = :name, description = :description
                WHERE id = :id
                """
            ),
            {"name": name, "description": description, "id": id},
        )
        db.session.commit()

        flash("Category updated", "success")
        return redirect("/categories")

    return render_template("categories_form.html",
        mode="edit",
        action_url=f"/categories/edit/{id}",
        category=category,)

@app.route("/categories/delete/<int:id>", methods=["POST"])
@login_required
def categories_delete(id):
        usage = db.session.execute(text("SELECT COUNT(*) FROM expenses WHERE category_id = :id"), {"id":id}).scalar()

        if usage > 0 :
            flash("Category can't be in use.", "danger")
            return redirect("/categories")
        else:

            delete_result = db.session.execute(text("""DELETE FROM categories WHERE id = :id AND NOT EXISTS (SELECT 1 FROM expenses WHERE category_id = :id)"""), {"id": id})

            if delete_result.rowcount == 1:
                db.session.commit()
                flash("Catgory delete successfully.", "success")
            else:
                db.session.rollback()
                flash("Category not found or already deleted.", "warning")
        return redirect("/categories")



@app.route("/account_settings", methods = ["GET", "POST"])
@login_required
def account_settings():

    user_id = session.get("user_id")
    user = db.session.execute(text("SELECT username FROM users WHERE id = :id"), {"id": user_id}).mappings().one()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("Username is required!", "danger")
            return redirect("/account_settings")
        elif username != user["username"]:
            db.session.execute(text("UPDATE users SET username = :username WHERE id = :id"), {"username": username, "id": user_id})


        if password and not confirmation:
            flash("Confirmation of new password is required", "danger")
            return redirect("/account_settings")

        if password != "":
            if password != confirmation:
                flash("Passwords and confirmation do not match!", "danger")
                return redirect("/account_settings")
            else:
                pass_has = generate_password_hash(password)
                db.session.execute(text("UPDATE users SET hash = :hash WHERE id = :id"), {"id": user_id, "hash":pass_has })
        db.session.commit()
        flash("Account settings saved", "info")
        return redirect("/")

    return render_template("account_settings.html", user=user)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)