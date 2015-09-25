top2: 二进制数值和计数系统

这节主要就是理解二进制数值，能够进行相关的转换和操作，理解计算机系统如何使用二进制计数。知识点涵盖如下：

- 数字分类
- 位置计数
- 其他基数的的数字转换成十进制
- 十进制转换为其他基数的数字
- 基数2，8，16之间的关系
- 为什么以2的幂为基数？

# 一.数字和计算
>数字是属于抽象数学系统的一个单位，服从特定的顺序法则，运算法则

数字的分类：

- 自然数：是0和通过在0上重复加1得到的任何数
- 负数：小于0的数
- 整数：所有自然数和他们的负数
- 有理数：包括整数和两个整数的商

数字对计算至关重要，用到那呢？

1. 运算
2. 所有计算机存储和管理的数据都以数字形式存储
3. 所有信息都是用数字0，1存储

# 二.位置记数法
**基数**：决定了系统数字量，从0开始，到基数-1结束。例如以2为基数，有两个数字0和1；以8为基数，有8个数字，0~7；以10为基数，有10个数字，0~9

## 1.1 十进制(Decimal)
基数10， 范围0~9, 标识`D`或下标`10`, 如 (123)D

## 1.2 二进制(Binary)
基数2，范围0~1, 标识`B`或下标`2`, 如 (1001010)B

## 1.3 八进制(Octal)
基数8，范围0~7, 标识`Q`或`O`或下标`8`, **在C/C++中，一定要标识O表明是八进制**

## 1.4 十六进制(Hexadecilmal)
基数16，范围0~15, 标识`H`或下标`16`, **在C/C++， 一定要`0X`开头**

## 1.5 重点小结

- 计算机的运算都是二进制
- 计算机为什么出现这么多进制的原因**数据用二进制表示太长**
- C/C++代码中不能直接写二进制， 而是普遍采用八进制或十六进制
- 为什么不是9进制或20进制，原因就是**2,8,16分别是2的次方，这就是三种进制之间可以直接互相转换**

# 三.不同进制间的互相转换
## 3.1 非十进制转换为十进制
采用**按权相加**

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/CS/media/cs3.png)

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/CS/media/cs4.png)

十六进制也同上

## 3.2 十进制转换为非十进制

### 3.2.1 十进制整数转二进制

>这里是**整数**， 方法**除2逆序取余法**， 先将十进制数除以2，得到一个商(也是下一步的被除数)和余数；然后再将商除以2，又得到一个商和余数；以此类推，直到商数小于2为止。然后从最后得到小于2的商开始将其他各步所得的余数(也是小于2)排列起来，就得到了对应的二进制

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/CS/media/cs5.png)

### 3.2.2 十进制小数转换为二进制

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/CS/media/cs6.png)

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/CS/media/cs7.png)

### 3.2.3 十进制转八进制
与转二进制类似，不过基数变成了8

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/CS/media/cs8.png)

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/CS/media/cs9.png)

### 3.2.4 十进制转16进制

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/CS/media/cs10.png)


**实例1：十进制转其他任意进制：**


	#include <stdio.h>

	// 十进制整数转其他进制
	void dec_inter2other()
	{
	    int i=0, m, n, r, a[40];                // m:十进制整数， r:进制， a:40位，一般的十进制整数大概范围
	    char str[16] ="0123456789ABCDEF";       // 列举所有进制对应的字符
	    scanf("%d %d", &m, &r);
	    m = m > 0 ? m : -m;                     // 负数变正数
	    
	    do{
	        a[i++] = m % r; // 取余
	        printf("i=%d,取余:%d\n", i, m%r);
	        m = m / r;      // 取商，也就是下一位的被除数
	        printf("下一步的被除数：m=%d\n", m);
	    }while (m > 0);
	    
	    for (n=i-1; n>=0; n--) {        // 倒序循环打印a数组元素
	        printf("%c", str[a[n]]);    // %c 一定要对应字符类型
	    }
	}

	// 十进制小数转其他进制
	void dec_point2other()
	{
	    // 乘2正序取整法
	    int i=0, n, r, a[40];
	    float m;
	    char str[16] = "0123456789ABCDEF";
	    scanf("%f %d", &m, &r);
	    m = m>1 ? 0: m >0 ? m: -m;
	    while (m != 0) {
	        a[i++] = (int)(m * r);
	        printf("乘积取整：%d\n", (int)(m * r));
	        m = m * r - (int)(m * r);
	        printf("下一步的乘数:%f\n",m);
	    };
	    
	    // 十进制小数转换为其他进制也为小数，注意要加上它
	    
	    for (n=0; n<i; n++) {
	        printf("%c", str[a[n]]);
	    }
	}


	int main(int argc, char *argv[]) {
	    dec_point2other();
	    return 0;
	}


