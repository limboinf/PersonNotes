第四章：基本的TCP套接字编程

- 完成整个TCP客户/服务端程序所需的所有基本套接字函数
- 并发服务器，这里只考虑`frok`出对付每个客户请求的单进程模型

# 一.TCP客户与服务器发生的典型事件时间表

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/tcp_process.png)

# 二.socket函数
为了执行网络I/O，一个进程的第一件事就是创建`socket`函数，如下函数原型：

	#include <sys/socket.h>
	int socket(int family, int type, int protocol);
	/*返回：success:返回非负描述符； 失败则返回-1*/

成功则返回一个与文件描述符类似的小非负整数，我们称为**套接字描述符(socket descriptor), 简称 `sockfd`**

(1). `family`常值参数指明协议族，如下：

family | desc
----|------
AF_INET | IPv4 Protocols  
AF_INET6 | IPv6 Protocols  
AF_LOCAL | Uinx domain protocols
AF_ROUTE | Routing sockets
AF_KEY | Key socket

(2). `type`常值指明套接字类型,如下：

type | desc
----|------
SOCK_STREAM | 字节流套接字
SOCK_DGRAM | 数据报套接字
SOCK_SEQPACKET | 有序分组套接字
SOCK_RAM | 原始套接字

(3). `protocol`某个协议类型的常值，或设为0，以选择给定的`family`和`type`组合的系统默认值， 如下：

protocol | desc
----|------
IPPROTO_CP | TCP传输协议
IPPROTO_UDP | UDP传输协议
IPPROTO_SCTP | SCTP传输协议

并非所有的`family`和`type`组合都有效，下图给出一些有效组合和对应的真正协议：

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/family_type.png)

# 三.connect函数
TCP client 用`connect`与 TCP service建立连接，函数原型：

	#include <sys/socket.h>
	int connect(int sockfd, const struct sockaddr *servaddr, socklen_t addrlen);
	/*success: return 0; fail: return 1*/

1. `sockfd`是前面的套接字描述符
2. `const struct sockaddr *servaddr`: 套接字地址结构指针
3. `socklen_t addrlen`: 套接字地址结构大小

套接字地址结构要包含服务器IP和端口，在[上一章节](https://github.com/BeginMan/BookNotes/blob/master/Unix/Unix-Network-Programming-Volume-1-The-Sockets-Networking-API-3rd-Edition/top3.md)已经学过, 接下来分析下`connect`所带来的情况：

- client 调用 `connect` 不用 `bind`， 如果需要，内核会确定源IP，并选择一个临时端口作为源端口。
- 对于TCP套接字，`connect`则会发生**[三路握手](https://github.com/BeginMan/BookNotes/blob/master/Unix/Unix-Network-Programming-Volume-1-The-Sockets-Networking-API-3rd-Edition/top2.md#二-tcp通信三部曲)**, 且仅连接成功或出错时才有返回，其出错返回可能有以下情况：

	1. TCP clinet 没有收到`SYN`分节响应，则返回`ETIMEDOUT`错误。举个栗子：如果client connect,则4.4BSD内核发送一个SYN,若无响应则等待6s再发送一个，仍无响应则等待24s在发送一个，总共等待75s后还没有收到响应则返回本错误。
	2. 如果对client 的SYN响应是`RST(复位)`，表示 server进程没有等待与之连接(例如server服务没有运行)，客户端立马返回`ECONNREFUSED`
	3. client发出的SYN在中间的某个路由器引发一个"destination unreachable(目的地不可达)"的ICMP错误，则client保存该消息并按照第一种情况重发，如果再第一种情况返回 `ETIMEDOUT`错误则把保存的消息(ICMP错误)作为`EHOSTUNREACH`或`ENTUNREACH`错误返回给进程。

在第二章总结的[TCP状态转换图](https://github.com/BeginMan/BookNotes/blob/master/Unix/Unix-Network-Programming-Volume-1-The-Sockets-Networking-API-3rd-Edition/top2.md#24-tcp状态转换图)中可以看出：

>每个连接均开始于 CLOSED 状态。当一方执行了被动的连接原语（ LISTEN ）或主动的连接原语（ CONNECT ）时，它便会脱离 CLOSED 状态。如果此时另一方执行了相对应的连接原语，连接便建立了，并且状态变为 ESTABLISHED 。任何一方均可以首先请求释放连接，当连接被释放后，状态又回到了 CLOSED 。

那么注意了：**当connect失败则该套接字不可再用，必须调用close关闭并重新调用socket。**

# 四.bind函数
`bind`把本地协议地址赋予给一个socket，对于网际协议( Internet protocols), 协议地址包括32-bit IPv4 address，128-bit IPv6 address和16-bit TCP or UDP 端口号的组合。

	#include <sys/socket.h>
	int bind(int sockfd, const struct sockaddr *myaddr, socklen_t addrlen);
	/*Returns: 0 if OK,-1 on error*/

bind可以指定IP和端口，也可不指定，下图给出一系列情况：

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/bind_ip_port.png)

bind返回常见错误就是`EADDRINUSE`("Address already in use"),更多详尽bind情况翻阅原著。

# 五.listen函数
listen仅仅由TCP服务器调用，它做两件事：

1. 调用listen导致套接字从`CLOSED`状态转换成`LISTEN`
2. 第二个参数(`int backlog`)规定内核应该为相应套接字排队的最大连接个数

如下函数原型：

	#include <sys/socket.h>
	int listen(int sockfd, int backlog);
	/*Returns: 0 if OK,-1 on error*/

内核为任意一个监听的套接字维护两个队列：

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/listen_two_queues.png)

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/three_ways_listen_translate.png)

