import re

import requests

b = 'https://www.androeed.ru/files/google-play-market.html?hl=en'

r = requests.get(url=b)

from lxml import etree

content = etree.HTML(r.text)

mod_nuber = content.xpath("//a[@class='google_play round5']/@href")
print(mod_nuber)
if mod_nuber:
    temp = re.findall("\d+", mod_nuber[-1])
    if temp:
        pass
    else:
        print('i comein')
        mod_nuber = content.xpath("//div[@class='c in_holder']/img/@data-src")
        print(mod_nuber)
if mod_nuber:
    temp = re.findall("\d+",mod_nuber[-1])
    if temp:
        download_url = temp[-1]
        print('download_url:'+str(download_url))
