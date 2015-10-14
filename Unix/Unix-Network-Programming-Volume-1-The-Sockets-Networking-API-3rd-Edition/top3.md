第3章 套接字编程简介

首先从**套接字地址结构**开始

# 一.套接字地址结构
socket functions require a pointer(指针) to a socket address structure as an argument.每个协议都定义了它字节的套接字地址结构。都以`sockaddr_`开头，并对应每个协议族的唯一后缀.

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

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/posix_datatype.png)
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


