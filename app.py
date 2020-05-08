from flask import Flask,request
from base64 import b64encode
import requests
import json
import pymongo
import time

## ZOOM MARKETPLACE APP CONFIGURATION ########
client_id = 'KAat0evuQpSP5ejpBvKU_Q'
clent_secret = 'mhOHPrO1agPwaPEsMbU825fbWr1vhjyX'
zoom_bot_jid = 'v1q7xqhebxrhybtwtaoekt1q@xmpp.zoom.us'

## DATABASE ENDPOINT ######
# mongo_url = "mongodb://localhost:27017/"
mongo_url = 'mongodb://%s:%s@103.201.141.99:27018' % ('root', 'root')

# DATABASE CONNECTION
client = pymongo.MongoClient(mongo_url)
mydb = client["chatbot_database"]
mycol = mydb["customers"]

#FLASK APP##
app = Flask(__name__)


def authorize_token():
    url = "https://api.zoom.us/oauth/token?grant_type=client_credentials"
    message_bytes = client_id+":"+clent_secret
    message_bytes= message_bytes.encode('ascii')
    base64_bytes = b64encode(message_bytes).decode("utf-8")
    print (base64_bytes)
    payload = {}
    headers = {
      'Authorization': 'Basic %s'%base64_bytes,
      'Cookie': '_zm_ssid=aw1_c_OfgeOorJSGyQX-t3m8_nYg; _zm_page_auth=aw1_c_KYiTAXTNSy2aziPHw6EFig; _zm_ctaid=rAB7PRyvRd6l5cSdkuLmjA.1588685478021.91a808971825087e83302c5723223179; _zm_chtaid=908; cred=01FDD8B151ADA831F88E6BFF19FE4D68'
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    res = response.text
    print (" Authenticate chatbot session %r"%res)
    return json.loads(res)

def reply_bot(data):
    token_data = authorize_token()
    reply_url = "https://api.zoom.us/v2/im/chat/messages"
    headers = {
      'Authorization': "Bearer %s"%token_data.get('access_token'),
      'Content-Type': 'application/json'
    }
    msg = "Please use proper declaration to 'set' or 'get' the value of variable. Format Type e.g: /skeleton set 12345 or /skeleton get."
    value = data.get("payload").get('cmd')
    if 'set' in value:
        if len(value.split(" ")) > 1 and value.split(" ")[1].isnumeric():
            temp_var = value.split(" ")[1]
            temp_dict = data.get("payload")
            temp_dict.update({"numeric_value":temp_var})
            try:
                update_query = mycol.insert_one(temp_dict)
                print ("update mongodb customers table %r"%update_query)
                msg = "Numerical value is set in the skeleton chat-bot i.e %r."%temp_var
            except Exception as e:
                print ("Exception occur when setting the data from DB :- %r"%e)
                msg =  "Something went wrong with chat bot."
    elif 'get' == value:
        try:
            fetch_mongo_data = mycol.find_one({},sort=[( '_id', pymongo.DESCENDING )])
            print ("Variable=%r"%fetch_mongo_data.get('numeric_value'))
        except Exception as e:
            print ("Exception occur when getting the data from DB :- %r"%e)
            fetch_mongo_data = []
        if fetch_mongo_data:
            msg = "Numerical value is %r."%fetch_mongo_data.get('numeric_value')
        else:
            msg = "Numerical value is not set use the following command to set value '/skeleton set 12345'."
    revert_msg = {
              "robot_jid": zoom_bot_jid,
              "to_jid": data.get("payload").get('toJid'),
              "account_id":data.get("payload").get('accountId'),
              "content": {
                "head": {
                  "text": msg
                }
              }
            }

    response = requests.request("POST", reply_url, headers=headers, data = json.dumps(revert_msg))
    result = json.loads(response.text)
    print (" POST data coming from Zoom = %r"%result)
    return result


## REDIRECT URL #####
@app.route("/authorize")
def authorize():
    code = request.args.get('code')
    if code:
        print (code)
        try:
            mycol2 = mydb["code_collection"]
            update_query = mycol2.insert_one({"code":code,"timestamp":int(time.time())})
            print (update_query)
        except Exception as e:
            print ("Exception occur while update in db during authorize :-%r"%e)
            return "Issue in Database connection . Please check :("
        return "Everything looks fine Zoom App Authorization Successfully."
    return "Something Went Wrong Zoom App Authorization failed."


## BOT ENDPOINT URL FOR SERVER COMMUNICATION #####
@app.route("/skeleton",methods = ['POST','GET'])
def skeleton():
    status = "Wrong Http request method only valid for POST method"
    if request.method == 'POST':
        data = request.json
        status = reply_bot(data)
    return "Reply bot status : %r"%status


### INDEX PAGE ######
@app.route("/")
def index():
    return "Welcome to the Zoom App...."

@app.route("/privacy")
def privacy():
    return "privacy."

@app.route("/support")
def support():
    return "support"


@app.route("/deactivate")
def deactivate():
    return "App is deactivated."

@app.route("/verifyzoom.html")
def verifyzoom():
    return "af0e4f630f914d25905227557f67ea0c"






if __name__ == "__main__":
    app.run()
