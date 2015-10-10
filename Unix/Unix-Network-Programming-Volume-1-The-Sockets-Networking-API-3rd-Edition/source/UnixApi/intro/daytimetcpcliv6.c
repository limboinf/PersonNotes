#include "unp.h"   /*该头文件包含大部分网络程序需要的系统头文件，并定义了所用到的各种常量值如MAXLINE*/
//ipv6版本
int main(int argc, char **argv)
{
	int sockfd, n;
	char recvline[MAXLINE+1];
	struct sockaddr_in6 servaddr;		// sockaddr_in --> sockaddr_in6
	if (argc !=2)
		err_quit("usage:a.out <IPaddress>");
	
	/*
	 * socket 函数创建一个网际(AF_INET)字节流(SOCK_STREAM)套接字
	 * 该函数返回一个小整数描述符，以后的所有函数调用(如connect, read)就用该描述符标识这个套接字
	 * 如果socket调用失败(小于0)，则用我们自定义(unp.h)的err_sys放弃程序运行
	 */
	if((sockfd=socket(AF_INET6, SOCK_STREAM, 0)) < 0)	// AF_INET --> AF_INET6
		err_sys("socket error");
	/*
	 * 把服务器IP和端口填入一个网际套接字地址结构中(一个名为servaddr的sockaddr_in结构变量)
	 * 使用bzero把整个结构清零
	 * 置地址族为AF_INET,端口号13（时间服务器端口号，支持tcp/ip）
	 * htons为库函数(主机到网络短整数)去转换二进制端口号
	 * inet_pton为库函数(呈现形式到数据)去把ASCII命令行参数（如：216.228.192.69）转换为合适的格式
	 */
	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin6_family = AF_INET6;			// sin_*--> sin6_*
	servaddr.sin6_port = htons(13);		/*daytime server*/
	if(inet_pton(AF_INET6, argv[1], &servaddr.sin6_addr) <= 0)
		err_quit("inet_pton error for %s", argv[1]);
	/*
	 * connect函数应用于一个TCP套接字时，将与由它的第二个参数指向的套接字地址结构指定的服务器建立TCP连接
	 * 该套接字地址结构的长度也必须作为第三个参数
	 */
	if(connect(sockfd, (SA *) &servaddr, sizeof(servaddr)) < 0)
		err_sys("connect error");
	/*
	 * 读入并输出服务器应答
	 * read函数读取服务器应答，并用标准I/O函数fputs输出结果
	 * TCP套接字读取数据时，总需要把read编写在某个循环中，当read为0(表明对端关闭连接)或负数(表明发生错误)时终止程序
	 */
	while((n = read(sockfd, recvline, MAXLINE)) > 0){
		recvline[n] = 0;		/*null terminate*/
		if(fputs(recvline, stdout) == EOF)
			err_sys("fputs error");
	}

	if(n < 0)
		err_sys("read error");
	/*
	 * exit终止程序运行
	 * Unix在一个进程终止时总是关闭该进程所有打开的描述符，TCP套接字就被关闭
	 */
	exit(0);
}

/*
 * 操作
 * gcc daytimetcpcli.c -o daytimetcpcli -lunp
 * ./daytimetcpcli 216.228.192.69 
 * 57305 15-10-10 07:42:43 23 0 0  10.1 UTC(NIST) * 
 */

