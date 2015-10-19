第五章：TCP客户/服务器程序示例


这一节算是对前四节的总结和实战了，如下我们要实现的回射服务器：

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/acc4.png)

# 一.实战分析

需要做到的是：

- 通过前几节编写上面的回射服务器
- client和server启动时发生了什么？
- client和server终止时发生了什么？
- server突然终止，则client会发生什么？
- server主机崩溃，client会发生什么？

通过书中的回射服务器实例([在这里](https://github.com/BeginMan/BookNotes/blob/master/Unix/Unix-Network-Programming-Volume-1-The-Sockets-Networking-API-3rd-Edition/source/unpv13e))，client([客户端代码](https://github.com/BeginMan/BookNotes/blob/master/Unix/Unix-Network-Programming-Volume-1-The-Sockets-Networking-API-3rd-Edition/source/unpv13e/tcpcliserv/tcpcli01.c))和server([服务端代码](https://github.com/BeginMan/BookNotes/blob/master/Unix/Unix-Network-Programming-Volume-1-The-Sockets-Networking-API-3rd-Edition/source/unpv13e/tcpcliserv/tcpserv01.c))都在**本地测试**， 通过`netstat -a`,`lsof`和`ps`命令来查看这些网络状态。注意`netstat`打印出的信息中，`*`表示一个为0的IP地址(INADDR_ANY, 通配地址)或为0的端口。


## 2.1 正常启动
此时要看下`netstat`输出信息的变化， 三路握手成功后则进入`ESTABLISHED`状态，接下来的步骤就是：

1. client 调用[`str_cli`函数](https://github.com/BeginMan/BookNotes/blob/master/Unix/Unix-Network-Programming-Volume-1-The-Sockets-Networking-API-3rd-Edition/source/unpv13e/lib/str_cli.c),该函数阻塞于`fgets`调用，因为client还未曾键入任何文本
2. server fork子进程，子进程调用[`str_echo`函数](https://github.com/BeginMan/BookNotes/blob/master/Unix/Unix-Network-Programming-Volume-1-The-Sockets-Networking-API-3rd-Edition/source/unpv13e/lib/str_echo.c),该函数阻塞与`read`等待client的请求送入.
3. server父进程再次阻塞于`accept`等待下一个客户连接。至此，三个进程都已睡眠（阻塞）

## 2.2 正常终止
client键入终端EOF字符(Control-D)终止client,期间发生过程如下：

1. 键入`EOF`字符，`fgets`返回一个空指针，于是`str_cli`函数返回
2. 当str_cli返回到client main函数中，main调用`exit`终止
3. 进程终止处理的部分工作就是关闭所有打开的描述符，由内核关闭，这导致client TCP发送一个`FIN`给server， server TCP则以`ACK`响应，这就是TCP连接终止序列的前半部分，至此，server套接字处于`CLOSE_WAIT`状态，client套接字处于`FIN_WAIT_2`状态
4. 当server TCP接收`FIN`时，server子进程阻塞于`readline`调用，于是readline返回0，这导致str_echo函数返回到server子进程的main函数中
5. server子进程接收0，调用exit终止，由内核关闭所有已打开的描述符
6. 由于子进程关闭已打开的描述符时，会引发TCP连接终止序列的最后两个字节：一个从server到client的`FIN`和一个client到server的ACK。至此，连接完全终止，client套接字进入`TIME_WAIT`状态。
7. 子进程终止给父进程发送一个`SIGCHLD`信号(下面讲解),如果没有发送，则父进程未处理，子进程便进入了僵死状态（僵尸进程）

# 二. POSIX信号处理
要弄清楚以下知识点：

1. 信号的概念，作用
2. 信号发送方式（进程<->进程，内核->进程）
3. 每个信号都有与之关联的行为(action),通过调用`sigaction`来设定

在[**嗨翻C第十章学习了信号量**](https://github.com/BeginMan/BookNotes/blob/master/C/top10.md#三信号量),这里面涉及了**信号映射表**，**sigaction结构体以及创建方法**以及一些实例。

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top10_14.png)

"unp.h"自定义头部通过`typedef`来简化`sigaction`函数，`sigemptyset(&action.sa_mask)`掩码过滤，因为在调用信号处理函数被**阻塞**，**任何阻塞的信号都不能递交给进程，我们把`sa_mask`成员设置为空集，意味着除了被捕获的信号外，不阻塞额外信号。**

## 2.1 处理SIGCHLD信号
对于僵死进程(zombie)，init进程将`wait`它们，从而去除它们的僵死状态。大量的僵死进程会占用内核空间，好紧进程资源，所以**无论何时fork后要wait它们**

**处理僵死进程的可移植方法就是：捕获`SIGCHLD`,并调用`wait`或`waitpid`。**

书中给出了[例子](https://github.com/BeginMan/BookNotes/blob/7b242727235c8ebbc6bacb8e3cfd875be2dd8e23/Unix/Unix-Network-Programming-Volume-1-The-Sockets-Networking-API-3rd-Edition/source/unpv13e/tcpcliserv/tcpserv02.c)，但是对于信号量的处理书中的例子并没有讲的太清楚，这里先埋坑吧~

## 2.2 wait和waitpid函数

	#include <sys/wait.h>
	pid_t wait(int *statloc);
	pid_t waitpid(pid_t pid, int *statloc, int options);
	/*成功则返回进程ID，失败则返回0或-1*/

这两个函数都返回两个值：已终止子进程的ID和通过statloc指针返回的子进程的终止状态。重点是：

1. 理解wait和waitpid函数
2. 区别wait和waitpid函数

如下给出了[最终版本](https://github.com/BeginMan/BookNotes/blob/7b242727235c8ebbc6bacb8e3cfd875be2dd8e23/Unix/Unix-Network-Programming-Volume-1-The-Sockets-Networking-API-3rd-Edition/source/unpv13e/tcpcliserv/tcpserv04.c), 上述实例主要说明了以下几点：

1. 当fork子进程时，必须捕获SIGCHLD信号
2. 当捕获信号时，必须处理被中断的系统调用
3. SIGCHLD的信号处理函数必须正确编写，应该用waitpid函数以免留下僵死进程.

