from app import db, app
from sqlalchemy import text

mock_categories =[
  ("Food", "Groceries, restaurants, snacks"),
  ("Transport", "Fuel, public transport, taxi"),
  ("Bills", "Electricity, water, internet"),
  ("Entertainment", "Cinema, games, trips"),
  ("Health", "Medications, doctors"),
]
with app.app_context():
  for name, description in mock_categories:
    db.session.execute(text("INSERT INTO categories (name, description) VALUES (:name, :description)"), {"name" : name, "description": description})

    db.session.commit()

print("Categories seeded.")