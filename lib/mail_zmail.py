from queue import Queue

from lib.getMAC import get_mac_address
from lib.lib_base import highlight_str
from conf.Client_setting import submit_mail_flag, ConfFile
import os
import time
import threading
import zmail

# from core import record_send_history


def subThreadAndInf(sendMailFunc, info=""):
    """执行后台程序 并在前台提示信息"""
    subThread = threading.Thread(target=sendMailFunc)
    subThread.start()
    while True:
        for i in ['-', '\\', '|', '/']:
            time.sleep(0.2)
            print(info, i, end='\r')
        if not subThread.is_alive():
            break

    # subThread.join()

def getMailIWant(getRuleServer, str_in="RuleUpdate"):
    """获得感兴趣邮件"""
    t1 = time.time()
    mailQuantity = getRuleServer.stat()[0]
    index = mailQuantity
    for i in range(mailQuantity):  # 遍历所有收件
        mail = getRuleServer.get_mail(index)
        if mail['content_text']:
            if str_in in mail['content_text'][0]:
                useTime = round(time.time() - t1, 2)
                return mail, useTime
        index -= 1  # 如果不是，则向下递减，遍历更老的邮件


#
# def queryMailSended(mailAccount, mailPsd, getRuleServer=None):
#     """查询已发邮件"""
#     t1 = time.time()
#     # mailQuantity = getRuleServer.stat()[0]
#
#     z = zmail.server(mailAccount,mailPsd,
#                      smtp_host='smtp.exmail.qq.com',
#                      # smtp_port=465, smtp_ssl=True
#                      )
#     mail = {
#         'subject': f'{submit_mail_flag}测试',  # .encode("utf-8").decode("utf-8"),
#         'content_text': '' + str(get_mac_address()),
#         'attachments': [],
#     }
#     z.send_mail(mailAccount, mail)
#     # print(z.stat())
#
#     maillst = z.get_mails(subject="作业提交")
#     for mail in maillst:
#         print(mail['attachments'] if mail['attachments'] else "无文件",
#               mail['subject'])
#     # print(z.get_mails(sender=identity)[0])
#
#     useTime = round(time.time() - t1, 2)
#     print(useTime)
#     return


def updateConfig(ConfFilePath, qqacc, qqpsd, q):
    """下载并保存配置"""
    # 保存邮件的作业配置文件
    try:
        getRuleServer = zmail.server(qqacc, qqpsd)
        isNet = True
        # latest_rule_update_mail = server.get_mails(subject='RuleUpdate')[-1]  # 返回来[7,8,9] 的列表
        latest_rule_update_mail, useTime = getMailIWant(getRuleServer)
        # print(latest_rule_update_mail)

        os.remove(ConfFile)
        zmail.save_attachment(latest_rule_update_mail, target_path=ConfFilePath, overwrite=True)
        print(f'\033[1;32;40m[OK]\033[0m更新作业规则完成 耗时:{useTime}s')
    except Exception as E:
        print(f'\033[1;31;40m[Error]\033[0m更新作业规则时出现了问题:{E}')
        isNet = False
    q.put(isNet)


if __name__ == "__main__":
    pass
    # from settings.submit_settings import *
    # record_send_history("孟骏清", ["第一节课"], ['C://233.txt'])
    # get_all_submmit(czjtuacc, czjtupsd, 2)
    # sendMail(czjtuacc, czjtupsd,
    #        ["D:\system\桌面\软件1909-19852331-孟骏清-爬虫代码数据分析.zip"],
    #        czjtuacc, plantation='测试大文件')
