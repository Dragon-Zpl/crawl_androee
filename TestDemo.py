import asyncio

import aiomysql
import yaml

from Mysql_.mysql_op import MysqlHeaper


async def get_pool( loop=None, config='mysql'):
    fr = open('./config/config.yaml', 'r')
    config_file = yaml.load(fr)
    local_mysql_config = config_file[config]
    pool = await aiomysql.create_pool(host=local_mysql_config["host"], port=local_mysql_config["port"],
                                           user=local_mysql_config["user"], password=local_mysql_config["password"],
                                           db=local_mysql_config["database"], loop=loop,
                                           charset=local_mysql_config["charset"], autocommit=True)
    return pool


loop = asyncio.get_event_loop()
pool = loop.run_until_complete(get_pool())
mysql_op = MysqlHeaper(pool=pool)
data = {'name': 'My Talking Tom 2', 'what_news': 'Mod Money', 'icon': 'https://i1.androeed.ru/icons/2018/11/08/w_160_22558.png', 'categories': 'Arcade,For kids,Simulators', 'version': '1.3.1.366', 'os': 'Android 4.1 or above', 'size': '98.9 Mb', 'img_urls': 'https://i1.androeed.ru/screens/2018/09/30/664903.png,https://i1.androeed.ru/screens/2018/09/30/664904.png,https://i1.androeed.ru/screens/2018/09/30/664905.png,https://i1.androeed.ru/screens/2018/09/30/664906.png,https://i1.androeed.ru/screens/2018/09/30/664907.png', 'description': "You have a great opportunity to get a new friend! As in the first part of  My Talking Tom, you have to take care of a little kitten and watch, so he grew up in a comfortable environment. Feed him, play with him, care for him and surround him with care and attention. Be careful and make sure that Tom does not get sick and hurt himself!   In this part of the game, new interesting mini-games, new food, clothes and furniture for your beloved pet are prepared for you.  Download for free on Android My Talking Tom 2 and have a great time with your new friend. Now you can take Tom in your arms, twist it, drop it, put it on a bed and even on a plane. Yes, yes, now Tom has his own plane, and he can also get his pet. There are 5 of the same cute and funny animals, like the\xa0talking Tom. Observe how they communicate with each other or spend time with Tom's pet.  My Talking Volume 2 - is great fun for the whole family! Эту игру можно скачать в официальном Google Play Маркет.", 'app_url': 'https://www.androeed.ru/files/my-talking-tom-2.html?hl=en', 'download_first_url': ['http://s45.androeed.ru/files/2019/03/31/moy_govoryaschiy_tom_2_-1554042908-www.androeed.ru.apk']}
loop.run_until_complete(mysql_op.update_version(data))