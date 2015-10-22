# coding=utf-8
"""
将IPv4地址转换不同的格式
(1). `inet_aton`,`inet_addr`和`inet_ntoa`在点分十进制数串(如201.33.211.89)与它32位网络字节序二进制值间转换IPv4地址
(2). `inet_pton`和`inet_ntop`比较新，对于IPv4和IPv6都适用,p代表表达，n代表数值
参考《Unix网络编程套接字联网API》
https://github.com/BeginMan/BookNotes/blob/master/Unix/Unix-Network-Programming-Volume-1-The-Sockets-Networking-API-3rd-Edition/top3.md#五地址转换函数

    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '15/10/22'

import socket
from binascii import hexlify

def convert_ipv4_address():
    for ip_addr in ['127.0.0.1', '192.168.0.110']:
        packed_ip_addr = socket.inet_aton(ip_addr)          # 打包成32位二进制数据格式
        unpacked_ip_addr = socket.inet_ntoa(packed_ip_addr)
        print "IP address: %s => Packed: %s => Unpacked: %s" \
              % (ip_addr, hexlify(packed_ip_addr), unpacked_ip_addr)        # hexlify(binData) 以16进制展示

if __name__ == '__main__':
    convert_ipv4_address()
    # outprint:
    # IP address: 127.0.0.1 => Packed: 7f000001 => Unpacked: 127.0.0.1
    # IP address: 192.168.0.110 => Packed: c0a8006e => Unpacked: 192.168.0.110
