#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

def to_dict():
    return{
    }
def find_restaurant_by_id(id):
    found_restaurant = Restaurant.query.where(Restaurant.id == id ).first()

    return found_restaurant

@app.get("/restaurants")
def get_all_restaurants():
    all_restaurants = Restaurant.query.all()
    
    try:

        return jsonify([restaurant.to_dict(rules= ('restaurant_pizzas',)) for restaurant in all_restaurants]), 200
    
    except Exception as e:
        print(f"Error retrieving restaurants: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    

@app.get("/restaurants/<int:id>")
def get_restaurant_by_id(id):
    found_restaurant = Restaurant.query.where(Restaurant.id == id ).first()

    
    if found_restaurant:
        return found_restaurant.to_dict(), 200
    else:
        return {"message": "Restaurant not found", "status": "404"}, 404

@app.delete("/restaurants/<int:id>")
def delete_restaurants_by_id(id):
    found_restaurant = find_restaurant_by_id(id)
    if found_restaurant:

        db.session.delete(found_restaurant)
        db.session.commit()

        return { "message": "successfull Deletion" },204

    else:
        return {"status": 404, "message":"Restaurant not found" }, 404


@app.get("/pizzas")
def get_pizzas():
    all_pizzas = Pizza.query.all()

    try:

        return jsonify([pizza.to_dict(rules=('restaurant_pizzas') ) for pizza in all_pizzas]), 200
    
    except Exception as e:
        print(f"Error retrieving restaurants: {e}")
        return jsonify({'error': 'Internal server error'}), 500



@app.post('/restaurant_pizzas')
def post_restaurants_pizzas():
    body = request.json

    try:
        new_restaurants_pizzas = RestaurantPizza(price= body.get('price'),
                                                 restaurant_id= body.get('restaurant_id'),
                                                 pizza_id= body.get('pizza_id'))

        db.session.add(new_restaurants_pizzas)
        db.session.commit()

        return new_restaurants_pizzas.to_dict(), 201
    
    
    except Exception as validation_error:
        return {
            "status": "400",
            "message": "something went wrong",
            "error_text": str(validation_error)
        }, 400
    

    


if __name__ == "__main__":
    app.run(port=5555, debug=True)