关于这两个队列的处理要注意：

1. backlog参数被规定为两个队里总和的最大值
2. 不要把backlog设置为0
3. 未完成队里中的任意一项并非长时间保存，有一个留存时间(`RTT`),对于web服务器，Client与单服务器之间的中值RTT是187ms
4. 许多系统允许修改最大backlog， 如下我们通过一个包裹函数来通过环境变量自定义backlog大小

如下包裹函数：
	
	void Listen(int fd, int backlog)		/*包裹函数一般与之同名，只不过第一个字母往往大写*/
	{
		char *ptr;
		/* can override 2nd argument with environment variable */
		if((ptr = getenv("LISTENQ")) != NULL)
			backlog = atoi(ptr);

		if (listen (fd, backlog) < 0)
			err_sys ("listen error");
	}


增大backlog的理由是：**随着client SYN分节的到达，未完成连接队列中的项数可能增大，它们等待着三路握手的完成**。当一个client SYN到达但未连接队列已满，则TCP就会**忽略分节**，也就是不发送`RST`。这样的话客户TCP将重发SYN,期待在队列中能找到空间让自己居住，如果server立即响应一个RST,则client的connect就会立即返回一个错误，强制应用程序处理这种情况，而不是TCP正常的重传机制处理。另外，Client无法区别响应SYN的RST是“该端口没有服务监听”还是“该端口有服务在监听，不过它的队列已经满了”

# 六.accept函数
**`accept`用于服务器TCP，用于从已完成连接队列的队头返回下一个已完成的连接，如果已完成连接的队列为空则进程进入休眠（假设套接字为默认的阻塞方式）**

	#include <sys/socket.h>
	int accetp(int sockfd, struct sockaddr *cliaddr, socklen_t *addrlen);
	/*成功则返回非负描述符，出错则返回-1*/

