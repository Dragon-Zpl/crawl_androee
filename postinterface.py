import base64
import hashlib
import json
import random
from datetime import datetime, date
import logging
import pymysql
import requests
import yaml

fr = open('./config/config.yaml', 'r')
config_file = yaml.load(fr)
local_mysql_config = config_file['mysql']
conn = pymysql.connect(**(local_mysql_config))
cursor = conn.cursor()

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        else:
            return json.JSONEncoder.default(self, obj)



def pack_data(data_list, url):
    rdstr = randonstr()
    skey = "OHDKD*&HJldhkfg"
    # 转化为json格式
    appinfo = json.dumps(data_list, ensure_ascii=False, cls=CJsonEncoder)
    data = base64.b64encode(appinfo.encode('utf-8'))
    sign = hashlib.md5((str(data, encoding='utf-8') + skey + rdstr).encode('utf-8')).hexdigest()
    post_data = {
        'data': data,
        'sign': sign,
        'oncestr': rdstr
    }
    try:
        print(post_data)
        r = requests.post('http://192.168.183.58/index.php?r=apiandroid/crawler/UpdateAppInfoBatch', data=post_data,
                          timeout=60)
        print(r.text)
        if r.ok == True:
            print('修改数据库')
            sql = "update crawl_androeed_app_info set isinfosynced=1 where url=%s"
            update_data(sql, (url,))
    except Exception as e:
        logging.error(e)
        pass


def randonstr():
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt

def update_data(command, data, commit=False):
    try:
        x = cursor.execute(command, data)
        if commit:
            conn.commit()
        return x
    except Exception as e:
        logging.info('mysql insert_data exception msg:%s' % e)



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




if __name__ == '__main__':
    print(pack_data(data, "https://www.androeed.ru/files/drive-ahead.html?hl=en"))