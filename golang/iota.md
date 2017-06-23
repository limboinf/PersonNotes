在看go-colortext这个项目时，一个`iota`关键字很有意思。如下分析：

```go
package main

import "fmt"

type Color int

// 自增长变量包含一个自定义类型
const (
	// No change of color
	None = Color(iota)
	Black
	_
	_		// _ to skip value
	Red
	Green
	Yellow
	Blue
	Magenta
	Cyan
	White
)

// Can't set (i int)
func getColor(i Color) string {
	var s string
	switch i {
	case Black:
		s = "black"
	case Green:
		s = "green"
	default:
		s = "unknown"
	}
	return s
}

func main()  {
	fmt.Println(getColor(5))           // green
	fmt.Println(getColor(Green))       // green
}
```

或者：

```go
const (
	A, B = iota +1, iota +2
	C,D
	E=iota
	//F error
)
```

`iota` 只能在下一行自增。




