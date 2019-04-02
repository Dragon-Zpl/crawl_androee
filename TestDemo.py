url = 'https://www.androeed.ru/files/mx-player-pro.html?hl=en'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
}
import requests
r = requests.get(url=url,headers=headers)
print('stasu:'+str(r.status_code))