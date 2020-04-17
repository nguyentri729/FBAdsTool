from FBAuto import autofb
import sys
import base64
import json
import time
#enter command
for index in range(1, len(sys.argv)):
    if sys.argv[index] == '-credit': 
        message_bytes = base64.b64decode(sys.argv[index + 1])
        message = message_bytes.decode('ascii')
        creditCard = json.loads(message)
    if sys.argv[index] == '-acc':

        message_bytes = base64.b64decode(sys.argv[index + 1])
        message = message_bytes.decode('ascii')
        account = json.loads(message)
fb = autofb()

fb.login(account, 'cookie')
result = {
    'status': 'fail',
    'msg': 'unknown'
}
if fb.checkLogin():
    x = fb.addAdsAccount()
    result = {
        'status': 'success',
        'msg': 'add ads account success!'
    }
else:
    result = {
        'status': 'fail',
        'msg': 'login fail'
    }
fb.quit()
print(json.dumps(result, indent=4, sort_keys=True))

