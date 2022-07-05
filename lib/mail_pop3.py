from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import base64
import poplib
import re
import time

from conf.Client_setting import update_mail_flag, receive_mail_flag


def parser_file(msg):
    """返回 30 Mar 2022 22:42:58      :    gwills@qq.com     >>>  [学委]  软件1909-19852311-赵浩天-UML作业2.png
        """
    content, file_data = msg.get_payload()
    content_charset = content.get_content_charset()
    file_name = ''
    if "attachment;" in str(msg):
        file_data = file_data.get_payload(decode=True)
        # file_data = content[1]._headers.
        file_bin = file_data.as_string().split('base64')[0]
        file_name = re.findall('utf-8\?b\?(.{20,})?"', file_bin)[0]
        file_name = base64.b64decode(file_name).decode()
        f = open(file_name, 'wb')  # 注意一定要用wb来打开文件，因为附件一般都是二进制文件
        f.write(file_data)
        f.close()
        # TODO: 将邮件标为已读
        # TODO: 保存回执所需参数  ToMail 科目(title.strip('[客户端作业提交]')
        print('save attach file succeed')

    text = content.as_string().split('base64')[-1]
    hdr, from_addr = parseaddr(msg['From'])
    text_content = base64.b64decode(text).decode(content_charset)  # base64解码
    file_path = text_content.split('\\')[-1].split('-本消息')[0]
    title = parser_subject(msg)

    # hdr, to_addr = parseaddr(msg['To'])
    # if to_addr == "19852331@czjtu.edu.cn":
    #     to_addr = "\033[1;36;40m[学委]\033[0m"
    date = re.findall("Date: \w{3}, (.*\d\d)? +", str(msg))[0]
    print(f" {date:^22}: {from_addr:^20} {file_path:<40}")
    return file_name, text_content, from_addr, title


def get_all_submmited(useraccount, file_rule_acc, password, count, pop3_server='imap.exmail.qq.com'):
    """已弃用"""
    server = poplib.POP3(pop3_server)
    try:

        # 打开或者关闭调试信息，为打开，会在控制台打印客户端与服务器的交互信息
        # server.set_debuglevel(1)
        print(server.getwelcome().decode('utf8'))  # 打印POP3服务器的欢迎文字，

        # 开始进行身份验证
        server.user(useraccount)
        server.pass_(password)

        # 使用list()返回所有邮件的编号，默认为字节类型的串
        rsp, msg_list, rsp_siz = server.list()
        # print("服务器的响应: {0},\n消息列表： {1},\n返回消息的大小： {2}".format(rsp, msg_list, rsp_siz))
        # print('邮件总数： {}'.format(len(msg_list)))

        # 获取五十个邮件
        msg_50_list = []
        total_mail_numbers = len(msg_list)
        for _ in range(count):
            rsp, msglines, msgsiz = server.retr(total_mail_numbers)
            msg_content = b'\r\n'.join(msglines).decode('gbk')
            msg = Parser().parsestr(text=msg_content)

            # to_mail, course, file_name = Parser_fileSave(msg)
            file_name, text_content, from_addr, title = parser_file(msg)
            if from_addr == file_rule_acc:
                continue
            # TODO:  准备回执处理
            msg_50_list.append(file_name)
            server.dele(total_mail_numbers)
            total_mail_numbers -= 1
        return msg_50_list
    except KeyboardInterrupt:
        pass
    server.close()


def get_pop3_server(useraccount, password, pop3_server='imap.exmail.qq.com'):
    """仅供个人用户使用
    1. 建立server"""
    # 开始连接到服务器
    server = poplib.POP3(pop3_server)
    # 开始进行身份验证
    server.user(useraccount)
    server.pass_(password)

    # 返回邮件总数目和占用服务器的空间大小（字节数）， 通过stat()方法即可
    email_num, email_size = server.stat()
    # print("消息的数量: {0}, 消息的总大小: {1}".format(email_num, email_size))

    # 使用list()返回所有邮件的编号，默认为字节类型的串
    rsp, msg_list, rsp_siz = server.list()
    return server, rsp, msg_list, rsp_siz


