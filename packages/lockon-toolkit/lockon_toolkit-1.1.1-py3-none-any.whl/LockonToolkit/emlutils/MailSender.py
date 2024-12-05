import os
import smtplib
import json
import logging
from abc import abstractmethod
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Union, Dict, Any


class MetaAutoMail:
    """用于自动化发送邮件的类，支持从参数列表或JSON文件初始化"""

    # 类属性定义
    mail_user: str = ""  # 发件人邮箱地址
    mail_pwd: str = ""  # 发件人邮箱密码
    host: str = ""  # SMTP服务器地址
    port: int = -1  # SMTP服务器端口
    smtpObj: smtplib.SMTP  # SMTP连接对象
    receivers: List[str] = []  # 收件人邮箱列表
    msg: Union[MIMEText, MIMEMultipart] = None

    def __init__(self, *args, from_json: str = "", **kwargs):
        """
        初始化MetaAutoMail实例

        Args:
            *args: 可变参数列表，用于直接传递邮箱配置
            from_json: JSON文件路径，如果指定则从文件加载配置
            **kwargs: 关键字参数，用于直接传递邮箱配置
        """
        if from_json or (len(args) == 1 and os.fspath(args[0])):
            # 如果指定了from_json参数或者第一个参数是文件路径，则从JSON文件初始化
            self.init_from_json(from_json or args[0])
        else:
            # 否则，从参数列表或关键字参数初始化
            self.init_from_args(args, kwargs)

    def init_from_args(self, args: tuple, kwargs: Dict[str, Any]):
        """
        从参数列表或关键字参数初始化邮箱配置

        Args:
            args: 参数列表
            kwargs: 关键字参数
        """
        try:
            if args:
                # 使用位置参数初始化
                self.mail_user, self.mail_pwd, self.host, self.port, self.receivers = args
            else:
                # 使用关键字参数初始化
                self.mail_user = kwargs["mail_user"]
                self.mail_pwd = kwargs["mail_pwd"]
                self.host = kwargs["host"]
                self.port = kwargs["port"]
                self.receivers = kwargs["receivers"]
        except KeyError as ke:
            logging.error(f"缺少必要的参数: {ke}")
            raise Exception(f"参数错误: 缺少必要的参数 {ke}")
        except Exception as e:
            logging.error(f"初始化失败: {e}")
            raise
        self.test_login()  # 测试登录

    def init_from_json(self, json_path: str):
        """
        从JSON文件初始化邮箱配置

        Args:
            json_path: 包含邮箱配置的JSON文件路径
        """
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            self.mail_user = json_data["mail_user"]
            self.mail_pwd = json_data["mail_pwd"]
            self.host = json_data["host"]
            self.port = json_data["port"]
            self.receivers = json_data["receivers"]
        except FileNotFoundError:
            logging.error(f"文件未找到: {json_path}")
            raise
        except json.JSONDecodeError:
            logging.error(f"JSON解码错误: 文件可能不是有效的JSON格式")
            raise
        except Exception as e:
            logging.error(f"JSON文件错误: {e}")
            raise
        self.test_login()  # 测试登录

    def test_login(self):
        """测试SMTP服务器的登录"""
        try:
            self.smtpObj = smtplib.SMTP(self.host, self.port)  # 这里修复了一个潜在的bug，应该是使用self.port而不是self.host两次
            self.smtpObj.login(self.mail_user, self.mail_pwd)
            logging.info("SMTP服务器登录测试成功")
        except smtplib.SMTPAuthenticationError:
            logging.error("认证失败: 用户名或密码错误")
            raise
        except smtplib.SMTPException as se:
            logging.error(f"SMTP异常: {se}")
            raise
        except Exception as e:
            logging.error(f"未知错误: {e}")
            raise

    def send_mail(self):
        """
        发送邮件

        """
        if not self.msg:
            logging.error("邮件内容未设置")
            raise Exception("邮件内容未设置")
        try:
            self.smtpObj.sendmail(self.mail_user, self.receivers, self.msg.as_string())
            logging.info("邮件发送成功")
        except smtplib.SMTPRecipientsRefused:
            logging.error("收件人拒绝: 所有收件人都被拒绝")
        except smtplib.SMTPHeloError:
            logging.error("HELO错误: 服务器拒绝响应")
        except smtplib.SMTPSenderRefused:
            logging.error("发件人拒绝: 发件人地址被拒绝")
        except smtplib.SMTPDataError:
            logging.error("数据错误: 服务器对数据作出非肯定响应")
        except smtplib.SMTPException as se:
            logging.error(f"SMTP异常: {se}")
        except Exception as e:
            logging.error(f"未知错误: {e}")

    @abstractmethod
    def set_content(self, *args, **kwargs):
        """设置邮件内容"""
        pass

    def __del__(self):
        self.smtpObj.quit()