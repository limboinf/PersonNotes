/* include signal 
 * 定义signal函数，它只是调用POSIX的sigaction函数
 * 头文件unp.h定义了Sigfunc类型来简化signal函数
 * */
#include	"unp.h"

Sigfunc *
signal(int signo, Sigfunc *func)
{
	struct sigaction	act, oact;		//sigaction结构

	act.sa_handler = func;				//sigaction结构的sa_handler设置为func，即设置处理函数
	sigemptyset(&act.sa_mask);			//把sa_mask设置为空集，不阻塞额外信号
	act.sa_flags = 0;					//设置SA_RESTART标志
	if (signo == SIGALRM) {
#ifdef	SA_INTERRUPT
		act.sa_flags |= SA_INTERRUPT;	/* SunOS 4.x */
#endif
	} else {
#ifdef	SA_RESTART
		act.sa_flags |= SA_RESTART;		/* SVR4, 44BSD */
#endif
	}
	//最后调用sigaction函数，将相应信号的旧行为作为signal函数的返回值
	if (sigaction(signo, &act, &oact) < 0)
		return(SIG_ERR);
	return(oact.sa_handler);
}
/* end signal */

Sigfunc *
Signal(int signo, Sigfunc *func)	/* for our signal() function */
{
	Sigfunc	*sigfunc;

	if ( (sigfunc = signal(signo, func)) == SIG_ERR)
		err_sys("signal error");
	return(sigfunc);
}
