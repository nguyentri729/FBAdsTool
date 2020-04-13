from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import requests
class autofb:
    def __init__(self):
        option = Options()
        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")
        option.add_argument("window-size=800,1000")
        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", { 
            "profile.default_content_setting_values.notifications": 1 
        })
        self.driver = webdriver.Chrome(options=option, executable_path=r"D:\Projects\autoFB\chromedriver.exe")
    def login(self, data, type):
        self.driver.get('https://www.facebook.com/')
        if type == 'cookie':
            cookies = data['cookie'].split(';')
            for cookie in cookies:
                try:
                    cookie = cookie.split('=')
                    self.driver.add_cookie({
                        'name': cookie[0],
                        'value': cookie[1]
                    })
                except:
                    pass
        if type == 'account':
            emailInput = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
            passwordInput = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
            emailInput.send_keys(data['username'])
            passwordInput.send_keys(data['password'])
            
            webdriver.ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            #check 2fa
            try:
                codeInput = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "approvals_code")))
                submitButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "checkpointSubmitButton")))
                r = requests.get('https://jickmeaz.000webhostapp.com/getCode.php?secrect=' + data['2faSecret'] + '')
                
                if r.status_code == 200:
                    codeInput.send_keys(r.text)
                    submitButton.click()
                else:
                    return False
            except:
                pass
            for x in range(6):
                try:
                    submitButton = WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.ID, "checkpointSubmitButton")))
                    submitButton.click()
                    time.sleep(3)
                except:
                    break
        try:
            print('done roi ne')
            self.driver.get('https://www.facebook.com/')
            userNav = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, "userNav")))
            return True
        except:
            return False
        
    def addCredit(self, creditCard):
        self.driver.get('https://www.facebook.com/ads/manager/account_settings/account_billing/')
        #wait button show
        addCreditButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='cm_add_pm_button']")))
        addCreditButton.click()
        time.sleep(3)
        
        #cardName send
        webdriver.ActionChains(self.driver).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(creditCard['cardName']).perform()
        
        #cardNumber send
        webdriver.ActionChains(self.driver).send_keys(Keys.TAB).send_keys(creditCard['cardNumber']).perform()
        
        #cardExperied send
        cardExperied = creditCard['cardExperied'].split('/')
        webdriver.ActionChains(self.driver).send_keys(Keys.TAB).send_keys(cardExperied[0]).send_keys(cardExperied[1]).perform()
        
        #CCV send
        webdriver.ActionChains(self.driver).send_keys(Keys.TAB).send_keys(creditCard['ccv']).perform()

        #enter =)))
        webdriver.ActionChains(self.driver).send_keys(Keys.TAB + Keys.TAB + Keys.TAB + Keys.ENTER).perform()

        time.sleep(100000)
    
    def inbox(self, userID, messages, type):
        self.driver.get("https://www.facebook.com/messages/t/" + userID)
        # time.sleep(10)
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).send_keys(messages).send_keys(Keys.ENTER).perform()

    def reaction(self, idPost, reactType):
        self.driver.get("https://www.facebook.com/" + idPost)
        hoverElement = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_8c74")))
        webdriver.ActionChains(self.driver).move_to_element(hoverElement).perform()
        reaction = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@aria-label='"+reactType+"']")))
        reaction.click()
        time.sleep(1)
    def comment(self, idPost, comment):
        self.driver.get("https://www.facebook.com/" + idPost)
        commentBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_7c_r")))
        commentBox.click()
        webdriver.ActionChains(self.driver).send_keys(comment).send_keys(Keys.ENTER).perform()
        time.sleep(1)
    def uploadImage(self): 
        self.driver.get("https://www.facebook.com/?soft=composer")
        elm = self.driver.find_element_by_xpath("//input[@type='file']")
        elm.send_keys(os.getcwd() + "/icon.png")
        time.sleep(1000)
    def quit(self):
        self.driver.stop_client()
        self.driver.close()
