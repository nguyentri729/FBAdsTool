import requests
import time
import re

ibanRegex = r'title="Click To Copy">(.*)</span></span> \(<a href="#"'
bicRegex = r'<th scope="row">BIC</th>\n<td class="copy"><span data-toggle="tooltip" data-placement="top" title="Click To Copy">(.*)</span></td>'
nameRegex =  r'<th scope="row">Name</th>\n<td class="copy"><span data-toggle="tooltip" data-placement="top" title="Click To Copy">(.*)</span></td>'
addressRegex =  r'<th scope="row">Address</th>\n<td class="copy"><span data-toggle="tooltip" data-placement="top" title="Click To Copy">(.*)</span></td>'
cityRegex =  r'<th scope="row">City</th>\n<td class="copy"><span data-toggle="tooltip" data-placement="top" title="Click To Copy">(.*)</span></td>'
zipRegex =  r'<th scope="row">Postcode</th>\n<td class="copy"><span data-toggle="tooltip" data-placement="top" title="Click To Copy">(.*)</span></td>'
req = requests.get('https://fake-it.ws/it/')
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
    'zipcode': zipcode,
    'bic': bic,
    'iban': iban
})
