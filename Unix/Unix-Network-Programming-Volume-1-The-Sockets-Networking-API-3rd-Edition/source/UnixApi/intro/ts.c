#include <stdio.h>
#include <arpa/inet.h>

int main(void)
{
	unsigned int x = 0x12345678;
	unsigned char *p = (unsigned char *) &x;
	printf("%x,%x,%x,%x\n", p[0], p[1], p[2], p[3]);

	unsigned int y = htonl(x);
	p = (unsigned char *)&y;
	printf("%x,%x,%x,%x\n", p[0], p[1], p[2], p[3]);
	return 0;
}
