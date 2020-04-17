import sys
import json
import base64
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
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
    def __init__(self, proxyIP=''):
        option = Options()
        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("window-size=1000,800")
        option.add_argument('--proxy-server="socks5://51.15.13.157:3320"')
        #option.add_argument('--host-resolver-rules="MAP * ~NOTFOUND , EXCLUDE '+'51.15.13.157'+'')
        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 1
        })
        capabilities = webdriver.DesiredCapabilities.CHROME
        if proxyIP != '':
            prox = Proxy()
            prox.proxy_type = ProxyType.MANUAL
            prox.ssl_proxy = proxyIP
            prox.add_to_capabilities(capabilities)
        self.driver = webdriver.Chrome(
            options=option, executable_path=r".\\chromedriver.exe", desired_capabilities=capabilities)
    # Login with account
    # data (array)
    # type (string): 'account', 'cookie'

    def testChangeIP(self):
        self.driver.get('https://api.myip.com/')

fb = autofb()

fb.testChangeIP()
time.sleep(10000)

