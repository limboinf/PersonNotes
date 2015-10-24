# coding=utf-8
"""
利用SocketServer模块提供的ThreadingMixIn为每一个client请求派生一个新进程
实现1-12的echo服务器
参考myblog: http://beginman.cn/python/2015/04/06/python-SocketServer/
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '15/10/24'
import os
import sys
import socket
import threading
import SocketServer


SERVER_HOST = 'localhost'
SERVER_PORT = 0     # 内核动态生成端口
BUF_SIZE = 1024


def client(ip, port, msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(msg)
        response = sock.recv(BUF_SIZE)
        print '客户端接收消息:%s\n' % response
    finally:
        sock.close()


# 定义请求处理类
class ThreadServerRequestHandler(SocketServer.BaseRequestHandler):
    """继承基础的请求处理类"""
    def handle(self):
        data = self.request.recv(BUF_SIZE)      # 接收数据
        current_thread = threading.currentThread()
        response = '%s : %s' % (current_thread.name, data)
        print 'Server sending response: %s' % response
        self.request.sendall(response)


class ThreadServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def main(client_num):
    # 实例化服务类对象
    server = ThreadServer((SERVER_HOST, SERVER_PORT),      # address
                           ThreadServerRequestHandler)     # 请求类
    ip, port = server.server_address
    print 'Run server: ip:%s port:%s' % (ip, port)
    # 以线程方式开启服务
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    print 'Server loop running on thread:%s' % server_thread.name

    # 启动多个客户端
    for i in range(int(client_num)):
        print u'第%d个客户端启动' % (i+1)
        client(ip, port, 'Hello data:%d' % (i+1))

    # Server cleanup
    server.shutdown()


if __name__ == '__main__':
    main(sys.argv[1])       # 在我MacBook Air OS X 10.10 4G 版本下启动16370个客户端就会出现：socket.error: [Errno 60] Operation timed out
    # out:
    # Run server: ip:127.0.0.1 port:60691
    # Server loop running on thread:Thread-1
    # 第1个客户端启动
    # Server sending response: Thread-2 : Hello data:1
    # 客户端接收消息:Thread-2 : Hello data:1
    #
    # 第2个客户端启动
    # Server sending response: Thread-3 : Hello data:2
    # 客户端接收消息:Thread-3 : Hello data:2
    # ....