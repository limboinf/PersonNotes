默认情况下，Scala 对象的访问级别都是 public

private 类和对象内部可见

### 作用域

```scala
private[x] 
protected[x]
```



### 方法与函数区别

函数可赋值给一个变量

`val`定义函数、`def` 定义方法

```scala
class Dark {

  def m(x: Int) = x +3
  val f = (x: Int) => x + 3

}
```

方法声明：

```scala
def fName ([参数列表]) : [return type]
```

> 如果你不写等于号和方法主体，那么方法会被隐式声明为**抽象(abstract)**，包含它的类型于是也是一个抽象类型

方法定义：

```scala
def fName ([参数列表]) : [return type] = {
   function body
   return [expr]
}
```

> 如果方法没有返回值，可以返回为 **Unit**，这个类似于 Java 的 **void**,



### 函数

#### 解析函数参数两种方式

- 传值调用（call-by-value）：先计算参数表达式的值，再应用到函数内部；
- 传名调用（call-by-name）：将未计算的参数表达式直接应用到函数内部

#### 可变参数

参数的类型之后放一个星号来设置可变参数，如 `def pp(str: String*)`

#### 默认参数

参数类型指定值，varName: Type=value, 如 `a: Int=10`

#### 偏函数

#### 命名参数

跟Python类似，可以 `fn(b=1, a=2)` 不用按照顺序传递

#### 递归

尾递归

#### 高阶函数

就是操作其他函数的函数，高阶函数可以使用其他函数作为参数，或者使用函数作为输出结果

```scala
// 函数 f 和 值 v 作为参数，而函数 f 又调用了参数 v
def apply(f:Int=>String, v:Int) = f(v)
def layout[T](x: T) = "[" + x.toString + "]"
println(apply(layout, 10))  // [10]
```

#### 匿名函数

> 箭头左边是参数列表，右边是函数体



#### 闭包

> 在函数中引入外部自由变量

```scala
val factor = 3
// 引入一个自由变量 factor，这个变量定义在函数外面
scala> val f = (i:Int) => i * factor
f: Int => Int = <function1>

scala> f(2)
res0: Int = 6
```



### 三、数组

```scala
// java
String[] z = new String[3];
```

java比较显而易见，看下Golang的

```go
package main

import (
	"fmt"
)

// 声明
var goZ [3] string

func main() {
  // 初始化数组
  var b = [3]int{1,2,3}
  // 动态评估大小
  var c = [...]int{1,2,3,4}
  fmt.Printf("%v\n", goZ)  // [  ]
  fmt.Printf("%v\n", b)   // [1 2 3]
  fmt.Printf("%v\n", c)   // [1 2 3 4]
}
```

跟scala类似，Scala是：

```scala
// 声明方式1：
scala> val a: Array[Int] = new Array[Int](3)
a: Array[Int] = Array(0, 0, 0)
// 声明方式2：
scala> val b = new Array[Int](3)
b: Array[Int] = Array(0, 0, 0)
// 取索引是以()来的，不是传统[]
scala> a(0) = 1
scala> b(0) = 100
scala> b
res4: Array[Int] = Array(100, 0, 0)
scala> b(0)
res5: Int = 100
// 直接初始化
scala> val c = Array(100, 0, 0)
c: Array[Int] = Array(100, 0, 0)
```

总感觉有点怪怪的….

scala数组操作：

```scala
// 循环
for ( x <- c) { println(x)}
// 累加
var total = 0
for (i <- 0 to (c.length - 1)) { total += c(i) }

// 合并
import Array._  // 导入依赖
scala> concat(b, c)
res10: Array[Int] = Array(100, 0, 0, 100, 0, 0)

// range, 跟Python类似
scala> range(10, 20, 2)
res11: Array[Int] = Array(10, 12, 14, 16, 18)
```



### 四、Collection

分为:`List`, `Set`, `Map`, `元祖`, `Option`, `Iterator`

可直接定义:

```scala
// 定义整型 List
val x = List(1,2,3,4)

// 定义 Set
val x = Set(1,3,5,7)

// 定义 Map
val x = Map("one" -> 1, "two" -> 2, "three" -> 3)

// 创建两个不同类型元素的元组
val x = (10, "Runoob")

// 定义 Option
val x:Option[Int] = Some(5)
```

#### 4.1 列表

定义：

```scala
scala> val co: List[String] = List("java", "python", "golang", "scala")
co: List[String] = List(java, python, golang, scala)

scala> val coo = List("java", "python", "golang", "scala")
coo: List[String] = List(java, python, golang, scala)

scala> val empty: List[Nothing] = List()
empty: List[Nothing] = List()
```

构造：

>构造列表的两个基本单位是 **Nil** 和 **::**

```scala
scala> val xo = "java" :: ("python" :: ("golang" :: ("scala" :: Nil)))
xo: List[String] = List(java, python, golang, scala)

scala> val xEmpty = Nil
xEmpty: scala.collection.immutable.Nil.type = List()
```

