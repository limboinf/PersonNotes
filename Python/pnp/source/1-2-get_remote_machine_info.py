# coding=utf-8
"""
获取远程主机IP
通过`gethostbyname(远程主机)`来获取
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '15/10/22'

import socket


def get_remote_machine_info():
    remote_host = "www.python.org"
    try:
        ip_address = socket.gethostbyname(remote_host)
        print "remote host (%s) IP: %s" % (remote_host, ip_address)
    except socket.error, msg:
        print socket.error, msg


if __name__ == '__main__':
    get_remote_machine_info()
    # outprint:
    # remote host (www.python.org) IP: 103.245.222.223