Scala(Scalable Language)是一门简洁的高级编程语言，同时结合了面向对象编程（OOP）和函数式编程（FP）两种编程范式

**语言风格：**

>Scala本质上是一门混合型编程语言，我们既可以使用命令式风格也可以使用函数式风格，这是把双刃剑。其优点在于，当使用Scala编写代码时，我们可以先使其工作，然后再做优化。

![image-20181113123040642](https://ws2.sinaimg.cn/large/006tNbRwly1fx6bq93ongj319a0ui792.jpg)

版本：Welcome to Scala 2.12.6 (Java HotSpot(TM) 64-Bit Server VM, Java 1.8.0_172).

[第一段代码](https://github.com/ReactivePlatform/Pragmatic-Scala/blob/7578df39f14af413ffaadf900efbc1957306f8b4/src/main/scala/chapter1/TopStock.scala)图例

![image-20181113112717764](https://ws2.sinaimg.cn/large/006tNbRwly1fx69wjr7rvj30hp079wfr.jpg)

第二段代码求列表最大值图例

- [FindMax.java](https://github.com/ReactivePlatform/Pragmatic-Scala/blob/7578df39f14af413ffaadf900efbc1957306f8b4/src/main/scala/chapter1/FindMax.java)
- [FindMaxImperative.scala](https://github.com/ReactivePlatform/Pragmatic-Scala/blob/7578df39f14af413ffaadf900efbc1957306f8b4/src/main/scala/chapter1/FindMaxImperative.scala)
- [FindMaxFunctional.scala](https://github.com/ReactivePlatform/Pragmatic-Scala/blob/7578df39f14af413ffaadf900efbc1957306f8b4/src/main/scala/chapter1/FindMaxFunctional.scala)

```scala
// 函数式编程
package chapter1

object FindMaxFunctional extends App {

  // = {}, 返回值类型推断
  def findMax(list: List[Int]) = {
    // 集合的foldLeft() 方法在集合的每一个元素上应用Math.max()
    list.foldLeft(Integer.MIN_VALUE) {Math.max}
  }

  println(findMax(List(23, 27, 17)))
}

```



![image-20181113120625922](https://ws2.sinaimg.cn/large/006tNbRwly1fx6b10l3j8j30j20803zd.jpg)

第三段代码：**函数是一等公民，可作为参数或返回值**

```scala
// val 不可变(immutable)
val values = List(1,2,3,4,5)

// _ * 2是个匿名函数
// 下划线 _ 表示传递给此函数的参数，该匿名函数本身作为参数传给了map()函数
// map函数遍历集合，把集合中每一个元素做为参数值来调用匿名函数
val doubleValues = values.map(_ * 2)
```

