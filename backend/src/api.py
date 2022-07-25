import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()
# routes for all the functions

#to get menu of drinks avialable 
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in drinks]
    }), 200

#to get detail description of drinks 
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_detail(payload):
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    }), 200

#to a add a drink to the menu with its descriptions
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_a_drink(payload):

    drink_title = request.get_json()['title']
    drink_recipe = json.dumps(request.get_json()['recipe'])

    if not drink_title or not drink_recipe:
        abort(400)
    else:
        try:
            drink = Drink(title=drink_title, recipe=drink_recipe)
            drink.insert()
             
            return jsonify({
                "success": True,
                "drinks": drink.long()
            }), 200
        except BaseException:
            abort(422)

#to edit an already exsiting drink in the menu
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    req = request.get_json()
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if not drink:
        abort(404)

    try:
        drink_title = req.get('title')
        drink_recipe = req.get('recipe')
        if drink_title:
            drink.title = drink_title

        if drink_recipe:
            drink.recipe = json.dumps(req['recipe'])

        drink.update()
    except BaseException:
        abort(400)

    return jsonify({
        'success': True, 
        'drinks': [drink.long()]
    }), 200

#to delete a drink from the mune with its characteristics
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if not drink:
        abort(404)

    try:
        drink.delete()
    except BaseException:
        abort(400)

    return jsonify({
        'success': True, 
        'delete': id
    }), 200

# Error Handlers for task

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(409)
def duplicate(error):
    return jsonify({
        "success": False,
        "error": 409,
        "message": "conflict"
    }), 409


@app.errorhandler(404)
def not_found(error):
    return({
        "success": False,
        "message": "resource not found",
        "error": 404
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return({
        "success": False,
        "message": "bad request",
        "error": 400
    }), 400


@app.errorhandler(405)
def not_found(error):
    return (jsonify({"success": False, "error": 405,
                     "message": "method not allowed"}), 405)


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code