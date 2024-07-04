from flask import Flask

app = Flask(__name__)

@app.route("/home")
def hello_world():
    return "<h1>Hello, Bhavy!</h1>"

@app.route("/contactus")
def contact_us():
    return "please reach out"