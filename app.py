from flask import Flask
from config.database import Config
from flasgger import Swagger
from routes.api import api  # Make sure the import matches the actual file and blueprint name
from utils import UPLOAD_FOLDER
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'supersecretkey'

# Initialize Swagger
swagger = Swagger(app)

# Register blueprints
app.register_blueprint(api)  # Add URL prefix for clarity

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)