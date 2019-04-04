import asyncio
import base64
import datetime
import hashlib
import json
import logging.config
import os
import re
import shutil
import time
import subprocess
import requests
from Crypto.Cipher import DES3
from lxml import etree

from utils.init import config_file, loop, logger
from utils.project_helper import ProjectHepler

basic_dir = "/home/feng/pkgtest/"
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


class Helper:
    des3 = config_file['DES3']
    key = des3['key']
    appkey = des3['appkey']
    pkgpath = "/home/feng/{}/google_files/app_page".format(ProjectHepler.get_basic_path(ProjectHepler.get_ip()))

    @classmethod
    def file_path_detail(cls):
        now = datetime.datetime.now()
        now_date = now.strftime('%Y-%m-%d')
        download_dir = "%s/%s/" % (cls.pkgpath, now_date)
        return download_dir

    @classmethod
    def build_tpk(cls, basic_dir, obbpath, dict_tpk,data_dic):
        # tpkdir = basic_dir + hashlib.md5((docid).encode('utf-8')).hexdigest()
        tpkdir = "/home/feng/pkgtest/" + hashlib.md5((data_dic["name"]).encode('utf-8')).hexdigest()
        print('tpkdir', tpkdir)
        config_info = cls.encryptapkinfo(dict_tpk, cls.key, cls.appkey)
        cls.writeencryptapkinfo(config_info, tpkdir)
        cls.downIcon(tpkdir,dict_tpk)
        obbname = obbpath.split('/')[-1]
        detfile_obb = tpkdir + '/data/' + obbname
        cls.mymovefile(obbpath, detfile_obb)

        apkpath = tpkdir + ".apk"

        detfile_apk = tpkdir + '/pkg.apk'
        cls.mymovefile(apkpath, detfile_apk)

        tpkfilename = tpkdir.split('/')[-1]
        tpkfilename = ''.join(tpkfilename)
        zip_str = 'cd ' + tpkdir + ' && zip -r ' + tpkfilename + '.tpk *'

        os.system(zip_str)

        cls.mymovefile(tpkdir + '/' + tpkfilename + '.tpk', basic_dir + tpkfilename + '.tpk')
        del_srcfile = 'rm -fr ' + tpkdir
        os.system(del_srcfile)

    @classmethod
    def encryptapkinfo(self, data, key, appkey):
        data['expired_date'] = int(time.time()) + 12 * 60 * 60
        data = json.dumps(data)
        iv = 'wEiphTn!'
        block_size = DES3.block_size
        logger.info('block_size is {} is {}'.format(block_size, block_size % 8 == 0))
        PADDING = lambda s: s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)
        des3 = DES3.new(key, DES3.MODE_CBC, iv)
        ciphertext = base64.b64encode(des3.encrypt(PADDING(data)))
        str_ciphertext = str(ciphertext, encoding='utf-8')
        verify = hashlib.md5(
            (hashlib.md5(appkey.encode('utf-8')).hexdigest() + key + str_ciphertext).encode(
                'utf-8')).hexdigest()
        cbc_base = base64.b64encode((json.dumps(
            {'app_key': hashlib.md5(appkey.encode('utf-8')).hexdigest(), 'encrypt_data': ciphertext,
             'verify': verify}, cls=MyEncoder)).encode('utf-8'))
        return cbc_base

    @classmethod
    def downIcon(self, tpkdir, data_dict):
        try:
            # sql = 'SELECT coverimgurl from crawl_google_play_app_info where pkgname=\'{}\''.format(pkg_name)
            # task = asyncio.ensure_future(mysqlwapper.fetch_one(sql, ))
            # loop.run_until_complete(task)
            # image_url = task.result()
            # image_url = image_url[0]
            image_url = data_dict["icon"]
            print(image_url)
            image_response = requests.get(image_url, verify=False).content
            image_path = os.path.join(tpkdir, r'icon.png')
            with open(image_path, 'wb') as fp:
                fp.write(image_response)
        except Exception as e:
            print(e)

    @classmethod
    def configinfo(cls, data_dic, apkpath,obb_path):
        aapk_str = 'aapt dump badging {} > tmp.txt'.format(apkpath)
        os.system(aapk_str)
        with open('tmp.txt', 'r', encoding='utf8', errors='ignore') as f:
            result = f.readlines()
            print('result:'+str(result))
        results = ''.join(result)
        logger.info('results:'+str(results))
        try:
            pkgname = re.search(r'package: name=\'(.*?)\'', results).group(1)
            print("pkgname is {}".format(pkgname))
        except:
            print("re pkgname error")
            os.remove(apkpath)
            os.remove(obb_path)
            return
        file_dir = obb_path.split('/')[:-1]
        file_dir = '/'.join(file_dir)
        sys_str = "cd " + file_dir + " && unzip -t {}".format(obb_path)
        f = os.popen(sys_str)
        # 删除zip文件
        result_unzip = f.readlines()
        result_unzip = ''.join(result_unzip)
        try:
            obbname = re.search(r'.*?ing.*?/(.*?obb).*', result_unzip).group(1)
        except:
            return None, None
        unzip_str = 'cd ' + file_dir + " && unzip -j {}".format(obb_path)
        os.system(unzip_str)
        new_obb_path = file_dir + '/' + obbname

        delete_command = 'rm -rf {} {} {}'.format(obb_path, file_dir + '/' + 'Read*', file_dir + '/' + 'ReXdl.com.url')
        os.system(delete_command)

        app_version_code = re.search(r'versionCode=\'(.*?)\'', results).group(1)
        app_version = re.search(r'versionName=\'(.*?)\'', results).group(1)
        apkfile_size = os.path.getsize(apkpath)
        obbfile_size = os.path.getsize(new_obb_path)
        developer = cls.get_app_other_info(pkgname)
        data_path = '/sdcard/android/obb/' + pkgname + '/'
        dict_tpk = {
            'app_name': data_dic["name"],
            'pkg_name': pkgname,
            'app_version': app_version,
            'app_version_code': app_version_code,
            'developer': developer,
            'apksize': str(apkfile_size),
            'data_path': data_path,
            'data_size': str(obbfile_size)
        }
        return dict_tpk

    @classmethod
    def writeencryptapkinfo(cls, config_info, tpkdir):
        des3_configinfo = config_info
        if not os.path.exists(tpkdir):
            os.makedirs(tpkdir)
        config_path = os.path.join(tpkdir, 'config')
        with open(config_path, 'w') as fp:
            fp.write(des3_configinfo.decode())

    @classmethod
    def mymovefile(cls, srcfile, dstfile):
        if not os.path.isfile(srcfile):
            logger.info("%s not exist!" % (srcfile))
        else:
            fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
            if not os.path.exists(fpath):
                os.makedirs(fpath)  # 创建路径
            shutil.move(srcfile, dstfile)  # 移动文件
            logger.info("move %s -> %s" % (srcfile, dstfile))

    @classmethod
    def get_app_other_info(cls,pkgname):
        #获取图片 开发者 price信息
        url = 'https://play.google.com/store/apps/details?id=' + pkgname
        google_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
            'origin': 'https://play.google.com',
            'x-client-data': 'CKC1yQEIlrbJAQiitskBCMG2yQEImpjKAQipncoBCKijygE=',
            'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'upgrade-insecure-requests': '1'
        }
        response = requests.get(url, headers=google_headers)
        if response.status_code == 200:
            html = etree.HTML(response.text)
            developer = html.xpath("//span[@class='T32cc UAO9ie'][1]/a[@class='hrTbp R8zArc']/text() | //div[@class='info-container']//div[@itemprop='author']/a/span[@itemprop='name']/text()")[0]
            return developer


    @classmethod
    def get_conpose_tpk_info(cls, url):
        file_dir = ""
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_name = url.split("id=")[-1]
        apk_filename = file_name + '.apk'
        obb_filename = file_name + '.zip'
        apk_path = file_dir + '/' + apk_filename
        obb_path = file_dir + '/' + obb_filename
        tpkdir = file_dir + '/' + file_name
        return tpkdir, apk_path, obb_path, file_dir

    @classmethod
    def runProcess(cls, commandString):
        logger.info("runProcess")
        p = subprocess.Popen(commandString, shell=True, stderr=subprocess.PIPE)
        output, err = p.communicate()

    @classmethod
    def urlFetch(cls, targetUrl, targetFile):
        print("wget --no-check-certificate --output-document \"" + targetFile + "\" \"" + targetUrl + "\"")
        cls.runProcess("wget --no-check-certificate --output-document \"" + targetFile + "\" \"" + targetUrl + "\"")

    @classmethod
    def build_download_task(cls,data_dic):
        basic = "/home/feng/pkgtest/" + hashlib.md5((data_dic["name"]).encode('utf-8')).hexdigest()
        apk_path = basic + '.apk'
        cls.urlFetch(targetFile=apk_path,targetUrl=data_dic["download_first_url"][0])
        if len(data_dic["download_first_url"])>1:
            logger.info('have obb pkg')
            obb_path = basic + '.zip'
            cls.urlFetch(targetFile=obb_path, targetUrl=data_dic["download_first_url"][1])
            dict_tpk = cls.configinfo(data_dic=data_dic,apkpath=apk_path,obb_path=obb_path)
            cls.build_tpk(basic_dir=basic_dir,obbpath=obb_path,dict_tpk=dict_tpk,data_dic=data_dic)
# b = Helper.configinfo(apk_details="PewDiePie's Tuber Simulator",apkpath="/home/feng/pkgtest/PewDiePies_Tuber_Simulator_-1553936520-www.androeed.ru.apk",obb_path="/home/feng/pkgtest/PewDiePies_Tuber_Simulator_-1553936709-www.androeed.ru.zip")
# print(b)
# dict_tpk = {'app_name': "PewDiePie's Tuber Simulator", 'pkg_name': 'com.outerminds.tubular', 'app_version': '1.36.0', 'app_version_code': '120', 'developer': 'Outerminds Inc.', 'apksize': '33941074', 'data_path': '/sdcard/android/obb/com.outerminds.tubular/', 'data_size': '96421912'}
# b = Helper.build_tpk(basic_dir="/home/feng/pkgtest/",obbpath="/home/feng/pkgtest/main.120.com.outerminds.tubular.obb",docid="com.outerminds.tubular",dict_tpk=dict_tpk)


