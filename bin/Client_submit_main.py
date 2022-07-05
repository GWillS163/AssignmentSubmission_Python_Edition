import os
import sys
sys.path.append("..")

from lib.config_lib import *
from lib.lib_base import acquireSecletion_echo, wait_anime
from lib.mail_zmail import *
from lib.mail_pop3 import *
from lib.getStuInfo import *
from core.lib_submit import *
from functools import partial


def configCLI():
    while True:
        os.system('cls')
        print(color_title)
        IDENTITY = ''
        mailPasswd = False
        try:
            [CLAZZ, ACCOUNT, IDENTITY, mailAccount, mailPasswdEncry] = getStudentInfo(ConfFile, encoding)
            mailPasswd = decrypt(IDENTITY, mailPasswdEncry, )
            stu_info_str = f"{highlight_str(f'{CLAZZ},{ACCOUNT}, {IDENTITY}', 'green', 'Loaded')}"
        except Exception as E:
            stu_info_str = highlight_str("无个人信息", "red", "Error")

        # Menu
        advance_mode_str = highlight_str('', 'green', 'Opened') \
            if mailPasswd else highlight_str(
            f'未配置邮箱 - 需留意及时更新', 'red', 'Closed')
        menu_list = {'1': menu1_chg_config,
                     '2': menu2_open_advanced,
                     '3': menu3_submitted_query,
                     '4': menu4_about}
        print(f"\t{'=' * 10}菜单{'=' * 10}\n"
              f"\t{'1.修改个人信息':<20} {stu_info_str}\n"
              f"\t{'2.打开高级模式':<20} {advance_mode_str}\n"
              f"\t{'3.已交作业查询':<20} {advance_mode_str}\n"
              f"\t{'4.作业被收提醒':<20} {advance_mode_str}\n"
              f"\t{'  Ctrl + C 返回上一级菜单或退出':<20}\n"
              f"\t{'=' * 23}")

        try:
            menu_choose = input(highlight_str("选择菜单序号", "input"))
            if not menu_choose in menu_list:
                print(' ' * 18)
                print(highlight_str("请重新输入", 'red', '输入有误'))
                continue
            menu_list.get(menu_choose)(IDENTITY, mailPasswd)
            print(' ' * 18)
        except KeyboardInterrupt:
            return


