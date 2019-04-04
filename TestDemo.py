import re

import requests


url = "https://www.androeed.ru/files/pewdiepies-tuber-simulator.html"

mod_pkg_url = "https://www.androeed.ru/index.php?m=files&f=load_commen_ebu_v_rot_dapda&ui="
r = requests.get(url)
host = "https://www.androeed.ru"
data = r.text

from lxml import etree

from Analysis_data.Xpath_word import Xpaths
analysis = Xpaths()
def analysis_data(data):
    content = etree.HTML(data)
    data_dic = {}
    name = content.xpath(analysis.pkg_name)
    if name and '[' in name[0]:
        data_dic["name"] = re.search(r'[\d\D]*\[', name[0]).group().replace(' [', "")
        data_dic["what_news"] = re.search("\[[\d\D]+?\]", name[0]).group().replace('[', '').replace(']', '')
    elif name:
        data_dic["name"] = name[0]
    else:
        data_dic["name"] = ""
    data_dic["icon"] = content.xpath(analysis.icon)[0]
    data_dic["categories"] = ','.join(content.xpath(analysis.categories))
    data_dic["version"] = content.xpath(analysis.version)[0]
    data_dic["os"] = content.xpath(analysis.os)[0]
    data_dic["internet"] = content.xpath(analysis.internet)[0]
    data_dic["size"] = content.xpath(analysis.size)[0]
    data_dic["raiting"] = content.xpath(analysis.raiting)[0]
    data_dic["russian"] = content.xpath(analysis.russian)[0]
    img_urls = re.findall(r"\('#images_while'\)\.load[\d\D]+?\)", data)
    if len(img_urls) > 0:
        try:
            img_url = img_urls[0].replace("('#images_while').load('", "").replace("\" ')", "").replace("')", "")
            r = requests.get(url=host + img_url)
            data = r.text
            if data:
                img_content = etree.HTML(data)
                if img_content.xpath(analysis.img_urls):
                    data_dic["img_urls"] = ','.join(img_content.xpath(analysis.img_urls))
            else:
                print('img_url:' + img_url)
                data_dic["img_urls"] = "None"
        except Exception as e:
            print("error:{},img_urls:{}".format(e, str(img_urls)))
    else:
        data_dic["img_urls"] = "None"
    data_dic["description"] = ''.join(content.xpath(analysis.description))
    data_dic["app_url"] = content.xpath(analysis.app_url)[0]

    mod_nuber = content.xpath(analysis.mod_number2)
    if mod_nuber:
        temp = re.findall("\d+", mod_nuber[-1])
        if temp:
            pass
        else:
            mod_nuber = content.xpath(analysis.mod_number1)
    if mod_nuber:
        temp = re.findall("\d+", mod_nuber[-1])
        if temp:
            download_url = temp[-1]
            print('download_url:' + str(download_url))
            r = requests.get(url=mod_pkg_url + download_url)
            data = r.text
            if data:
                mod_content = etree.HTML(data)
                # data_dic["download_first_url"] = mod_content.xpath(analysis.download_first_url)[-1]
                download_url_len = len(mod_content.xpath(analysis.download_first_url))
                if download_url_len == 1 or download_url_len == 2:
                    temp_apk_download_url = mod_content.xpath(analysis.download_first_url)[-1]
                    temp_apk_download_url_data = etree.HTML(requests.get(temp_apk_download_url).text)
                    apk_download_url = temp_apk_download_url_data.xpath(analysis.pkg_download_url)[0]

                    data_dic["download_first_url"] = [apk_download_url]
                elif download_url_len == 3:
                    # 第一个为apk包，第二个为破解包
                    temp_apk_download_url = mod_content.xpath(analysis.download_first_url)[-2]
                    temp_obb_download_url = mod_content.xpath(analysis.download_first_url)[-1]
                    apk_download_url = temp_apk_download_url.xpath(analysis.pkg_download_url)[0]
                    obb_download_url = temp_obb_download_url.xpath(analysis.pkg_download_url)[0]
                    data_dic["download_first_url"] = [apk_download_url,obb_download_url]
                elif download_url_len == 4:
                    temp_apk_download_url = mod_content.xpath(analysis.download_first_url)[-2]
                    apk_download_url = temp_apk_download_url.xpath(analysis.pkg_download_url)[0]
                    data_dic["download_first_url"] = [apk_download_url]
                else:
                    data_dic["download_first_url"] = "None"
                    print('长度有问题请查看' + data_dic["app_url"])
            else:
                data_dic["download_first_url"] = "None"
        else:
            data_dic["download_first_url"] = "None"
            print('is questsion:' + data_dic["app_url"] + ":" + str(mod_nuber) + ',' + str(temp))
    else:
        print('没有的url：' + data_dic["app_url"] + str(mod_nuber))
        data_dic["download_first_url"] = "None"
    print(data_dic)
    return data_dic


data_dic = analysis_data(data)


from helper import Helper

Helper.build_download_task(data_dic=data_dic)