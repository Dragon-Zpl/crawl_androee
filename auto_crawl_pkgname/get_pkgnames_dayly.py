import asyncio
from random import choice
import re
from Analysis_data.Xpath_word import Xpaths
from CrawlProxy.crawl_proxies import asyncCrawlProxy
from Mysql_.mysql_op import MysqlHeaper
from utils.init import *

class CrawlPkgnames:
    def __init__(self):
        self.mods_urls = ["https://www.androeed.ru/files/vzlomannie_igri_na_android-" + str(page) + ".html?hl=en" for page in range(1,6)]
        self.host = "https://www.androeed.ru"
        self.app_url = "https://www.androeed.ru/android/programmy.html?hl=en"
        self.flag = 1
        self.lock = asyncio.Lock(loop=loop)
        self.crawlProxy = asyncCrawlProxy()
        self.analysis = Xpaths()
        self.pkg_urls = set()
        self.download_urls =set()
        self.mysql_op = MysqlHeaper()
        self.proxies = []
    async def request_web(self,url,proxy=None):
        for i in range(3):
            try:
                async with session.get(url=url, proxy=proxy, headers=headers, timeout=15) as r:
                    if r.status in [200, 201]:
                        data = await r.text()
                        return data
                    elif r.status in [403, 400, 500, 502, 503, 429]:
                        proxy = await self.get_proxy()
                    else:
                        logger.info(url+",status:"+str(r.status))
                        return None
            except Exception as e:
                logger.info(e)
                proxy = await self.get_proxy()
        else:
            logger.info('fail 3 time3,checkout please!')
    async def get_proxy_pool(self):
        async with self.lock:
            if len(self.proxies) <= 3:
                self.proxies = await self.crawlProxy.run(session)

    async def get_proxy(self):
        if len(self.proxies) < 3:
            await self.get_proxy_pool()
        try:
            proxy = choice(self.proxies)
        except:
            await self.get_proxy_pool()
            proxy = choice(self.proxies)
        return proxy


    def build_async_tasks(self):
        tasks = []
        if self.flag == 1:
            for url in self.mods_urls:
                task = asyncio.ensure_future(self.request_web(url=url),loop=loop)
                tasks.append(task)
                self.flag += 1
        else:
            task = asyncio.ensure_future(self.request_web(url=self.mods_urls[0]),loop=loop)
            tasks.append(task)
        task = asyncio.ensure_future(self.request_web(url=self.app_url),loop=loop)
        tasks.append(task)
        return tasks

    def get_app_urls(self,data):
        content = etree.HTML(data)
        urls = content.xpath(self.analysis.get_app_urls)
        for url in urls:
            self.pkg_urls.add(self.host + url)

    def analysis_data(self,data):
        content = etree.HTML(data)
        data_dic = {}
        name = content.xpath(self.analysis.pkg_name)
        if name and '[' in name:
            data_dic["name"] = re.search(r'.+?\[', name[0]).group().replace(' [', "")
        elif name:
            data_dic["name"] = name[0]
        else:
            data_dic["name"] = ""
        data_dic["icon"] = content.xpath(self.analysis.icon)[0]
        data_dic["categories"] = ','.join(content.xpath(self.analysis.categories))
        data_dic["version"] = content.xpath(self.analysis.version)[0]
        data_dic["os"] = content.xpath(self.analysis.os)[0]
        data_dic["internet"] = content.xpath(self.analysis.internet)[0]
        data_dic["size"] = content.xpath(self.analysis.size)[0]
        data_dic["raiting"] = content.xpath(self.analysis.raiting)[0]
        data_dic["russian"] = content.xpath(self.analysis.russian)[0]
        data_dic["img_urls"] = ','.join(content.xpath(self.analysis.img_urls))
        data_dic["description"] = ''.join(content.xpath(self.analysis.description))
        data_dic["download_first_url"] = content.xpath(self.analysis.download_first_url)[-1]
        data_dic["app_url"] = content.xpath(self.analysis.app_url)[0]
        self.download_urls.add(data_dic["download_first_url"])
        return data_dic
    def build_detail_tasks(self):
        tasks = []
        for url in self.pkg_urls:
            task = asyncio.ensure_future(self.request_web(url=url),loop=loop)
            tasks.append(task)
        return tasks
    def run(self):
        self.pkg_urls.clear()
        logger.info('start crawl ...')
        tasks = self.build_async_tasks()
        results = loop.run_until_complete(asyncio.gather(*tasks))
        for result in results:
            self.get_app_urls(result)
        logger.info('pkg_urls:'+str(self.pkg_urls))
        detail_tasks = self.build_detail_tasks()
        detail_results = loop.run_until_complete(asyncio.gather(*detail_tasks))

        all_data = []

        for result in detail_results:
            data = self.analysis_data(data=result)
            print(data)
            all_data.append(data)

        # sql = """
        #     insert into crawl_androeed_app_info(pkg_name, file_sha1, is_delete, file_path, create_time, update_time) VALUES (%s,%s,%s,%s,%s,%s)
        #                          ON DUPLICATE KEY UPDATE file_sha1=VALUES(file_sha1), is_delete=VALUES(is_delete), file_path=VALUES(file_path), update_time=VALUES(update_time)
        # """
        #
        # for data in all_data:
        #     params = ()
        #     task = asyncio.ensure_future(self.mysql_op.update(sql,params=params))