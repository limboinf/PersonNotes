example:

    char* pArry[] = {"abc","defg","dddddd", "Jack", "xixi"};
    int z = sizeof(pArry) / sizeof(char *);     // or: sizeof(pArry) / sizeof(pArry[0]);
    printf("%d\n", z);
    
    int m[] = {1,2,3,4,5,6,7,8,9, 10};
    int b = sizeof(m) / sizeof(int);
    printf("%d\n", b);



