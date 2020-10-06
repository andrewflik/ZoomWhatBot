"""
    Author - DEVESH
    Description - ZoomWhatBot
    A WhatsApp BOT capable of :
    -> Arranging Meetings  - create
    -> Getting Attendance  - get
    -> Know More           - about
"""

from flask import Flask, request, json
from flask_ngrok import run_with_ngrok
import requests
from twilio.twiml.messaging_response import MessagingResponse
from zoomus import ZoomClient
import os
from drive_ import *   # Import
import pandas as pd

app = Flask(__name__)
run_with_ngrok(app)

""" Setting Up ZOOM Client """
API_KEY = "2lGdVPlHSB2tf3q51D5wFQ"
API_SECRET = "JF7uEaoeDqG1M3J363wSkZT9NcSbBrY4Th5H"
client = ZoomClient(API_KEY, API_SECRET)
GOOGLE_API_KEY = "e508d1f42da2f1948fe8072d7d34e4398a356c00"
miD = ""
userList = dict()


""" Setting Up DRIVE and SHEETS """
SERVICE_ACCOUNT_FILE = f".secrets/{os.listdir('.secrets')[0]}"
SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file"]

googl = Googl(SERVICE_ACCOUNT_FILE, SCOPES)

A_Token = "ya29.a0AfH6SMC9ucuu7__WJZd1Ejj6_8WCcbhGcuV7ztnVTpD8N6ahEQuiKKKQ3auphRetKdtmKndenTa4heMq2QbJttuEWmBnF5YfXXy7H8-cNpOcymsjhkaFUvK35IlRR4XTjMiUXByxqRK8H8bJuz14vEF88k6Zd56tKwY"


def init():
    print("Starting SERVER...")
    return


def uploadToDrive(fileName):
    headers = {
        "Authorization": "Bearer " + A_Token
    }
    para = {
        "name": fileName,
        "parents": ["1-HQDPtcH0DxqwOOQWycW6Km8aQHyHZPH"]
    }
    files = {
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': (open("./" + fileName, "rb"))
    }
    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files,
    )
    print(r.json())
    print("Here....")
    uniqueID = r.json()["id"]
    print(uniqueID)
    r.close()
    link = f"https://drive.google.com/file/d/{uniqueID}/view?usp=sharing"   # return the SHAREABLE Link
    return link


@app.route('/', methods=['POST', 'GET'])
def zoom():
    # Keep Track of users that JOIN/LEAVE
    # [waiting, started]
    keep = False
    zoom_meeting = client.get_request(
        "/meetings/{}".format(miD),
    )
    flag = zoom_meeting.json()["status"]
    if flag == "started":
        # Save every user
        keep = True
    else:
        print("Waiting for meeting to start...")
        keep = False
        return

    if request.json['event'] == 'meeting.ended':
        keep = False
        return

    # JOIN
    if request.json['event'] == 'meeting.participant_joined':
        print(request.json)
        userList[request.json['payload']['object']['participant']['user_id']] = [request.json['payload']['object']['participant']['user_name'], request.json['payload']['object']['participant']['join_time']]
    # LEAVE
    if request.json['event'] == 'meeting.participant_left':
        print(request.json)
        userList[request.json['payload']['object']['participant']['user_id']].append(request.json['payload']['object']['participant']['leave_time'])


@app.route('/bot', methods=['POST'])
def bot():
    global miD
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if 'cmd' in incoming_msg:
        cmds = """ 1. create now/later : Create Instant Zoom Meeting/Schedule it for later \n 2. get : Return attendance of the last meeting \n 3. caption On\Off : Turn on/off caption \n 4. about - Know about BOT """
        msg.body(cmds)
        responded = True

    if 'create meeting' == incoming_msg or 'create' == incoming_msg:
        msg.body("""When do you want the meeting to be created ? PeeP PeeP""")
        responded = True

    if 'now' == incoming_msg:
        # create meeting
        mail = "deveshrajput978@gmail.com"
        zoom_meeting = client.meeting.create(user_id=mail)
        if zoom_meeting.status_code == 201:
            miD = zoom_meeting.json()["id"]
            print(zoom_meeting.json())
            link = zoom_meeting.json()["join_url"]
            joinLink = zoom_meeting.json()["start_url"]
            password = zoom_meeting.json()["password"]
            msg.body(f"Zoom meeting created successfully, \n Host Link : {joinLink} \n Join Link : {link} \n Password : {password}")
        else:
            msg.body(f"Failed to create Zoom Meeting! Error {zoom_meeting.status_code}")
        responded = True

    if 'get' == incoming_msg:
        if not userList:
            msg.body(f"Last Meeting {miD} was empty")
        else:
            msg.body(f""" --- Last Attendance of Meeting {miD} ---\n """)
            output_file = f"zoom_report_{miD}"
            print(userList)
            df = pd.DataFrame.from_dict(userList, orient='index', columns=["Name", "Joining Time", "Leaving Time"])
            print(df)
            df.to_excel(f"{output_file}.xlsx")
            sheetLink = uploadToDrive(f"{output_file}.xlsx")
            print(sheetLink)
            msg.body(sheetLink)
        #msg.body(f"--- Last Attendance of Meeting {miD} ---\n")
        #msg.media(sheetLink)
        #sheet_link = googl.get_sheet_link(result.get("spreadsheetId"))
        #msg.body(sheet_link)
        #for i in userList:
        #    msg.body(f"{userList[i][0]} - {userList[i][1]} '\n'")
        responded = True

    if 'about' in incoming_msg:
        msg.body(""" I'm a whatsapp bot that can take care of all your zoom lecutres! PeeP PeeP \n """)
        responded = True

    if not responded:
        msg.body(""" I only know about zoom lecture commands, sorry! Text cmd to know more. """)
        responded = True

    return str(resp)


if __name__ == '__main__':
    init()
    app.run()