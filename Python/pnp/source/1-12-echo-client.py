# coding=utf-8
"""
echo client
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '15/10/24'
import socket
import sys

port = 8050


def echo_client(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', port))
    # send datas
    try:
        print 'send msg:%s' % message
        sock.sendall(message)
        # lock for all respone
        has_recved = 0
        all_datas = len(message)

        while has_recved < all_datas:
            recv_data = sock.recv(16)
            has_recved += len(recv_data)
            print 'recv data:%s' % recv_data

    except socket.error, e:
        print 'socket errro:%s' % e
    finally:
        sock.close()

if __name__ == '__main__':
    echo_client(sys.argv[1])