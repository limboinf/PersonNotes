Go的接口对于新手来说不好掌握，特别是从Python转过来的。。雨痕的《GO语言学习笔记》对接口的描述有点少，不尽兴，所以这里网上找了些资源，加上最近遇到的问题，做个笔记。

# 一. 定义

**接口定义了方法集，但是不包含实现，所以是抽象!!!。注意，接口里不能包含变量!**

接口定义：

```go
type Namer interface {
    Method1(param_list) return_type
    ....
}
```

按照约定：**接口名最好+er**, 这样表示更加清晰些, 比如标准库的io 包里有一个接口类型 Reader:

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}
```

定义变量 `r：var r io.Reader`

那么就可以写如下的代码：

```go
var r io.Reader
r = os.Stdin
r = bufio.NewReader(r)
r = new(bytes.Buffer)
f,_ := os.Open("test.txt")
r = bufio.NewReader(f)
```

上面 r 右边的类型都实现了 Read() 方法，并且有相同的方法签名，r 的静态类型是 io.Reader。

接口可以嵌套，如：io标准库的：

```go
type Reader interface {
	Read(p []byte) (n int, err error)
}
type Writer interface {
	Write(p []byte) (n int, err error)
}
type Closer interface {
	Close() error
}
// 接口嵌套
type ReadWriteCloser interface {
	Reader
	Writer
	Closer
}
```

# 二.类型断言

就是检测和转换接口变量的类型。因为接口类型变量可以接受任何值，而且是动态的，所以要在运行时确定其存储值的实际类型。

声明一个`interface{}`空接口，可接收任何类型。例如：

- 万能切片 `[]interface{}`
- 任意Map `map[string]interface{}`



```go
v := varI.(T)  // varI 为接口类型变量， T为类型
```

上面可能会有运行时错误，所以更安全的做法是：`ok-idiom`

```go
if v, ok := varI.(T); ok {  // checked type assertion
    Process(v)
    return
}
// varI is not of type T
```

下面说说我最近遇到的问题，在使用go-redis这个库时，准备在Redis里Load并运行Lua脚本，Lua脚本返回值如下:`return {ID, errMsg, true}`, 我的程序处理逻辑如下：

```go
rd := GetRedis()
shaCode, err := rd.ScriptLoad(luaScript).Result()
if err !=nil {
	fmt.Println("error")
}
fmt.Println(shaCode)
res := rd.EvalSha(shaCode, []string{"a", "b"})
ts, err := res.Result()
fmt.Println(ts)
fmt.Println(reflect.TypeOf(ts), reflect.ValueOf(ts).Kind())
```

打印如下：

```bash
$ go run test.go
ping redis ok: PONG
c2dff896914584a26324802968a848e8f2cb1025
[ can not lpop a and b <nil>]
[]interface {} slice
```

可见程序正常的，返回三个值，空字符串，错误信息和nil。且ts是接口类型，接下来要解析interface, 正确的处理方式如下：

```go
// 这里在我们清楚ts类型的情况下
values := ts.([]interface{})
for i := range values {
	fmt.Println(values[i])
}
```

[如下示例](https://stackoverflow.com/questions/24453420/how-to-convert-interface-to-int)：

```go
a := []interface{}{1, "2", 3, 4, 5}
for i, value := range a {
   switch typedValue := value.(type) {
   case int:
       fmt.Println("int", i, value, typedValue)
       break
   case string:
       fmt.Println("string", value, typedValue)
       break
   default:
       fmt.Println("Not an int: ", value)
   }
}

// convert interface{} to []int?
a := []interface{}{1, 2, 3, 4, 5}
b := make([]int, len(a))
for i := range a {
   b[i] = a[i].(int)
}
fmt.Println(a, b)
```



**测试一个值是否实现了某个接口:**

```go
// 假定 v 是一个值，然后我们想测试它是否实现了 Stringer 接口，可以这样做：
type Stringer interface {
    String() string
}

if sv, ok := v.(Stringer); ok {
    fmt.Printf("v implements String(): %s\n", sv.String()) // note: sv, not v
}
```

# 三.空接口

这篇文章写得不错：https://www.kancloud.cn/kancloud/the-way-to-go/72528




