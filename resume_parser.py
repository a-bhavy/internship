import fitz  # PyMuPDF
import spacy
import re

# Load Spacy model
nlp = spacy.load("en_core_web_trf")

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    text = ""
    
    # Extract text from each page
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    
    return text

def extract_sections(text):
    sections = {
        "name": "",
        "contact_info": "",
        "education": [],
        "experience": [],
        "skills": []
    }

    # Use SpaCy for named entity recognition
    doc = nlp(text)

    # Extract name (assuming it's a PERSON entity)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            sections["name"] = ent.text
            break

    # Extract contact info (simplistic approach, needs enhancement)
    contact_info = ""
    contact_info_pattern = r"[\w\.-]+@[\w\.-]+|\+?\d[\d -]{8,12}\d"
    contact_info_matches = re.findall(contact_info_pattern, text)
    sections["contact_info"] = ", ".join(contact_info_matches)

    # Extract sections based on headings
    education_section = re.findall(r'(Education|EDUCATION)(.*?)(Experience|EXPERIENCE|Skills|SKILLS|$)', text, re.S)
    if education_section:
        sections["education"].append(education_section[0][1].strip())

    experience_section = re.findall(r'(Experience|EXPERIENCE)(.*?)(Education|EDUCATION|Skills|SKILLS|$)', text, re.S)
    if experience_section:
        sections["experience"].append(experience_section[0][1].strip())

    skills_section = re.findall(r'(Skills|SKILLS)(.*?)(Education|EDUCATION|Experience|EXPERIENCE|$)', text, re.S)
    if skills_section:
        sections["skills"].append(skills_section[0][1].strip())

    return sections

def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    sections = extract_sections(text)
    return sections

def save_to_file(parsed_resume, output_path):
    with open(output_path, "w") as file:
        file.write(f"Name: {parsed_resume['name']}\n")
        file.write(f"Contact Info: {parsed_resume['contact_info']}\n\n")
        
        file.write("Education:\n")
        for edu in parsed_resume['education']:
            file.write(f"{edu}\n\n")
        
        file.write("Experience:\n")
        for exp in parsed_resume['experience']:
            file.write(f"{exp}\n\n")
        
        file.write("Skills:\n")
        for skill in parsed_resume['skills']:
            file.write(f"{skill}\n\n")

if __name__ == "__main__":
    # Example usage
    resume_path = "sample_resume/ My Resume.pdf"
    parsed_resume = parse_resume(resume_path)
    output_path = "output2.txt"
    save_to_file(parsed_resume, output_path)

    print(f"Parsed resume saved to {output_path}")
