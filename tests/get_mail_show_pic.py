import os

import zmail

from lib.lib_base import file_re
from lib.mail_zmail import updateConfig
from conf.Client_setting import *

if __name__ == '__main__':

    # Server = zmail.server(file_rule_acc, file_rule_psd)
    # mail = Server.get_mails(subject="测试作业展示图片")
    # # config_pic = "D:\\info.jpg"
    # # # mail[-1]
    # img_folder = '.'
    # zmail.save_attachment(mail[0], img_folder, overwrite=True)
    # # if os.path.exists(img_)
    # lst = file_re(img_folder, '.*\.jpg')
    # if not lst:
    #     lst = file_re(img_folder, '.*\.png')
    # os.system(f"start {lst[0]}")

    updateConfig(ConfFilePath, file_rule_acc, file_rule_psd)

    if os.path.exists(img_path):
        os.system(f"start {img_path}")
    print("continue")
