import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import aiomysql

from utils.init import *

class SMTP(object):
    def __init__(self, email):
        self.sender = "@qq.com"
        self.receivers = [email]
        self.host = "smtp.qq.com"
        self.user = "@qq.com"
        self.password = "lxnctbyxqaupbbha"
        self.ver_code = str(random.randint(1000, 10000))
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
    def send_email(self, tel, data):
        try:
            logger.info('begging send')
            meg = '''
                <h1>需要手动下载的URL</h1>
            '''
            for url in data:
                sql = "select * from crawl_androeed_app_info WHERE url=\'{}\'".format(url)
                recond = loop.run_until_complete(self.mysql_op.fetch_all(sql))
                logger.info(recond)
                if recond:
                    recond = recond[0]
                    decription = recond[5]
                    what_news = recond[6]
                    word = '<p>' + '<a href="' + url + '">' + url + '</a>' + '</p>'
                    word += '<p> decription:{} </p> <p> whatnews:{} </p>'.format(decription,what_news)
                    meg += word
                sql = "select coverimg_path from crawl_androeed_coverimg WHERE url=\'{}\'".format(url)
                recond = loop.run_until_complete(self.mysql_op.fetch_all(sql))
                logger.info(recond)
                if recond:
                    recond = recond[0][0]
                    cover_path = recond.replace('/home/feng/android_files1/', 'http://crawer2.tutuapp.net:8080/')
                    word = '<p> cover_path:{} </p>'.format(cover_path)
                    meg += word
                sql = "select screenshot_path from crawl_androeed_screenshots WHERE url=\'{}\'".format(url)
                recond = loop.run_until_complete(self.mysql_op.fetch_all(sql))[0][0]
                recond_screens = recond.split(",")
                re_reconds = []
                if recond:
                    for recond in recond_screens:
                        recond = ''.join(recond)
                        recond = recond.replace('/home/feng/android_files1/', 'http://crawer2.tutuapp.net:8080/')
                        re_reconds.append(recond)
                    word = '<p> screenshot_path:{} </p>'.format(str(re_reconds))
                    meg += word

            self.message = MIMEText(meg, "html", "utf-8")
            self.message["Form"] = Header("需要手动下载的URL", "utf-8")
            self.message["To"] = Header(tel, "utf-8")
            self.message["Subject"] = Header("需要手动下载的URL", "utf-8")
            smtp_obj = smtplib.SMTP()
            smtp_obj.connect(self.host, 25)
            smtp_obj.login(self.user, self.password)
            smtp_obj.sendmail(self.sender, self.receivers, self.message.as_string())
            print("Email send success")
            return True
        except smtplib.SMTPException:
            print("Email send error")
            return False

    def get_ver_code(self):
        return self.ver_code


if __name__ == '__main__':
    email = ""
    # email = "15260826071@163.com"
    tel = ""
    data = {'https://www.androeed.ru/files/stardew-valley.html?hl=en','https://www.androeed.ru/files/toca-hair-salon-2.html?hl=en','https://www.androeed.ru/files/homescapes.html?hl=en', 'https://www.androeed.ru/files/badland.html?hl=en', 'https://www.androeed.ru/files/madout2-bigcityonline.html?hl=en', 'https://www.androeed.ru/files/dawn-of-titans.html?hl=en', 'https://www.androeed.ru/files/angry-birds-evolution.html?hl=en', 'https://www.androeed.ru/files/toca-life-world.html?hl=en', 'https://www.androeed.ru/files/morphite-unreleased.html?hl=en', 'https://www.androeed.ru/files/driving-school-2017.html?hl=en', 'https://www.androeed.ru/files/world-truck-driving-simulator-.html?hl=en', 'https://www.androeed.ru/files/frontline-eastern-front.html?hl=en', 'https://www.androeed.ru/files/soul-knight-unreleased-.html?hl=en', 'https://www.androeed.ru/files/world-war-heroes-unreleased.html?hl=en', 'https://www.androeed.ru/files/trials-frontier.html?hl=en', 'https://www.androeed.ru/files/dont-starve-pocket-edition.html?hl=en', 'https://www.androeed.ru/files/real-steel-world-robot-boxing.html?hl=en', 'https://www.androeed.ru/files/construction-simulator-3.html?hl=en'}
    smtp = SMTP(email)
    smtp.send_email(tel,data)
