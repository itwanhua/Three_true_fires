#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_mail(data, receiver):
    '''
    函数功能：发送邮件
    函数参数: data为邮件内容，receiver为邮件接收方
    返回值：发送成功返回0，否则返回1
    '''
    # 第三方 SMTP 服务
    mail_host="smtp.exmail.qq.com"  #设置服务器
    mail_user="wh@ithz.xyz"    #用户名 
    mail_pass="Vc9npRB5Gnxx7XNQ"   #口令 
    
    
    sender = 'wh@ithz.xyz'
    receivers = [receiver]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    
    message = MIMEText(data, 'plain', 'utf-8')
    message['From'] = Header("wh@ithz.xyz", 'utf-8')
    message['To'] =  Header(receiver, 'utf-8')
    
    subject = '”三味真火“'
    message['Subject'] = Header(subject, 'utf-8')
      
    try:
        smtpObj = smtplib.SMTP_SSL(host=mail_host) 
        smtpObj.connect(mail_host, 465)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        return 0
    except smtplib.SMTPException as e:
        print("无法发送邮件", e)
        return 1
    except Exception as e:
        print("发送失败", e)
        return 1

if __name__ == "__main__":
    send_mail("我喜欢你")

