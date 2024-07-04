from flask import Flask, jsonify, redirect, render_template, request, url_for
from bson import ObjectId
from pymongo import MongoClient

# MongoDB connection URI
MONGO_URI = 'mongodb://localhost:27017/'

# Create a Flask app
app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.get_database('internship')
collection = db['test']

@app.route('/')
def index():
    return render_template('index.html')

# Define a route to insert data into MongoDB
@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.get_json()
    result = collection.insert_one(data)
    return jsonify({'message': 'Data inserted successfully', 'id': str(result.inserted_id)}), 201

# Define a route to retrieve data from MongoDB
@app.route('/get', methods=['GET'])
def get_data():
    try:
        data = list(collection.find())
        # Convert ObjectId to string in each document
        for item in data:
            item['_id'] = str(item['_id'])  # Convert ObjectId to string
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/submit', methods=['POST'])
def submit():
    data = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'age': int(request.form.get('age')),
        'city': request.form.get('city')
    }
    # Insert data into MongoDB
    collection.insert_one(data)
    return redirect(url_for('index'))
# Run the app
if __name__ == '__main__':
    app.run(debug=True)   