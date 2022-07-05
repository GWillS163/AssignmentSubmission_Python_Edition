# -*- coding: utf-8 -*-

default_config = r""" # 2022-4-19 版
[data]
data_path = .\\data.csv
# data_path 用来指向存放的花名册的路径.首列是姓名,次列是学号,其他为自定义值
display_col = 2
# display colum 用来 显示花名册的列值. 程序固定显示第一列(姓名), 2为显示第二列(班级), 2,3,4 为显示2,3,4列.

[execute_path]
# 在所有文件名格式相同的情况下，自动通过基准姓名(按花名册逐个匹配作业)，匹配到其他人在文件中的姓名。
path = D:\hbxy\Phase2\SoftwareTest\黑盒测试收集
     #D:\hbxy\Phase2\UML\UML2
       #D:\hbxy\Phase2\UML\UML1-作业1收集
       #D:\hbxy\Phase2\AlgorithmDesign\数据结构作业2_2022-3-24
       #D:\hbxy\Phase2\Hadoop\homework1_spider
# 多参数填写：可回车 + 空格填写. 除了第一个行都可用 # 号注释掉（不执行）
"""

default_csv = """姓名,班级,学号,<自定义值1>,<自定义值2>
张三,2,20001111,男,173
李四,3,19992222,女,165"""

if __name__ == '__main__':
    import csv
    with open('2323.csv', 'w', encoding='gbk') as f:
        f.write(default_csv)
        csv_data = csv.writer(f)
        # f.write(csv_data)