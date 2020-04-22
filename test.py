
import re
url = 'https://www.facebook.com/ads/manager/account_settings/information/?act=3017526274992860&pid=p1&page=account_settings&tab=account_information'
idCampRegex = r"https://www\.facebook\.com/ads/manager/account_settings/information/\?act=(.*?)&"
idCamp = re.findall(idCampRegex, url)
print(idCamp[0])