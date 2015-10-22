# coding=utf-8
"""
设定和获取套接字超时时间
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '15/10/22'

import socket


def socket_timeout():
    # 创建socket实例
    so = socket.socket(family=socket.AF_INET,
                       type=socket.SOCK_STREAM,
                       proto=0,
                       _sock=None)
    print "default timeout:", so.gettimeout()

    # 设定自己的超时时间，这对网络编程很重要
    so.settimeout(100)          # 秒数(float)或者是None(禁止超时检测)
    print "current timeout:", so.gettimeout()


if __name__ == '__main__':
    socket_timeout()
    # out:
    # default timeout: None
    # current timeout: 100.0
