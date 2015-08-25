[图解HTTP](http://book.douban.com/subject/25863515/)

![](http://img3.douban.com/mpic/s27283822.jpg)

>本书对互联网基盘——HTTP协议进行了全面系统的介绍。作者由HTTP协议的发展历史娓娓道来，严谨细致地剖析了HTTP协议的结构，列举诸多常见通信场景及实战案例，最后延伸到Web安全、最新技术动向等方面。本书的特色为在讲解的同时，辅以大量生动形象的通信图例，更好地帮助读者深刻理解HTTP通信过程中客户端与服务器之间的交互情况。读者可通过本书快速了解并掌握HTTP协议的基础，前端工程师分析抓包数据，后端工程师实现REST API、实现自己的HTTP服务器等过程中所需的HTTP相关知识点本书均有介绍。本书适合Web开发工程师，以及对HTTP协议感兴趣的各层次读者。


该书已读2遍，有感而发遂整理思维导图以及总结如下：

# TOP1:了解web及网络基础

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/TOP1%3A了解web及网络基础.png)

对于与HTTP相关的协议如TCP,IP,DNS,ARP等，它们之间协作关系如下：

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/http_tcp_dns_arp.png)


# TOP2:简单的HTTP协议
![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/TOP2简单的HTTP协议.png)

## 1.请求与响应
HTTP协议通过客户端(request)，服务器端(response)实现网络通信

请求报文：

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/request.png)

响应报文：

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/reponses.png)

## 2.HTTP非持久连接和持久连接

>HTTP既可以使用非持久连接（nonpersistent connection），也可以使用持久连接（persistent connection）。HTTP/1.0使用非持久连接，HTTP/1.1默认使用持久连接。

[HTTP持久连接](https://zh.wikipedia.org/wiki/HTTP%E6%8C%81%E4%B9%85%E8%BF%9E%E6%8E%A5)（HTTP persistent connection，也称作HTTP keep-alive或HTTP connection reuse）是**使用同一个TCP连接来发送和接收多个HTTP请求/应答，而不是为每一个新的请求/应答打开新的连接的方法**。

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/HTTP_persistent_connection.png)


## 3.HTTP管线化
[HTTP管线化](https://zh.wikipedia.org/wiki/HTTP%E7%AE%A1%E7%B7%9A%E5%8C%96):HTTP pipelining,将多个HTTP请求整批提交，而在发送过程中不需先等待服务端的回应。

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/HTTP_pipelining.png)






