import re

import requests
from lxml import etree
r = requests.get(url='https://www.androeed.ru/files/downhill-masters.html?hl=en')

content = etree.HTML(r.text)
host = "https://www.androeed.ru"
img_urls = re.findall(r"load[\d\D]+?\" \'\)",r.text)
data_dic = {}
if len(img_urls) > 0:
    try:
        print(img_urls)
        img_url = img_urls[0].replace("load('", "").replace("\" ')", "")
        print(img_url)
        r = requests.get(url=img_url + host)
        print(r.status_code)
        img_content = etree.HTML(r.text)
        if img_content.xpath("//img/@src"):
            data_dic["img_urls"] = ','.join(img_content.xpath("//img/@src"))
    except Exception as e :
        print("error:{},img_url:{}".format(e,str(img_urls)))


print(data_dic)