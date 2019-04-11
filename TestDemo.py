
import asyncio

import aiomysql
import yaml

from Mysql_.mysql_op import MysqlHeaper
async def get_pool(loop=None, config='mysql'):
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
sql = "select * from crawl_androeed_app_info WHERE url=\'{}\'".format("https://www.androeed.ru/files/homescapes.html?hl=en")
print(loop.run_until_complete(mysql_op.fetch_all(sql)))


