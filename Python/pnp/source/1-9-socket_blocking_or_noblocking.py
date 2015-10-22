# coding=utf-8
"""
把套接字改成阻塞或非阻塞模式
默认情况下TCP处于阻塞状态，可通过一个套接字对象调用`setblocking(1)`设置为阻塞模式
`setblocking(0)`设置为非阻塞模式
这个例子没啥价值.....
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '15/10/22'
import socket


def set_blocking_or_noblocking():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(1)
    sock.settimeout(0.5)
    sock.bind(("127.0.0.1", 0))

    sock_addr = sock.getsockname()
    print sock_addr
    while 1:
        sock.listen(1)

if __name__ == '__main__':
    set_blocking_or_noblocking()