from base64 import b64encode
import json
import requests
client_id = '3rP0flhiQ7aqWB9flz_sMg'
clent_secret = '5GWKy9gNkjUeMHCVClaoXi1WidZ62Oc9'
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

res = json.loads(response.text.encode('utf8'))
print (res)
