这章学习的是代码共享的方式，包含的知识点：

- include机制
- 静态库
- 动态库



# 一.include头文件

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top8_1.png)

# 二.共享代码之静态库
希望程序之间共享两类代码，`.h` , `.o`. Follow it:

## 2.1 共享头文件
共享头文件的方法有很多种：

- 1.把头文件保存到`/usr/local/include` 标准目录中，就可以用尖括号`#include <>`
- 2.include使用完整路径名，如`#include "/my_header_files/encrypt.h"`, 也可以是相对路径
- 3.通过`gcc -I/path_to_my_header` 告诉编译器去哪找头文件，如`gcc -I/my_header_files test_code.c ... -o test_code`

## 2.2 共享目标文件
可以把`.o`目标文件存放在一个类似共享目录的地方，当编译时只要在目标文件前加上完整路径即可，如下：

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top8_2.png)

	gcc -I/my_header_files test_code.c
		 /my_object_files/encrypt.o
		 /my_object_files/checksum.o -o test_code

如果共享多个文件，则这种方式就显得麻烦了，有没有办法可以告诉编译器我想共享一大堆目标文件呢？

**只要创建目标文件存档,就可以一次告诉编译器一批目标文件。**

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top8_3.png)

### 2.2.1 用ar命令创建存档

用存档命令`ar`存档一批目标文件：

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top8_4.png)

注意：**存档是静态的(static library), 所以要以`lib`开头， 务必把存档命名为`libxxxx.a`, 否则编辑器找不到它们**

`.a`文件保存的位置选择：

- `/usr/local/lib`下
- 放在其他目录，如`/my_lib`

如我们把上面的libhfsecurity.a文件放在标准目录下， 然后执行编译：

	sudo mv libhfsecurity.a /usr/local/lib

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top8_5.png)


现在知道为什么要把存档命名为libXXX.a了吧。`-l`选项后的名字必须与存档名的一部分􏱃配。如果你的存档叫libawesome.a,可以用`-lawesome`开关编译程序。

如果想把存档放在其他地方呢?比如/my_lib。你可以 用`-L`(**注意大写**)选项告诉编译器去哪个目录查找存档:

	gcc test_code.c -L/my_lib -lhfsecurity -o test_code


使用`ar -t <文件名>` 列出存档中的目标文件：

	➜  lib git:(master) ar -t libhfsecurity.a 
	__.SYMDEF SORTED
	encrypt.o
	checksum.o

可以使用`ar -x 存档名 目标文件` 取出某一目标文件

**通过上面的例子知道为什么加`静态链接`， 就是一旦链接后就不能修改**

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top8_6.png)

记住命令后，下面一个实例：

step1: 创建elliptical.c文件：

	#include <stdio.h>
	#include <hfcal.h>      // 注意这里是尖括号

	int main(int argc, char *argv[]) {
	    display_calories(115.2, 11.3, 0.79);
	    return 0;
	}


step2: 创建hfcal.h头文件保存到项目`./includes`下， 创建hfcal.c

	#include <hfcal.h>

	void display_calories(float weight, float distance, float coeff) {
	    printf("Weight: %3.2f lbs\n", weight);
	    printf("Distance: %3.2f miles\n", distance);
	    printf("Calories burned: %4.2f cal\n", coeff * weight * distance);
	}

	// 头文件只声明

step3:创建hfcal.o目标文件

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top8_7.png)

	gcc -I./includes -c hfcal.c -o hfcal.o


step4:创建创建elliptical.o目标文件

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top8_8.png)

	gcc -I./includes -c elliptical.c -o elliptical.o

step5:创建hfcal存档库，并保存到`./libs`下

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top8_9.png)

	ar -rcs ./libs/libhfcal.a hfcal.o

step6.用elliptical.o和hfcal存档创建elliptical可执行文件：

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top8_10.png)

	gcc elliptical.o -L ./libs -lhfcal -o elliptical


那么整个项目目录如下：

	.
	├── hfcal.c
	├── hfcal.o
	
	├── includes
	│   └── hfcal.h
	
	├── libs
	│   └── libhfcal.a

	├── elliptical
	├── elliptical.c
	├── elliptical.o



# 三.动态链接(热插拔)

上面的都是静态链接，不能修改可执行文件中的目标代码,是因为它们在编译程序时静态链接在了一起。`.a`能不能在运行时动态链接呢？

## 3.1 动态库-加强版目标文件

>动态库和你屡屡创建的`.o`目标文件很像,但又不完全一样。动态库和存档也很像,也可以从多个`.o`目标文件创建。不同的是,这些目标文件在动态库中链接成了一段
目标代码。

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top8_11.png)


### 3.1.1 创建目标文件

在把hfcal.c代码转换为动态库之前需要把它先编译 为.o目标文件,像这样:

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top8_12.png)

发现区别了吗?这次在创建hfcal.o时多加了一个标志:`-fPIC`。它告诉gcc你想创建**位置无关代码(无论加载到存储器中哪个位置都可以运行的代码)**。有的操作系统和处理器要用位置无关代码创建库,这样它们才能在运行时决定把代码加载到存储器的哪
个位置。事实上在大多数操作系统中都不需要加这个选择。 试试吧,不加也没有关系。

### 3.1.2 多平台认知

>绝大部分操作系统都支持动态库,它们的工作方式也大抵相同,但称􏵍却大相径庭。在Windows中,动态库通常叫**动态链接库**,后缀名是`.dll`;在Linux和Unix上,它们叫**共享目标文件**,后缀名`.so`;而在Mac上,它们就叫**动态库**,后缀名`.dylib`。尽管后􏵎名不同,但创建它们的方法相同:

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top8_13.png)


`-shared`选项告诉gcc你想把`.o`目标文件转化为动态库

编译器创建动态库时会把库的名字保存在文件中,假设你在Linux 中创建了一个叫libhfcal.so的库,那么libhfcal.so文件就会记住它的库名叫hfcal。也就是说,**一旦你用某个名字编译了库, 就不能再修改文件名了,这一点很重要。若想重命名库,就必须用新的名字重新编译一次**。


**一旦创建了动态库,你就可以像静态库那样使用它**。可以像这样建立elliptical程序:

	gcc -I/include -c elliptical.c -o elliptical.o
	gcc elliptical.o -L./libs -lhfcal -o elliptical


尽管你使用的命令和静态存档一模一样,但两者编译的方式不同。**因为库是动态的,所以编译器不会在可执行文件中包含库代码,而是插入一段用来查找库的“占位符”代码,并在运行时链接库**。


# 四.动态库Vs静态库

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/C/media/top8_14.png)





