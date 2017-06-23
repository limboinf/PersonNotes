go三个重要环境变量：

- $GOPATH： 项目路径，可允许多个，Unix用`:`风格，Win:`;`
- $GOBIN: 打包的可执行文件
- $GOROOT：go root

比较坑的一点是当有多个GOPATH,则go get的内容放在第一个目录下。GOPATH目录结构如下：

```bash
$ cd $GOPATH
$ tree -d -L 1
.
├── pkg      --> 编译生成的文件
└── src      --> 存放源码
└── main.go  --> 项目代码..
```

分别看下吧：

```bash
$ cd src && ls
github.com      golang.org

$ cd pkg && ls
darwin_amd64

$ cd $GOBIN && ll
total 91224
-rwxr-xr-x  1 me  staff   2624176 May 22  2016 ds   # 可执行文件直接可运行
```

# 目录结构

在src下新建**应用包**,然后编译安装：

```bash
$ cd $GOPATH/src && tree -d -L 1
.
├── github.com
├── golang.org
└── ponn        # 新建一个名为 ponn的应用包(相对于py库)
```

在ponn应用包目录下新建luck.go文件


```go
package ponn      // 应用包名要与目录名保持一致

import "fmt"

func Luck() {
    fmt.Println("Lucky ..... ")
}
```

编译应用：

两种方式：

1. 进入应用包目录，`go install`
2. 任意目录 `go install ponn`

查看下编译的文件：

```bash
$ cd $GOPATH/pkg/darwin_amd64 && ls
github.com      ponn.a
```

最后新建一个名为myponn的应用包，里面新建一个main.go的可执行应用来调用 ponn。

```bash
$ cd $GOPATH/src && tree -d -L 1
.
├── github.com
├── golang.org
├── myponn
└── ponn
```

代码如下：

```go
package main
import "ponn"

func main() {
    ponn.Luck()
}
```

好了，在打包安装成可执行文件把：

```bash
$ go install myponn
$ myponn
Lucky .....
```

# go get 

> go get本质上可以理解为首先第一步是通过源码工具clone代码到src下面，然后执行go install

```bash
$GOPATH
  src
   |--github.com
		  |-astaxie
			  |-beedb
   pkg
	|--相应平台
		 |-github.com
			   |--astaxie
					|beedb.a
```



