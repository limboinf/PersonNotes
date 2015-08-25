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

# TOP3:HTTP报文内HTTP信息
![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/TOP3HTTP报文内HTTP信息.png)

## 1.请求报文
![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/1a4e7e6a-6d7b-38f1-af8a-043140034c8f.jpg)

下面是一个实际请求：

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/412b4451-2738-3ebc-b1f6-a0cc13b9697b.jpg)

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/cdc4dbbb-f98e-31d5-8270-3c37bf1c54e5.jpg)

## 2.响应报文
![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/0236098f-1a98-3a4f-ba6c-4a44c6ec4ed0.jpg)

以下是一个实际的HTTP响应报文： 

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/bddb00b6-a3e1-3112-a4f4-4b3cb8687c70.jpg)

# TOP4:返回结果的HTTP状态码

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/http1.jpg)
# TOP5: 与HTTP协作的Web服务器

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/TOP5与HTTP协作的Web服务器.png)

# TOP6:HTTP首部
![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/TOP6HTTP首部.png)
## 1.通用首部字段
![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/header1.png)
## 2.请求首部字段
![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/header2.png)
## 3.响应首部字段
![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/header3.png)
## 4.实体首部字段
![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/header4.png)
## 5.为 Cookie 服务的首部字段
![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/header5.png)

# TOP7:确保Web安全的Https

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/TOP7确保Web安全的Https.png)

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/img_0137.png)

# TOP8:确认访问用户身份的认证
![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/TOP8确认访问用户身份的认证.png)

# TOP9:基于HTTP的功能追加协议
![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/HTTP/media/TOP9基于HTTP的功能追加协议.png)

**注：TOP10,TOP11略过**







