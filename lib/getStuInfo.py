from db.realStuInfo import database_string


class student():
    def __init__(self, clazz, name, gender, stu_num, phone, qq, dorm):
        self.clazz = clazz
        self.name = name
        self.gender = gender
        self.stu_num = stu_num
        self.phone = phone
        self.qq = qq
        self.dorm = dorm

    def __str__(self):
        return '{} {:^4} {} |学号: {} |电话: {} |QQ: {:11} |宿舍: {}'.format(self.clazz, self.name, self.gender, self.stu_num,
                                                                       self.phone, self.qq, self.dorm, chr(12288))


# 筛选数据
# res = re.findall('\n(.{2,3})	(.)	(\d{8})	(\d{11})	(\d{8,12})	(.{6})\n', database_string,)
res = [i.split() for i in database_string.split('\n')]
# print(res)

# 数据集
stu_lst = []
for i in res:
    s = student(i[0], i[1], i[2], i[3], i[4], i[5], i[6])
    stu_lst.append(s)


def getOtherInfo(stu_num):
    """输入学号获取其他信息"""
    for i in stu_lst:
        if stu_num == i.stu_num:
            return i.name, i.clazz, i.stu_num


if __name__ == '__main__':
    print(getOtherInfo('19852331'))