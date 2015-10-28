#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>

int main()
{
	pid_t pid;
	pid = fork();
	if(pid < 0)
	{
		perror("fork error");
		exit(1);
	} else if (pid == 0){
		//第一个子进程
		printf("I am the first child process.pid:%d\tppid:%d\n",getpid(),getppid());
		//子进程再创建一个子进程
		pid = fork();
		if(pid < 0){
			perror("fork error:");
			exit(1);
		} else if (pid > 0){
			//第一个子进程退出
			printf("first procee is exited.\n");
			exit(0);
		}
		//睡眠3s保证第一个子进程退出，这样第二个子进程的父亲就是init进程里
		sleep(3);
		printf("I am the second child process.pid: %d\tppid:%d\n",getpid(),getppid());
		exit(0);
	}

	if(waitpid(pid, NULL, 0) != pid)
	{
		perror("waitpid error");
		exit(1);
	}
	return 0;
}
