# coding=utf-8
"""
获取设备信息
python help 查看函数信息：
>>> help(socket.gethostname)

    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '15/10/22'
import socket

def print_machine_info():
    host_name = socket.gethostname()                # 获取主机信息
    ip_address = socket.gethostbyname(host_name)    # 通过主机信息获取IP地址
    print "Host Name:%s" % host_name
    print "IP Address:%s" % ip_address


if __name__ == '__main__':
    print_machine_info()
    # outprint:
    # Host Name:fangpengdeMacBook-Air.local
    # IP Address:192.168.0.106

