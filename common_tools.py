#coding:utf-8
import itertools as its
import pywifi
from pywifi import const
import time
import datetime


def scan_wifi(sign=-90):
    iface = get_inface()[0]
    iface.scan()  # 扫描周围wifi
    time.sleep(8)  # 不缓冲显示不出来
    result = iface.scan_results()  # 获取扫描结果，wifi可能会有重复
    has = []  # 初始化已扫描到的wifi
    wifi_list = []  # 初始化扫描结果
    for i in result:
        if i not in has:  # 若has中没有该wifi，则
            has.append(i)  # 添加到has列表
            if i.signal > -90:  # 信号强度<-90的wifi几乎连不上
                wifi_list.append((i.ssid, i.signal))  # 添加到wifi列表
                print('wifi信号强度：{0}，名称：{1}。'.format(i.signal, i.ssid))  # 输出wifi名称
    return sorted(wifi_list, key=lambda x: x[1], reverse=True)  # 按信号强度由高到低排序

#测试连接，返回链接结果
def wifiDisconnect():
    wifi = pywifi.PyWiFi()
    # 获取第一个无线网卡
    ifaces = wifi.interfaces()[0]
    # 断开所有连接
    ifaces.disconnect()

def get_inface():
    #抓取网卡接口
    wifi=pywifi.PyWiFi()
    #获取第一个无线网卡
    return wifi.interfaces()

def wifiConnect(pwd, wifi_name):
    iface = get_inface()[0]
    #断开所有连接
    iface.disconnect()
    time.sleep(0.5)

    wifistatus=iface.status()
    if wifistatus ==const.IFACE_DISCONNECTED:
        #创建WiFi连接文件
        profile=pywifi.Profile()
        #要连接WiFi的名称
        profile.ssid=wifi_name
        #网卡的开放状态
        profile.auth=const.AUTH_ALG_OPEN
        #wifi加密算法,一般wifi加密算法为wps
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        #加密单元
        profile.cipher=const.CIPHER_TYPE_CCMP
        #调用密码
        profile.key=pwd
        #删除所有连接过的wifi文件
        iface.remove_all_network_profiles()
        #设定新的连接文件
        tep_profile=iface.add_network_profile(profile)
        iface.connect(tep_profile)
        #wifi连接时间
        time.sleep(2)
        if iface.status()==const.IFACE_CONNECTED:
            return True
        else:
            return False
    else:
        print("已有wifi连接")


def get_passwd(repeat=8):
    words = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDGFHJKLZXCVBNM'#这里可以加入字母和其他字符，使用string包更方便
    words = '1234567890'
    # 生成密码的位数
    r = its.product(words, repeat=repeat)#4即生成4位密码，正常情况下热点密码位数为8
    return r


def skip_history_passwd(fh, lines):
    for i in range(0, lines):
        fh.readline()