def dragCLI(raw_file_lst):
    global testDDL, isNet
    """拖拽触发CLI代码"""
    print(color_title)
    file_lst = []
    for file in raw_file_lst:
        if os.path.exists(file):
            file_lst.append(file)
    if not file_lst:
        print(highlight_str("无有效文件", "red", "错误"))
        return
    print("读取个人信息...", end='')
    stuResult = getStudentInfo(ConfFile, encoding)
    if 'Error' in stuResult:
        print(stuResult)
        return
    # 更新配置 - 1：获取个人信息
    [CLAZZ, ACCOUNT, IDENTITY, mailAccount, mailPasswdEncryed] = stuResult
    print(f"{highlight_str(f'{CLAZZ},{ACCOUNT},{IDENTITY}', 'green', 'OK')} -"
          f"{highlight_str(f'高级模式', 'green', 'Opened') if mailPasswdEncryed else highlight_str('高级模式', 'red', 'Closed')}")

    # 更新配置 - 2：下载通用配置
    q = Queue()
    subThreadAndInf(partial(updateConfig, ConfFilePath, file_rule_acc, file_rule_psd, q), "正在更新作业收集规则")
    isNet = q.get()
    if os.path.exists(img_path):
        os.system(f"start {img_path}")
    time.sleep(1)

    # 更新配置 - 3：写入个人信息
    writeSTUCFG(CLAZZ, ACCOUNT, IDENTITY, ConfFile, encoding)
    writeMailCFG(mailAccount, mailPasswdEncryed, ConfFile, encoding)
    mailPasswd = decrypt(IDENTITY, mailPasswdEncryed)
    newCFG, acclaim, info, permitVersion, AssignList, version_ddl = ReadOutputConfigAssign(ConfFile, encoding)  # 读取配置和作业列表
    ReadOutput_notice(acclaim, info, permitVersion, AssignList)
    testDDL = version_ddl[version]
    if not isNet:
        print(highlight_str("进入离线模式，仅可查看上次更新时的作业与更名", 'yellow', 'notice'))

    if not newCFG and not AssignList:
        return
    # 用户指定作业对应的 文件规则
    match_list = {}
    print('\n\033[1;34m请输入序号作答:\033[0m')
    prevent_duplicate = []
    for file in file_lst:
        file_name = file.split("\\")[-1]
        while True:  # 一直选择防止重复。
            print("文件:" + highlight_str("是什么作业?", 'light_blue', file_name))
            # print(f'\033[1;36;52m<{file_name}>\033[0m是什么作业?')
            curriculumNum = acquireSecletion_echo(AssignList)
            if not curriculumNum in prevent_duplicate:
                break
            print(highlight_str("已选择过本课程作业", "red", "Error"))
        prevent_duplicate.append(curriculumNum)
        match_list[file] = {"FileRule": newCFG[AssignList[curriculumNum]]['FileRule'],
                            "AssignNickName": newCFG[AssignList[curriculumNum]]['AssignNickName']
                            }

    # 匹配文件到规则自动命名
    allAssignFileList = []
    allAssignNameList = []
    account_courseName = f"{ACCOUNT}:"
    match_list_keys = match_list.keys()
    for file in match_list_keys:
        fileRule1 = match_list[file]['FileRule']
        account_courseName = f"{account_courseName}_{match_list[file]['AssignNickName']}"
        try:
            new_file_path = RenameByRule(file, fileRule1, CLAZZ, IDENTITY, ACCOUNT)
            print(f'\t{file} \n\t已重命名成功为>> \n\t{new_file_path}\n')
            allAssignFileList.append(new_file_path)
            allAssignNameList.append(match_list[file]['AssignNickName'])
        except FileNotFoundError as E:
            print(f'\t{file} \n\t{highlight_str("文件不存在，将不被发送","red","Error")}:\n\t{E}\n')
        except FileExistsError as E:
            print(f'\t{file} \n\t{highlight_str("文件已存在，无法覆盖, 将不被发送","red","Error")}:\n\t{E}\n')
        except Exception as E:
            print(f'\t{file} \n\t{highlight_str("发生了其他未知错误", "red", "Error")}:\n\t{E}\n')

    # 发送邮件
    if not allAssignFileList:
        print(DingGrandfather)
        print(highlight_str("无文件被需要发送", 'red', 'Error'))
        return

    # 没网
    if not isNet:
        print(highlight_str("重命名结束", "yellow", "离线模式"))
        return
    # 有网 - 公共版本版
    if isOverDDL(testDDL) and not mailPasswd:  # 截止日期后还没配置邮箱的话
        print(highlight_str("重命名结束", "green", "OK"))
        print('\033[1;33m[Notice] \033[0m此版本(' + version + ')发送功能可用至' + testDDL, "请在非拖拽状态下双击打开设置个人账户")
        return
    # 有网 - 登录账号版
    if not mailPasswd:  # 没有邮箱的话 替换
        mailAccount = file_rule_acc
        mailPasswd = file_rule_psd
    subThreadAndInf(partial(sendMail, ACCOUNT, allAssignNameList,
                            mailAccount, mailPasswd, allAssignFileList, send_to, account_courseName),
                    "正在发送作业")

    # 最终提示
    print(f"{len(file_lst)}个作业，执行结束")


def menu1_chg_config(Old_IDENTITY, mailPasswd):
    while True:
        IDENTITY = input(highlight_str('学号(例:19852331):', "input"))
        if IDENTITY == Old_IDENTITY:
            print(highlight_str("与之前相同", "yellow", "提示"))
            time.sleep(2)
            return
        print(f"\t\t(本软件仅对限定人员开放使用)")
        try:
            ACCOUNT, CLAZZ, IDENTITY = getOtherInfo(IDENTITY)
            writeSTUCFG(CLAZZ, ACCOUNT, IDENTITY, ConfFile, encoding, mode='w')
            writeMailCFG("", "", ConfFile, encoding,)
            break
        except Exception as E:
            print(E)

