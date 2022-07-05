from imbox import Imbox
import base64
import zmail
from conf.Server_setting import *


# from conf.Client_settings import file_rule_acc, file_rule_psd, submit_mail_flag, update_mail_flag
# from mail_zmail import getMailIWant


def get_unread_File(username, password, download_path, stmp_server="smtp.exmail.qq.com"):
    reply_data_lst = []
    with Imbox(stmp_server, username, password, ssl=True, ssl_context=None,
               starttls=False) as imbox:
        unread_box_messages = imbox.messages(unread=True)
        length = len(unread_box_messages)
        print(f"连接[{stmp_server}]成功, 共{length}个, 正在下载")
        n = 1

        for uid, message in unread_box_messages:
            print(f"[{n}/{length}]", end='')
            title = message.subject
            if update_mail_flag in title:
                imbox.mark_seen(uid)
                print("标记了 [RuleUpdate] 已读")
                n += 1
                continue
            if not submit_mail_flag in title:
                print(f"非 {submit_mail_flag}， 跳过")
                n += 1
                continue
            title = title.replace(f'{submit_mail_flag}', '')
            try:
                date = message.date
            except AttributeError:
                date = '未知时间'
            # content = message.body['plain']
            from_addr = message.sent_from[0]['email']
            print(f"{title:^34},\t {date:^32},\t {from_addr}")

            # 保存文件
            for attach in message.attachments:
                file_name_lst = []
                try:
                    file_name = base64.b64decode(attach['filename'].replace('=?utf-8?b?', '')).decode()
                    with open(download_path + file_name, 'wb') as f:
                        f.write(attach['content'].getvalue())
                    file_name_lst.append(file_name)

                    # 发送回执
                    if from_addr == file_rule_acc or '提醒' in title:
                        print(f"     不需发送回执，来自旧版本{file_rule_acc}:", from_addr, title)
                        imbox.mark_seen(uid)
                        # n += 1
                        continue
                    send_reply_mail(f"{receive_mail_flag}您的文件({title})已被自动处理脚本下载",
                                    f"接收文件列表内容:{','.join(file_name_lst)}\n"
                                    f"Date:{date}",
                                    f"{from_addr}")
                    print(f" 回执发送完成")
                    imbox.mark_seen(uid)
                except Exception as E:
                    print("保存文件出现了问题:", E)
            n += 1
    return reply_data_lst


# server = zmail.server(czjtuacc, czjtupsd, smtp_host='smtp.exmail.qq.com')
server = zmail.server(file_inbox_acc, file_inbox_psd, smtp_host='smtp.qq.com')


# server = zmail.server(qqacc, qqpsd)
def send_reply_mail(title, context, to_mail):
    """以19852331@czjtu.edu.cn 发送单个回执"""

    server.send_mail(to_mail, {
        'subject': title,  # .encode("utf-8").decode("utf-8"),
        'content_text': context,
    }, timeout=200)
    return True


def main_down_reply():
    """接收文件并下载"""
    reply_data_lst = get_unread_File(czjtuacc, czjtupsd, download_path)
    n = 1
    length = len(reply_data_lst)
    print("\n正在发送回执:")
    for reply in reply_data_lst:
        print(f"[{n}/{length}] ", end="")
        send_reply_mail(f"[接收提醒]您的文件({reply['title']})已被自动处理脚本下载",
                        f"接收文件列表内容:{reply['file_name']}"
                        f"<br>"
                        f"Date:{reply['date']}",
                        reply['from_addr'])
        print(f"{reply['title']:^30} 发送完成")
        n += 1


def receive_main():
    get_unread_File(czjtuacc, czjtupsd, download_path, 'smtp.exmail.qq.com')
    get_unread_File(file_rule_acc, file_rule_psd, download_path, 'smtp.qq.com')
    get_unread_File(file_inbox_acc, file_inbox_psd, download_path, 'smtp.qq.com')

    input("任意键退出")


if __name__ == '__main__':
    # main_down_reply()
    receive_main()
