from flask import Blueprint, flash, redirect, jsonify, render_template, request
from models import db
from flasgger import swag_from
from werkzeug.utils import secure_filename
# from resume_parser_spacy1 import parse_resume, save_to_file
from resume_parser_openai import extract_text_openai
from utils import UPLOAD_FOLDER, allowed_file, extract_text_from_pdf, save_raw_text_to_file, save_to_mongodb
import os
import json

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
        resume_text = extract_text_from_pdf(file_path)
        response  = extract_text_openai(resume_text)
        extracted_details = response.choices[0].message.content
        # Convert JSON string to dictionary
        data = json.loads(extracted_details)

        save_raw_text_to_file(text=str(data), output_path=f"outputs/output_openai_{filename}.txt")

        # save_to_mongodb(parsed_resume)
        # save_to_file(parsed_resume, output_path="output3.txt")

        # Check for 'response_type' query parameter to determine response format
        response_type = request.headers.get('Accept')
        # print(response_type)
        if response_type and 'application/json' in response_type:
            return jsonify(data)
        else:
            return render_template("parsed_resume.html", **data)
    else:
        flash('Allowed file types are pdf, doc, docx')
        return redirect(request.url)
