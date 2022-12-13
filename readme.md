## 介绍 Description
本软件主要用来解决交作业并重命名的问题:
学生提交作业，老师异步下载。

分为学生端和服务端。使用邮箱服务，无需服务器费用。

## 安装后使用方法
1. 学生拖拽打开软件，输入选择文件，回车发送即可。
2. 老师打开软件，回车即可下载。

首次学生使用需双击打开（配置界面），进行配置个人信息
![image](https://user-images.githubusercontent.com/49674629/191522387-c1a03cae-73e4-4ab9-9f49-96cd0e09fd34.png)
之后拖拽作业文件打开，即可选择提交


## 用户/自定义 方式：
请查看bin/readme.md

> 学生端& 服务端 主程序入口在.\bin下
![](res/eacca210-fc2d-11ec-9101-c54c4dd9fcf6.jpeg?v=1&type=image)

>### the Folder tree I learned in last month ago
>![](res/76325cf0-fc2e-11ec-9101-c54c4dd9fcf6.jpeg?v=1&type=image)

>some libs![](res/e8135900-fc2e-11ec-9101-c54c4dd9fcf6.jpeg?v=1&type=image)


# 开发者如何部署
这部分没有需求还未完成。

## 定制你的客户端。
修改config.py
将config.py中的邮箱配置改为自己的邮箱配置

然后使用pyinstaller 打包成exe文件，

## 定制你的服务端
修改config.py， 收件人信息应该是你的邮箱地址。
最后运行某个.py文件，就能下载文件了。
