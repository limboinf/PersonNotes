# coding=utf-8
"""
通过给定端口和协议找到对应的服务名
getservbyport(port, protocolname)
getservbyname(servicename, protocolname)
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '15/10/22'
import socket


def find_service_name():
    protocolname = 'tcp'
    for port in (80, 22, 25, 3306, 6379):
        try:
            print "Port:%s => ServiceName:%s" % (port, socket.getservbyport(port, protocolname))
        except socket.error, msg:
            print msg           # 对应6379端口对应的服务如果没有启动则返回：port/proto not found

    # 通过
    print socket.getservbyname("mysql", protocolname)       # 返回 3306

if __name__ == '__main__':
    find_service_name()
    # outprint:
    # Port:80 => ServiceName: http
    # Port:22 => ServiceName: ssh
    # Port:25 => ServiceName: smtp
    # Port:3306 => ServiceName: mysql
    # port/proto not found