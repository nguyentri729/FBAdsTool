
import sys
import json
import base64
import time
from autoFB import autofb
from tinydb import TinyDB, Query, where
# code by nguyentri729
# 17/04/2020
# auto ads facebook

# enter command
createAds = False
testChangeIP = False
updateCookie = False
hideWindow = False
checkKey = False
auto50 = False
proxyIP = ''
fakeURL = 'https://identinator.com/?for_country=aut'
createAdsAccount = False
shareAccountAds = False
keyActive = ''
pathExcel = ''
mainID = ''
numberThread = 1
totalThread = 1

for index in range(1, len(sys.argv)):
    if sys.argv[index] == '-credit':
        message_bytes = base64.b64decode(sys.argv[index + 1])
        message = message_bytes.decode('ascii')
        creditCard = json.loads(message)
    if sys.argv[index] == '-acc':
        message_bytes = base64.b64decode(sys.argv[index + 1])
        message = message_bytes.decode('ascii')
        account = json.loads(message)
    # ads get params
    if sys.argv[index] == '-createAdsAccount':
        createAdsAccount = True
    if sys.argv[index] == '-moneyIndex':
        moneyIndex = sys.argv[index + 1]
    if sys.argv[index] == '-timeIndex':
        timeIndex = sys.argv[index + 1]
    if sys.argv[index] == '-countryIndex':
        countryIndex = sys.argv[index + 1]
    if sys.argv[index] == '-updateCookie':
        updateCookie = True
    if sys.argv[index] == '-proxy':
        proxyIP = sys.argv[index + 1]
    if sys.argv[index] == '-test':
        testChangeIP = True
    if sys.argv[index] == '-hideWindow':
        hideWindow = True
    if sys.argv[index] == '-fakeURL':
        fakeURL = sys.argv[index + 1]
    if sys.argv[index] == '-keyActive':
        keyActive = sys.argv[index + 1]
    if sys.argv[index] == '-checkKey':
        checkKey = True
    if sys.argv[index] == '-auto50':
        auto50 = True
    if sys.argv[index] == '-typeAcc':
        typeAcc = sys.argv[index + 1]
    if sys.argv[index] == '-shareAccountAds':
        shareAccountAds = True
    if sys.argv[index] == '-pathExcel':
        pathExcel = sys.argv[index + 1]
    if sys.argv[index] == '-mainID':
        mainID = sys.argv[index + 1]
    if sys.argv[index] == '-auto50.changeMoney':
        if sys.argv[index + 1] == 'true':
            auto50ChangeMoney = True
        else:
            auto50ChangeMoney = False
    if sys.argv[index] == '-numberThread':
        numberThread = sys.argv[index + 1]
    if sys.argv[index] == '-totalThread':
        totalThread = sys.argv[index + 1]
