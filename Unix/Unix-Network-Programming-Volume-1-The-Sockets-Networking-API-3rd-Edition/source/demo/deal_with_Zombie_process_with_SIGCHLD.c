/*
 * 子进程退出时向父进程发送SIGCHILD信号，父进程处理SIGCHILD信号。
 * 在信号处理函数中调用wait进行处理僵尸进程。测试程序如下所示：
 */
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <signal.h>

static void sig_child(int signo);

int main()
{
	pid_t pid;
	pid = fork();
	// 创建捕获SIGCHLD通知
	signal(SIGCHLD, sig_child);

	if(pid < 0){
		perror("fork error\n");
	} else if(pid == 0){
		printf("I am child process pid:%d, i'm exiting\n", getpid());
		exit(0);
	} else {
		printf("I am father process, sleep 3s\n");
		sleep(3);
		system("ps -o pid,ppid,state,tty,command");
		printf("father process exit\n");
	}
	return 0;
}

static void sig_child(int signo)
{
	pid_t	pid;
	int		stat;
	// 处理僵尸进程
	while((pid = waitpid(-1, &stat, WNOHANG)) > 0){
		printf("zombie process terminated\n");
	}
}
