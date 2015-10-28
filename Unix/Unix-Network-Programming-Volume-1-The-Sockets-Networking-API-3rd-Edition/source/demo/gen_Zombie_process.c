#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>

int main()
{
	pid_t pid;
	pid = fork();
	if(pid < 0){
		perror("fork error");
	} else if (pid == 0) {
	    printf("I am child process.I am exiting.\n");
		exit(0);
	}
	printf("I am father process.I will sleep two seconds\n");
	//等待子进程先退出
	sleep(2);
	//输出进程信息
	system("ps -o pid,ppid,state,tty,command");
	printf("father process is exiting.\n");
	
	return 0;
}