# 四. 二进制转8，16进制 以及 八进制转2，16进制 以及 十六进制转2，8进制

原则都是：**先转10进制，然后再转其他进制**

**实例2： 二进制转其他进制**

	// 二进制转其他任意进制
	// 二进制转10，8，16进制, 都采用按权相加
	void bin2other()
	{
	    int i=0, r, a=0;
	    char bin[40];
	    scanf("%s %d", bin, &r);
	    //unsigned long n = strlen(bin);
	    int n = (int)(strlen(bin));
	    for (n-=1; bin[n] != '\0'; n--) {
	        i++;
	        if (bin[n] == '1') {
	            a += pow(2, i-1);
	        }
	    }
	    
	    printf("十进制：%d\n", a);
	    
	    // 转换其他进制
	    int j=0, others[40], k;
	    char str[16] = "0123456789ABCDEF";
	    if (r != 10) {
	        do{
	            others[j++] = a % r;    // 取余
	            a = a / r;              // 取商，也就是下一位的被除数
	        }while (a > 0);
	        
	        for (k=j-1; k>=0; k--) {        // 倒序循环打印a数组元素
	            printf("%c", str[others[k]]);    // %c 一定要对应字符类型
	        }

	    }
	}


**实例3：八进制转其他进制**

	// 八进制转其他进制
	// 八进制转10，2，16
	void oct2other()
	{
	    int i=0, r, a=0;
	    char oct[40];
	    scanf("%s %d", oct, &r);
	    int n = (int)(strlen(oct));
	    //先将八进制转10进制
	    for (n-=1; oct[n] != '\0'; n--) {
	        i++;
	        if (oct[n] != '0') {
	            switch (oct[n]) {
	                case '1':
	                    a += pow(8, i-1);
	                    break;
	                case '2':
	                    a += 2*(pow(8, i-1));
	                    break;
	                case '3':
	                    a += 3*(pow(8, i-1));
	                    break;
	                case '4':
	                    a += 4*(pow(8, i-1));
	                    break;
	                case '5':
	                    a += 5*(pow(8, i-1));
	                    break;
	                case '6':
	                    a += 6*(pow(8, i-1));
	                    break;
	                case '7':
	                    a += 7*(pow(8, i-1));
	                    break;
	                default:
	                    break;
	            }
	        }
	    }
	    printf("十进制：%d\n", a);
	    
	    // 转换其他进制
	    int j=0, others[40], k;
	    char str[16] = "0123456789ABCDEF";
	    if (r != 10) {
	        do{
	            others[j++] = a % r;    // 取余
	            a = a / r;              // 取商，也就是下一位的被除数
	        }while (a > 0);
	        
	        for (k=j-1; k>=0; k--) {        // 倒序循环打印a数组元素
	            printf("%c", str[others[k]]);    // %c 一定要对应字符类型
	        }
	        
	    }

	}

	// 同理 十六进制也一样.


**实例4：十六进制转其他进制**

原理同上。 [全部代码在这里](https://github.com/BeginMan/BookNotes/blob/master/CS/source/int_bin_oct_hex_translate.c)


# 四.二进制数值与计算机

- 位(bit): 一个存储单元，二进制数字的简称
- 字节(byte): 8个二进制位
- 字(word)：一个或多个字节， 字中的位数称为字长



