# coding=utf-8
"""
利用SocketServer模块提供的ForkingMixIn为每一个client请求派生一个新进程
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


class ForkingClient(object):
    """client"""
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def run(self, msg):
        current_process_id = os.getpid()
        sent_data_length = self.sock.send(msg)
        print u'客户端 PID:%d 发送回射数据到服务器: "%s" [发送: %d 字符]' % (current_process_id, msg, sent_data_length)

        response = self.sock.recv(BUF_SIZE)
        print '客户端 PID:%d 接收消息:%s\n' % (current_process_id, response)

    def shutdown(self):
        self.sock.close()


# 定义请求处理类
class ForkingServerRequestHandler(SocketServer.BaseRequestHandler):
    """继承基础的请求处理类"""
    def handle(self):
        data = self.request.recv(BUF_SIZE)      # 接收数据
        current_process_id = os.getpid()
        response = '%s : %s' % (current_process_id, data)
        print 'Server sending response: %s' % response
        self.request.send(response)
        return


class ForkingServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    pass


def main(client_num):
    # 实例化服务类对象
    server = ForkingServer((SERVER_HOST, SERVER_PORT),      # address
                           ForkingServerRequestHandler)     # 请求类
    ip, port = server.server_address
    print 'Run server: ip:%s port:%s' % (ip, port)
    # 以线程方式开启服务
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()

    msg = '1234567890abcdefg'
    # 多个客户端(每次有新的client连接时，server fork一个来处理)
    clients = []
    for i in range(int(client_num)):
        client = ForkingClient(ip, port)
        client.run(msg)
        print u'第%d个客户端启动' % (i+1)
        clients.append(client)

    # clean them up
    server.shutdown()
    for client in clients:
        client.shutdown()


if __name__ == '__main__':
    main(sys.argv[1])       # 在我MacBook Air OS X 10.10 4G 版本下启动250个客户端就会出现：socket.error: [Errno 24] Too many open files
    # out:
    # .....
    # 第247个客户端启动
    # 客户端 PID:20201 发送回射数据到服务器: "1234567890abcdefg" [发送: 17 字符]
    # Server sending response: 20449 : 1234567890abcdefg
    # 客户端 PID:20201 接收消息:20449 : 1234567890abcdefg
    # ....