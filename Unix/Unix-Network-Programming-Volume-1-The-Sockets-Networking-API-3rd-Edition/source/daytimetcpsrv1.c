//本程序是一个基于多进程的并发echo服务器，父进程派生一个子进程来处理每个新的连接请求
#include "unp.h"
//echo程序，用于向客户端发送响应主体
void echo(int connfd)
{
    int n;
    char buf[MAXLINE];
    rio_t rio;
     
    rio_readinitb(&rio,connfd);
    //带缓冲的读取函数
    while((n=rio_readlineb(&rio,buf,MAXLINE))>0) {
        //向连接符写入内容
        printf("server received %d bytes \n",n);
        rio_writen(connfd,buf,n);
    }
}
 
//信号处理函数，用于处理僵死进程，即回收已经终止的进程给系统带来的资源占用
void sigchld_handler(int sig)
{
    //-1代表回收父进程的子进程组，由于unix信号是不排队的，因此必须准备好回收多个僵死子进程的准备
    while(waitpid(-1,0,WNOHANG)>0)
        ;
    return;
}
 
int main(int argc,char **argv)
{
    int listenfd,connfd,port;
    socklen_t clientlen=sizeof(struct sockaddr_in);
    struct sockaddr_in clientaddr;
     
    if(argc!=2) {
        fprintf(stderr,"usage :%s <port>\n",argv[0]);
        exit(0);
    }
    //将字符串转化为整型，端口号
    port=atoi(argv[1]);
    //启动信号处理函数监听器
    signal(SIGCHLD,sigchld_handler);
    //启动服务器监听描述符
    listenfd=open_listenfd(port);
    while(1) {
        //已连接描述符,接受连接
        connfd=accept(listenfd,(SA *)&clientaddr,&clientlen);
        //开辟子进程，用于处理连接请求
        if(fork()==0) {
            //由于子进程共享父进程的所有资源，因此先关闭监听描述符，再调用请求体命令，然后关闭已连接描述符，并且正常终止此进程
            close(listenfd);
            echo(connfd);
            close(connfd);
            exit(0);
        }
        //关闭父进程的已连接描述符
        close(connfd);
    }
}
