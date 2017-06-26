# 一. Base

- go 通过`package <packageName>`(像py模块)来组织代码
- package 为 main表示主包(入口, 一个可独立运行的包),编译后会产生可执行文件
- 其他package编译后都会生成`*.a`文件（也就是包文件)在pkg下
- go utf-8编码比Py省事多了..

# 二. 变量与常量

- `var` 定义变量, `const` 定义常量
- 定义的变量和常量必须要用
- 多个变量逗号隔开
- 变量类型在变量名后
- `:=` 可省略`var`和变量类型
- `:=` 仅能用在函数内部

# 三. 类型

- rune是int32别称，byte是uint8别称。
- go的字符串是不可变的，修改则出错

go字符串不可修改， 但是**可以转成数组来修改**，如下：

```go
s := "测试"
c := []rune(s)
c[0] = 'A'
s2 := string(c)
fmt.Println(s2, s)
```

通过 "`" 来声明多行字符串（Raw），原样输出：

## 数组

- 数组长度不能改变
- 数组做参数传入时是传递副本，而不是指针，如果用指针则用切片
- 省略长度而采用`...`的方式

![](http://beginman.qiniudn.com/2017-06-23-14982320484468.jpg)


## 切片

slice 不是动态意义的数组，而是一个引用，底层有个Array.

![](http://beginman.qiniudn.com/2017-06-23-14982273650679.jpg)

**slice 不需要长度**

```go
Array_a := []byte{'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'}
Slice_a := Array_a[2:5]
```

slice包含三个元素：

- 一个指针，指向数组中slice指定的开始位置
- len: 长度，即slice的长度
- cap: 最大长度，也就是slice开始位置到数组的最后位置的长度

![](https://github.com/astaxie/build-web-application-with-golang/raw/master/zh/images/2.2.slice2.png?raw=true)

## map

>map和其他基本型别不同，它不是thread-safe，在多个go-routine存取时，必须使用mutex lock机制

## new and make

[书上讲解很NB了](https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/02.2.md#makenew操作)

![](http://beginman.qiniudn.com/2017-06-23-14982318596989.jpg)

# 四.流程控制

## if

- go的if不需要括号
- 条件判断语句里可声明变量，且作用域仅此if内

```go
if x:= xxx; x > 10 {
    // ...
}
```

## for

- 用for代替while

```go
for exp1; exp2; exp3 {}
```

如下打印99乘法口诀：

```go
for i:=1; i < 10; i++ {
	for j:=1; j <=i; j++ {
		fmt.Printf("%d*%d=%d ", j,i, i*j)
	}
	fmt.Println()
}
```

对于for循环的多个赋值要注意：

```go
// 多个赋值操作没法 i++, j++
// 由于Go里面没有,操作符，可使用平行赋值 i, j = i+1, j-1
for i, j:=1,2; i+j < 10; i, j=i+1, j+1 {
	fmt.Println(i, j, i * j)
}
```

for 实现while挺简单的：

```go
sum := 1
for sum < 5 {
	fmt.Println(sum)
	sum++
}
```

## switch

说实话很久没有用过switch了，写Python没见过这玩意。。

语法:

```go
switch sExpr {
case expr1:
    ....
....
default:
    ...
}
```

**注意：**

- sExpr和expr1、expr2、expr3的类型必须一致
- 每个case默认最后带有break， 匹配成功则跳出整个switch
- 可以使用fallthrough强制执行后面的case代码。

```go
i := 10
switch i {
case 1:
	fmt.Println("1..")
case 2,3,4:				// 带多个表达式
	fmt.Println("1,2,3")
	fallthrough		// 强制执行后续而非跳出， 竟然不能用 {} 括起来!!??
case 5:
	{
		fmt.Println("5")
		fmt.Println("多行用{}也可省略...")
	}
default:
	fmt.Println("艹!!")
	fmt.Println("default!")
}
```

# 五. 函数

变参：`func myfunc(arg ...int) {}`, 参数的类型全部是int, 在函数体内 arg是int类型切片。

```go
func myFunc(arg ...int)  {
	for _, n := range arg {
		fmt.Print(n)
	}
}
```

go的传参都是copy操作，不同的是copy值和copy引用(指针), `channel`，`slice`，`map`这三种类型的实现机制类似指针，所以可以直接传递，而不用取地址后传递指针。（注：若函数需改变slice的长度，则仍需要取地址传递指针）

```go
// fc 的类型为：func(string)
fc := func(msg string) {
	fmt.Println("Msg: ", msg)
}
fc("Java")

// 匿名函数直接执行
func(msg string) {
	fmt.Println("Msg: ", msg)
}("Python")
```

## 函数做参数和返回值

```go
package main

import (
	"fmt"
	"strconv"
)

// 定义一个saveLog函数类型
type saveLog func(msg string)

// 定义具体实现(接口)
func Log(msg string)  {
	fmt.Println("err: ", msg)
}

func stringToInt(s string, log saveLog) int64 {
	if value, err := strconv.ParseInt(s, 0, 0); err != nil {
		log(err.Error())
		return 0
	} else {
		return value		// 必须在 if .. else 块里
	}
}

func main()  {
	stringToInt("123", Log)
	stringToInt("s", Log)
}
```


## defer

- 在defer后指定的函数会在函数退出前调用。
- 这些defer语句会按照逆序执行
- 常用关闭资源等清理性工作

```go
// 会打印54321
for i:=1; i <= 5; i++ {
	defer fmt.Println(i)
}
```

## Painc 和 Recover

TODO


