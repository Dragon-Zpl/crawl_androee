# _*_ coding: utf-8 _*_
import aiomysql

import json
import requests
import hashlib
import random
from datetime import datetime
from datetime import date
import base64

from utils.init import *
# from raven import Client
#
# client = Client('https://c0b2bc2f89c148edabc66c9e7006915e:b6415829768d40209691775302dcc2b0@sentrys.test.com/4')

#消除日期不能转化为json格式
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

class PostModData:
    def __init__(self):
        pool = loop.run_until_complete(self.get_pool())
        self.mysql_op = MysqlHeaper(pool=pool)

    async def get_pool(self, loop=None, config='mysql'):
        fr = open('./config/config.yaml', 'r')
        config_file = yaml.load(fr)
        local_mysql_config = config_file[config]
        self.pool = await aiomysql.create_pool(host=local_mysql_config["host"], port=local_mysql_config["port"],
                                               user=local_mysql_config["user"], password=local_mysql_config["password"],
                                               db=local_mysql_config["database"], loop=loop,
                                               charset=local_mysql_config["charset"], autocommit=True)
        return self.pool

    def run_post(self,pkgname):
        data_list = []
        pkgname_url_list = []
        #查询未同步的app
        # sql = "SELECT detail_url FROM androidmod_app_info WHERE is_info_synced=0 AND is_sync_failed=0"
        sql = "select pkg_name from crawl_androeed_apk_info WHERE pkg_name=\'{}\' and is_delete=0".format(pkgname)
        logger.info(sql)
        # sql = "select pkg_name from apkdlmod_apk_info WHERE id<800"
        url_reconds = loop.run_until_complete(self.mysql_op.fetch_one(sql))
        logger.info("url_reconds"+str(url_reconds))
        if url_reconds != None:
            sql = "select * from crawl_androeed_app_info WHERE pkgname=\'{}\'".format(pkgname)# AND is_info_synced=0 AND is_sync_failed=0"
            recond_all = loop.run_until_complete(self.mysql_op.fetch_all(sql))
            logger.info(recond_all)
            if recond_all:
                appinfo_dict = {}
                appinfo_dict['filebundleid'] = pkgname
                appinfo_dict['appDevelopers'] = recond_all[6].encode('utf-8')
                appinfo_dict['categoryCode'] = recond_all[1].encode('utf-8')
                appinfo_dict['appUpdateDate'] = recond_all[7]
                appinfo_dict['storeCode'] = 'en'
                sql_cover = "select coverimg_path from crawl_androeed_coverimg where url=\'{}\'".format(
                    recond_all[-1])
                coverRomoteUrl = loop.run_until_complete(self.mysql_op.fetch_one(sql_cover))[0]
                appinfo_dict['coverRomoteUrl'] = coverRomoteUrl.replace('/home/feng/android_files1', 'http://crawer2.tutuapp.net:8080/')
                sql_screens = "select screenshot_path from crawl_androeed_screenshots where url=\'{}\'".format(recond_all[-1])
                recond_screens = loop.run_until_complete(self.mysql_op.fetch_one(sql_screens))[0]
                recond_screens = list(recond_screens)
                re_reconds = []
                try:
                    for recond in recond_screens:
                        recond = ''.join(recond)
                        recond = recond.replace('/home/feng/android_files1', 'http://crawer2.tutuapp.net:8080/')
                        re_reconds.append(recond)
                    appinfo_dict['screenshots'] = re_reconds
                except:
                    appinfo_dict['screenshots'] = ""
                country_appinfo = {}

                country_appinfo['en'] = {'appName':recond_all[9].encode('utf-8') + ' MOD', 'appIntroduction':recond_all[4].encode('utf-8'),
                                         'appRecentChanges':'','currencyCode':'USD','appPrice' : '','compatibility': ""}
                appinfo_dict['localization'] = country_appinfo
                appinfo_dict['source'] = 'p'
                if appinfo_dict['filebundleid']:
                    appinfo_dict['filebundleid'] = appinfo_dict['filebundleid'].encode('utf-8')
                    sql_apk = "select file_path,file_sha1 from crawl_androeed_apk_info WHERE pkg_name=\'{}\' and is_delete=0".format(appinfo_dict['filebundleid'])
                    file_info = {}
                    recond = loop.run_until_complete(self.mysql_op.fetch_one(sql_apk))
                    logger.info(recond)
                    if recond:
                        apk_path = ''.join(recond[0])
                        apk_path = apk_path.replace('/home/feng/android_files1', 'http://crawer2.tutuapp.net:8080/')
                        file_info['downloadUrl'] = apk_path.encode('utf8')
                        file_info['fileMd5'] = ''.join(recond[1])
                        file_info['callbackUrl'] = 'http://192.168.182.155:5000/api/v1.0/deleteapk/p/' + appinfo_dict['filebundleid']
                    appinfo_dict['fileInfo'] = file_info
                    logger.info(appinfo_dict)
                    data_list.append(appinfo_dict)
                    # print(appinfo_dict)
                else:
                    #丢弃未下载到apk的数据
                    return None
                logger.info(data_list)

    # def pack_data(self, data_list, pkgname_url_list):
    #     rdstr = self.randonstr()
    #     skey = "OHDKD*&HJldhkfg"
    #     # print(len(data_list))
    #     # 转化为json格式
    #     appinfo = json.dumps(data_list, ensure_ascii=False, cls=CJsonEncoder)
    #     data = base64.b64encode(appinfo)
    #     sign = hashlib.md5(data + skey + rdstr).hexdigest()
    #     post_data = {
    #         'data': data,
    #         'sign': sign,
    #         'oncestr': rdstr
    #     }
    #     r = requests.post('http://192.168.183.58/index.php?r=apiandroid/crawler/UpdateAppInfoBatch', data=post_data)
    #     print(r.text.encode('UTF-8'))
    #     print(type(r.text))
    #     # 将以及同步的app 同步状态更新
    #     if r.ok == True:
    #          for pkgname in pkgname_url_list:
    #              sql = "update apkdlmod_app_info set is_info_synced=1 where pkg_name=%s"
    #              self.mysqlwapper.update_data(sql, (pkgname,))



    def randonstr(self):
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        sa = []
        for i in range(8):
            sa.append(random.choice(seed))
        salt = ''.join(sa)
        return salt





