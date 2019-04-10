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
            <h1>错误的url</h1>
            <p>{}</p> 
        '''.format(str(data))
        self.message = MIMEText(meg, "html", "utf-8")
        self.message["Form"] = Header("好鲜生", "utf-8")
        self.message["To"] = Header(tel, "utf-8")
        self.message["Subject"] = Header("好鲜生", "utf-8")

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
    data = ('www,baidu.com','dasdasdsada')
    smtp = SMTP(email, tel,data)
    smtp.send_email()
