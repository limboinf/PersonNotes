Linux shell创建空文件(0字节大小)文件方法

`echo>fileName`创建的文件是**1个字节**的。

学习后发现创建空文件(0字节大小)的文件有以下几个方法

1. file不存在时，`touch file`可以创建空文件
2. `:>file`可以创建空文件，如果file存在，则把file截断为0字节
3. `>file`可以在bash下完成和`:>file`相同的功能，但是tcsh下不能使用
4. `&>file`和`>file`一样，在bash完成`:>file`相同的功能，但是tcsh下不能使用.可以理解`&`和`:`为占位符，在这里不输出任何内容。
5. `cat /dev/null > file`
6. `mktemp`

ref:[Linux shell创建空文件(0字节大小)文件方法](http://laoxu.blog.51cto.com/4120547/1273831)