def menu2_open_advanced(IDENTITY, mailPasswd):
    try:
        mailAccount = f"{IDENTITY}@czjtu.edu.cn"
        print(highlight_str("http://mail.czjtu.edu.cn2, 官网←可重设密码", "blue", "官网找回密码👉") +
              f"\n你的账号: {IDENTITY}@czjtu.edu.cn")
              # "\n初始密码:Czjt+身份证后六位 或 Abc+身份证后六位 或 Hbxy+身份证后六位。但建议直接重设密码")
        while True:
            mailPasswd = input(highlight_str(f'请输入密码:', "input"))
            print("\n正在发送测试邮件")
            try:
                sendMail(ACCOUNT, [], mailAccount, mailPasswd, [], mailAccount, f"测试邮件 By Assignment_Submit_Tool_v{version}")
            except Exception as E:
                print("请重新输入，因为出现了异常", E)
                continue
            time.sleep(1)
            break
            # if not input(highlight_str("你是否收到测试邮件[回车确认保存/N]", "input")):
            #     break
    except KeyboardInterrupt:
        print("\n退出，将不保存")
        return
    mailPasswdEncryed = encrypt(IDENTITY, mailPasswd, )
    writeMailCFG(mailAccount, mailPasswdEncryed, ConfFile, encoding)
    print('\033[1;32;40m[OK]\033[0m 模式更新')


def menu3_submitted_query(IDENTITY, mailPasswd):
    """

    :param IDENTITY:
    :param mailPasswd:
    :return:
    """
    if not mailPasswd:
        print(highlight_str("未激活高级模式", "red", "Error"))
        return
    if not os.path.exists(LocalSendHistory):
        print(highlight_str("未记录过发送历史", "red", "Error"))
        return
    print(highlight_str("仅为本地发送的记录", 'yellow', "Notice"))
    try:
        with open(LocalSendHistory, mode='r', encoding=encoding) as f:
            for line in f:
                print(line, end='')
                time.sleep(0.3)
        wait_anime(20)
    except KeyboardInterrupt:
        return


def menu4_about(IDENTITY, mailPasswd):
    """服务端向邮箱发送提醒，本函数进行查询邮件"""
    if not mailPasswd:
        print(highlight_str("未激活高级模式", "red", "Error"))
        return
    print(highlight_str("正在查询", 'blue', "历史消息记录"))
    print(f"{'日期':^22}\t {'来自':^28}\t {'标题':^15}\n")
    try:
        get_all_receive(f"{IDENTITY}@czjtu.edu.cn", mailPasswd, 50, submit_mail_flag)
    #     print("查询结束")
        print("本内测版开发中... 客户端不受影响")
        # print("如何打开被收提醒")
        print("当作业被收集时，会将向你的账号发送一个提醒")
        print("当将你的企业邮账号绑定至手机QQ，即可及时收到提醒")
        wait_anime(40)
    except KeyboardInterrupt:
        return


def main():
    os.system("color 08")
    file_lst = detect_file()  # 收集文件，指定对应的作业

    # 直接双击打开-填写个人信息
    if not file_lst:
        configCLI()
        return
    # 拖拽上传触发以下代码
    dragCLI(file_lst)
    wait_anime(40)


if __name__ == "__main__":
    isNet = None
    color_title = "您正在使用尊贵的"f"\033[1;33;52mAssignment_Submit_Tool\033[0m"f" \033[1;32;40mUltra\033[0m"f" \033[1;31;40mPremium\033[0m"f" \033[1;35;40mMax\033[0m \033[1;36;40mPlus\033[0m \033[1;34;40mC\033[0m\033[1;31;40mo\033[0m\033[1;37;40ml\033[0m\033[1;32;40mo\033[0m\033[1;31;40mr\033[0m \033[1;33;40mVIP\033[0m+ Edition\n"\
                  f"\tVersion: {version} \t \n"
    main()

    # try:
    #     main()
    # except Exception as E:
    #     print("主程序报错:", E)
