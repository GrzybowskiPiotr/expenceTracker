import os
from flask import Flask, flash, redirect, render_template, request, session
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route("/")
def index():
  return render_template("index.html")
@app.route("/test_db")
def test_db():
  try:
    result1 = db.session.execute(text("SELECT 1 AS value;"))
    print([dict(row._mapping) for row in result1])
    return "ok"
    # return {"db" : "ok", "result": [r for r in result_list]}
  except Exception as e:
    return {"db" : "error", "message": str(e)}

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)