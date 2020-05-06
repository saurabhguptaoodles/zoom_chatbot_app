from flask import Flask,request
from base64 import b64encode
import requests
import json
app = Flask(__name__)

client_id = 'I2PBvB9nQkCvP4U7qwedgg'
clent_secret = '4UHFIJFh673zatIBRABdOwo6YK60i4nW'
zoom_bot_jid = 'v1bhbqcfi5tnswq9pk0bybtg@xmpp.zoom.us'
temp_var = 0

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
    global temp_var
    if 'set' in value:
        if len(value.split(" ")) > 1 and value.split(" ")[1].isnumeric():
            temp_var = value.split(" ")[1]
            msg = "Numerical value is set in the skeleton chat-bot i.e %r."%temp_var
    elif 'get' == value:
        print ("Variable=%r"%temp_var)
        if temp_var:
            msg = "Numerical value is %r."%temp_var
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

@app.route("/authorize")
def authorize():
    code = request.args.get('code')
    if code:
        print (code)
        return "Everything looks fine Zoom App Authorization Successfully."
    return "Something Went Wrong Zoom App Authorization failed."

@app.route("/skeleton",methods = ['POST','GET'])
def skeleton():
    status = "Wrong Http request method only valid for POST method"
    if request.method == 'POST':
        data = request.json
        status = reply_bot(data)
    return "Reply bot status : %r"%status

@app.route("/")
def index():
    return "Welcome to the Zoom App."


if __name__ == "__main__":
    app.run()
