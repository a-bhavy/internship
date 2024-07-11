from flask import Flask
from pymongo import MongoClient
from config.database import Config
from models import db
from routes.api import api 
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize swagger
    swagger = Swagger(app)

    # Initialize MongoDB connection
    client = MongoClient(app.config['MONGO_URI'])
    db.init_app(client)

    # Register blueprints
    app.register_blueprint(api)

    return app

if __name__ == '__main__':
    app=create_app()
    app.run(debug=True)