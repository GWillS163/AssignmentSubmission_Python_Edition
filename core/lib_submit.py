#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time

import zmail

from lib.getNetTime import get_webServerTime
from lib.getMAC import get_mac_address
from lib.lib_base import highlight_str
from conf.Client_setting import *
import datetime
import sys
import os

CLAZZ = ''
ACCOUNT = ''
IDENTITY = ''
mailAccount = ""  # 19852331@czjtu.edu.cn
mailPasswd = ''


def record_send_history(Account_name, allAssignNameList, AssginList):
    """

    :param Account_name:
    :param allAssignNameList:
    :param AssginList:
    """
    currentTime = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    if os.path.exists(LocalSendHistory):
        # 获得原文
        raw_f = open(LocalSendHistory, mode='r', encoding=encoding)
        raw_text = raw_f.read()
        raw_f.close()
    else:
        raw_text = ''
    try:
        with open(LocalSendHistory, mode='w', encoding=encoding) as f:
            # 先写入新发送的，后写入原有的
            f.write(f"{Account_name} 在 {currentTime}发送了")
            f.write('\n')
            for course_name, path in zip(allAssignNameList, AssginList):
                f.write('\t')
                f.write(highlight_str('——' + path, "light_blue", course_name))
                f.write('\n')
            f.write('\n')
            f.write(raw_text)
        print(highlight_str('可以在菜单中查看提交记录', 'green', "记录成功"))
    except Exception as E:
        print(highlight_str(str(E), 'red', "记录失败"))


def ReadOutput_notice(acclaim, info, permitVersion, AssignList):
    """
    用来输出 课程作业以下的 通知部分
    :param acclaim:
    :param info:
    :param permitVersion:
    :param AssignList:
    :return:
    """
    if acclaim:
        print('')
        acclaim = f"\033[1;33m[通知] \033[0m{acclaim}"
        for i in range(4):
            print(acclaim, end='\r')
            time.sleep(0.5)
            print('  ' * 40, end='\r')
        print(acclaim)
    # if not updateStatus:  # 旧版本停止开关。如果status == False
    #     print('\n\n本软件已停止使用，请留意更新提醒！')
    #     return '', ''
    if info:
        print(f"\033[1;34m[提示] \033[0m{info}")
    # if not version in permitVersion:
    #     print(f"\033[1;31;40m [Error]  \033[0m此版本未被允许, 仅允许{permitVersion}留意更新")
    #     return '', ''
    if not AssignList:
        print("\033[1;33m[Notice] \033[0m无正在收集的文件")
        return '', ''
    # return cfg, AssignList


def isOverDDL(testDDL):
    """测试是否超时的主函数"""
    tt = get_webServerTime()
    ddl = datetime.datetime.strptime(testDDL, "‘%Y-%m-%d")
    # 是否超过ddl
    return tt.timestamp() > ddl.timestamp()


def detect_file():
    """
     通过sys模块来识别参数demo, http://blog.csdn.net/ouyang_peng/
    """
    file_lst = []
    if len(sys.argv) == 1:
        return file_lst
    print(f'您正在提交:{len(sys.argv) - 1}个文件。')
    if len(sys.argv) == 2:
        print("\t 可同时拖拽多个课程作业上传")
    for i in range(1, len(sys.argv)):
        print('\t作业 %s 为：%s' % (i, sys.argv[i].split('\\')[-1]))
        file_lst.append(sys.argv[i])
    return file_lst


