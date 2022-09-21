import configparser
import sys
sys.path.append("..")
import datetime
import os
import zmail
from lib.lib_base import wait_anime, highlight_str
from lib.config_lib import ReadOutputConfigAssign, parseCsv2Config
from conf.Server_setting import *
from conf.Client_setting import *

# 向自己邮箱发送规则
server = zmail.server(file_rule_acc, file_rule_psd)
destinationMail = file_rule_acc
# 就业课作业纸质收集：简历打印使用A4纸，手写作业使用信纸或A4纸。按作业顺序上下放置，左侧装订。收集时间未定
print('邮箱登陆成功')
# 检查邮箱工作情况

# 发送作业规则

# 收集作业们
currentTime = datetime.datetime.now().strftime('-%Y%m%d_%H%M%S')
currentTime_ver = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
currentDate = datetime.datetime.now().strftime('%Y%m%d')


def parseStr2config(str):
    """输入,分割的字符串, 转化为config字符串"""
    config = configparser.ConfigParser()
    config.add_section('UpdateInfo')
    config.add_section('Version')
    # config.add_section('assignment')  # 曾想着把Assignment 全部装入 这个section下，算了
    lenLine = 7

    # 从 csv 自动生成[updateInfo] & [version]
    config_content = str.split('\n')
    for config_line_str in config_content[1:11]:  # 逐行查看 配置
        lineItem = config_line_str.split(',')
        if not lineItem[0]:
            continue
        if lineItem[0] == 'version':
            config.set('Version', lineItem[1], lineItem[2])
        else:
            config.set('UpdateInfo', lineItem[0], lineItem[1])

    # 自动生成 [assignment]
    for assign_line_str in config_content[11:]:  # 逐行查看 作业
        if not assign_line_str:
            continue
        lineItem = assign_line_str.split(',')
        if not len(lineItem) >= lenLine:
            print(f'解析作业分发csv时出现异常:{len(lineItem)}不为{lenLine}')
            print(lineItem)
            continue
        if lineItem[7]:  # 表格内停止收集
            continue
        config.add_section(lineItem[0])
        config.set(lineItem[0], "curriculum", lineItem[1])
        config.set(lineItem[0], "assignnickname", lineItem[2])
        config.set(lineItem[0], "deadline", lineItem[3])
        config.set(lineItem[0], "description", lineItem[4])
        config.set(lineItem[0], "filerule", lineItem[5])
        config.set("UpdateInfo", "assignmentversion", currentTime_ver)
        # configStr += assign_str_line
        config.write(open(local_conf, 'w', encoding='utf-8'))
    return local_conf


def makeAssignment(assignment_str, update_info):
    """config 新建配置文件, 已弃用"""
    with open(local_conf, mode='w', encoding='utf-8') as f:
        f.write(f"# {currentTime}")
        f.write(assignment_str)
        f.write(update_info)
        f.write(f"\nassignmentversion={currentTime_ver}")
    return local_conf


def Dispatch_Rule(local_conf, img=None):
    """发布规则"""
    attachments = [local_conf] if not img else [local_conf, img]
    mail = {
        'subject': f'{update_mail_flag}{currentDate}',  # Anything you want.
        'content_text': f'{update_mail_flag}桌面作业提交软件来自{currentDate}的更新',  # 可以写入配置文件文本，然后收件放保存
        'attachments': attachments,  # Absolute path will be better.
    }
    server.send_mail(destinationMail, mail)
    print('邮件发送成功， 作业规则已更新')


def move2History():
    confFile = config_folder + f'AssignConf{currentTime}.ini'
    os.rename(local_conf, confFile)
    return confFile


def move_img2history(img_path):
    imgConf = config_folder + f'AssginImg{currentTime}.jpg'
    os.rename(img_path, imgConf)
    return imgConf


def despatch_main():
    """编辑配置文件并下发"""
    os.system(f"start {csvFile}")
    # os.system(f"notepad {Server_setting}")
    print(highlight_str("我已确认更改好 作业内容与 提示", "input"))
    input()
    from conf.Server_setting import img_conf
    if not img_conf:
        img_conf = None
    elif not os.path.exists(img_conf):
        img_conf = None
    local_config_path = parseStr2config(parseCsv2Config(csvFile))
    # local_config_path = makeAssignment(assignment_str, update_info)
    Dispatch_Rule(local_config_path, img_conf)
    ReadOutputConfigAssign(local_config_path, encoding)
    move2History()
    if img_conf:  # 归档图片
        move_img2history(img_conf)
    wait_anime(10)


if __name__ == '__main__':
    despatch_main()
    # print(parseStr2config(parseCsv2Config(csvFile)))
