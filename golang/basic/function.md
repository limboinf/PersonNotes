## Summary

3 种函数:

- 具名函数
- 匿名(or lambda) 函数
- 方法

什么是函数签名？参数+返回值+类型

go没有函数重载

## 参数传递

按值传递（call by value） 按引用传递（call by reference）

默认call by value, 也就是传递参数副本，对参数副本变量的修改不会影响原变量，如果需要修改则传递参数地址(`&variable`), 此时是call by reference, 传递的是指针。

> 在函数调用时，像切片（slice）、字典（map）、接口（interface）、通道（channel）这样的引用类型都是默认使用引用传递（即使没有显示的指出指针）

## 传递变长参数

- golang: `…type`, 如 `fn(a, b, args ...int)`
- python: `*args`, 如 `fn(a, b, *args)`
- java: `type…` 如 `fn(String a, String b, String... args)`
- scala: `type*`, 如 `(args Int*)`

各自代表：

- golang: 变长参数作为slice
- python: 变长参数作为tuple
- Java： 变长参数作为数组
- scala: 数组，如Array[Int]

example:

```golang
arr := []int{1,23,4,22,3}
Min(arr...)
// define Min
// func Min(a ...int) int {....}
```

## 函数一等公民

函数是一等公民思想，函数可作为参数，也可作为返回值。

函数作为参数时，不需要带参数名，如strings.IndexFunc

```go
// 返回 s 中第一个满足 f(rune) 的字符的字节位置
// 如果没有满足 f(rune) 的字符，则返回 -1
func IndexFunc(s string, f func(rune) bool) int { .... }
```

实例：

```go
func isSlash(r rune) bool {
	return r == '\\' || r == '/'
}

func main() {
	s := "/opt/data"
	i := strings.IndexFunc(s, isSlash)
	fmt.Printf("%v\n", i)
}
```

如作为返回值：

```go
func Adder(a int) (func(b int) int)
```

实例：

```go
func main() {
	fmt.Println(Adder(1)(2))
}

func Adder(a int) func (b int) int  {
	return func(b int) int {
		return a + b
	}
}
```

从中能够看到闭包的影子

## 匿名函数

两种调用方式：

1. 赋给某个变量，然后调用
2. 直接调用

```go
// 方式1
f := func(x, y int) int { return x + y }
f(1, 2)
// 方式2
func(x, y int) int {return x + y} (1, 2)
```