# share account Ads
if shareAccountAds:
    result = {
        'status': 'fail',
        'msg': 'unknown error',
    }
    if typeAcc == 'main':
        
        fbMain = autofb(proxyIP, hideWindow, fakeURL, keyActive, 'left')
        fbMain.login(account)
        fbInfo = fbMain.getInfo()
        if fbInfo:
            #add to database
            mainDB = TinyDB('mainDB.json')
            Main = Query()
            checkUID = mainDB.search((where('uid') == fbInfo['uid']) & (where('name') ==  fbInfo['name']))

            if len(checkUID) <= 0:
                mainDB.insert({
                    'uid': fbInfo['uid'],
                    'name': fbInfo['name']
                })
            #find infor

            while (True):
                cloneDB = TinyDB('cloneDB.json')
                
                #add friends 
                waitingList = cloneDB.search((where('mainID') == fbInfo['uid']) & (where('status') == 'WAITING'))
                print('waiting add')
                print(waitingList)
                for cloneInfo in waitingList:
                    #add friend to 
                    print('add friend to ')
                    print(cloneInfo)
                    fbMain.addFriends(cloneInfo['cloneUID'])
                    #update status 
                    cloneDB.update({'status': 'ADDED'}, (where('mainID') == fbInfo['uid']) & (where('cloneUID') == cloneInfo['cloneUID']))
                
                
                waitingImport = cloneDB.search((where('mainID') == fbInfo['uid']) & (where('status')== 'WAITING_IMPORT'))
                

                for cloneInfo in waitingImport:
                    fbMain.importAdsExcel(cloneInfo['campID'], pathExcel)
                    cloneDB.update({'status': 'DONE'}, (where('mainID') == fbInfo['uid']) & (where('cloneUID') == cloneInfo['cloneUID']))
                time.sleep(3)
                print('repeat---------')
        else:
            result['msg'] = 'login fail'
    else:
        fbClone = autofb(proxyIP, hideWindow, fakeURL, keyActive, 'right', numberThread, totalThread)
        account['loginType'] = 'account'
        fbClone.login(account)
        fbInfo = fbClone.getInfo()
        if fbInfo:
            #fbClone.shareAccountAdsCloneAuto(fbInfo['uid'], moneyIndex, timeIndex, countryIndex)
            #search info of main uid
            mainDB = TinyDB('mainDB.json')
            mainAccount = mainDB.search(where('uid') == mainID)
            cloneDB = TinyDB('cloneDB.json')
            Clone = Query()
            if len(mainAccount) > 0:
                
                cloneDB.insert({
                    'cloneUID': fbInfo['uid'],
                    'mainID'  : mainID,
                    'campID'  : '',
                    'status'  : 'WAITING'
                })
                while(True):
                    print('repeat ')
                    cloneDB = TinyDB('cloneDB.json')
                    
                    checkAdded = cloneDB.search((where('cloneUID') == fbInfo['uid']) & (where('status') == 'ADDED') & (where('mainID') == mainID))


                    if len(checkAdded) > 0:
                        fbClone.acceptFriends(mainID)
                        fbClone.addAdsAccount(moneyIndex, timeIndex, countryIndex)
                        idCamp = fbClone.addMainCloneAds(mainAccount[0]['name'])
                        #update camp
                        cloneDB.update({'status' : 'WAITING_IMPORT', 'campID': idCamp}, Clone.cloneUID == fbInfo['uid'])
                        break
                    time.sleep(1)
            # update message
            result['status'] = 'success'
            result['msg'] = ''
        else:
            result['msg'] = 'login fail'

    print(json.dumps(result, indent=4, sort_keys=True))
    exit()










if testChangeIP:
    fb.testChangeIP()
    time.sleep(10000)
    exit()
if checkKey:
    check = requests.get('http://199.34.16.50/checkKeys.php?key='+keyActive+'')
    print(check.text)
    exit()
fb = autofb(proxyIP, hideWindow, fakeURL, keyActive)
if updateCookie:
    fb.login(account)
    if fb.checkLogin():
        cookies = fb.getCookie()
        result = {
            'status': 'success',
            'msg': 'ok',
            'cookie': cookies
        }
    else:
        result = {
            'status': 'fail',
            'msg': 'Login fail'
        }
    print(json.dumps(result, indent=4, sort_keys=True))
    fb.quit()

else:
    result = {
        'status': 'fail',
        'msg': 'connect fail ! retry '
    }
    fb.login(account)
    try:
        # check login account
        if fb.checkLogin():
            if createAdsAccount:
                addAdsAction = fb.addAdsAccount(
                    moneyIndex, timeIndex, countryIndex)
                if addAdsAction:
                    result = {
                        'status': 'success',
                        'msg': ''
                    }
                else:
                    result = {
                        'status': 'fail',
                        'msg': 'checkpoint'
                    }
            else:
                fb.addCredit(creditCard)
                result = {
                    'status': 'success',
                    'msg': 'action call success'
                }
        else:
            result = {
                'status': 'fail',
                'msg': 'login fail'
            }
    except:
        pass

    fb.quit()
    print(json.dumps(result, indent=4, sort_keys=True))
