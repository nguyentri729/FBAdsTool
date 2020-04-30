 def auto50MainAccoutAutoAction(self, uid):
        if uid == '':
            return False
        self.addFriends(uid)
        initialID = self.readFileisDone()
        while True:
            nowID = self.readFileisDone()
            if initialID != nowID:
                self.importAdsExcel(nowID, pathExcel)
                initialID = nowID
                break
            time.sleep(5)
        return True

    def auto50MainAccoutAuto(self, pathExcel):
        # read clone uid
        # and connect
        uid = self.readFileCloneID()
        self.auto50MainAccoutAutoAction(uid, pathExcel)
        while(True):
            readFile = self.readFileCloneID()
            if readFile != uid:
                uid = readFile
                self.auto50MainAccoutAutoAction(uid, pathExcel)
            time.sleep(5)

    def auto50CloneAccountAuto(self, uid, credit, changeMoney):
        while(True):
            readFileMainID = self.readFileMainID()
            checkAction = self.checkCloneActionDone(uid, 'ADD_FRIEND')
            if readFileMainID != '' and checkAction:
                mainInfo = readFileMainID.split('|')
                self.auto50CloneAccountAutoAction(mainInfo[0], mainInfo[1], credit, changeMoney)
                break
            time.sleep(5)
    def auto50CloneAccountAutoAction(self, uid, name, credit, changeMoney):

        return True
    def shareAccountAdsMainAutoAction(self, uid, pathExcel):
        if uid == '':
            return False
        self.addFriends(uid)
        initialID = self.readFileisDone()
        while True:
            nowID = self.readFileisDone()
            if initialID != nowID:
                self.importAdsExcel(nowID, pathExcel)
                initialID = nowID
                break
            time.sleep(5)
        return True

    def shareAccountAdsCloneAutoAction(self, uid, name, moneyTypeIndex,timeIndex, countryIndex):
        self.acceptFriends(uid)
        self.addAdsAccount(moneyTypeIndex,timeIndex, countryIndex)
        time.sleep(3)
        self.addMainCloneAds(name)
        time.sleep(10)
        self.quit()
        return True

    # main account call actions
    def shareAccountAdsMainAuto(self, pathExcel):
        # read clone uid
        # and connect
        uid = self.readFileCloneID()
        self.shareAccountAdsMainAutoAction(uid, pathExcel)
        while(True):
            readFile = self.readFileCloneID()
            if readFile != uid:
                uid = readFile
                self.shareAccountAdsMainAutoAction(uid, pathExcel)
            time.sleep(5)

    def shareAccountAdsCloneAuto(self, uid, moneyTypeIndex = '12', timeIndex='61', countryIndex='13'):
        while(True):
            time.sleep(5)