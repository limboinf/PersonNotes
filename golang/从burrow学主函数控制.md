golang `defer`, `panic`,`recover` 三剑客来进行异常处理和善后工作，一个个的总结下。



## defer

```golang
/ defer是在return调用之后才执行的
// defer代码块的作用域在函数内，可以读取函数内的变量
func deferExm()  (x int) {
	i := 0
	// 规则1：变量被defer声明时就已经确定值了
	defer fmt.Printf("first defer: %d\n", i)
	i++
	// 规则2：defer顺序：先进后出，先定义后执行
	defer fmt.Printf("last defer: %d\n", i)

	// 规则3：可以读取有名返回值
	defer func() { x++; fmt.Printf("value: %d\n", x) } ()
	return i
}
```

## painc

制造恐慌，相当于python `raise`, 如果没有`recover`则会导致程序退出.

## recvover

如果在 defer 中使用了 recover() 函数,则会捕获错误信息

## 应用

在 [burrow](<https://github.com/linkedin/Burrow>) 里，main.go 写的主函数控制写的很好，对于 defer, painc, recover 应用的很好。可以这样写：

```golang
package main

import (
//	"errors"
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"
)

type exitCode struct {
	Code int
}

func handleExit()  {
	if e := recover(); e != nil {
		if exit, ok := e.(exitCode); ok {
			if exit.Code == 0 {
				fmt.Fprintln(os.Stderr, "process failed at ", time.Now().Format("January 2, 2006 at 3:04pm (MST"))
			} else {
				fmt.Fprintln(os.Stderr, "process stop at ", time.Now().Format("January 2, 2006 at 3:04pm (MST"))
			}

			os.Exit(exit.Code)
		}
		panic(e)
	}
}


func main() {

	defer handleExit()

	err := fn()
	if err != nil {
		fmt.Fprintln(os.Stderr, "error ...")
		panic(exitCode{1})
	}

	// Register signal handlers for exiting
	exitChannel := make(chan os.Signal, 1)
	signal.Notify(exitChannel, syscall.SIGINT, syscall.SIGQUIT, syscall.SIGTERM)

	panic(exitCode{core(exitChannel)})

}

// mock error function
func fn()  (err error) {
	// return errors.New("unknown error")
  return nil
}

func core(exitChannel chan os.Signal) int {
	// 核心操作....
	<-exitChannel
	fmt.Println("shutdown triggered")
	// exit cleanly
	return 0
}

```

可以借鉴到自己项目里。

