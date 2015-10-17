第3章 套接字编程简介

首先从**套接字地址结构**开始

# 一.套接字地址结构
socket functions require a pointer(指针) to a socket address structure as an argument.每个协议都定义了它自己的套接字地址结构。都以`sockaddr_`开头，并对应每个协议族的唯一后缀.

## 1.1 IPv4套接字地址结构

IPv4套接字地址结构，以`sockaddr_in`命名，定义在`<netinet/in.h>`头文件中.它的POSIX定义:

	struct in_addr {
	 	in_addr_t s_addr; 	/* 32-bit IPv4 address */
	 						/* network byte ordered */
	};

	struct sockaddr_in {
	 	uint8_t 		sin_len; 	/* length of structure (16) */
	 	sa_family_t 	sin_family; /* AF_INET */
	 	in_port_t 		sin_port; 	/* 16-bit TCP or UDP port number */
	 								/* network byte ordered */
	 	struct in_addr 	sin_addr; 	/* 32-bit IPv4 address */
	 								/* network byte ordered */
	 	char sin_zero[8]; 			/* unused */
	 }


- `sin_len`: 长度字段，`uint8_t`数据类型是典型的，只要符合POSIX都提供这种形式的数据类型，这个字段的作用在于**简化长度可变套接字地址结构的处理**
- POSIX规范只需要这个结构的3个字段：`sin_family`,`sin_port`,`sin_addr` 
- POSIX数据类型

数据类型|说明|头文件
----|----|----
`int8_t` | 带符号的8位整数 | `<sys/types.h>`
`uint8_t` | 无符号的8位整数 | `<sys/types.h>`
`int16_t` | 带符号的16位整数 | `<sys/types.h>`
`uint16_t` | 无符号的16位整数 | `<sys/types.h>`
`int32_t` | 带符号的32位整数 | `<sys/types.h>`
`uint32_t` | 无符号的32位整数 | `<sys/types.h>`
`sa_family_t` | 套接字地址结构的地址族 | `<sys/socket.h>`
`socklen_t` | 套接字地址结构的长度，一般为uint32_t | `<sys/socket.h>`
`in_addr_t` | IPv4地址，一般为uint32_t | `<netinet/in.h>`
`in_port_t` | TCP或UDP端口，一般为uint16_t | `<netinet/in.h>`



- `sin_zero`总是设置为0，按照惯例在填写前总是把整个结构置为0，而不单单是sin_zero字段置为0

## 1.2 通用套接字地址结构

套接字函数必须处理来自不同协议族的指向套接字结构指针的参数，在ANSI C出现后，通过`void *` **通用指针类型**很容易解决，然而在此之前是这样定义的：

	struct sockaddr {
		uint8_t 		sa_len;
		sa_family_t		sa_family;	/*address family: AF_xxx value */
		char 			sa_data[4]; /*指定协议的地址*/
	};

**所以套接字函数被定义为以指向某个通用套接字地址结构的一个指针作为参数之一**。如`bind`函数的ANSI C函数原型：

	int bind(int, struct sockaddr *, socklen_t);

**这要求这些函数的任何调用都必须将指向特定协议的套接字地址结构的指针进行类型强制转换，变成指向某个通用套接字地址结构的指针**， 如：

	struct sockaddr_in serv; /* IPv4 socket address structure */
	/* fill in serv{} */
	bind(sockfd, (struct sockaddr *) &serv, sizeof(serv));

如果省略了`(struct sockaddr *)`类型强制转换部分则会报错.

## 1.3 IPv6套接字地址结构
以`sockaddr_in6`命名。

	struct in6_addr {
		uint8_t 		s6_addr[16]; /* 128-bit IPv6 address */
	};

	#define SIN6_LEN 				/* required for compile-time tests */
	struct sockaddr_in6 {
		uint8_t 		sin6_len; 		/* length of this struct (28) */
		sa_family_t 	sin6_family; 	/* AF_INET6 */
		in_port_t 		sin6_port; 		/* transport layer port# */
		uint32_t 		sin6_flowinfo; 	/* flow information, undefined */
		struct in6_addr sin6_addr; 		/* IPv6 address */
		uint32_t 		sin6_scope_id; 	/* set of interfaces for a scope */
	};

## 1.4 新的通用套接字地址结构
`struct sockaddr_storage`足以容纳系统中任何套接字地址结构

	struct sockaddr_storage {
		uint8_t 	ss_len; 	/* length of this struct (implementation dependent) */
		sa_family_t ss_family; 	/* address family: AF_xxx value */
	};

与`sockaddr`不同的是：

1. 满足最苛刻的套接字地址结构对齐
2. 足够大

# 二.值-结果参数
向套接字函数传递套接字地址结构指针，该结构的长度也作为一个参数传递，**传递的方式取决于该结构的传递方向：是从进程到内核，还是从内核到进程**

## 2.1 从进程到内核
从进程到内核传递套接字地址结构的函数有3个：`bind`、`connect`,`sendto`.这些函数第一个参数是指向某个套接字地址结构的指针，另一个参数是*该结构的整数大小*:

	struct sockaddr_in serv;
	connect (sockfd, (struct sockaddr *) &serv, sizeof(serv));

**指针和指针所指内容的大小都告诉了内核，内核就知道从进程中复制多少数据来：**

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/process_to_kernel.png)

## 2.2 从内核到进程

