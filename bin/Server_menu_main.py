import sys
sys.path.append("..")
from bin.Server_check_main import check_status_main
from lib.lib_base import acquireSelection_raw
from core.Server_DespatchFileRule import *
from core.Server_receive_mail import *


def menu_(func):
    try:
        func()
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    while True:
        os.system('cls')
        print("请选择菜单")
        menu_list = {'发送作业': despatch_main,
                     '下载作业': receive_main,
                     '查看本地作业': check_status_main,
                     }
        lst = [i for i in menu_list.keys()]
        choice = acquireSelection_raw(lst)
        menu_(menu_list[lst[choice]])
