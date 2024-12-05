#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：LockonToolAlpha
@File    ：eml_reader.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/7/1 上午9:39
@explain : 文件说明
"""

import email.header
import os
import logging
from email.parser import Parser
import json
import pandas as pd
from email.utils import parsedate_to_datetime
import email.message


class MailReader:
    """
    用于读取和解析EML格式邮件的类。

    Attributes:
        eml_path (str): 邮件文件路径。
        debug (bool): 是否开启调试模式。
        raw_email (str): 原始邮件内容。
        email_content (email.message.Message): 解析后的邮件内容对象。
        process_log (str): 处理日志。
        debug (bool): 调试模式开关。
        header_dict (dict): 邮件头信息字典。
        mail_text (list): 邮件文本内容。
        all_links (list): 邮件中的所有链接。
        date (str): 邮件发送日期。
    """

    def __init__(self, eml_path="", debug=False):
        """
        初始化邮件读取器，设置默认值。

        Args:
            eml_path (str): 邮件文件路径。
            debug (bool): 是否开启调试模式。
        """
        self.raw_email = None
        self.email_content = None
        self.process_log = ""
        self.debug = debug
        self.header_dict = {}
        self.mail_text = ""
        self.all_links = []
        self.date = ""
        # 如果提供了邮件路径，则读取邮件
        if eml_path:
            self.__mail_reader(eml_path)
            self.eml_path = eml_path

    @staticmethod
    def decode_header(header_str):
        """
        解码邮件头信息。

        Args:
            header_str (str): 需要解码的头信息字符串。

        Returns:
            email.header.Header: 解码后的头信息对象。
        """
        temp = email.header.decode_header(header_str)
        result = email.header.make_header(temp)
        return result

    def to_string(self):
        """
        输出邮件内容字符串。

        Prints:
            邮件内容。
            如果处于调试模式，输出处理日志。

        Returns:
            str: 邮件内容字符串。
        """
        print("email内容:", self.email_content)
        if self.debug:
            print("process_log:", self.process_log)
        return self.email_content

    def to_dict(self):
        """
        将邮件头信息转换为字典格式。

        Returns:
            dict: 包含邮件头信息的字典。
        """
        if self.header_dict != {}:
            return self.header_dict

        for each_key in set(self.email_content.keys()):
            self.header_dict.update({each_key: self.email_content.get_all(each_key)})

        for each_key in ["From", "To", "Subject"]:
            temp = []
            for each_str in self.header_dict.get(each_key, []):
                each_str = str(self.decode_header(each_str))
                temp.append(each_str)
            self.header_dict.update({each_key: temp})
        return self.header_dict

    def to_json(self):
        """
        将邮件头信息转换为JSON格式。

        Returns:
            str: 包含邮件头信息的JSON字符串。
        """
        if self.header_dict == {}:
            self.header_dict = self.to_dict()
        return json.dumps(self.header_dict)

    def __mail_reader(self, eml_path):
        """
        私有方法，用于读取指定路径的EML文件并解析。

        Args:
            eml_path (str): EML文件路径。

        Returns:
            MailReader: 返回自身实例，用于方法链。
        """
        try:
            if os.path.exists(eml_path):
                with open(eml_path, "r", encoding="utf-8") as fp:
                    self.raw_email = fp.read()
                self.email_content = Parser().parsestr(self.raw_email)
                self.date = parsedate_to_datetime(
                    email.message_from_string(self.raw_email)["Date"]
                ).strftime("%Y%m%d")
                self.detailed_date = parsedate_to_datetime(
                    email.message_from_string(self.raw_email)["Date"]
                )
            else:
                raise FileNotFoundError(f"邮件文件不存在: {eml_path}")
        except Exception as e:
            self.process_log += f"读取邮件失败:{str(e)}\n"
            if self.debug:
                logging.error(f"读取邮件失败: {str(e)}")
        return self

    def parse_mail(self, eml_path):
        """
        解析邮件。

        Args:
            eml_path (str): EML文件路径。

        Returns:
            MailReader: 返回自身实例，用于方法链。
        """
        self.header_dict = {}
        return self.__mail_reader(eml_path)

    def get_content(self):
        """
        获取邮件的所有内容，包括文本和HTML。

        Returns:
            list: 包含所有内容的列表。
        """
        all_content = []
        for par in self.email_content.walk():
            if not par.is_multipart():
                str_charset = par.get_content_charset(failobj=None)
                str_content_type = par.get_content_type()
                if str_content_type in ("text/plain", "text/html"):
                    content = par.get_payload(decode=True)
                    if str_charset:
                        all_content.append(content.decode(str_charset))
                    else:
                        all_content.append(content.decode("utf-8", "ignore"))
        self.mail_text = all_content
        return all_content

    def get_df_from_html(self):
        """
        从邮件HTML中提取并返回第一个表格作为DataFrame。

        Returns:
            pandas.DataFrame: 从HTML中提取的DataFrame，如果无法提取则返回空DataFrame。
        """
        if self.email_content is None:
            return pd.DataFrame()
        email_message = email.message_from_string(self.email_content.as_string())
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/html":
                    body = part.get_payload(decode=True)
                    break
        else:
            body = email_message.get_payload(decode=True)
        try:
            df = pd.read_html(body)[0]
        except Exception as e:
            logging.error(f"解析HTML表格失败: {str(e)}")
            df = pd.DataFrame()
        return df

    def get_attr(self, attr_dir):
        """
        从邮件中提取附件并保存到指定目录。

        Args:
            attr_dir (str): 保存附件的目录路径。
        """
        for par in self.email_content.walk():
            if not par.is_multipart():
                name = par.get_param("name")
                if name:
                    file_name = email.header.decode_header(name)[0]
                    if file_name[1]:
                        attr_name = file_name[0].decode(file_name[1])
                    else:
                        attr_name = file_name[0]
                    attr_data = par.get_payload(decode=True)
                    attr_fp = os.path.join(attr_dir, attr_name)
                    try:
                        with open(attr_fp, "wb") as f_write:
                            f_write.write(attr_data)
                    except Exception as e:
                        logging.error(f"保存附件失败: {str(e)}")
                        continue
