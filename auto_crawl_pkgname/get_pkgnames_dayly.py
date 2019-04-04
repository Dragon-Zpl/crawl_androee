import asyncio
from random import choice
import re

import requests

from Analysis_data.Xpath_word import Xpaths
from CrawlProxy.crawl_proxies import asyncCrawlProxy
from Mysql_.mysql_op import MysqlHeaper
from helper import Helper
from utils.init import *

class CrawlPkgnames:
    def __init__(self):
        self.mods_urls = ["https://www.androeed.ru/files/vzlomannie_igri_na_android-" + str(page) + ".html?hl=en" for page in range(1,6)]
        self.host = "https://www.androeed.ru"
        self.app_url = "https://www.androeed.ru/android/programmy.html?hl=en"
        # 包的下载地址在该接口下
        self.mod_pkg_url = "https://www.androeed.ru/index.php?m=files&f=load_commen_ebu_v_rot_dapda&ui="
        self.flag = 1
        self.lock = asyncio.Lock(loop=loop)
        self.crawlProxy = asyncCrawlProxy()
        self.analysis = Xpaths()
        self.pkg_urls = set()
        self.mysql_op = MysqlHeaper()
        self.proxies = []
    async def request_web(self,url,proxy=None):
        for i in range(3):
            try:
                async with session.get(url=url, proxy=proxy, headers=headers, timeout=15) as r:
                    logger.info("url:{},status:{}".format(url,r.status))
                    if r.status in [200, 201]:
                        data = await r.text()
                        return data
                    elif r.status in [403, 400, 500, 502, 503, 429]:
                        proxy = await self.get_proxy()
                    else:
                        logger.info(url+",status:"+str(r.status))
                        return None
            except Exception as e:
                logger.info("url:{},error:{}".format(url,e))
                proxy = await self.get_proxy()
        else:
            logger.info('fail 3 time3,checkout please!url:{}'.format(url))
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

    async def analysis_data(self,data):
        content = etree.HTML(data)
        data_dic = {}
        name = content.xpath(self.analysis.pkg_name)
        if name and '[' in name[0]:
            data_dic["name"] = re.search(r'[\d\D]*\[', name[0]).group().replace(' [', "")
            data_dic["what_news"] = re.search("\[[\d\D]+?\]",name[0]).group().replace('[','').replace(']','')
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
        img_urls = re.findall(r"\('#images_while'\)\.load[\d\D]+?\)", data)
        if len(img_urls) > 0:
            try:
                img_url = img_urls[0].replace("('#images_while').load('","").replace("\" ')","").replace("')","")
                data = await self.request_web(url=self.host + img_url)
                if data:
                    img_content = etree.HTML(data)
                    if img_content.xpath(self.analysis.img_urls):
                        data_dic["img_urls"] = ','.join(img_content.xpath(self.analysis.img_urls))
                else:
                    logger.info('img_url:'+img_url)
                    data_dic["img_urls"] = "None"
            except Exception as e :
                logger.info("error:{},img_urls:{}".format(e,str(img_urls)))
        else:
            data_dic["img_urls"] = "None"
        data_dic["description"] = ''.join(content.xpath(self.analysis.description))
        data_dic["app_url"] = content.xpath(self.analysis.app_url)[0]

        mod_nuber = content.xpath(self.analysis.mod_number2)
        if mod_nuber:
            temp = re.findall("\d+", mod_nuber[-1])
            if temp:
                pass
            else:
                mod_nuber = content.xpath(self.analysis.mod_number1)
        if mod_nuber:
            temp = re.findall("\d+",mod_nuber[-1])
            if temp:
                download_url = temp[-1]
                logger.info('download_url:'+str(download_url))
                data = await self.request_web(url=self.mod_pkg_url+download_url)
                if data:
                    mod_content = etree.HTML(data)
                    # data_dic["download_first_url"] = mod_content.xpath(self.analysis.download_first_url)[-1]
                    download_url_len = len(mod_content.xpath(self.analysis.download_first_url))
                    if download_url_len ==1 or download_url_len ==2:
                        temp_apk_download_url = mod_content.xpath(self.analysis.download_first_url)[-1]
                        data = await self.request_web(url=temp_apk_download_url)
                        temp_apk_download_url_data = etree.HTML(data)
                        apk_download_url = temp_apk_download_url_data.xpath(self.analysis.pkg_download_url)[0]
                        data_dic["download_first_url"] = [apk_download_url]
                    elif download_url_len == 3:
                        # 第一个为破解包，第二个为apk包
                        temp_apk_download_url = mod_content.xpath(self.analysis.download_first_url)[-2]
                        data = await self.request_web(url=temp_apk_download_url)
                        temp_apk_download_url_data = etree.HTML(data)
                        apk_download_url = temp_apk_download_url_data.xpath(self.analysis.pkg_download_url)[0]
                        temp_obb_download_url = mod_content.xpath(self.analysis.download_first_url)[-1]
                        data = await self.request_web(url=temp_obb_download_url)
                        temp_obb_download_url_data = etree.HTML(data)
                        obb_download_url = temp_obb_download_url_data.xpath(self.analysis.pkg_download_url)[0]
                        data_dic["download_first_url"] = [apk_download_url,obb_download_url]
                    elif download_url_len == 4:
                        temp_apk_download_url = mod_content.xpath(self.analysis.download_first_url)[-2]
                        data = await self.request_web(url=temp_apk_download_url)
                        temp_apk_download_url_data = etree.HTML(data)
                        apk_download_url = temp_apk_download_url_data.xpath(self.analysis.pkg_download_url)[0]
                        data_dic["download_first_url"] = [apk_download_url]
                    else:
                        data_dic["download_first_url"] = "None"
                        logger.info('长度有问题请查看'+data_dic["app_url"])
                else:
                    data_dic["download_first_url"] = "None"
            else:
                data_dic["download_first_url"] = "None"
                logger.info('is questsion:'+data_dic["app_url"]+":"+str(mod_nuber)+','+str(temp))
        else:
            logger.info('没有的url：'+ data_dic["app_url"]+str(mod_nuber))
            data_dic["download_first_url"] = "None"
        logger.info(data_dic)
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

        data_tasks = []

        for result in detail_results:
            if result:
                task = asyncio.ensure_future(self.analysis_data(data=result))
                data_tasks.append(task)

        results = loop.run_until_complete(asyncio.gather(*data_tasks))

        # for result in requests:
        #     Helper.build_download_task()
        # sql = """
        #     insert into crawl_androeed_app_info(pkg_name, file_sha1, is_delete, file_path, create_time, update_time) VALUES (%s,%s,%s,%s,%s,%s)
        #                          ON DUPLICATE KEY UPDATE file_sha1=VALUES(file_sha1), is_delete=VALUES(is_delete), file_path=VALUES(file_path), update_time=VALUES(update_time)
        # """
        #
        # for data in all_data:
        #     params = ()
        #     task = asyncio.ensure_future(self.mysql_op.update(sql,params=params))