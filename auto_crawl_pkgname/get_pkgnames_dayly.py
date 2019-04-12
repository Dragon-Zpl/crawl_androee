import asyncio
import datetime
import hashlib
import os
from random import choice
import re

import aiomysql
import requests

from Analysis_data.Xpath_word import Xpaths
from CrawlProxy.crawl_proxies import asyncCrawlProxy
from Mysql_.mysql_op import MysqlHeaper
from helper import Helper
from postinterface import PostModData
from utils.init import *
from send_email import SMTP
class CrawlPkgnames:
    def __init__(self):
        self.mods_urls = ["https://www.androeed.ru/files/vzlomannie_igri_na_android-" + str(page) + ".html?hl=en" for page in range(1,6)]
        self.host = "https://www.androeed.ru"
        self.app_url = "https://www.androeed.ru/android/programmy.html?hl=en"
        # 包的下载地址在该接口下
        self.mod_pkg_url = "https://www.androeed.ru/index.php?m=files&f=load_comm_dapda_otsosal_2_raza&ui="
        self.flag = 1
        self.lock = asyncio.Lock(loop=loop)
        self.crawlProxy = asyncCrawlProxy()
        self.analysis = Xpaths()
        self.pkg_urls = set()
        pool = loop.run_until_complete(self.get_pool())
        self.mysql_op = MysqlHeaper(pool=pool)
        self.proxies = []
        self.bad_pkg_url = set()
        self.post_data = PostModData()

    async def get_pool(self, loop=None, config='mysql'):
        fr = open('./config/config.yaml', 'r')
        config_file = yaml.load(fr)
        local_mysql_config = config_file[config]
        self.pool = await aiomysql.create_pool(host=local_mysql_config["host"], port=local_mysql_config["port"],
                                               user=local_mysql_config["user"], password=local_mysql_config["password"],
                                               db=local_mysql_config["database"], loop=loop,
                                               charset=local_mysql_config["charset"], autocommit=True)
        return self.pool

    async def request_web(self,url,proxy=None):
        for i in range(3):
            try:
                proxy = await self.get_proxy()
                async with session.get(url=url, proxy=proxy, headers=headers, timeout=15) as r:
                    logger.info("url:{},status:{}".format(url,r.status))
                    if r.status in [200, 201]:
                        data = await r.text()
                        return data
                    elif r.status in [403, 400, 500, 502, 503, 429]:
                        proxy = await self.get_proxy()
                    else:
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
        logger.info("flag:" + str(self.flag))
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
            data_dic["what_news"] = ""
        else:
            data_dic["name"] = ""
            data_dic["what_news"] = ""
        if content.xpath(self.analysis.icon):
            data_dic["icon"] = content.xpath(self.analysis.icon)[0]
        else:
            data_dic["icon"] = ""
        if content.xpath(self.analysis.categories):
            data_dic["categories"] = ','.join(content.xpath(self.analysis.categories))
        else:
            data_dic["categories"] = ""
        if content.xpath(self.analysis.version):
            data_dic["version"] = content.xpath(self.analysis.version)[0].strip(" ")
        else:
            data_dic["version"] = ""
        if content.xpath(self.analysis.os):
            data_dic["os"] = content.xpath(self.analysis.os)[0]
        else:
            data_dic["os"] = ""
        if content.xpath(self.analysis.size):
            data_dic["size"] = content.xpath(self.analysis.size)[0]
        else:
            data_dic["size"] = ""
        img_urls = re.findall(r"\('#images_while'\)\.load[\d\D]+?\)", data)
        if len(img_urls) > 0:
            try:
                img_url = img_urls[0].replace("('#images_while').load('","").replace("\" ')","").replace("')","")
                parameter1 = img_url.split('&')[-2]
                parameter2 = img_url.split('&')[-1]
                data = await self.request_web(url=self.host + "/index.php?m=files&f=images_while&" + parameter1 + "&" + parameter2)
                if data:
                    img_content = etree.HTML(data)
                    if img_content.xpath(self.analysis.img_urls):
                        data_dic["img_urls"] = ','.join(img_content.xpath(self.analysis.img_urls))
                    else:
                        data_dic["img_urls"] = ""
                else:
                    data_dic["img_urls"] = ""
            except Exception as e :
                data_dic["img_urls"] = ""
                logger.info("error:{},img_urls:{}".format(e,str(img_urls)))
        else:
            data_dic["img_urls"] = ""
        if content.xpath(self.analysis.description):
            data_dic["description"] = ''.join(content.xpath(self.analysis.description))
        else:
            data_dic["description"] = ''
        if content.xpath(self.analysis.app_url):
            data_dic["app_url"] = content.xpath(self.analysis.app_url)[0]
        else:
            logger.info('抓取不到app_url'+str(data_dic))
            data_dic["app_url"] = ""
        mod_nuber = content.xpath(self.analysis.mod_number2)
        if mod_nuber:
            temp = re.findall("\d+",mod_nuber[-1])
            if temp:
                download_url = temp[-1]
                logger.info('download_url:'+str(download_url))
                data = await self.request_web(url=self.mod_pkg_url+download_url)
                if data:
                    try:
                        mod_content = etree.HTML(data)
                        download_url_len = len(mod_content.xpath(self.analysis.download_first_url))
                        if download_url_len == 1 or download_url_len == 2:
                            temp_apk_download_url = mod_content.xpath(self.analysis.download_first_url)[-1]
                            data = await self.request_web(url=temp_apk_download_url)
                            temp_apk_download_url_data = etree.HTML(data)
                            apk_download_url = temp_apk_download_url_data.xpath(self.analysis.pkg_download_url)[0]
                            if '.apk' in apk_download_url:
                                data_dic["download_first_url"] = [apk_download_url]
                            else:
                                data_dic["download_first_url"] = []
                                # self.bad_pkg_url.add(data_dic["app_url"])
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
                            if '.zip' in obb_download_url:
                                data_dic["download_first_url"] = [apk_download_url, obb_download_url]
                            else:
                                data_dic["download_first_url"] = [apk_download_url,'need_info']
                                # self.bad_pkg_url.add(data_dic["app_url"])
                        elif download_url_len == 4:
                            temp_apk_download_url = mod_content.xpath(self.analysis.download_first_url)[-2]
                            data = await self.request_web(url=temp_apk_download_url)
                            temp_apk_download_url_data = etree.HTML(data)
                            apk_download_url = temp_apk_download_url_data.xpath(self.analysis.pkg_download_url)[0]
                            data_dic["download_first_url"] = [apk_download_url]
                        else:
                            data_dic["download_first_url"] = []
                            logger.info('长度有问题请查看' + data_dic["app_url"])
                    except Exception as e:
                        logger.info("error:{},url:{}".format(e,data_dic["app_url"]))
                        data_dic["download_first_url"] = []
                else:
                    data_dic["download_first_url"] = []
            else:
                logger.info('is questsion:' + data_dic["app_url"] + ":" + str(mod_nuber) + ',' + str(temp))
                data_dic["download_first_url"] = []
        else:
            logger.info('没有的url：'+ data_dic["app_url"]+str(mod_nuber))
            data_dic["download_first_url"] = []
        return data_dic
    def build_detail_tasks(self):
        tasks = []
        for url in self.pkg_urls:
            task = asyncio.ensure_future(self.request_web(url=url),loop=loop)
            tasks.append(task)
        return tasks

    def build_check_tasks(self,datas):
        tasks = []
        for data in datas:
            if data:
                task = asyncio.ensure_future(self.mysql_op.check_version(data))
                tasks.append(task)

        return tasks

    def download_pkg(self,results):
        for data_dic in results:
            if data_dic:
                if len(data_dic["download_first_url"]) > 0:
                    data_dic = Helper.build_download_task(data_dic=data_dic)
                    if data_dic:
                        loop.run_until_complete(self.mysql_op.insert_update_app(data_dic=data_dic))
                    else:
                        data_dic["pkgname"] = ""
                        data_dic["md5"] = ""
                        data_dic["developer"] = ""
                        data_dic["file_path"] = ""
                        self.bad_pkg_url.add(data_dic["app_url"])
                        loop.run_until_complete(self.mysql_op.insert_update_app(data_dic=data_dic))
                    if data_dic and data_dic["file_path"]:
                        loop.run_until_complete(self.mysql_op.insert_update_apk(data_dic=data_dic))
                        #下载成功更新版本
                        loop.run_until_complete(self.mysql_op.update_version(data_dic))
                        self.post_data.run_post(data_dic["pkgname"])
                    if data_dic and data_dic["file_path"] is None:
                        self.bad_pkg_url.add(data_dic["app_url"])
                else:
                    data_dic["pkgname"] = ""
                    data_dic["md5"] = ""
                    data_dic["developer"] = ""
                    data_dic["file_path"] = ""
                    self.bad_pkg_url.add(data_dic["app_url"])
                    loop.run_until_complete(self.mysql_op.insert_update_app(data_dic=data_dic))
                    logger.info('have question' + str(data_dic))
                    logger.info('不存在download_url'+str(data_dic))

    def download_image_tasks(self,datas):
        if not os.path.exists(PKGSTORE):
            os.makedirs(PKGSTORE)
        tasks = []
        for data in datas:
            if data:
                if data["icon"]:
                    task = asyncio.ensure_future(self.download_icon(datas=data))
                    tasks.append(task)
                if data["img_urls"]:
                    task = asyncio.ensure_future(self.download_screen(datas=data))
                    tasks.append(task)
        return tasks

    def file_path_detail(self, url):
        file_name = url.replace('https://i1.androeed.ru/', '').replace('/', '')
        if 'i3.androeed.ru' in url:
            file_name = url.replace('https://i3.androeed.ru/', '').replace('/', '')
        file_name = hashlib.md5((file_name).encode('utf-8')).hexdigest() + '.png'
        now = datetime.datetime.now()
        now_date = now.strftime('%Y-%m-%d')
        return file_name, now_date


    async def download_icon(self,datas,proxy_put=None):
        proxy = proxy_put
        for i in range(3):
            try:
                async with session.get(url=datas["icon"], proxy=proxy, timeout=15) as r:
                    if r.status in [200, 201]:
                        data = await r.read()
                        file_name, nowdate = self.file_path_detail(datas["icon"])
                        image_dir = ICONSTORE + nowdate + '/'
                        if os.path.exists(image_dir) is False:
                            os.makedirs(image_dir)
                        file_path = image_dir + file_name
                        with open(file_path, 'wb') as fp:
                            fp.write(data)
                        datas["icon_path"] = file_path
                        await self.mysql_op.insert_update_icon(datas)
                        # loop.run_until_complete(self.mysql_op.insert_update_icon(datas))
                        break
                    elif r.status in [403, 400, 500, 502, 503, 429]:
                        proxy = await self.get_proxy()
                    else:
                        break
            except Exception as e:
                proxy = await self.get_proxy()
                logger.info(e)

    async def download_screen(self,datas,proxy=None):
        urls = datas['img_urls'].split(',')
        urls_list = []
        for url in urls:
            for i in range(3):
                try:
                    async with session.get(url=url, proxy=proxy, timeout=15) as r:
                        if r.status in [200, 201]:
                            data = await r.read()
                            file_name, nowdate = self.file_path_detail(url)
                            image_dir = SCREENSTORE + nowdate + '/'
                            if os.path.exists(image_dir) is False:
                                os.makedirs(image_dir)
                            file_path = image_dir + file_name
                            with open(file_path, 'wb') as fp:
                                fp.write(data)
                            urls_list.append(file_path)
                            break
                        elif r.status in [403, 400, 500, 502, 503, 429]:
                            proxy = await self.get_proxy()
                        else:
                            break
                except Exception as e:
                    logger.info(e)
                    proxy = await self.get_proxy()

        try:
            datas['screen_path'] = ','.join(urls_list)
            # loop.run_until_complete(self.mysql_op.insert_update_screen(datas))
            await self.mysql_op.insert_update_screen(datas)
        except Exception as e:
            logger.info(e)

    def run(self):
        self.pkg_urls.clear()
        self.bad_pkg_url.clear()
        # loop.run_until_complete(self.get_pool())
        logger.info('start crawl ...')
        tasks = self.build_async_tasks()
        results = loop.run_until_complete(asyncio.gather(*tasks))
        for result in results:
            if result:
                self.get_app_urls(result)
        logger.info('pkg_urls:'+str(self.pkg_urls))
        detail_tasks = self.build_detail_tasks()
        detail_results = loop.run_until_complete(asyncio.gather(*detail_tasks))

        data_tasks = []
        logger.info('second')
        for result in detail_results:
            if result:
                task = asyncio.ensure_future(self.analysis_data(data=result))
                data_tasks.append(task)

        results = loop.run_until_complete(asyncio.gather(*data_tasks))
        logger.info('three'+str(results))
        logger.info('three_len:'+str(len(results)))
        #检查更新
        tasks = self.build_check_tasks(datas=results)

        results = loop.run_until_complete(asyncio.gather(*tasks))
        logger.info('检查剩下的:'+str(results))
        logger.info(('dict_len:'+str(len(results))))
        #下载icon和screenshots

        tasks = self.download_image_tasks(results)
        loop.run_until_complete(asyncio.gather(*tasks))

        #检查是否需要下载包
        # check_tasks = self.build_check_need_download(results)
        # need_results = loop.run_until_complete(asyncio.gather(*check_tasks))
        # 下载包
        self.download_pkg(results)



        logger.info("self.bad_pkg_url:"+str(self.bad_pkg_url))
        logger.info('start send email')
        if self.bad_pkg_url:
            email = SMTP("jian.zou@office.feng.com")
            email.send_email("15260826071",self.bad_pkg_url)