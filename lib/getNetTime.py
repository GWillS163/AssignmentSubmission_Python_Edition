import datetime
import http.client
import time


def get_webServerTime():
    time_conn = http.client.HTTPConnection('www.baidu.com')
    time_conn.request("GET", "/")
    r = time_conn.getresponse()
    # r.getheaders() #获取所有的http头
    ts = r.getheader('date')  # 获取http头date部分
    # 将GMT时间转换成北京时间
    ltime = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    # print(ltime)
    ttime = time.localtime(time.mktime(ltime) + 8 * 60 * 60)
    # print(ttime)
    dat = "%u-%02u-%02u" % (ttime.tm_year, ttime.tm_mon, ttime.tm_mday)
    tm = "%02u:%02u:%02u" % (ttime.tm_hour, ttime.tm_min, ttime.tm_sec)
    currenttime = dat

    return datetime.datetime.strptime(currenttime, "%Y-%m-%d")

