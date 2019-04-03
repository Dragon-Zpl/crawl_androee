import requests

b = 'https://www.androeed.ru/files/karta-rossii-dlya-navitel.html?hl=en'

r = requests.get(url=b)

from lxml import etree

co = etree.HTML(r.text)

print(co.xpath("//a[@class='google_play round5']/@href"))

print('2:'+str(co.xpath("//div[@class='c in_holder']/img/@src")))