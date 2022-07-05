import os.path

from lib.lib_base import highlight_str
from lib.check_status_lib import detect_file_existence_state


def get_simple_stu_status_lst(stu_lst, path_list):
    " 遍历所有课程文件夹，将stu 对象， 都进行添加作业状态"
    stu_status_lst = []
    not_rule_lst_all = []
    base_printed_str_lst = []
    for path in path_list:  # 遍历所有课程 添加stuObj数据
        try:
            stu_status_lst, not_rule_lst, base_printed_str \
                = detect_file_existence_state(stu_lst, path, '.*')
            not_rule_lst_all.append({'course': path.split('\\')[-1],
                                     'base_printed_str': base_printed_str,
                                     'file_list': not_rule_lst})
            # base_printed_str_lst.append(base_printed_str)
        except Exception as E:
            print(f"检查作业提交情况时出现了问题{E}")
            return

    return stu_status_lst, not_rule_lst_all,  # base_printed_str_lst


def get_sub_unsub_list(stu_status_lst, course_list):
    """限定了 选择的科目才会判断"""
    # 但凡有一个 x 的，就放入 UnSubmittedLst

    SubmittedLst, UnSubmittedLst = [], []
    for stu_obj in stu_status_lst:
        # 存储个人限定科目状态
        status_list = []
        for course in course_list:  # 取出需要找的值
            status_list.append(stu_obj.status[course])

        # 检查个人限定的科目
        if "\x1b[0;31;31m[×]\x1b[0m" in status_list:
            UnSubmittedLst.append(stu_obj)
        else:
            SubmittedLst.append(stu_obj)
    return SubmittedLst, UnSubmittedLst


def simple_print_form(stuobj_lst, curriculum, display_col='1'):
    """把 {课程：[学生,学生]} 转置为
    {学生：[课程1，课程2]}
    """
    for stuobj in stuobj_lst:
        stu_name = stuobj.name
        line = ""
        for cur in stuobj.status.keys():
            line += f"{stuobj.status[cur]:^23} "
        line += f"{stu_name:<4}\t"  # 制作一行， 名字置后
        if '2' in display_col:
            line += f"{stuobj.clazz:^8} "
        if '3' in display_col:
            line += f"{stuobj.c:^8} "
        if '4' in display_col:
            line += f"{stuobj.d:^8} "
        if '5' in display_col:
            line += f"{stuobj.e:^8} "
        if '6' in display_col:
            line += f"{stuobj.f:^8} "

        # if stuobj.clazz == "1910":  # 10班的则先打印
        print(line)
        # else:
        # late_print += f"{line}\n"  # 9 班放到后面
    # print('-' * 40)
    course_title = f""
    for cur_name in curriculum:
        course_title += f"{cur_name:^6} |"
    files_count = f""
    for cur_name in curriculum:
        files_count += f"{len(stuobj_lst):^6} |"
    print('-' * 40)
    print(course_title)
    print(files_count)
    print('-' * 40)


def simple_print_not_rule(not_rule_lst_all):
    for not_rule_dict in not_rule_lst_all:
        if not not_rule_dict["file_list"]:
            continue
        print()
        # print(base_printed_str)
        print(f"{highlight_str('', 'light_blue', not_rule_dict['course']):35}")
        print(not_rule_dict['base_printed_str'])
        uncanny_symbol = highlight_str(f"未知", 'yellow', '❓')
        # print(uncanny_symbol)
        index = 0
        for file in not_rule_dict["file_list"]:
            index += 1
            print(f"{index:4} - {uncanny_symbol:20} - {file}")
    print()
