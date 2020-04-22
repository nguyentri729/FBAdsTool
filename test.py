


#https://identinator.com/?for_country=aut


import requests
import re

req = requests.get('https://identinator.com/?for_country=aut')
regexName = (r"<th width=\"30%\">Name<\/th>\n"
	r"					<td style=\"max-width:50px; word-wrap:break-word;\">(.*)<\/td>")
addressRegex = (r"<th width=\"30%\">Adresse<\/th>\n"
	r"					<td style=\"max-width:50px; word-wrap:break-word;\">(.*)<\/td>")
cityRegex = (r"<th width=\"30%\">Stadt<\/th>\n"
	r"					<td style=\"max-width:50px; word-wrap:break-word;\">(.*)<\/td>")
bicRegex = (r"<th width=\"30%\">BIC<\/th>\n"
	r"					<td style=\"max-width:50px; word-wrap:break-word;\">\n						\n"
	r"						<div class=\"row\">\n							<div class=\"col-md-8\">(.*) </div>")
ibanRegex = (r"					<th width=\"30%\">IBAN</th>\n"
	r"					<td style=\"max-width:50px; word-wrap:break-word;\">\n"
	r"						\n"
	r"						<div class=\"row\">\n"
	r"							\n"
	r"							<div class=\"col-md-8\">\n(.*)<form")

name = re.findall(regexName, req.text)[0]
address = re.findall(addressRegex, req.text)[0]
city = re.findall(cityRegex, req.text)[0]
bic = re.findall(bicRegex, req.text)[0]
iban = re.findall(ibanRegex, req.text)[0]



print(name)
print(address)
print(city)
print(bic)
print(iban)

