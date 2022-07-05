import configparser
import os

from lib.lib_base import highlight_str
from lib.getNetTime import *


def getStudentInfo(ConfFile, encoding):
    """
    获得学生在配置文件中的信息
    :param ConfFile:
    :param encoding:
    :return: [CLAZZ, ACCOUNT, IDENTITY, mailAccount, mailPasswd]
    """
    global mailAccount, mailPasswd
    cfg = configparser.ConfigParser()
    try:
        cfg.read(filenames=ConfFile, encoding=encoding)
        CLAZZ = cfg['StudentInfo']['Class']
        ACCOUNT = cfg['StudentInfo']['Account']
        IDENTITY = cfg['StudentInfo']['Identity']
        if not cfg.has_section('MailInfo'):
            mailAccount = ''
            mailPasswd = ''
        else:
            mailAccount = cfg['MailInfo']['mailAccount']
            mailPasswd = cfg['MailInfo']['mailPasswd']

        return [CLAZZ, ACCOUNT, IDENTITY, mailAccount, mailPasswd]
    except Exception as E:
        return '\033[1;31;40m [Error] 无个人信息：' + str(E) + \
               '\n请双击运行填写个人信息\033[0m'


def getConfInstance(ConfFile, encoding):
    cfg = configparser.ConfigParser()
    cfg.read(filenames=ConfFile, encoding=encoding)
    return cfg


def writeSTUCFG(CLAZZ, ACCOUNT, IDENTITY, ConfFile, encoding, mode="a+"):
    """读取原配置， 更新进入学生配置"""
    NEWCFG = getConfInstance(ConfFile, encoding)
    if not NEWCFG.has_section('StudentInfo'):
        NEWCFG.add_section('StudentInfo')
    NEWCFG.set('StudentInfo', 'Class', CLAZZ)
    NEWCFG.set('StudentInfo', 'Account', ACCOUNT)
    NEWCFG.set('StudentInfo', 'Identity', IDENTITY)
    with open(ConfFile, "w", encoding=encoding) as conff:
        conff.write('\n')
        NEWCFG.write(conff)
    print('\033[1;32;40m[OK]\033[0m个人信息更新')


def writeMailCFG(mailAccount, mailPasswd, ConfFile, encoding, mode="a+"):
    """读取原配置， 更新进入学生配置"""
    NEWCFG = getConfInstance(ConfFile, encoding)
    if not NEWCFG.has_section('MailInfo'):
        NEWCFG.add_section('MailInfo')
    NEWCFG.set('MailInfo', 'mailAccount', mailAccount)
    NEWCFG.set('MailInfo', 'mailPasswd', mailPasswd)
    with open(ConfFile, "w", encoding=encoding) as conff:
        conff.write('\n')
        NEWCFG.write(conff)
    print('\033[1;32;40m[OK]\033[0m邮箱信息已更新')


def ReadOutputConfigAssign(ConfFile, encoding):
    """输出配置文件 作业，info，acclaim， 检测Status， 版本允许"""
    cfg = configparser.ConfigParser()
    cfg.read(filenames=ConfFile, encoding=encoding)

    AssignList = []
    acclaim = ''
    # updateStatus = ''
    info = ''
    permitVersion = ''
    assignmentVersion = ''
    version_ddl = {}
    for Assgin in cfg.sections():
        if Assgin == 'UpdateInfo':
            continue
        if Assgin == 'StudentInfo':
            continue
        if Assgin == 'MailInfo':
            continue
        if Assgin == 'Version':
            continue
        AssignList.append(Assgin)
    acclaim = cfg["UpdateInfo"]['acclaim']
    # updateStatus = cfg.getboolean("UpdateInfo", "Status")
    info = cfg.get("UpdateInfo", "Info")
    permitVersion = cfg.get("UpdateInfo", "permitVersion")
    assignmentVersion = cfg.get("UpdateInfo", "assignmentVersion")

    for version in cfg.items("Version"):
        version_ddl.update({version[0]: version[1]})
    if assignmentVersion:
        print(f"规则更新日期:{assignmentVersion}")

    os.system('color 08')
    print(highlight_str('=' * 90, 'green', '当前募集'))
    print(f"{'课程': ^15}|{'作业': ^12}\t|{'DDL': ^12}\t|{'说明': ^28}")
    for Assgin in AssignList:
        try:
            ddl = cfg[Assgin]['deadline']
            desc = cfg[Assgin]['description']
        except Exception as E:
            ddl = ''
            desc = ''
            print("跳过了一条无法解析的作业-", E)
        print(f"\033[1;35;40m{cfg[Assgin]['curriculum']: ^15}\t\033[0m"
              f"{cfg[Assgin]['assignNickName']: <12}\t"
              f"{ddl: ^10}\t"
              f"{desc: <28}")
        time.sleep(0.2)
    print('=' * 90)
    return cfg, acclaim, info, permitVersion, AssignList, version_ddl


def parseCsv2Config(csvFile):
    with open(csvFile, mode='r', encoding='utf-8') as f:
        csvStr = f.read()
    return csvStr


if __name__ == '__main__':
    from conf.Server_setting import csvFile
