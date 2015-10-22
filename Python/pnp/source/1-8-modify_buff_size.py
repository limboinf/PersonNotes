# coding=utf-8
"""
修改套接字发送和接收的缓冲区大小
setsockopt()设置缓冲区大小，接收三个参数：level, optname, value
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '15/10/22'
import socket

SEND_BUF_SIZE = 4096
RECV_BUF_SIZE = 4096

def modify_buff_size():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取socket 发送缓冲区大小
    bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print "Buffer size [Before]: %d" % bufsize

    # 设置缓冲区大小
    sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
    # 设置send缓冲区大小
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SIZE)
    # 设置recv缓冲区大小
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUF_SIZE)

    bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print "Buffer size [After]: %d" % bufsize


if __name__ == '__main__':
    modify_buff_size()
    # out:
    # Buffer size [Before]: 131072
    # Buffer size [After]: 4096