def RenameByRule(FileFullPath, FileRule, CLAZZ, IDENTITY, ACCOUNT):
    """
    给定收集规则和全路径的文件名， 自动读取学生信息，替换关键字进行重命名
    :param FileFullPath:
    :param FileRule:
    :return:
    """
    if '班级' in FileRule:
        FileRule = FileRule.replace('班级', CLAZZ)
    if '学号' in FileRule:
        FileRule = FileRule.replace('学号', IDENTITY)
    if '姓名' in FileRule:
        FileRule = FileRule.replace('姓名', ACCOUNT)
    file_name = FileFullPath.split('/')[-1]  # xxx.doc, 无法应对这个情况 'E:/-Java上机作业8 - 副本.pdf' -> '--软件工程导论分析作业2.pdf'
    if ':' in file_name:
        file_name = FileFullPath.split('\\')[-1]
    file_suffix = file_name.split('.')[-1]  # .doc
    file_folder = FileFullPath.strip(file_name)  # D://xxx/
    new_file_path = os.path.join(file_folder, FileRule + "." + file_suffix)
    if not new_file_path == FileFullPath:
        os.rename(FileFullPath, new_file_path)
    return new_file_path


# 加密算法,参数：秘钥，文本
def encrypt(key, text):
    if len(key) > 2 and len(key) < 10:
        text2 = ''
        # 将key转化成ascii码列表
        newkey = []
        for i in key:
            newkey.append(ord(i))
        ii = 0
        for i in text:
            if ord(i) != 10:
                text2 = text2 + chr(ord(i) + newkey[ii])  # 关键部分，加密公式
            else:  # 处理\n
                text2 = text2 + chr(10)
            ii = ii + 1
            if ii >= len(newkey):
                ii = 0
        return text2


def decrypt(key, text):
    if len(key) > 2 and len(key) < 10:
        text2 = ''
        newkey = []
        for i in key:  # 将key转化成ascii码列表
            newkey.append(ord(i))
        ii = 0
        for i in text:
            if ord(i) != 10:
                text2 = text2 + chr(ord(i) - newkey[ii])  # 关键部分，解密公式
            else:
                text2 = text2 + chr(10)
            ii = ii + 1
            if ii >= len(newkey):
                ii = 0
        return text2


def sendMail(Account, allAssignNameList, mailAccount, mailPasswd, AssginList, submitTo, plantation=''):
    """提交作业和 发送本人验证邮件时使用"""
    if "czjtu.edu.cn" in mailAccount:
        submitServer = zmail.server(mailAccount, mailPasswd, smtp_host='smtp.exmail.qq.com')
        send_copy = mailAccount
    else:
        submitServer = zmail.server(mailAccount, mailPasswd, smtp_host='smtp.qq.com')
        send_copy = False
    try:
        content_text = ''
        for i in AssginList:
            content_text += i
        content_text += '-本消息由1909学委工具箱自动发送'
    except Exception as E:
        content_text = f'{submit_mail_flag}, 文件异常' + str(E) + '本消息由1909学委工具箱自动发送'

    mail = {
        'subject': submit_mail_flag + plantation + version,  # .encode("utf-8").decode("utf-8"),
        'content_text': content_text + str(get_mac_address()),
        'attachments': AssginList,
    }
    timeout_time = 3000
    while True:
        try:
            submitServer.send_mail(submitTo, mail, timeout=timeout_time)
            print(highlight_str('!!!发送成功', 'green', "OK"))
            if send_copy and AssginList:  # 提交文件时向自己发送一个副本
                mail_copy = {
                    'subject': "[作业提交成功副本]" + plantation,  # .encode("utf-8").decode("utf-8"),
                    'content_text': content_text.split('-')[0] + "<br> 本邮件为提交副本，无附件, 仅供查询使用",
                    'attachments': [],
                }
                submitServer.send_mail(send_copy, mail_copy, timeout=timeout_time)
            break
        except Exception as E:
            print(highlight_str(f'!!!发送失败：{E}', 'red', "Error"))
            if not 'connect' in str(E):
                print("账号问题？")
                break
            timeout_time += 300000
            print(f"文件过大？网络太差？重试中 timeout={timeout_time}")
    record_send_history(Account, allAssignNameList, AssginList)


if __name__ == '__main__':
    # from settings import *
    # queryMailSended()
    # updateConfig()
    print(isOverDDL())
    print(get_mac_address())
    # record_send_history(["2","2","4"])
    # sendMail(czjtuacc, czjtupsd, [], '19852331@czjtu.edu.cn')
