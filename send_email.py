import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header


class SMTP(object):
    def __init__(self, email, tel, data):
        self.sender = "786283772@qq.com"
        self.receivers = [email]
        self.host = "smtp.qq.com"
        self.user = "786283772@qq.com"
        self.password = "lxnctbyxqaupbbha"
        self.ver_code = str(random.randint(1000, 10000))
        meg = '''
            <h1>需要手动下载的URL</h1>
        '''.format(str(data))
        for url in data:
            word = '<p>' + '<a href="' + url  + '">' + url + '</a>' + '</p>'
            meg += word
        self.message = MIMEText(meg, "html", "utf-8")
        self.message["Form"] = Header("需要手动下载的URL", "utf-8")
        self.message["To"] = Header(tel, "utf-8")
        self.message["Subject"] = Header("需要手动下载的URL", "utf-8")

    def send_email(self):
        try:
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
    # email = "jian.zou@office.feng.com"
    email = "15260826071@163.com"
    tel = "15260826071"
    data = {'https://www.androeed.ru/files/lego-city-my-city.html?hl=en', 'https://www.androeed.ru/files/into-the-badlands-champions.html?hl=en', 'https://www.androeed.ru/files/zombie-labs-idle-tycoon.html?hl=en', 'https://www.androeed.ru/files/badland.html?hl=en', 'https://www.androeed.ru/files/torque-burnout.html?hl=en', 'https://www.androeed.ru/files/frontline-eastern-front.html?hl=en', 'https://www.androeed.ru/files/morphite-unreleased.html?hl=en', 'https://www.androeed.ru/files/risuem-multfilmi-2.html?hl=en', 'https://www.androeed.ru/files/madout2-bigcityonline.html?hl=en', 'https://www.androeed.ru/files/dawn-of-titans.html?hl=en', 'https://www.androeed.ru/files/world-war-heroes-unreleased.html?hl=en', 'https://www.androeed.ru/files/soul-knight-unreleased-.html?hl=en', 'https://www.androeed.ru/files/homescapes.html?hl=en', 'https://www.androeed.ru/files/real-steel-world-robot-boxing.html?hl=en', 'https://www.androeed.ru/files/toca-life-world.html?hl=en', 'https://www.androeed.ru/files/angry-birds-evolution.html?hl=en', 'https://www.androeed.ru/files/driving-school-2017.html?hl=en', 'https://www.androeed.ru/files/world-truck-driving-simulator-.html?hl=en'}
    smtp = SMTP(email, tel,data)
    smtp.send_email()
