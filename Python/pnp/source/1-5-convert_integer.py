# coding=utf-8
"""
主机字节序和网络字节序之间的相互转换
参考my blog: http://beginman.cn/unp/2015/10/15/unp-socket/
#include <arpa/inet.h>
uint32_t htonl(uint32_t hostlong);
uint16_t htons(uint16_t hostshort);
uint32_t ntohl(uint32_t netlong);
uint16_t ntohs(uint16_t netshort);

这些函数名很好记:
h表示host
n表示network
l表示32位长整数
s表示16位短整数。

    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '15/10/22'

import socket


def convert_integer():
    data = 1234
    # 32-bit
    print data, socket.ntohl(data), socket.htonl(data)
    # 16-bit
    print data, socket.ntohs(data), socket.htons(data)


if __name__ == '__main__':
    convert_integer()
    # out:
    # 1234 3523477504 3523477504
    # 1234 53764 53764
