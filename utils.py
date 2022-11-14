
# import .myemail
from smtplib import SMTP_SSL
from email.mime.text import MIMEText


def email(message,Subject,sender_show,recipient_show,to_addrs,cc_show=''):
    '''
    :param message: str 邮件内容
    :param Subject: str 邮件主题描述
    :param sender_show: str 发件人显示，不起实际作用如："xxx"
    :param recipient_show: str 收件人显示，不起实际作用 多个收件人用','隔开如："xxx,xxxx"
    :param to_addrs: str 实际收件人
    :param cc_show: str 抄送人显示，不起实际作用，多个抄送人用','隔开如："xxx,xxxx"
    '''
    # 填写真实的发邮件服务器用户名、密码
    user = '499908174@qq.com'
    password = 'sqzumccutcqvbiaf'
    # 邮件内容
    msg = MIMEText(message, 'plain', _charset="utf-8")
    # 邮件主题描述
    msg["Subject"] = Subject
    # 发件人显示，不起实际作用
    msg["from"] = sender_show
    # 收件人显示，不起实际作用
    msg["to"] = recipient_show
    # 抄送人显示，不起实际作用
    msg["Cc"] = cc_show
    smtpObj = SMTP_SSL("smtp.qq.com",465)
    smtpObj.login(user,password)
    smtpObj.sendmail(user,to_addrs.split(','),msg=msg.as_string())
    smtpObj.quit()