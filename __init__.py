from flask import Flask,flash,request,redirect,send_file,render_template
import os
import slack
import requests
import json
import urllib.request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
slack_token = os.environ["SLACK_TOKEN"]
client = slack.WebClient(token = slack_token)
timeStamp = 1583944378
UPLOAD_FOLDER = '/home/prajwal/Desktop/Projects/Internship/SlackApiIntegration/Flask/FlaskApp/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
db = SQLAlchemy(app)

@app.route("/")
def homepage():
    return "Successful"

@app.route("/upload/")
def upload():
    return render_template("upload_file.html", {})

class FileContent(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)

if __name__ == '__main__':
    app.run()
    

