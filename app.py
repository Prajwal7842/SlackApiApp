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
os.environ["TIMESTAMP"] = "0"
UPLOAD_FOLDER = 'static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
timeStamp = 0

@app.route("/")
def upload():
    global timeStamp
    timeStamp = (int)(os.environ["TIMESTAMP"])
    print(timeStamp)
    channels = get_visible_channels()
    data = FileContent.query.all()
    print(data)
    result = get_conversation_history("CV6P11B0F", True)
    download_files(result)
    return str(timeStamp)

def get_visible_channels():
    url = "https://slack.com/api/conversations.list?token="+slack_token
    r = requests.get(url = url)
    return r.json()

def get_conversation_history(channel_id, latest = False):
    global timestamp
    if latest:
        Url = "https://slack.com/api/conversations.history?token="+slack_token+"&channel="+channel_id+"&oldest="+str(timeStamp)
    else:
        Url = "https://slack.com/api/conversations.history?token="+slack_token+"&channel="+channel_id
    r = requests.get(url = Url)
    return r.json()

def download_files(response):
    global timeStamp
    latest_time_stamp = timeStamp
    for message in response["messages"]:
        if "files" in message:
            for files in message["files"]:
                if latest_time_stamp < (int)(files["timestamp"]):
                    saveFile(files["url_private_download"], files["name"])
                    latest_time_stamp = (int)(files["timestamp"])
    update_timeStamp(latest_time_stamp)

def saveFile(url, file_name):
    response = urllib.request.urlopen(url)
    newFile = FileContent(name = file_name, data = response.read())
    db.session.add(newFile)
    db.session.commit()
    print("Succesfully Stored in the Database")

def printResult(res):
    print(json.dumps(res, indent=4))

def update_timeStamp(latest_time_stamp):
    global timestamp
    timeStamp = latest_time_stamp
    os.environ["TIMESTAMP"] = str(timeStamp)
    print(timeStamp)

class FileContent(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)
    
if __name__ == '__main__':
    app.run(debug=True)
    

