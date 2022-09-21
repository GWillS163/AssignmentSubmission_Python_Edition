import os
import re


def highlight_str(string, status, char='default'):
    """返回彩色提示"""
    flag = ''
    if status == 'green':
        flag = f'\033[1;32;32m[{char}]\033[0m'
    elif status == 'red':
        flag = f'\033[0;31;31m[{char}]\033[0m'
    elif status == 'yellow':
        flag = f'\033[1;33;33m[{char}]\033[0m'
    elif status == 'blue':
        flag = f'\033[1;34;34m[{char}]\033[0m'
    elif status == 'light_blue':
        flag = f'\033[1;36;36m[{char}]\033[0m'
    elif status == 'input':
        return f"{string}\033[1;32;40m>>>\033[0m"
    return f"{flag}{string}"


def wait_anime(stride):
    """n 秒后退出"""
    symbol = "\033[1;33m#\033[0m"
    input(f"[[Enter]退出-]{'--' * stride}{symbol}")
    # print(f"[[Ctrl C]退出-{stride}]{'--' * stride}{symbol}", end='\r')
    # printed_str = ''
    # try:
    #     for quantity in range(stride + 1):
    #         for pri in range(2):
    #             printed_str += f"{symbol}"
    #             print(f"[[Ctrl C]退出-{stride - quantity}]{printed_str}", end='\r')
    #             time.sleep(0.5)
    # except KeyboardInterrupt:
    #     exit(0)

    print(f"[已退出]{symbol * stride}")


def file_re(paths, re_str):
    """通过正则筛选某个目录下的文件"""
    file_lst = []
    for i in os.listdir(paths):
        if re.match(re_str, i):
            file_lst.append(i)
    return file_lst


def acquireSelection_print(lst):
    """打印选择时的 选择框"""
    index = 0
    for i in lst:
        print(f"\t{index} > {i}", end='\n')
        index += 1


def acquireSelection_valid(choice, lst):
    """检验单选选项是否有效"""
    if choice.isdigit():
        choice = int(choice)
        if 0 <= choice < len(lst):
            return choice
    return


def acquireSelection_raw(lst):
    """
    给定lst 返回选择序号
    :param lst:
    :return:
    """
    while True:
        acquireSelection_print(lst)
        choice = input(highlight_str("\t输入选择序号:", "input"))
        if not choice.isdigit():
            print('\t\033[1;31;40m输入不合法, 请重新输入\033[0m')
        if not(0 <= int(choice)) or (not int(choice) <= len(lst)):
            print('\t\033[1;31;40m输入范围不正确, 请重新输入\033[0m')
        return acquireSelection_valid(choice, lst)


def acquireSelection_echo(lst, echo_str="\t您的文件名将会以 \033[1;35m <%s> \033[0m!作业要求的形式自动命名\n"):
    """
    给定列表 和含%s 的字符串， 获取用户选择， 打印回显
    :param lst:
    :param echo_str: 回显字符串
    :return:
    """
    acquire_num = acquireSelection_raw(lst)
    print(echo_str.replace("%s", lst[acquire_num]))
    return acquire_num


def acquireSelection_multi(lst, echo_str='\t您的文件名将会以 \033[1;35m <%s> \033[0m!作业要求的形式自动命名\n'):
    """
    给定列表 和含%s 的字符串， 获取用户选择
    :param lst:
    :param echo_str: 回显字符串
    :return:
    """
    result_lst = []
    while True:
        acquireSelection_print(lst)
        choice_str = input(highlight_str("\t输入选择序号(多选 空格分割) :", "input"))
        if choice_str == '':
            return lst
        choice_list = choice_str.split(' ')
        for choice in choice_list:
            result = acquireSelection_valid(choice, lst)
            if result == 0 or result:
                result_lst.append(lst[result])
        return result_lst


if __name__ == '__main__':
    acquireSelection_echo([2, 3, 4])
    wait_anime(3)
