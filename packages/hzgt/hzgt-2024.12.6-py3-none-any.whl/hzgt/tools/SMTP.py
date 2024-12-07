# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Union, Iterable

class Smtpop:
    """
    基于SMTPLib库封装, 提供SMTP邮件发送功能
    """

    def __init__(self, smtp_server: str, port: int, username: str, password: str):
        """
        初始化SMTP客户端

        :param smtp_server: SMTP服务器地址 例如: "smtp.qq.com"
        :param port: SMTP服务器端口 例如: 587
        :param username: 登录用户名
        :param password: 授权码
        """
        self.smtp_server = smtp_server
        self.port = int(port)
        self.username = username
        self.password = password
        self.server = None
        self.recipients = []
        self.msg = MIMEMultipart()

    def __enter__(self):
        """
        上下文管理器进入方法, 登录SMTP服务器
        """
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        上下文管理器退出方法, 关闭SMTP连接
        """
        self.close()

    def login(self):
        """
        登录SMTP服务器
        """
        self.server = smtplib.SMTP(self.smtp_server, self.port)
        self.server.starttls()  # 启用TLS加密
        self.server.login(self.username, self.password)

    def add_recipient(self, recipient: Union[str, Iterable[str]], *args):
        """
        添加收件人

        :param recipient: 收件人邮箱地址
        :type recipient: Union[str, Iterable[str]]

        :param args: *args也能接受单个的收件人邮箱地址或者可迭代的收件人邮箱地址容器(如列表、元组、集合)
        """
        try:
            # 处理主参数
            if isinstance(recipient, str):
                self._add_unique_recipient(recipient)
            elif isinstance(recipient, Iterable):
                self._add_unique_recipients(recipient)
            else:
                raise TypeError("Recipient 必须是字符串或字符串的可迭代对象")

            # 处理 *args 参数
            for arg in args:
                if isinstance(arg, str):
                    self._add_unique_recipient(arg)
                elif isinstance(arg, Iterable):
                    self._add_unique_recipients(arg)
                else:
                    raise TypeError("*args 中的每个参数都必须是字符串或字符串的可迭代对象")
        except Exception as e:
            raise Exception(f"添加收件人时出错: {e}") from None

    def _add_unique_recipient(self, recipient: str):
        """
        添加单个收件人

        :param recipient: 收件人邮箱地址
        :return:
        """
        if recipient not in self.recipients:
            self.recipients.append(recipient)

    def _add_unique_recipients(self, recipients: Iterable):
        """
        添加多个收件人

        :param recipients: 可迭代对象
        :return:
        """
        for r in recipients:
            if r not in self.recipients:
                self._add_unique_recipient(r)

    def add_file(self, file_path: str):
        """
        添加附件到邮件中

        :param file_path: 附件文件路径
        """
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={file_path}")
            self.msg.attach(part)

    def send(self, subject: str, body: str, html=False):
        """
        发送邮件

        :param subject: 邮件主题
        :param body: 邮件正文
        :param html: 布尔值, 指示邮件正文是否为HTML格式默认为False
        """
        self.msg["From"] = self.username
        self.msg["To"] = ", ".join(self.recipients)
        self.msg["Subject"] = subject

        if html:
            self.msg.attach(MIMEText(body, "html"))
        else:
            self.msg.attach(MIMEText(body, "plain"))
        # 发送邮件
        if self.server:
            self.server.sendmail(self.username, self.recipients, self.msg.as_string())
        else:
            raise ConnectionError("SMTP服务器未登录")

    def close(self):
        """
        关闭SMTP连接
        """
        if self.server:
            self.server.quit()


