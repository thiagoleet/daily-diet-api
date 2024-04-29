from database import db


class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    is_diet = db.Column(db.Boolean, nullable=True, default=True)

    def __init__(self, name, description, date_time, is_diet):
        self.name = name
        self.description = description
        self.date_time = date_time
        self.is_diet = is_diet
