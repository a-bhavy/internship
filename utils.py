from pymongo import MongoClient
from models import db
from config.database import Config

# Use the MONGO_URI attribute
mongo_uri = Config.MONGO_URI

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_to_mongodb(parsed_resume):
    client = MongoClient(mongo_uri)  # Connect to MongoDB
    db.init_app(client)
    db.collection.insert_one(parsed_resume)  # Insert the document
