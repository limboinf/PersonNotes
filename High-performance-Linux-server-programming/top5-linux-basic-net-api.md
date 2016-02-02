Linux网络编程基础API

- socket地址API
- socket基础API
- 网络信息API

# 一.字节序
[字节序：大端，小端](http://beginman.cn/unp/2015/10/15/unp-socket/)

[Python网络字节序和主机字节序](http://blog.sina.com.cn/s/blog_4b5039210100f2a0.html)

现代PC大多采用小端字节序，因此小端字节序又被称为**主机字节序**。

>**重点：**为了解决两台主机（还有可能是两个进程哦）使用不同字节序数据传递而解析错误，发送端总要把发送的数据转换成大端再发送，接收端根据自身的字节序进行转换即可。因此大端也称为**网络字节序**。

linux提供4个函数用于转换：参考我之前总结的[字节序：大端，小端](http://beginman.cn/unp/2015/10/15/unp-socket/)

ps.为什么该书上使用netinet/in.h?? 可能是作者搞错了，应该是`<arpa/inet.h>`, 且我在[socket编程中需要用到的头文件](http://staff.ustc.edu.cn/~mengning/np/linux_socket/new_page_4.htm) 中看到的也可证明作者搞错了。

# 二.知识点清单

## 2.1 通用socket地址

- 需要对socket地址结构体sockaddr进行学习和分析 
- 新的通用socket地址结构存储更多
- 专用socket地址
- IP地址转换函数，用于点分十进制字符串和网络字节序整数转换





