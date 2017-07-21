## 操作符重载

这一点很有趣，如：

```scala
scala> 3 + 2
res20: Int = 5

scala> 3.+(2)
res21: Int = 5

scala> 1 to (10)
res22: scala.collection.immutable.Range.Inclusive = Range(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

scala> 1.to(10)
res23: scala.collection.immutable.Range.Inclusive = Range(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
```

这里`+`是操作符，但是也是方法名，Scala的方法可以这样：`a 方法 b` 或 `a.方法(b)`, 很奇葩吧。


## 方法和函数

比如导入math方法：

```scala
import scala.math._  // _字符是通配符，等于 *
sqrt(2)
```

不带参数的方法在调用时不需要`()`, 如：

```scala
// 获取不重复的字符
scala> "hello".distinct
res25: String = helo
```

**apply方法**

在python中可以`"hello"[1] = e` 来获取元素，在scala中则`[]`变成了`()`

```scala
scala> "hello"(1)
res27: Char = e
```

可以把`()`视为重载了，其实原理是`apply`方法（上面是简写行为）

```scala
scala> "hello".apply(1)
res28: Char = e
```




