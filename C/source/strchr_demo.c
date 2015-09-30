#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[])
{
	char *pMysite = "www.beginman.cn";
	// 如果str中存在字符ch,返回最后出现ch的位置的指针；否则返回NULL。
	char *pFind = strrchr(pMysite, '.');		//查找在s字符串中最后一次出现字符c的位置
	if(pFind != NULL)
		printf("%s", pFind);
}
