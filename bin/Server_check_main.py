from lib.check_initial import default_config, default_csv
from lib.check_status_lib import get_student_name_list
from lib.lib_base import highlight_str, acquireSecletion_multi
from core.check_core import get_simple_stu_status_lst, simple_print_form, simple_print_not_rule, get_sub_unsub_list
from conf.Server_setting import conf_file, init_data_file
import os.path
import configparser
import csv

# sys.path.append("D:\Project\hbxy_tools_env")  # 添加工作目录
# conf_file = 'D:\Tools\config.ini' #TODO: 仅测试


def init():
    """读取 或 重置配置"""
    def make_confile():
        with open(conf_file, 'w', encoding='utf-8') as f:
            f.write(default_config)
        print(highlight_str(f'未发现配置文件，已初始化. 请留意同目录下的{conf_file}', 'green', 'OK'))

    def make_datacsv():
        with open(init_data_file, 'w', encoding='gbk') as f:
            f.write(default_csv)
            csv.writer(f)
        print(highlight_str('新建了默认花名册，请参照更改为你的花名册。', 'green', 'OK'))
        print('格式如下：')
        print(default_csv)
        print()

    # 首次启动:
    if not os.path.exists(conf_file):
        make_confile()
        make_datacsv()
        print(highlight_str('首次启动初始化完成，留意新建了两个配置文件', 'green', 'OK'))
        print(highlight_str(f'请配置{conf_file}内 几个初始键值，再次双击运行本软件', 'yellow', 'Notice'))
        print(highlight_str(f'ヾ(￣▽￣)Bye~Bye~', 'red', '再见'))
        raise KeyboardInterrupt
    # 新建默认配置
    data_path, path_list = '', []
    try:
        cfg = configparser.ConfigParser()
        cfg.read(filenames=conf_file, encoding='utf-8', )
        data_path = cfg['data']['data_path']
        display_col = cfg['data']['display_col']
        paths = cfg['execute_path']['path']
        # base_name = cfg['execute_path']['base_name']
        path_list = [pathOne for pathOne in paths.split('\n')]
        print(f'{highlight_str("已读取配置:", "green", "OK")}\n'
              f'作业路径:{path_list}\n'
              f'数据文件:{data_path}\n'
              )
    except Exception as E:
        print("出现了一些问题:", E)
        make_confile()
        return

    if not data_path:
        print(highlight_str("无人员信息！请填写['data']下['data_path']的路径", "red", "Error"))
        return
    if not path_list:
        print(highlight_str("无作业文件夹信息！请填写['execute_path']下['path']的路径", "red", "Error"))
        return
    # if not base_name:
    #     print(highlight_str("无基准姓名信息！请填写['execute_path']下['base_name']， "
    #                         "基准姓名的作用在于从众多文件中定位到其他人的姓名，"
    #                         "因此相同的问及那命名格式也很重要", "red", "Error"))
    #     return
    # 新建数据文档
    if os.path.exists(data_path):
        try:
            dataHeader, stuobj_lst, student_list = get_student_name_list(data_path)
        except UnicodeError:
            print('数据编码错误！')
            return
    else:
        make_datacsv()
        return
    return path_list, stuobj_lst, student_list, dataHeader, display_col

# def old_main():
#     from print_out import get_curriculum_stu_lst, trans2stu_curriculum, \
#         print_as_final_form, print_not_rule
#     # 主程序 - 查目录 - 整理格式 - 打印输出
#     curriculum_stu_lst = get_curriculum_stu_lst(stuobj_lst, path_list, base_name)
#     print_data_unsub = trans2stu_curriculum(curriculum_stu_lst)
#     print_as_final_form(print_data_unsub, curriculum_stu_lst, display_col)
#     print_not_rule(curriculum_stu_lst)


def check_status_main():
    n = 1
    select_path_list = []
    while True:
        raw_path_list, stuobj_lst, student_name_list, dataHeader, display_col = init()
        # 存储合规路径
        valid_path_list = []
        for path in raw_path_list:
            if not os.path.exists(path):
                print(path, "that path is NOT existence")
                continue
            valid_path_list.append(path)

        if select_path_list:
            path_list = select_path_list
        else:
            path_list = valid_path_list
        curriculum_lst = [path.split('\\')[-1] for path in path_list]
        curriculum_lst_display = [path[:6] for path in curriculum_lst]
        if not display_col:
            input('信息不全，回车退出')
            exit(0)

        # 把数据存到stu obj内， 会方便很多
        stu_status_lst,  not_rule_lst_all \
            = get_simple_stu_status_lst(stuobj_lst, path_list)
        SubmittedLst, UnSubmittedLst = get_sub_unsub_list(stu_status_lst, curriculum_lst)
        simple_print_form(SubmittedLst, curriculum_lst_display, display_col)
        simple_print_form(UnSubmittedLst, curriculum_lst_display, display_col)
        # for base_str in base_printed_str_lst:
        #     print(base_str)
        simple_print_not_rule(not_rule_lst_all)

        print(highlight_str("输入选择项 筛选仅显示某项作业", 'green', '重新运行'))
        select_path_list = acquireSecletion_multi(valid_path_list)
        # input()


if __name__ == '__main__':
    check_status_main()
