from json_handler import json_write, reset_json, send_json
from flask import Flask ,request, abort
from datetime import datetime
import requests as req
import json


app = Flask(__name__)



@app.route('/twilio-sms',methods=['POST'])
def webhook():
    Body= ''
    From=''
    Time=''
    if request.method == "POST":
        message = request.form
        Body = message['Body']
        From = message['From']
        Time =  datetime.now().strftime("%H:%M:%S")

        data ={
            "body": Body,
            "from": From,
            "time": Time
        }
        json_write(data,"message.json")
        print(data)
        return data, 200
    else:
        abort(400)

@app.route('/twilio-sms',methods=['GET'])
def reset():
    data = send_json("message.json")
    return data,200

@app.route('/square-payment',method=['POST'])
def payment():
    if request.method == "POST":
        data = request.form
        json_write(data,"payments.json")
        print(data)
        return data, 200
    else:
        abort(400)

@app.route('/square-payment',method=['GET'])
def reset():
    data = send_json("payments.json")
    return data,200


@app.route('/vonage',method=['GET'])
def CallLog():
   response= req.get('https://api.nexmo.com/v2/reports?account_id=7b4aa824&status=PENDING, PROCESSING, SUCCESS, ABORTED, FAILED, TRUNCATED', auth=('7b4aa824', 'LPX0YS6nSfJUGjdG'))
   file_length=0
   if request.method == "GET":
       with open("logs.data",'r+') as file:
        file_data = json.load(file)
        file_length = len(file_data)
        file.close()

        data = response.form
        if(file_length > len(data)):
            json_write(data,"logs.json")
            print(data)
            return data, 200
        else:
            return "No New Data is founded!!!", 200
   else:
        abort(400)


if __name__ == "main":
    app.run()

