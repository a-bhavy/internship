from utils import extract_text_from_pdf
from utils import save_raw_text_to_file
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def extract_text_openai(resume_text):

    prompt = f"""
    Extract the required details from the given resume:
    {resume_text}

    Required details format:
    {{
        "first_name": "",
        "last_name": "",
        "email": "",
        "phone": "",
        "linkedin_url": "",
        "twitter_url": "",
        "github_url": "",
        "skills": [],
        "job_title": "",
        "experience": [],
        "summary": "",
        "visa": "",
        "state": "",
        "city": "",
        "location": "",
        "experiences": [
            {{
                "job_title": "",
                "company": "",
                "location": "",
                "location_city": "",
                "location_state": "",
                "duration": "",
                "duration_startdate": "",
                "duration_enddate": "",
                "job_summary": ""
            }}
        ],
        "educations": [
            {{
                "education_title": "",
                "college": "",
                "duration": "",
                "duration_startdate": "",
                "duration_enddate": ""
            }}
        ],
        "certifications": [
            {{
                "certificate_title": "",
                "certificate_organization": "",
                "certificate_duration": ""
            }}
        ]
    }}
    """

    response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                max_tokens=1500
            )
    return response

if __name__ == "__main__":
    resume_path = "sample_resume/Vijendra Maurya.docx (1).pdf"
    resume_text = extract_text_from_pdf(resume_path)
    response  = extract_text_openai(resume_text)
    print(response)
    extracted_details = response.choices[0].message.content
    save_raw_text_to_file(text=extracted_details, output_path="outputs/output_openai.txt")


    print(extracted_details)
