# import asyncio
# import re
#
# import requests
#
# from helper import Helper
#
# data = [
#     {'name': 'Castle Cats', 'what_news': 'Mod Money', 'icon': 'https://i1.androeed.ru/icons/2019/03/31/w_160_14555.png',
#      'categories': 'Arcade,Сlickers,RPG,Squad to squad', 'version': ' 2.5', 'os': 'Android 4.2 or above',
#      'internet': 'Required', 'size': '89 Mb', 'raiting': ' 4.8', 'russian': 'Present',
#      'img_urls': 'https://i1.androeed.ru/screens/2018/10/26/666132.png,https://i1.androeed.ru/screens/2018/10/26/666133.png,https://i1.androeed.ru/screens/2018/10/26/666134.png,https://i1.androeed.ru/screens/2018/10/26/666135.png,https://i1.androeed.ru/screens/2018/10/26/666136.png',
#      'description': "Create your own guild of brave warriors in the castle of cats! Collect legendary heroes and adventurous adventurers - control your guild and send them to an epic adventure to collect rewards! But be careful - the darkness of the Evil Pugomancer in spreads like a forest fire, and it's your mission to save the kingdom of Catania! Эту игру можно скачать в официальном Google Play Маркет.",
#      'app_url': 'https://www.androeed.ru/files/castle-cats-mod-mnogo-deneg.html?hl=en',
#      'download_first_url': ['http://s36.androeed.ru/files/2019/03/31/Castle_Cats_-1554024963-www.androeed.ru.apk']},
#     {'name': 'Hill Climb Racing 2', 'icon': 'https://i1.androeed.ru/icons/2018/11/15/w_160_16127.png',
#      'categories': 'Arcade,Cars,Racing', 'version': ' 1.24.2', 'os': 'Android 4.2 or above', 'internet': 'Not required',
#      'size': '82.76 Mb', 'raiting': ' 4.6', 'russian': 'Present',
#      'img_urls': 'https://i1.androeed.ru/screens/2018/08/03/662055.png,https://i1.androeed.ru/screens/2018/08/03/662056.png,https://i1.androeed.ru/screens/2018/08/03/662057.png,https://i1.androeed.ru/screens/2018/08/03/662058.png,https://i1.androeed.ru/screens/2018/08/03/662059.png',
#      'description': 'Hill Climb Racing 2 is back! Bill returned to the red jeep in the continuation of the most popular racing game in Google Play with more than 500 million total downloads! The Hill Climb Racing 2 has it all: a plurality of stages, improved graphics and a more modern physics engine. Dozens of different options for your car. Update the engine, tires, suspension, chassis, change the color - the list is endless! Эту игру можно скачать в официальном Google Play Маркет.',
#      'app_url': 'https://www.androeed.ru/files/hill-climb-racing-2_.html?hl=en', 'download_first_url': [
#         'http://s37.androeed.ru/files/2019/03/26/Hill_Climb_Racing_2_-1553612093-www.androeed.ru.apk']},
# {'name': "PewDiePie's Tuber Simulator",  'icon': 'https://i1.androeed.ru/icons/2019/03/30/w_160_15919.png', 'download_first_url': ['http://s42.androeed.ru/files/2019/03/30/PewDiePies_Tuber_Simulator_-1553936520-www.androeed.ru.apk','http://s41.androeed.ru/files/2019/03/30/PewDiePies_Tuber_Simulator_-1553936709-www.androeed.ru.zip']}
#
#
# ]
# #
# #
from helper import Helper
# #
Helper.build_download_task(data_dic={'name': "PewDiePie's Tuber Simulator",  'icon': 'https://i1.androeed.ru/icons/2019/03/30/w_160_15919.png', 'download_first_url': ['http://s42.androeed.ru/files/2019/03/30/PewDiePies_Tuber_Simulator_-1553936520-www.androeed.ru.apk','http://s41.androeed.ru/files/2019/03/30/PewDiePies_Tuber_Simulator_-1553936709-www.androeed.ru.zip']})
# loop = asyncio.get_event_loop()
# tasks = []
# for i in data:
#     task = Helper.build_download_task(data_dic=i)
#     tasks.append(task)
#
# loop.run_until_complete(asyncio.wait(tasks))
# import hashlib
#
# 
# def Filemd5(filepath):
#     fp = open(filepath, 'rb')
#     md5_obj = hashlib.md5()
#     while True:
#         tmp = fp.read(8096)
#         if not tmp:
#             break
#         md5_obj.update(tmp)
#     hash_code = md5_obj.hexdigest()
#     fp.close()
#     md5 = str(hash_code).lower()
#     return md5