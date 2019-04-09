import requests
from lxml import etree
r = requests.get("https://androeed.net/download/files/90596.php")

b = etree.HTML(r.text)

print(b.xpath("//div[@class='c']/a[@class='download round30']/@href"))