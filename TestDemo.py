# _*_ coding: utf-8 _*_
__time__ = '2018/4/12 10:22'

import os

from flask import Flask, jsonify
from flask import request

from MysqlWapper import Mysqlwrapper

app = Flask(__name__)


@app.route('/api/v1.0/deleteapk/<string:source>/<string:pkgname>', methods=['GET'])
def create_task(source, pkgname):
    "删除apk包的接口"
    p_list = ['androidmod_apk_info', 'apkdlmod_apk_info', 'apk_rex_dlmod_apk_info', 'crawl_androeed_apk_info']
    dict_apktable = {
        'a': 'apkpure_apk_info',
        'p': p_list,
        'g': 'crawl_google_play_apk_info'
    }
    if not source or not pkgname:
        result = {
             "success": 0,
             "info": "DELETE FAILED! PARAMETER ERR"
        }
        return jsonify({'result': result}), 400
    elif source not in dict_apktable:
        result = {
            "success": 0,
            "info": "DELETE FAILED!  ERR"
        }
        return jsonify({'result': result}), 400

    else:    
        data_info = {}
        mysqlwapper = Mysqlwrapper()
        conn = mysqlwapper.connection 
        cursor = mysqlwapper.getcursor()
        if source == 'p':
            mysql_tables = dict_apktable[source]
            result = ''
            for mysql_table in mysql_tables: 
                result = delete_apk_file(data_info, cursor, conn, mysql_table, pkgname)
        else:
            mysql_table = dict_apktable[source]
            result = delete_apk_file(data_info, cursor, conn, mysql_table, pkgname)

    return jsonify({'result': result}), 200

def delete_apk_file(data_info, cursor, conn, mysql_table, pkgname):
    sql_find = "select file_path from " + mysql_table + " WHERE pkg_name=\'" + pkgname + "\'"
    print(sql_find)
    rows = cursor.execute(sql_find)
    conn.commit()
    if rows != 0:
        filepath = cursor.fetchone()
        filepath = ''.join(filepath)
        if os.path.exists(filepath):
            delete_operation = "rm -f %s" % filepath
            os.system(delete_operation)
            sql_delelte = "update " + mysql_table + " set is_delete=1 WHERE pkg_name=\'" + pkgname + "\'"
            print(sql_delelte)
            cursor.execute(sql_delelte)
            data_info[pkgname] = 'haved deleted'
        else:
            data_info[pkgname] = 'have no this app'
    else:
        data_info[pkgname] = '{} have no this app'.format(mysql_table)

    result = {
        "success": 1,
        "data": data_info
    }
    return result



if __name__ == '__main__':
    app.run(host='0.0.0.0')
