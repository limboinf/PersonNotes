第一章：简介

涉及以下知识点：

- IPv4(IP version 4),和 IPv6(IP version 6)
- 因特网与互联网概念，这两个概念一致，这个可参考[因特网和互联网的差别？](http://www.zhihu.com/question/23079539/answer/66941405)
- 套接字的概念，以及创建简单的TCP套接字
- Unix errno值
- OSI模型
- BSD历史
- Unix标准

# 一. 套接字概念与创建
该书的例子在Mac OS X 下需要编译和配置一系列文件，可参考：[UNIX网络编程（第3版）环境搭建——使用MAC OSX10.10](http://www.jianshu.com/p/7e395e4f8515) 和[《网络编程》关于 UNIX网络编程 卷1 的 unp.h 和源码编译问题](http://blog.csdn.net/chenhanzhun/article/details/41827241)

其中书中IPv4和IPv6例子在这里:[daytimetcpcli.c](https://github.com/BeginMan/BookNotes/blob/master/Unix/Unix-Network-Programming-Volume-1-The-Sockets-Networking-API-3rd-Edition/source/UnixApi/intro/daytimetcpcli.c), [daytimetcpcliv6.c](https://github.com/BeginMan/BookNotes/blob/master/Unix/Unix-Network-Programming-Volume-1-The-Sockets-Networking-API-3rd-Edition/source/UnixApi/intro/daytimetcpcliv6.c)

如下以IPv4为例子（IPv6 仅仅在v4的基础上加个'6'即可）

## 1.1 创建TCP套接字

上面代码的例子创建了TCP套接字:

`socket()` 函数创建一个网际(`AF_INET`)字节流(`SOCK_STREAM`)套接字,该函数返回一个小整数描述符，以后的所有函数调用(如`connect`, `read`)就用该描述符标识这个套接字。
	
	int sockfd;
	struct sockaddr_in servaddr;
	if((sockfd=socket(AF_INET, SOCK_STREAM, 0)) < 0)
		err_sys("socket error");

如上正在使用的API称为**套接字API(sockets API)**.

## 1.2 指定服务器的IP地址和端口

	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_port = htons(13);		/*daytime server*/
	if(inet_pton(AF_INET, argv[1], &servaddr.sin_addr) <= 0)
		err_quit("inet_pton error for %s", argv[1]);


- 把服务器IP和端口填入一个网际套接字地址结构中(一个名为servaddr的`sockaddr_in`结构变量)
- 使用`bzero`把整个结构清零
- 置地址族为`AF_INET`,端口号13（时间服务器端口号，支持tcp/ip
- `htons`为库函数(主机到网络短整数)去转换二进制端口号
- `inet_pton`为库函数(呈现形式到数据)去把ASCII命令行参数（如：216.228.192.69）转换为合适的格式

## 1.3 content建立连接

	if(connect(sockfd, (SA *) &servaddr, sizeof(servaddr)) < 0)
		err_sys("connect error");

`connect`函数应用于一个TCP套接字时，将与由它的第二个参数指向的套接字地址结构指定的服务器建立TCP连接,该套接字地址结构的长度也必须作为第三个参数

## 1.4 读入并输出服务器的应答

	while((n = read(sockfd, recvline, MAXLINE)) > 0){
			recvline[n] = 0;		/*null terminate*/
			if(fputs(recvline, stdout) == EOF)
				err_sys("fputs error");
		}


`read`函数读取服务器应答，并用标准I/O函数`fputs`输出结果

**TCP套接字读取数据时，总需要把`read`编写在某个循环中，当read为0(表明对端关闭连接)或负数(表明发生错误)时终止程序**

# 二. Unix标准
我们简单地称**Unix标准为POSIX(可以执行操作系统接口, Portable Operating System Interface)规范**