if __name__ == '__main__':
    post_mod_data = PostModData()
    post_mod_data.run_post('com.dodreams.driveahead')
    # change_cover()





data = [{
    "source":"g",
    "filebundleid":"com.dodreams.driveahead",
    "appDevelopers":"Dodreams Ltd.",
    "categoryCode":"Arcade,Cars,Pixels",
    "appUpdateDate":"datetime.datetime(2018, 4, 11, 0, 0)",
    "storeCode":"us",
    "coverRomoteUrl":"http://crawer2.tutuapp.net:8080/androee_files/picture/screenshot/2019-04-102945878e4ad4f5dcb3588fa2b72296c7.png",
    "localization":{
        "en":{
        "appName":"Drive Ahead!",
        "appIntroduction":"Drive Ahead! - Arcade mini-cars and battle in the arena.Racing, Arcade, Action ... How about we combine the three genre? Get behind the wheel and crashed his car ramming enemy. Destroy his car, earn points and win in quick, sharp, dynamic and fun rides. You can even play with a friend on the same device! And of course to open new cars, so the game it was always interesting.Features:Crazy gameplayRetro-style graphics Twin Shooter.Simple operationOpportunity to play together on one device Эту игру можно скачать в официальном Google Play Маркет",
        "compatibility":"Android 4.4 or above",
        'currencyCode': 'KRW',
        "appPrice":'0',
        'appRecentChanges': '',
        }

    },
    "fileInfo":{
        "downloadUrl":"http://crawer2.tutuapp.net:8080/androee_files/app_page/2019-04-10/8cc2d062cb408c966bb2651826bb0814.apk",
        "fileMd5":"334594e625fcb5017ec217f7561268ad",
        "callbackUrl":"http://23.236.115.228:5001/appVideoView",
        "weight":5,

    }
}]




# if __name__ == '__main__':
#     print(pack_data(data, "https://www.androeed.ru/files/drive-ahead.html?hl=en"))