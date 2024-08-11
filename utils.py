from pymongo import MongoClient
from models import db
from config.database import Config
import fitz  # PyMuPDF

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

def save_raw_text_to_file(text, output_path):
    with open(output_path, "w") as file: 
        file.write(text)

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    text = ""

    # Extract text from each page
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()

    return text