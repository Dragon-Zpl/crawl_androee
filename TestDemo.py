import requests

r = requests.get("https://androeed.net/download/files/90596.php")

print(r.text)