诡异~

scala List合并的方法很灵活，3种

```scala
scala> val ca = "js" :: ("lua" :: Nil)
ca: List[String] = List(js, lua)

// ::: 运算符
scala> val rs = ca ::: co
rs: List[String] = List(js, lua, java, python, golang, scala)
// List.:::() 方法
scala> ca.:::(co)
res15: List[String] = List(java, python, golang, scala, js, lua)
// List.concat() 方法
scala> List.concat(ca, co)
res16: List[String] = List(js, lua, java, python, golang, scala)
```

scala 元素添加，**`:` 要靠近List**

```scala
scala> val x = List(1)
x: List[Int] = List(1)

scala> 2 +: x
res21: List[Int] = List(2, 1)

scala> 3 :: x
res22: List[Int] = List(3, 1)

scala> x +: 2
<console>:16: error: value +: is not a member of Int
       x +: 2
         ^

scala> x :+ 2
res24: List[Int] = List(1, 2)

scala> 2 +: x
res25: List[Int] = List(2, 1)

scala> x :: 2
<console>:16: error: value :: is not a member of Int
       x :: 2
         ^

scala> 2 :: x
res27: List[Int] = List(2, 1)

scala> List(3,2,4) ::: x
res28: List[Int] = List(3, 2, 4, 1)
```



常用方法可参考：<http://www.runoob.com/scala/scala-lists.html>

#### 4.2 Set

分可变和不可变，<http://www.runoob.com/scala/scala-sets.html>

#### 4.3 Map

也分可变与不可变，默认情况下 Scala 使用不可变 Map，使用可变集合，你需要显式的引入 **import scala.collection.mutable.Map** 类

定义：

```scala
// 空Hash表，key Char类型，值Int类型
scala> var A:Map[Char, Int] = Map()
A: Map[Char,Int] = Map()
// += 增加元素
scala> A += ('R' -> 1)
scala> A += ('Y' -> 2)
// 直接定义并初始化, 可变map
scala> val colors = Map("red" -> "R", "yellow" -> "Y")
colors: scala.collection.immutable.Map[String,String] = Map(red -> R, yellow -> Y)
// 默认是不可变map
scala> A
res33: Map[Char,Int] = Map(R -> 1, Y -> 2)
```

<http://www.runoob.com/scala/scala-maps.html>

#### 4.4 元祖

> 与列表一样，元组也是不可变的，但与列表不同的是元组可以包含不同类型的元素

定义

```scala
// 直接初始化
scala> val t = (1, 'L', "hello")
t: (Int, Char, String) = (1,L,hello)

// new Tuple{count}, 注意，数要对上，牛逼不。。。
scala> val tt = new Tuple3(1, 'L', "hello")
tt: (Int, Char, String) = (1,L,hello)
```

访问元组的元素可以通过数字索引, 如 `t._1`访问第一个元素

```scala
scala> t._1
res35: Int = 1

scala> t._2
res36: Char = L
// 报错
scala> t(1)
<console>:16: error: (Int, Char, String) does not take parameters
       t(1)
        ^
```

循环的时候，`for`是不行的，通过`.productIterator.foreach` 方法来循环

```scala
scala> for (x <- t) { println(x)}
<console>:17: error: value foreach is not a member of (Int, Char, String)
       for (x <- t) { println(x)}
                 ^

scala> t.productIterator.foreach{ i => println(i) }
1
L
hello
```

#### 4.5 Option(选项)

表示一个值是可选的（有值或无值)，`Option[T]` 有值则` Some[T] `, 无值`None`

```scala
scala> val map:Map[String, String] = Map("k1" -> "v1")
map: Map[String,String] = Map(k1 -> v1)

scala> val o:Option[String] = map.get("k1")
o: Option[String] = Some(v1)

scala> val x:Option[String] = map.get("k2")
x: Option[String] = None
```

可以通过模式匹配来输出匹配值:

```scala
scala> def show(x:Option[String]) = x match {
     |   case Some(s) => s
     |   case None => "?"
     | }
show: (x: Option[String])String

scala> show(map.get("k2"))
res41: String = ?

scala> show(map.get("k1"))
res42: String = v1
```

或者` getOrElse() `取默认值：

```scala
scala> o.getOrElse("default value")
res43: String = v1
scala> x.getOrElse("default value")
res44: String = default value
```

<http://www.runoob.com/scala/scala-options.html>



### 五、Iterator（迭代器）

跟java一样，迭代器 it 的两个基本操作是 **next** 和 **hasNext**。

```scala
scala> val it = Iterator("Java", "Python", "Golang", "Scala")
it: Iterator[String] = non-empty iterator

scala> while(it.hasNext) { println(it.next()) }
Java
Python
Golang
Scala
```

<http://www.runoob.com/scala/scala-iterators.html>

### 六、OOP

相关概念：

- 类参数