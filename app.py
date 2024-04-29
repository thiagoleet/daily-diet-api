from flask import Flask, jsonify, request
from database import db
from models.meal import Meal

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet"

db.init_app(app=app)


def is_meal_valid(meal):
    return "name" in meal and "description" in meal and "date_time" in meal and "is_diet" in meal


@app.route("/meals", methods=["POST"])
def register_meal():
    data = request.get_json()
    if (is_meal_valid(data)):
        meal = Meal(data["name"], data["description"],
                    data["date_time"], data["is_diet"])
        db.session.add(meal)
        db.session.commit()
        return jsonify({"message": "Refeição registrada com sucesso!"}), 201
    else:
        return jsonify({"message": "Dados inválidos!"}), 400


@app.route("/meals", methods=["GET"])
def get_meals():
    meals = Meal.query.all()
    return jsonify({"meals": [meal.to_dict() for meal in meals], "total": len(meals)}), 200


@app.route("/meals/<int:meal_id>", methods=["GET"])
def get_meal(meal_id):
    meal = Meal.query.get(meal_id)
    if meal:
        return jsonify(meal.to_dict()), 200
    else:
        return jsonify({"message": "Refeição não encontrada!"}), 404


@app.route("/meals/<int:meal_id>", methods=["PUT"])
def update_meal(meal_id):
    data = request.get_json()

    if not is_meal_valid(data):
        return jsonify({"message": "Dados inválidos!"}), 400

    meal = Meal.query.get(meal_id)
    if meal:
        meal.name = data["name"]
        meal.description = data["description"]
        meal.date_time = data["date_time"]
        meal.is_diet = data["is_diet"]
        db.session.commit()
        return jsonify({"message": "Refeição atualizada com sucesso!"}), 202
    else:
        return jsonify({"message": "Refeição não encontrada!"}), 404


@app.route("/meals/<int:meal_id>", methods=["DELETE"])
def delete_meal(meal_id):
    meal = Meal.query.get(meal_id)
    if meal:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message:": f"Refeição {meal_id} removida com sucesso!"}), 202
    else:
        return jsonify({"message": "Refeição não encontrada!"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=3000)
