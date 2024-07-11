from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from models import db
from bson import ObjectId
from flasgger import swag_from

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return render_template('index.html')

@api.route('/insert', methods=['POST'])
@swag_from("../swagger/insert.yaml")
def insert_data():
    data = request.get_json()
    result = db.collection.insert_one(data)
    return jsonify({'message': 'Data inserted successfully', 'id': str(result.inserted_id)}), 201

@api.route('/get', methods=['GET'])
@swag_from("../swagger/get.yaml")
def get_data():
    try:
        data = list(db.collection.find())
        for item in data:
            item['_id'] = str(item['_id'])
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/submit', methods=['POST'])
@swag_from("../swagger/submit.yaml")
def submit():
    data = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'age': int(request.form.get('age')),
        'city': request.form.get('city')
    }
    db.collection.insert_one(data)
    return redirect(url_for('api.index'))