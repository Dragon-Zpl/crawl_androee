import base64
import hashlib
import json
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



def pack_data(self, data_list, url):
    rdstr = self.randonstr()
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
        r = requests.post('http://192.168.183.58/index.php?r=apiandroid/crawler/UpdateAppInfoBatch', data=post_data,
                          timeout=60)
        if r.ok == True:
            sql = "update crawl_androeed_app_info set isinfosynced=1 where url=%s"
            update_data(sql, (url,))
    except Exception as e:
        logging.error(e)
        pass


def update_data(command, data, commit=False):
    try:
        x = cursor.execute(command, data)
        if commit:
            conn.commit()
        return x
    except Exception as e:
        logging.info('mysql insert_data exception msg:%s' % e)