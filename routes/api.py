from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from models import db
from bson import ObjectId

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return render_template('index.html')

@api.route('/insert', methods=['POST'])
def insert_data():
    data = request.get_json()
    result = db.collection.insert_one(data)
    return jsonify({'message': 'Data inserted successfully', 'id': str(result.inserted_id)}), 201

@api.route('/get', methods=['GET'])
def get_data():
    try:
        data = list(db.collection.find())
        for item in data:
            item['_id'] = str(item['_id'])
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/submit', methods=['POST'])
def submit():
    data = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'age': int(request.form.get('age')),
        'city': request.form.get('city')
    }
    db.collection.insert_one(data)
    return redirect(url_for('api.index'))