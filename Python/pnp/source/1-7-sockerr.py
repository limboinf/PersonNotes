# coding=utf-8
"""
优雅的处理套接字错误
socket.error
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '15/10/22'
import sys
import socket
import argparse


def main():
    # setup argument parsing
    parser = argparse.ArgumentParser(description="Socket error example")
    parser.add_argument('--host', action="store", dest="host", required=True)
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    parser.add_argument('--file', action="store", dest="file", required=False)
    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port
    filename = given_args.file

    # 创建socket实例异常处理
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(60)
    except socket.error, e:
        print "Error creating socket: %s" % e

    # connect连接异常处理
    try:
        s.connect((host, port))
    except socket.gaierror, e:      # socket.gaierror: 地址相关的错误
        print "Address-related error connecting to server: %s" % e
        sys.exit(1)
    except socket.error, e:
        print "Connection error: %s" % e
        sys.exit(1)

    # 发送数据异常处理
    try:
        s.sendall("GET %s HTTP/1.0\r\n\r\n" % filename)
    except socket.error, e:
        print "Error sending data: %s" % e
        sys.exit(1)

    while 1:
        # 数据接收异常处理
        try:
            buf = s.recv(2048)
        except socket.error, e:
            print "Error receiving data: %s" % e
            sys.exit(1)
        if not len(buf):
            break
        sys.stdout.write(buf)

if __name__ == '__main__':
    main()