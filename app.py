from flask import Flask, jsonify, request
from database import db
from models.meal import Meal

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet'

db.init_app(app=app)


def is_meal_valid(meal):
    return 'name' in meal and 'description' in meal and 'date_time' in meal and 'is_diet' in meal


@app.route('/meals', methods=['POST'])
def register_meal():
    data = request.get_json()
    if (is_meal_valid(data)):
        meal = Meal(data['name'], data['description'],
                    data['date_time'], data['is_diet'])
        db.session.add(meal)
        db.session.commit()
        return jsonify({'message': 'Refeição registrada com sucesso!'}), 200
    else:
        return jsonify({'message': 'Dados inválidos!'}), 400


@app.route('/meals', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    return jsonify({'meals': [meal.to_dict() for meal in meals], 'total': len(meals)}), 200


if __name__ == '__main__':
    app.run(debug=True, port=3000)