def parser_address(msg):
    """用来解析邮件来源"""
    hdr, addr = parseaddr(msg['From'])
    # name 发送人邮箱名称， addr 发送人邮箱地址
    name, charset = decode_header(hdr)[0]
    if charset:
        name = name.decode(charset)
    return name, addr


def parser_subject(msg):
    """用来解析邮件主题"""
    subject = msg['Subject']
    value, charset = decode_header(subject)[0]
    if charset:
        value = value.decode(charset)
    return value


def get_email(server, mail_num):
    """2. 通过 获取email"""
    rsp, msglines, msgsiz = server.retr(mail_num)
    # print("服务器的响应: {0},\n原始邮件内容： {1},\n该封邮件所占字节大小： {2}".format(rsp, msglines, msgsiz))
    msg_content = b'\r\n'.join(msglines).decode('gbk')

    msg = Parser().parsestr(text=msg_content)
    return msg


def parser_content(msg):
    """解析正文"""
    content = msg.get_payload()
    try:  # 获取编码格式
        content_charset = content[0].get_content_charset()
    except:
        content_charset = 'utf-8'
    try:
        text = content[0].as_string().split('base64')[-1]
        text_content = base64.b64decode(text).decode(content_charset)  # base64解码
    except:
        # text = content[1].as_string().split('base64')[-1]
        # text = content[1].split('base64')[-1]
        text_content = "未知无法解析信息(可能来自其他人发送):" + str(content)[:20] + "..."
    return text_content
    # 添加了HTML代码的信息
    # print('文本信息: {0}\n添加了HTML代码的信息: {1}'.format(text_content.split('\\')[-1].split('-本消息')[0], html_content))


def format_receive(msg, submit_mail_flag):
    """TODO:
    作业被下载通知
    作业开放提交通知
    作业提交状态公示"""
    title = parser_subject(msg)
    title = title.strip("By Assignment_Submit_Tool") \
        .replace(f"{submit_mail_flag}", "\033[1;36;40m[作业提交]\033[0m") \
        .replace(f"{update_mail_flag}", "\033[1;33;40m[作业提交提醒]\033[0m")\
        .replace(receive_mail_flag, "\033[1;31;40m[作业接收提醒]\033[0m")
    context = parser_content(msg)
    context = context.split('-')[0]

    hdr, from_addr = parseaddr(msg['From'])
    if from_addr == "gwills@qq.com":
        from_addr = "\033[1;32;40m[学委通知]\033[0m"
    date = re.findall("Date: \w{3}, (.*\d\d)? +", str(msg))[0]
    return f"{date:^22}\t {from_addr:^28}\t {title:^15}\n" \
           f"\t{context:^22}\n"


def get_all_receive(account, passwd, count, submit_mail_flag, pop3_server='imap.exmail.qq.com'):
    """普通用户无法查询已交作业"""

    server, rsp, msg_list, rsp_siz = get_pop3_server(account, passwd)
    is_empty = []
    if len(msg_list) < count:
        total_mail_numbers = len(msg_list)
    else:
        print(f"默认仅提供{count}条数据, 更多请移步官网")
        total_mail_numbers = count
    for _ in range(total_mail_numbers):
        rsp, msglines, msgsiz = server.retr(total_mail_numbers)
        msg_content = b'\r\n'.join(msglines).decode('gbk')
        msg = Parser().parsestr(text=msg_content)

        # title = parser_subject(msg)
        # if not submit_mail_flag in title: # TODO: 应该仅收到3 种通知
        #     continue
        format_str = format_receive(msg, submit_mail_flag)  # 格式化代码
        print(format_str)
        time.sleep(0.3)
        is_empty.append(format_str)
        total_mail_numbers -= 1
    if not is_empty:
        print("您尚未收到过提醒")
    server.close()
    return


if __name__ == '__main__':
    # from settings.submit_settings import *
    # get_all_receive(account, passwd, 50)
    pass
