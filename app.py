from flask import Flask, jsonify, request
from database import db
from models.meal import Meal

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet'

db.init_app(app=app)


@app.route('/meals', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    return jsonify({'meals': meals, 'total': len(meals)})


if __name__ == '__main__':
    app.run(debug=True, port=3000)
