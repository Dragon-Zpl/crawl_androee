# _*_ coding: utf-8 _*_
import datetime
import logging.config
import aiomysql, yaml

class MysqlHeaper(object):
    fr = open('./config/config.yaml', 'r')
    config_file = yaml.load(fr)
    """
    异步mysql class
    """
    def __init__(self,pool):
        self.pool = pool
    async def get_pool(self, loop=None, config='mysql'):

        local_mysql_config = self.config_file[config]
        self.pool = await aiomysql.create_pool(host=local_mysql_config["host"], port=local_mysql_config["port"],
                                               user=local_mysql_config["user"], password=local_mysql_config["password"],
                                               db=local_mysql_config["database"], loop=loop,
                                               charset=local_mysql_config["charset"], autocommit=True)
        return self

    async def insert_update_app(self,data_dic):
        try:
            sql = """
                insert into crawl_androeed_app_info(app_size,category, coverimgurl, currentversion, description,developer,whatsnew,last_update_date,minimum_os_version,name,screenshots,url,pkgname) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                     ON DUPLICATE KEY UPDATE app_size=VALUES(app_size), category=VALUES(category), coverimgurl=VALUES(coverimgurl), currentversion=VALUES(currentversion), url=VALUES(url), description=VALUES(description), developer=VALUES(developer), whatsnew=VALUES(whatsnew)
                                     , last_update_date=VALUES(last_update_date), minimum_os_version=VALUES(minimum_os_version), name=VALUES(name), screenshots=VALUES(screenshots), pkgname=VALUES(pkgname)
            """
            nowtime = (datetime.datetime.now() + datetime.timedelta(hours=13)).strftime("%Y-%m-%d %H:%M:%S")
            params = (
                data_dic["size"],data_dic["categories"],data_dic["icon"],data_dic["version"].strip(' '),data_dic["description"],
                data_dic["developer"],data_dic["what_news"],nowtime,data_dic["os"],data_dic["name"],data_dic["img_urls"],data_dic["app_url"],data_dic["pkgname"]
            )
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    results = await cur.execute(sql, params)
                    return results
        except Exception as e:
            print("{}".format(e))
            await self.get_pool()
            return None

    async def check_version(self,data):
        sql = 'select currentversion from crawl_androeed_app_info where name=\'{}\''.format(data["name"])
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(sql)
                    recond = await cur.fetchone()
                    if recond:
                        print("name:{},now:{},sql:{}".format(data["name"],data["version"],recond))
                        if recond[0] != data["version"]:
                            return data
                        else:
                            return None
                    else:
                        return data
                except Exception as e:
                    print(e)
                    return None

    async def insert_update_apk(self,data_dic):
        try:
            sql = """
                insert into crawl_androeed_apk_info(pkg_name,version_code, file_path, file_sha1, last_update_date) VALUES (%s,%s,%s,%s,%s)
                                     ON DUPLICATE KEY UPDATE pkg_name=VALUES(pkg_name), version_code=VALUES(version_code), file_path=VALUES(file_path), file_sha1=VALUES(file_sha1), last_update_date=VALUES(last_update_date)
            """
            nowtime = (datetime.datetime.now() + datetime.timedelta(hours=13)).strftime("%Y-%m-%d %H:%M:%S")
            params = (
                data_dic["pkgname"],data_dic["version"],data_dic["file_path"],data_dic["md5"],nowtime
            )
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    results = await cur.execute(sql, params)
                    return results
        except Exception as e:
            print("{}".format(e))
            await self.get_pool()
            return None

    async def insert_update_icon(self,data):
        try:
            sql = """
                              insert into crawl_androeed_coverimg(url,coverimg_path,romote_url,type,is_success_downland,need_update,create_date) VALUES (%s,%s,%s,%s,%s,%s,%s)
                             ON DUPLICATE KEY UPDATE coverimg_path=VALUES(coverimg_path), type=VALUES(type), is_success_downland=VALUES(is_success_downland), need_update=VALUES(need_update)
                            """
            nowtime = (datetime.datetime.now() + datetime.timedelta(hours=13)).strftime("%Y-%m-%d %H:%M:%S")
            params = (
                data["app_url"],data["icon_path"],data["icon"],"png", b'1', b'0',nowtime
            )
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    results = await cur.execute(sql, params)
                    return results
        except Exception as e:
            print("{}".format(e))
            await self.get_pool()
            return None

    async def insert_update_screen(self, data):
        try:
            sql = """
                              insert into crawl_androeed_screenshots(url,screenshot_path,romote_url,type,is_success_downland,need_update,create_date,update_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                          ON DUPLICATE KEY UPDATE screenshot_path=VALUES(screenshot_path), type=VALUES(type), is_success_downland=VALUES(is_success_downland), need_update=VALUES(need_update),update_date=VALUES (update_date)
                            """
            create_time = (datetime.datetime.now() + datetime.timedelta(hours=13)).strftime("%Y-%m-%d %H:%M:%S")
            update_time = (datetime.datetime.now() + datetime.timedelta(hours=13)).strftime("%Y-%m-%d %H:%M:%S")
            params = (
                data["app_url"],data["screen_path"],data["img_urls"],'png', b'1', b'0', create_time, update_time
            )
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    results = await cur.execute(sql, params)
                    return results
        except Exception as e:
            print("{}".format(e))
            await self.get_pool()
            return None

    async def fetch_one(self,sql):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(sql)
                    recond = await cur.fetchone()
                    if recond:
                        return True
                    else:
                        return None
                except Exception as e:
                    print(e)
                    return None

    async def fetch_all(self, sql, params=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(sql, params)
                    reconds = await cur.fetchall()
                    return reconds
                except Exception as e:
                    print(e)
                    return None
