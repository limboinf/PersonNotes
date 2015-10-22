# coding=utf-8
"""
重用套接字地址（这个在网络编程中很重要）
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '15/10/22'
import socket
import sys

def reuse_socket_addr():
    """创建套接字对象后查询地址重用状态
    再调用`setsockopt()`方法修改地址重用状态的值
    然后绑定一个地址开始监听client连接
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 获取 SO_REUSEADDR 选项信息
    old_state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    print "Old sock state: %s" % old_state          # 0

    # 启用 SO_REUSEADDR
    # 如果下面这段注释了那么第二次使用这个端口则"Address already in use"
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    new_state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    print "New sock state: %s" % new_state

    local_port = 8800

    sock.bind(('', local_port))
    sock.listen(1)
    print "Listening on port: %s" % local_port
    while True:
        try:
            connection, addr = sock.accept()
            print "Connected by %s:%s" % (addr[0], addr[1])
        except KeyboardInterrupt:       # 捕获Ctrl+C
            break
        except socket.error, msg:
            print msg


if __name__ == '__main__':
    reuse_socket_addr()