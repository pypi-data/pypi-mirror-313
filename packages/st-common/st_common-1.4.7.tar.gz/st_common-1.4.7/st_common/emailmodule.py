# -*- coding: utf-8 -*-

import smtplib
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header



class EMailMould(object):
    """
    邮件模板
    """
    def __init__(self):
        self.email = MIMEMultipart()

    def add_header(self, key, value):
        """
        添加email Header
        :param key: str, header key
        :param value: str, header value
        """
        self.email[key] = Header(value, charset='utf-8')

    def add_text(self, text):
        """
        追加正文
        :param text: str, 正文
        """
        self.email.attach(MIMEText(text, _subtype='plain', _charset='utf-8'))

    def add_file(self, fpath, filename):
        """
        追加附件
        :param fpath: str, 附件路径
        :param filename: str, 附件名称(邮件中显示的名字)
        """
        mimeapp = MIMEApplication(open(fpath, 'rb').read())
        mimeapp["Content-Type"] = 'application/octet-stream'
        mimeapp.add_header('Content-Disposition', 'attachment', filename=filename)
        self.email.attach(mimeapp)

    def as_string(self):
        return self.email.as_string()

    def __call__(self, *args, **kwargs):
        return self.as_string()


class SendEMailModule(object):
    """
    利用smtp发送邮件模块
    """
    def __init__(self, smtp_server, smtp_port, username, password):
        """
        初始化
        :param smtp_server: str, smtp服务器 地址
        :param smtp_port: str, smtp服务器 端口
        :param username: str, stmp服务 账号
        :param password: str, stmp服务 密码
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.smtp_service = self.init_smtp_service()

    def init_smtp_service(self):
        """
        初始化smtp服务
        :return: SMTP,
        """
        smtp_service = smtplib.SMTP()
        smtp_service.connect(self.smtp_server, port=self.smtp_port)
        smtp_service.login(self.username, self.password)
        return smtp_service

    def send_email(self, sender, receiver, msg):
        """
        发送email到指定接收人
        :param sender: str, 发件邮箱
        :param receiver: str, 收件邮箱
        :param msg: str, 来自MIMEMultipart.as_string()
        """
        self.smtp_service.sendmail(sender, receiver, msg)

    def close(self):
        """
        关闭smtp service
        :return:
        """
        self.smtp_service.quit()
