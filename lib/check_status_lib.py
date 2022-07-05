import csv
import re
from lib.lib_base import highlight_str
from lib.lib_base import file_re


def get_student_name_list(data_path):
    # 拿到数据列表
    student_name_lst = []
    try:
        dataHeader, stu_lst = getStuList(data_path)
    except Exception as E:
        raise f"读取文件时错误:{E}"
    for file_name in stu_lst:
        student_name_lst.append(file_name.name)

    return dataHeader, stu_lst, student_name_lst


def getStuList(datacsv):
    try:
        ff = open(datacsv)
    except Exception as E:
        raise "文件打开出错！" + str(E)
    res = csv.reader(ff)
    # 数据集
    dataHeader = []
    # print(f"数据来自{datacsv}")
    for i in res:  # 表头
        # print(i)
        for x in i:
            dataHeader.append(x)
        break

    stu_lst = []
    for i in res:
        for x in range(7 - len(i)):
            i.append('')
        s = newStudent(i[0], i[1], i[2], i[3], i[4], i[5])
        stu_lst.append(s)
    return dataHeader, stu_lst


class newStudent:
    """通用表头"""

    def __init__(self, a, b="", c="", d="", e="", f=""):
        self.name = a
        self.clazz = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.status = {}

    def __str__(self):
        return self.name


def detect_file_existence_state(stu_lst, path, re_str, base_name=None):
    """Core： 检测指定路径下的文件是否存在"""

    # 拿到本地数据文件名
    file_lst = file_re(path, re_str)
    course_name = path.split('\\')[-1]
    student_name_lst = [i.name for i in stu_lst]
    base_file = ''
    base_name = ''
    for stu_name in student_name_lst:  # 以所有学生为 基准拿到通用匹配方式
        for file_name in file_lst:
            if stu_name in file_name:
                base_file = file_name
                base_name = stu_name
                break
        if base_file:
            break
    base_printed_str = f"{'Base'} - {highlight_str('', 'blue', base_name):20}" \
                       f" - {highlight_str('', 'green', base_file):60}"
    # print()
    base_position = re.search(base_name, base_file)
    if not base_position:
        print("检测基准名时出现问题，检查路径和基准名\n\n\n", base_file, path)
        return

    local_file_name = []
    not_rule_file_name = []
    for file_name in file_lst:
        # 从文件名中extract 出 姓名
        local_file_stu_name = file_name[base_position.start():base_position.end()]
        # 如果 提取出的是学生 则进入下一个循环
        if local_file_stu_name in student_name_lst:
            local_file_name.append(local_file_stu_name)
            continue
        # 若匹配到的人名不在列表，则特殊处理
        if len(base_name) == 3:  # 基准名字是3个字时，注意匹配两个字的名字， 即减1
            local_file_stu_name = file_name[base_position.start():base_position.end() - 1]
        elif len(base_name) == 2:
            local_file_stu_name = file_name[base_position.start():base_position.end() + 1]

        if local_file_stu_name in student_name_lst:
            local_file_name.append(local_file_stu_name)
        else:
            # print('命名规则不一致:', file_name)
            not_rule_file_name.append(file_name)

    # 输出 已提交，未提交，和包含状态的所有
    # SubmittedLst = []
    # UnSubmittedLst = []
    for stu in stu_lst:
        # if stu.clazz == '1909':
        if stu.name in local_file_name:
            # stu.state = '✔已提交'
            stu.status.update({path.split('\\')[-1]: highlight_str("", "green", "√")})
            # SubmittedLst.append(stu)
        else:
            # stu.state = '❌未提交'
            stu.status.update({path.split('\\')[-1]: highlight_str("", "red", "×")})
            # UnSubmittedLst.append(stu)
    return stu_lst, not_rule_file_name, base_printed_str
    # return SubmittedLst, UnSubmittedLst, stu_lst, not_rule_file_name, base_printed_str


