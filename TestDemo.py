# import datetime
#
# import aiomysql
#
# data_dic = {'name': 'Google Photos', 'what_news': '', 'icon': 'https://i1.androeed.ru/icons/2018/08/17/w_160_8396.png', 'categories': 'Multimedia', 'version': ' 4.13.0', 'os': 'Depends on the device', 'internet': 'Required', 'size': '53.65 Mb', 'raiting': ' 4.5', 'russian': 'Present', 'img_urls': 'https://i1.androeed.ru/screens/2018/07/09/659966.png,https://i1.androeed.ru/screens/2018/07/09/659967.png,https://i1.androeed.ru/screens/2018/07/09/659968.png,https://i1.androeed.ru/screens/2018/07/09/659969.png,https://i1.androeed.ru/screens/2018/07/09/659970.png', 'description': 'Google Photo - online photo storage.\xa0Incredibly handy and useful tool that allows you to store all your photos, pictures and images on Google\'s servers, without fear that they will be gone somewhere else. The application will be indispensable for those who regularly change the device and does not want to wind up with a long and tedious transfer of content, or for those who do not like to store data on your phone (for security reasons or a small amount of physical space).\xa0Well, a real boon for those who like to travel would be a function of "assistant". The app will automatically make a selection at the place and time of creating a full photo album with pictures by placing them in chronological order with geographical marks. Do not forget to download Google Maps before your trip!\xa0By passing alia, Photo Service has a built-in photo editor and allows you to create collages, collections and compilations. Это приложение можно скачать в официальном Google Play Маркет.', 'app_url': 'https://www.androeed.ru/files/foto.html?hl=en', 'download_first_url': ['http://s40.androeed.ru/files/2019/03/27/Google_Photo_foto-1553713474-www.androeed.ru.apk'], 'md5': '0ca36a3ee23dae6e2658bccc56a99540', 'file_path': '/home/feng/pkgtest/39904b13c9433462b2148e4d154f5fb8.apk', 'pkgname': 'com.google.android.apps.photos', 'developer': 'Google LLC'}
#
# from Mysql_.mysql_op import MysqlHeaper
#
# from utils.init import *
#
#
# class test:
#     async def get_pool(self,loop=None, config='mysql'):
#         fr = open('./config/config.yaml', 'r')
#         config_file = yaml.load(fr)
#         local_mysql_config = config_file[config]
#         self.pool = await aiomysql.create_pool(host=local_mysql_config["host"], port=local_mysql_config["port"],
#                                                user=local_mysql_config["user"], password=local_mysql_config["password"],
#                                                db=local_mysql_config["database"], loop=loop,
#                                                charset=local_mysql_config["charset"], autocommit=True)
#         return self
#     async def save_mysql(self,params):
#         try:
#             sql = """
#                 insert into crawl_androeed_apk_info(pkgname,name, md5, is_delete, update_time,category,app_size,developer,file_path,icon_path,whatsnew,version,os,internet,raiting,russian,img_urls,description,url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#                                      ON DUPLICATE KEY UPDATE md5=VALUES(md5), is_delete=VALUES(is_delete), file_path=VALUES(file_path), description=VALUES(description), url=VALUES(url), update_time=VALUES(update_time), img_urls=VALUES(img_urls), version=VALUES(version)
#                                      , os=VALUES(os), app_size=VALUES(app_size), category=VALUES(category), icon_path=VALUES(icon_path), whatsnew=VALUES(whatsnew), name=VALUES(name)
#             """
#             async with self.pool.acquire() as conn:
#                 async with conn.cursor() as cur:
#                     results = await cur.execute(sql, params)
#                     return results
#         except Exception as e:
#             logger.error("{} {}".format(e,params))
#             await self.get_pool()
#             return None
#     def run(self):
#         loop.run_until_complete(self.get_pool())
#         nowtime = (datetime.datetime.now() + datetime.timedelta(hours=13)).strftime("%Y-%m-%d %H:%M:%S")
#         params = ('', '','', 0, '2019-04-04 16:59:50', 'Clash of Clans,Strategy', '99 Mb', '', '',
#          'https://i1.androeed.ru/icons/2019/04/02/w_160_2096.png', '', ' 11.446.11', 'Android 4.1 or above', 'Required',
#          ' 4.6', 'Present',
#          'https://i1.androeed.ru/screens/2019/04/02/674510.png,https://i1.androeed.ru/screens/2019/04/02/674511.png,https://i1.androeed.ru/screens/2019/04/02/674512.png,https://i1.androeed.ru/screens/2019/04/02/674513.png',
#          'Debut work of the studio Supercell - the game Clash of Clans, which literally translates as "Clash of Clans", instantly captured the Play Market, rising to the top of strategic games in a short time and collected more than 10 million downloads around the world. Game Clash of Clans for Android can be attributed to the ancestor of such strategic games, with which, as it usually happens, other developers have started to make numerous clones.Game Clash of Clans contains two main points. The first is the development and arrangement of your own base and the erection of fortifications that will protect you from the invasion of enemies. And the second - the military development of his camp, hiring units to attack and capture enemy resources.Clash of Clans for Android is completely free, but contains donat. In other words, for real money you can buy game valuesFeaturesFeatures:A completely free strategyOnline battle with players around the worldCombine with other players in alliances14 unique units with multiple update levelsA wide range of buildings for protection: guns, towers, mortars, bombs, traps and walls Эту игру можно скачать в официальном Google Play Маркет.',
#          'https://www.androeed.ru/files/clash-of-clans.html?hl=en')
#         loop.run_until_complete(self.save_mysql(params))
# t = test()
# t.run()

import requests
# https://www.androeed.ru/index.php?m=files&f=load_commen_ebu_v_rot_dapda&ui=10655,status:404