从内核到进程传递套接字地址结构的函数有4个：`accept`,`recvfrom`,`getsockname`,`getpeername`，需要两个参数，一个同上是指针，另一个则是**指向表示该结构大小的整数变量的指针**：

	struct sockaddr_un cli;			/*Unix domain*/
	socklen_t len;

	len = sizeof(cli);				/*len is a value*/
	getpeername(unixfd, (struct sockaddr *) &cli, &len)	 /*注意这里是 &len*/
	/* len may have changed */

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/kernel_to_process.png)

关于值-结果参数要明白：**用指针传递， 这样它的值可以被函数更改**。

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/value_result_param.png)


# 三.字节排序函数

可参考我这一篇文章：[Unix网络编程之理解Socket与字节序](http://beginman.cn/unp/2015/10/15/unp-socket/)

# 四.字节操纵函数
我们需要处理像IP地址这样的字段，此字段可能包含0个字节，却并不是C字符串。对于字符串：以空字符串结尾的C字符串通过`<string.h>`定义，并由`str`(表示字符串)开头的函数处理

对于字节，有两组操纵函数：

1. 以b开头(表示字节)的函数, 如`bzero`,`bcopy`,`bcmp`
2. 以mem(表示内存)开头的函数，如`memset`,`memcpy`, `memcmp`

# 五.地址转换函数
将在ASCII字符串与网络字节序的二进制值(存放在套接字地址结构中的值)之间转换网际地址。有如下两组：

(1). `inet_aton`,`inet_addr`和`inet_ntoa`在点分十进制数串(如201.33.211.89)与它32位网络字节序二进制值间转换IPv4地址

	#include <arpa/inet.h>
	/*将strptr所指的C字符串转换为32位网络字节序二进制，并通过指针addrptr来存储*/
	/*成功则返回1，否则返回0*/
	int inet_aton(const char *strptr, struct in_addr *addrptr);

	/*返回：如果字符串有效则为32位二进制网络字节序的IPv4地址，否则为INADDR_NONE*/
	int_addr_t inet_addr(const char *strptr);

	/*返回：指向点分十进制数串的指针*/
	char *inet_ntoa(struct in_addr inaddr);

(2). `inet_pton`和`inet_ntop`比较新，对于IPv4和IPv6都适用,p代表表达，n代表数值;书中有大量的解释，这里暂且泛读。

`inet_ntop`调用必须要知道这个结构的格式和地址族，如：

	/*IPv4*/
	struct sockaddr_in addr;
	inet_ntop(AF_INET, &addr.sin_addr, str, sizeof(str))

这使得与协议有关了，书中自行编写一个名为`sock_ntop`(非标准系统函数)来解决这个问题。

# 六.readn,writen和readline函数
字节流套接字上的read和write函数所表现的行为不同于通常的文件I/O.字节流套接字上调用read或write输入或输出的字节数可能比请求的数量少,然而这不是出错状态.这个现象的原因在于**内核中用于套接字的缓冲区可能已经达到了极限**.此时所需的是调用者再次调用read个write函数,以输入或输出剩余的字节. 我们提供的以下三个函数是每当我们读或写一个字节流套接字时要使用的函数.

	//从一个描述符读取n个字节
	ssize_t readn(int fd, void* vptr, size_t n)
	{
	 size_t  nleft = n;  //记录还剩下多少字节数没读取
	 ssize_t nread;      //记录已经读取的字节数
	 char*  ptr = vptr;  //指向要读取数据的指针
	 while(nleft > 0)    //还有数据要读取
	 {
	  if(nread = read(fd,ptr,nleft) < 0)
	   if(erron == EINTR)//系统被一个捕获的信号中断
	    nread = 0;       //再次读取
	   else
	    return -1;       //返回
	  else if(nread == 0)//没有出错但是也没有读取到数据
	   break;            //再次读取
	  nleft -= nread;    //计算剩下未读取的字节数
	  ptr  += nread;     //移动指针到以读取数据的下一个位置
	 }
	 return (n-nleft);   //返回读取的字节数
	}
	/**************************************************************************************************/
	//从一个描述符读文本行,一次一个字节
	ssize_t readline(int fd, void* vptr, size_t maxlen)//一个字节一个字节地读取
	{
	 ssize_t  rc;        //每次读取的字符
	 ssize_t  n;         //读取的次数也即读取字符串的长度
	 char     c;         //
	 char* ptr = vptr;   //指向要读取的数据的指针
	 for(n = 1;n < maxlen; n++)
	 {
	  again:
	  if((rc = read(fd,&c,1)) == 1)
	  {
	   *ptr++ = c;       //移动指针
	   if(c == '\n')     //换行符
	    break;           //跳出循环
	   else if(rc == 0)  //结束
	    *ptr = 0;        //字符串以0结尾
	   return (n-1);     //返回读取的字节数 末尾的0不算
	  }
	  else
	  {
	   if(erron == EINTR)
	    goto again;      //重新读取
	   return (-1)
	  }
	 }
	 *ptr=0;
	 return n;
	}
	/**************************************************************************************************/
	//往一个描述符写n个字节
	ssize_t writen(ind fd, const void* vptr, size_t n)
	{ 
	 size_t nleft = n;        //还需要写入的字节数 
	 ssize_t nwritten;        //每次写入的字节数 
	 const char* ptr = vptr;  //指向要写入的数据的指针 
	 while(nleft > 0) 
	 { 
	  if((nwritten = write(fd,ptr,nleft)) <= 0) 
	  { 
	   if(nwritten < 0 && erron == EINTR) 
	    nwritten = 0; 
	   else return -1; 
	  }
	   nleft -= nwritten;     //计算还需要写入的字节数 
	 ptr += nwritten;         //移动数据指针 
	  } 
	  return n;
	 }


