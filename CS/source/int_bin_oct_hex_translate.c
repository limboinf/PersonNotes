//
//  main.c
//  intoC
//
//  Created by 方朋 on 15/9/2.
//  Copyright (c) 2015年 方朋. All rights reserved.
//

#include <stdio.h>
#include <math.h>
#include <string.h>

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


int main(int argc, char *argv[]) {
//    bin2other();
//    dec_inter2other();
    oct2other();
    return 0;
}


