

# 一.系统调用


系统调用就是**操作系统内核函数**， 通过`stdlib.h`库，为C提供很多接口。

## 1.1 system()函数

	system("dir D:"); // windows:打印D盘内容
	system("gedit");	// *unix：启动编辑器
	system("say 'you are SB'");	//mac: 朗读文本

`system()`函数在操作系统上，当调用它时操作系统必须解释**命令字符串**，然后决定运行哪些程序和怎么运行，但存在很大安全问题， 如删除一些东西，注入恶意代码，更改环境变量等， 要解决这个问题就必须消除歧义，明确告诉操作系统运行什么程序，而不是由操作系统瞎解释。在C中用`exec()`函数来告知。

## 1.2 exec()函数替换当前进程
**进程是存储器中运行的程序**，如输入`ps -ef`则看到一堆输出，操作系统用一个数字来标识进程，叫**进程标识符(process identifier, 简称PID)**

exec()装入并运行其它程序的函数,把进程交接给了新程序.

## 1.3 exec()函数有很多
版本众多，分**列表函数**和**数组函数**

### 1.3.1 列表函数:execl()、execlp()、execle()

**列表函数以参数列表的形式接收命令行参数:**

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top9_1.png)

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top9_2.png)

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top9_3.png)

### 1.3.2 数组函数：execv(), execvp(), execve()

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top9_4.png)

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top9_5.png)


### 1.3.3 传递环境变量
**每个进程都有一组环境变量**, 命令行中使用`set`或`env`查看它们的值。C用`getenv()`系统调用读取环境变量.如果想用命令行参数和环境变量运行程序，可以这样做：

	// diner_info.c

	#include <stdio.h>
	#include <stdlib.h>

	int main(int argc, char *argv[]){
	    printf("%s\n", argv[1]);
	    printf("%s\n", getenv("JUICE"));
	    return 0;
	}

	// main.c

	#include <stdio.h>
	#include <stdlib.h>
	#include <unistd.h>

	int main(int argc, char *argv[]) {
	    char *my_env[] = {"JUICE=peach and apple", NULL};			// 字符串指针数组创建一组环境变量
	    execle("diner_info", "diner_info", "4", NULL, my_env);
	    return 0;
	}

main.c用来通过参数列表和环境变量字符数组来调用diner_info可执行文件：

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top9_6.png)

execle()函数将设置命令行参数和环境变量,然后用diner_info替换当前进程。

	gcc diner_info.c -o diner_info
	gcc main.c -o main 
	./main
	4
	peach and apple

## 1.4 系统调用失败的处理法则

一旦系统调用如`exec()`失败则就不会继续往下走了，处理失败的黄金法则摘抄如下：

- 尽可能收拾残局
- 把errno变量设为错误码
- 返回-1