- 参数`cliaddr`返回已连接的对端进程(client)的协议地址
- `addrlen`是[值-结果参数](https://github.com/BeginMan/BookNotes/blob/master/Unix/Unix-Network-Programming-Volume-1-The-Sockets-Networking-API-3rd-Edition/top3.md#二值-结果参数)：调用前，将由`*addrlen`所引用的整数值作为`cliaddr`所指的套接字地址结构的长度，返回时，该整数值即为由内核存放在该套接字地址结构内的确切字节数(被修改了)
- 弄清楚什么是监听套接字，什么是已连接套接字

# 七.fork和exec函数
在学习[《嗨翻C语言》一书中第九章： 进程与系统调用:打破疆界](https://github.com/BeginMan/BookNotes/blob/master/C/top9.md)已经很详尽的介绍了系统调用：`system()`,`exec()`函数和进程复制：`fork()`函数的使用。fork函数是Unix派生新进程的唯一方法

# 八.并发服务器
这里像Apache一样，每当有请求则fork一个进程来处理.

并发通常可以有三种，基于进程、基于IO多路复用、基于线程。

基于进程的并发构建思路如下：

1. 在父进程中接受客户端的连接请求，然后创建一个子进程来为每个新客户端提供服务。
2. 在连接接受请求之后，服务器**派生一个子进程**，这个子进程获取服务器描述符表的完整拷贝，子进程关闭它的拷贝的监听描述符，而父进程关闭它的已连接描述符，否则，将永远不会释放已连接描述符的文件表条目，而且由此引发的存储器泄露将最终消耗尽可用的服务器，使系统崩溃。

对于父、子进程间**共享状态**信息，进程有一个非常清晰的模型：**共享文件表**，但是不共享用户地址空间。进程有独立的地址空间既是优点，也是缺点，这样一来，一个进程不可能不小心覆盖另一个进程的虚拟存储器；另一方面，独立的地址空间使得进程之间共享信息变得更加困难。另外，基于进程的设计另一个缺点是，往往运行比较慢，因为进程控制和IPC开销比较高。

下面是：Unix C实现基于进程的小型并发服务器的轮廓：

	pid_t pid;
	int listenfd, connfd;
	listenfd = Socket(....);
	Bind(listenfd, ...);
	Listen(listenfd, LISTENQ);
	for( ; ; ){
		connfd = Accept(listenfd, ...);		/*可能阻塞*/
		if( (pid = Fork()) == 0){			/*有accept时则fork一个进程单独处理*/
			Close(listenfd);				/*子进程关闭监听套接字listenfd*/
			doit(connfd);					/*处理请求*/
			Close(connfd);					/*处理结束关闭连接套接字connfd*/
			exit(0);						/*子进程退出*/	
		}
		Close(connfd);						/*父进程关闭已连接的套接字*/
	}


注意：

- 这里首字母大写的都是原函数的包裹函数
- 父进程close已连接套接字后子进程也需要close已连接套接字
- 在子进程中close可有可无，因为有exit(0)的存在，它会清理已打开的描述符，是否显式调用，与编程习惯有关
- 思考为什么要两次close已连接的套接字？

**每一个文件或套接字都有一个引用计数，由文件表维护，所谓引用计数就是打开描述符的个数**。上例中监听套接字listenfd和已连接套接字connfd在`accept`时只有1个，然后`fork`后，这两个描述符在父进程和子进程间共享（也就是被复制），因此它们的访问计数都变成了2，这样一来当父进程close connfd时，它的引用计数为1，该套接字真正的清理和资源释放要等到其引用计数为0时才发生，这会在稍后子进程也close connfd是发生，如下状态图：

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/acc1.png)

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/acc2.png)

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/acc3.png)

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/acc4.png)



推荐这篇博客[ **UNIX网络编程——并发服务器（TCP）**](http://blog.csdn.net/ctthuangcheng/article/details/9412791)

# 九.close函数

关闭套接字

	#include <sys/socket.h>
	int close(int sockfd);
	/*Returns: 0 if OK,-1 on error*/


如果对某个TCP发送FIN，则可以用`shutdown`函数来代替close.

# 十.getsockname和getpeername函数
一个返回套接字关联的本地协议地址(getsockname),和外地协议地址(getpeername)。

	#include <sys/socket.h>
	int getsockname(int sockfd, struct sockaddr *localaddr, socklen_t *addrlen);
	int getpeername(int sockfd, struct sockaddr *peeraddr, socklen_t *addrlen);
	/*Both return: 0 if OK, -1 on error*/

这两个函数的最后一个参数都是**值-结果参数**。
