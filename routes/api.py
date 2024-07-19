from flask import Blueprint, flash, redirect, jsonify, render_template, request
from models import db
from flasgger import swag_from
from werkzeug.utils import secure_filename
from resume_parser import parse_resume, save_to_file
from utils import UPLOAD_FOLDER, allowed_file, save_to_mongodb
import os

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return render_template("upload_form.html")

@api.route('/upload', methods=['POST'])
@swag_from("../swagger/upload.yaml")
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        parsed_resume = parse_resume(file_path)
        save_to_mongodb(parsed_resume)
        save_to_file(parsed_resume, output_path="output3.txt")

        result = {
            "name": parsed_resume['name'],
            "contact_info": parsed_resume['contact_info'],
            "education": parsed_resume['education'],
            "experience": parsed_resume['experience'],
            "skills": parsed_resume['skills']
        }

        # Check for 'response_type' query parameter to determine response format
        response_type = request.headers.get('Accept')
        # print(response_type)
        if response_type and 'application/json' in response_type:
            return jsonify(result)
        else:
            return render_template("parsed_resume.html", **result)
    else:
        flash('Allowed file types are pdf, doc, docx')
        return redirect(request.url)
