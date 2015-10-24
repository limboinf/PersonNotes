# coding=utf-8
"""
编写一个简单的回射服务器
这里是服务端代码
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '15/10/22'

import socket

def service(port):
    # create TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 重用地址
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定地址
    sock.bind(('localhost', port))
    # 监听队列
    sock.listen(5)
    # 接收数据
    while True:
        client, address = sock.accept()
        data = client.recv(2048)
        if data:
            print "Datas:%s" % data
            client.send(data)
            print "sent %s types back to %s" % (data, address)
        # 关闭连接
        client.close()


if __name__ == '__main__':
    service(8050)