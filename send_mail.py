#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os
import smtplib
import sys
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from config import TO_ADDR, NT_PATH, NIX_PATH, KEYWORD, SMTP_SVR

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s- %(message)s')

log = logging.info


class MailSender:
    _from = None
    _attachments = []

    def __init__(self, smtpSvr, port):
        self.smtp = smtplib.SMTP()
        log("connecting...")
        self.smtp.connect(smtpSvr, port)
        log("connected!!!")

    def login(self, user, pwd):
        self._from = user
        log("login ...")
        self.smtp.login(user, pwd)

    def add_attachment(self, filename):
        """
            添加附件
        """
        attr_name = Path(filename).parts[-1]
        att = MIMEBase('application', 'octet-stream')
        att.set_payload(open(filename, 'rb').read())
        att.add_header('Content-Disposition',
                       'attachment',
                       filename=('gbk', '', attr_name))
        encoders.encode_base64(att)

        self._attachments.append(att)

    def send(self, subject, content, to_addr):
        """
            发送邮件
        """
        msg = MIMEMultipart('alternative')
        contents = MIMEText(content, "html", _charset='utf-8')
        msg['Subject'] = subject
        msg['From'] = self._from
        msg['To'] = to_addr
        for att in self._attachments:
            msg.attach(att)
        msg.attach(contents)
        try:
            self.smtp.sendmail(self._from, to_addr.split(','), msg.as_string())
            return True
        except Exception as e:
            log(str(e))
            return False

    def close(self):
        self.smtp.quit()
        log("logout.")


def check_latest_file(p, today):
    counter = 0
    for file in p.glob('*.csv'):
        if today in file.name:
            counter += 1
    return counter


def main(date=''):
    user = os.environ.get('EMAIL_NAME')
    pwd = os.environ.get('EMAIL_PWD')
    to_addr = TO_ADDR
    smtp_svr = SMTP_SVR
    content = '请查看附件'

    if date == '':
        today = datetime.now().strftime('%Y-%m-%d')
    else:
        today = date

    if os.name == 'nt':
        p = Path(NT_PATH)
    else:
        p = Path(NIX_PATH)

    subject = f'{today}{KEYWORD}销售情况'
    m = MailSender(smtp_svr, 25)
    m.login(user, pwd)
    for file in p.glob('*.csv'):
        if today in file.name:
            m.add_attachment(file)
    m.send(subject, content, to_addr)
    m.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
