import logging.config

import lxml.html
import aiohttp
import socket, asyncio
import redis
import yaml

from Mysql_.mysql_op import MysqlHeaper

etree = lxml.html.etree
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
}
conn = aiohttp.TCPConnector(
                            family=socket.AF_INET,
                            verify_ssl=False,
                            use_dns_cache=True
                            )
session = aiohttp.ClientSession(connector=conn)
loop = asyncio.get_event_loop()

# pool = redis.ConnectionPool(host='23.236.115.226', password="weiphone", port=6379, db=11)
# rcon = redis.Redis(connection_pool=pool)
with open('./config/config.yaml', 'r') as fr:
    config_file = yaml.load(fr)
redis_topic = config_file["redis_topic"]["test"]
logging.config.dictConfig(config_file['logger'])
logger = logging.getLogger('project')

loop.run_until_complete(MysqlHeaper().get_pool())

SCREENSTORE = "/home/feng/android_files1/androee_files/picture/coverimg/"
ICONSTORE = "/home/feng/android_files1/androee_files/picture/screenshot/"
PKGSTORE = "/home/feng/android_files1/androee_files/app_page/"