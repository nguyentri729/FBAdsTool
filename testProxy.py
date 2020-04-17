import json
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import sys
prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
#prox.http_proxy = "ip_addr:port"
#prox.socks_proxy = "180.104.96.226:41179"

if (len(sys.argv) > 1) :
    prox.ssl_proxy = sys.argv[1]



capabilities = webdriver.DesiredCapabilities.CHROME
prox.add_to_capabilities(capabilities)

driver = webdriver.Chrome(desired_capabilities=capabilities)
driver.get('https://api.myip.com/')


