# _*_ coding: utf-8 _*_
import logging.config
import aiomysql, yaml


class MysqlHeaper(object):
    fr = open('./config/config.yaml', 'r')
    config_file = yaml.load(fr)
    logging.config.dictConfig(config_file['logger'])
    logger = logging.getLogger('mysql')
    """
    异步mysql class
    """

    async def get_pool(self, loop=None, config='mysql'):

        local_mysql_config = self.config_file[config]
        self.pool = await aiomysql.create_pool(host=local_mysql_config["host"], port=local_mysql_config["port"],
                                               user=local_mysql_config["user"], password=local_mysql_config["password"],
                                               db=local_mysql_config["database"], loop=loop,
                                               charset=local_mysql_config["charset"], autocommit=True)
        return self

    async def insert_into(self, sql, params):
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    results = await cur.execute(sql, params)
                    return results
        except Exception as e:
            self.logger.error("{} {}".format(e,params))
            await self.get_pool()
            return None

    async def fetch_all(self, sql, params):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(sql, params)
                    reconds = await cur.fetchall()
                    return reconds
                except Exception as e:
                    print(e)
                    return None

    async def fetch_one(self, sql, params=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(sql, params)
                    recond = await cur.fetchone()
                    return recond
                except Exception as e:
                    print(e)
                    return None

    async def update(self, sql, params):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    reconds = await cur.execute(sql, params)
                    return reconds
                except Exception as e:
                    print(e)
                    return None

    async def execute(self, sql):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    reconds = await cur.execute(sql)
                    return reconds
                except Exception as e:
                    print(e)
                    return None

    def close_pool(self):
        self.pool.close()
