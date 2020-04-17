from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import re
import time
import requests
import pathlib

# code by nguyentri729
# 17/04/2020
# auto ads facebook


class autofb:
    def __init__(self):
        option = Options()
        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")
        option.add_argument("window-size=1000,800")
        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 1
        })
        self.driver = webdriver.Chrome(
            options=option, executable_path=r".\\chromedriver.exe")
    # Login with account
    # data (array)
    # type (string): 'account', 'cookie'
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
            emailInput = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "email")))
            passwordInput = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "pass")))
            emailInput.send_keys(data['username'])
            passwordInput.send_keys(data['password'])

            webdriver.ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            #check 2fa
            try:
                codeInput = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "approvals_code")))
                submitButton = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.ID, "checkpointSubmitButton")))
                r = requests.get(
                    'https://jickmeaz.000webhostapp.com/getCode.php?secrect=' + data['secret'] + '')

                if r.status_code == 200:
                    codeInput.send_keys(r.text)
                    submitButton.click()
                else:
                    return False
            except NameError:
                print('loi ne' + NameError)
            for x in range(6):
                try:
                    submitButton = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.ID, "checkpointSubmitButton")))
                    submitButton.click()
                    time.sleep(3)
                except:
                    break
        return self.checkLogin

    def checkLogin(self):
        try:
            self.driver.get('https://www.facebook.com/profile.php')
            #divdata-click="profile_icon"
            userNav = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-click='profile_icon']")))
            return True
        except:
            return False

    def addCredit(self, creditCard):
        self.driver.get(
            'https://www.facebook.com/ads/manager/account_settings/account_billing/')
        #wait button show
        addCreditButton = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-testid='cm_add_pm_button']")))
        addCreditButton.click()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//input[@data-testid='credit_card_number']")))

        #cardName send
        webdriver.ActionChains(self.driver).send_keys(Keys.TAB).send_keys(
            Keys.TAB).send_keys(creditCard['cardName']).perform()

        #cardNumber send
        webdriver.ActionChains(self.driver).send_keys(
            Keys.TAB).send_keys(creditCard['cardNumber']).perform()

        #cardExperied send
        cardExperied = creditCard['cardExperied'].split('/')
        webdriver.ActionChains(self.driver).send_keys(Keys.TAB).send_keys(
            cardExperied[0]).send_keys(cardExperied[1]).perform()

        #CCV send
        webdriver.ActionChains(self.driver).send_keys(
            Keys.TAB).send_keys(creditCard['ccv']).perform()

        #enter =)))
        webdriver.ActionChains(self.driver).send_keys(
            Keys.TAB + Keys.TAB + Keys.TAB + Keys.ENTER).perform()

        time.sleep(4)

    def addAdsAccount(self, moneyTypeIndex = '16', timeIndex = '61', countryIndex = '13'):
        try:
            #add ads
            self.driver.get(
                'https://www.facebook.com/ads/manager/account_settings/information/')
            changeMoney = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
                (By.XPATH, "//a[contains(text(),'Thay đổi đơn vị tiền tệ')]")))
            changeMoney.click()

            enterButton = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='currency']")))

            webdriver.ActionChains(self.driver).send_keys(Keys.TAB + Keys.ENTER).perform()
            time.sleep(3)
            self.driver.execute_script("document.getElementsByClassName('_54nh')["+str(moneyTypeIndex)+"].click(); ")

            time.sleep(2)
            webdriver.ActionChains(self.driver).send_keys(Keys.TAB + Keys.ENTER).perform()
            time.sleep(2)
            self.driver.execute_script("console.log(document.getElementsByClassName('_54nh')["+str(timeIndex)+"].click()) ")
            time.sleep(2)
            webdriver.ActionChains(self.driver).send_keys(Keys.TAB + Keys.TAB + Keys.ENTER).perform()
            
            afterClick = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='jazoest']")))
            webdriver.ActionChains(self.driver).send_keys(
                Keys.TAB + Keys.TAB + Keys.ENTER).perform()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_50f7")))
        except:
            time.sleep(2)
       
        time.sleep(2)
        try:
            # enter new ads
            self.driver.get(
                'https://www.facebook.com/ads/manager/account_settings/information/')

            businessName = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//input[@data-testid='business_name']")))
            businessName.send_keys(self.randomString(8))

            address_street1 = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//input[@data-testid='address_street1']")))
            address_street1.send_keys(self.randomString(8))

            address_city = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//input[@data-testid='address_city']")))
            address_city.send_keys(self.randomString(8))

            address_state = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//input[@data-testid='address_state']")))
            address_state.send_keys(self.randomString(8))

            self.driver.execute_script(
                "document.getElementsByClassName('_1f')[0].click();setTimeout(function(){document.getElementsByClassName('_3leq')["+str(countryIndex)+"].click()},2000)")
            time.sleep(3)

            cm_settings_page_save_button = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//button[@data-testid='cm_settings_page_save_button']")))
            cm_settings_page_save_button.click()

            time.sleep(5)
        except:
            time.sleep(5)

        #buoc tiep theo ne
        self.driver.get(
            'https://www.facebook.com/ads/manager/account_settings/account_billing/')
        #wait button show
        addCreditButton = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-testid='cm_add_pm_button']")))
        addCreditButton.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "new_direct_debit_v2_title")))
        self.driver.execute_script(
            "document.getElementById('new_direct_debit_v2_title').click();setTimeout(function(){document.getElementsByClassName('layerConfirm')[0].click()},3000)")

        #get data from fake IT site
        fakeData = self.fakeIT()
        account_holder_name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='account_holder_name']")))
        account_holder_name.send_keys(fakeData['name'])

        bankAccountNumber = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='bankAccountNumber']")))
        bankAccountNumber.send_keys(fakeData['iban'])
        routing_number = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='routing_number']")))
        routing_number.send_keys(fakeData['bic'])

        # addCreditButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@value='1']")))
        # addCreditButton.click()
        street = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='street']")))
        street.send_keys(fakeData['address'])

        city = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='city']")))
        city.send_keys(fakeData['city'])

        zipCode = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='zip']")))
        zipCode.send_keys(fakeData['zipcode'])

        approval = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='approval']")))
        approval.send_keys(Keys.SPACE)
        addButton = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "AdsPaymentsDirectDebitButton")))
        addButton.click()
        time.sleep(5)
        return self.checkLogin()

    def quit(self):
        self.driver.stop_client()
        self.driver.close()

    def randomString(self, stringLength=8):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    def fakeIT(self):
        ibanRegex = r'title="Click To Copy">(.*)</span></span> \(<a href="#"'
        bicRegex = r'<th scope="row">BIC</th>\n<td class="copy"><span data-toggle="tooltip" data-placement="top" title="Click To Copy">(.*)</span></td>'
        nameRegex = r'<th scope="row">Name</th>\n<td class="copy"><span data-toggle="tooltip" data-placement="top" title="Click To Copy">(.*)</span></td>'
        addressRegex = r'<th scope="row">Address</th>\n<td class="copy"><span data-toggle="tooltip" data-placement="top" title="Click To Copy">(.*)</span></td>'
        cityRegex = r'<th scope="row">City</th>\n<td class="copy"><span data-toggle="tooltip" data-placement="top" title="Click To Copy">(.*)</span></td>'
        zipRegex = r'<th scope="row">Postcode</th>\n<td class="copy"><span data-toggle="tooltip" data-placement="top" title="Click To Copy">(.*)</span></td>'
        
        req = requests.get('https://fake-it.ws/at/')
        iban = re.findall(ibanRegex, req.text)[0]
        bic = re.findall(bicRegex, req.text)[0]
        name = re.findall(nameRegex, req.text)[0]
        address = re.findall(addressRegex, req.text)[0]
        city = re.findall(cityRegex, req.text)[0]
        zipcode = re.findall(zipRegex, req.text)[0]

        return({
            'name': name,
            'address': address,
            'city': city,
            'zipcode': '43100',
            'bic': bic,
            'iban': iban
        })



