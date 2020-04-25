
from tinydb import TinyDB, Query
#using tinydb
db = TinyDB('cloneDB.json')
# db.insert({
#     'cloneUID': '1234',
#     'mainUID' : '13445',
#       'campID' : '1233213'
#     'status' : 'ADDED'
# })
Clone = Query()
#uid = db.search(Clone.mainUID == '1234' and  Clone.status== 'ADDED')
db.update({'status' : 'DONE'}, Clone.status == 'ADDED' && )
print(len(uid))
