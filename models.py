from app import db

class Users(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  hash = db.Column(db.String(255), nullable=False)

class Category(db.Model):
  __tablename__ = "categories"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False, unique=True)
  description = db.Column(db.String(255), nullable=True)

class Expense(db.Model):
  __tablename__ = "expenses"

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  amount = db.Column(db.Numeric(), nullable=False)
  description = db.Column(db.String(255), nullable=True)
  created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
  category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  category = db.relationship("Category", backref="expenses")
