#include "unp.h"

int main(int argc, char **argv)
{
	union {
		short		s;
		char		c[sizeof(short)];
	} un;

	un.s = 0x0102;									//短整数变量中存放2个字节的值0x0102
	printf("%s: ", CPU_VENDOR_OS);					//标识CPU类型，厂家和操作系统版本，如:i386-apple-darwin14.5.0
	if(sizeof(short) == 2) {
		//查看它的两个连续字节c[0],c[1]来确定字节序
		if (un.c[0] == 1 && un.c[1] == 2)
			printf("big-endian\n");
		else if (un.c[0] == 2 && un.c[1] == 1)
			printf("litter-endian\n");
		else
			printf("unknown\n");
	} else
		printf("sizeof(short) = %lu\n", sizeof(short));
	exit(0);
}
