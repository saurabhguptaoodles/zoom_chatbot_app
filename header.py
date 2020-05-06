client_id = 'ddMUISwRRGY1IviJkVLqQ'
clent_secret = '7CKujq9OfQ6MvG2X6DiZn4mhsWXHoUkG'
from base64 import b64encode
test_string = client_id+":"+clent_secret
test_string = bytes(test_string, 'utf-8')
userAndPass = b64encode(test_string)
headers = { 'Authorization' : 'Basic %s' %  userAndPass }
print (headers)
