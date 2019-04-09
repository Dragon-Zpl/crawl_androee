import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header


class SMTP(object):
    def __init__(self, email, tel):
        self.sender = "15260826071@163.com"
        self.receivers = [email]
        self.host = "smtp.163.com"
        self.user = "15260826071@163.com"
        self.password = "zpl123456"
        self.ver_code = str(random.randint(1000, 10000))
        meg = '''
            <h1>好鲜生</h1>
            <p>该邮件为验证码邮件,建议确认验证码后删除该邮件</p> 
            <p>您的验证码为: {}</p>
        '''.format(self.ver_code)
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
    email = "jian.zou@office.feng.com"
    tel = "15260826071"
    smtp = SMTP(email, tel)
    smtp.send_email()
