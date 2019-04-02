url = 'https://www.androeed.ru/files/mx-player-pro.html?hl=en'

import requests
r = requests.get(url=url)
print('stasu:'+str(r.status_code))