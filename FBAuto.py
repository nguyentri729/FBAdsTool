from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import random, string

import time
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
                    print('')
            return True
        if type == 'account':
            emailInput = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "email")))
            passwordInput = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "pass")))
            emailInput.send_keys(data['username'])
            passwordInput.send_keys(data['password'])
            
            webdriver.ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            #check 2fa
            try:
                codeInput = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "approvals_code")))
                submitButton = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "checkpointSubmitButton")))
                r = requests.get('https://jickmeaz.000webhostapp.com/getCode.php?secrect=' + data['secret'] + '')
                
                if r.status_code == 200:
                    codeInput.send_keys(r.text)
                    submitButton.click()
                else:
                    return False
            except NameError:
                print('loi ne' + NameError)
            for x in range(6):
                try:
                    submitButton = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, "checkpointSubmitButton")))
                    submitButton.click()
                    time.sleep(3)
                except:
                    break
        return self.checkLogin
    def checkLogin(self):
        try:
            self.driver.get('https://www.facebook.com/profile.php')
            #divdata-click="profile_icon"
            userNav = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-click='profile_icon']")))
            return True
        except errorShow:
            #print(errorShow)
            return False  
    def addCredit(self, creditCard):
        self.driver.get('https://www.facebook.com/ads/manager/account_settings/account_billing/')
        #wait button show
        addCreditButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='cm_add_pm_button']")))
        addCreditButton.click()
        
        

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@data-testid='credit_card_number']")))


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
        
        time.sleep(4)
    def addAds(self):
        #add ads  
        self.driver.get('https://www.facebook.com/ads/manager/account_settings/information/')
        changeMoney = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Thay đổi đơn vị tiền tệ')]")))
        changeMoney.click()

        enterButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='currency']")))

        webdriver.ActionChains(self.driver).send_keys(Keys.TAB + Keys.ENTER).perform()
        time.sleep(3)
        self.driver.execute_script("document.getElementsByClassName('_54nh')[16].click(); ")
        

        time.sleep(3)
        webdriver.ActionChains(self.driver).send_keys(Keys.TAB + Keys.TAB + Keys.TAB + Keys.ENTER).perform()
        
        time.sleep(3)

        afterClick = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='jazoest']")))
        webdriver.ActionChains(self.driver).send_keys(Keys.TAB + Keys.TAB + Keys.ENTER).perform()
        
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_50f7")))
        
        
        time.sleep(2)
        #enter new ads
        self.driver.get('https://www.facebook.com/ads/manager/account_settings/information/')

        businessName = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@data-testid='business_name']")))
        businessName.send_keys(self.randomString(8)).perform()


        address_street1 = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@data-testid='address_street1']")))
        address_street1.send_keys(self.randomString(8)).perform()

        address_city = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@data-testid='address_city']")))
        address_city.send_keys(self.randomString(8)).perform()
        
        address_state = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@data-testid='address_state']")))
        address_state.send_keys(self.randomString(8)).perform()
        
        self.driver.execute_script("document.getElementsByClassName('_1f')[0].click()setTimeout(function(){document.getElementsByClassName('_3leq')[235].click()},2000)")

        time.sleep(3)
        cm_settings_page_save_button = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='cm_settings_page_save_button']")))
        cm_settings_page_save_button.click()


        # time.sleep(2)
        # #afterClick = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Lúc khác')]")))
        # webdriver.ActionChains(self.driver).send_keys(Keys.TAB + Keys.ENTER).perform()
        # #afterClick.click()

    def quit(self):
        self.driver.stop_client()
        self.driver.close()
    def randomString(self, stringLength=8):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))