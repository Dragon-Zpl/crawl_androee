import re

import requests
from lxml import etree
# r = requests.get(url='https://www.androeed.ru/files/intro-maker-dlya-youtube-sozdatel-videorolikov.html?hl=en')
test = """
$('#images_while').load('/index.php?m=files&f=images_while&id=8525&youtube=9uXNn1AKon0" ');$(
"""

# print(r.status_code)
# content = etree.HTML(r.text)
host = "https://www.androeed.ru"
img_urls = re.findall(r"\('#images_while'\)\.load[\d\D]+?\)",test)
print(img_urls)
img_url = img_urls[0].replace("('#images_while').load('","").replace("\" ')","").replace("')","")
print(img_url)
# print(img_urls)
# data_dic = {}
# if len(img_urls) > 0:
#     try:
#         print(img_urls)
#         img_url = img_urls[0].replace("('#images_while').load('","").replace("\" ')","")
#         print(img_url)
#         r = requests.get(url=host + img_url)
#         print(r.status_code)
#         img_content = etree.HTML(r.text)
#         if img_content.xpath("//img/@src"):
#             data_dic["img_urls"] = ','.join(img_content.xpath("//img/@src"))
#     except Exception as e :
#         print("error:{},img_url:{}".format(e,str(img_urls)))
#
#
# print(data_dic)
#

