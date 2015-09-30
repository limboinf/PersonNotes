ref:[How can i check whether a string ends with “.csv” in C](http://stackoverflow.com/questions/10347689/how-can-i-check-whether-a-string-ends-with-csv-in-c)

使用到`strrchr()`函数，可查看文档：[C library function - strrchr()](http://www.tutorialspoint.com/c_standard_library/c_function_strrchr.htm)

如果检查字符串以`.csv`结尾可以这样：

	char *dot = strrchr(str, '.');
	if (dot && !strcmp(dot, ".csv"))
	    /* ... */

或者这样：

	if(strlen(str) > 4 && !strcmp(str + strlen(str) - 4, ".csv"))

