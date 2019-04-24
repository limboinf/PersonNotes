## 第三章：从Java到Scala

![第三章：从Java到Scala](https://ws2.sinaimg.cn/large/006tNbRwly1fx6pyhnipbj31240j0q5e.jpg)

## 1.Scala简洁的java

### 1.1 for loop

```scala
for ( i <- 1 to 3) { print(s"$i") }
```

`to` 方法的使用，如 1到3，`1 to 3`

```scala
scala> print(1 to 3)
Range(1, 2, 3)
```

for: `i <- 生成器表达式 `, 其中箭头左边`<-` 定义了一个`val`, 右边是一个生成器表达式，每次迭代都会创建一个新的`val`

### 1.2 until vs to

`to`生成的区间包括上下界，`until`不包括上届

```scala
scala> 1 until 3
res6: scala.collection.immutable.Range = Range(1, 2)

scala> 1 to 3
res7: scala.collection.immutable.Range.Inclusive = Range(1, 2, 3)

scala> 1.to(3)
res8: scala.collection.immutable.Range.Inclusive = Range(1, 2, 3)
```

`to`和`until`都是`RichInt`的**方法**，如上Int类型变量被隐式转换为RichInt, 然后调用该变量的方法，返回`Range`实例`1 to 3` 等价于`1.to(3)`

>在Scala中，如果方法没有参数，或者只有一个参数，就可以省略点号（`.`）和括号。如果一个方法带多个参数，则必须使用括号，但点号仍然是可选的
>
>a + b其实是a.+(b)，而1 to 3其实是1.to(3)

```scala
scala> 1+2
res11: Int = 3

scala> 1.+(2)
res12: Int = 3
```



### 1.3 val vs var

- `val`定义的变量是不可变的，即初始化后不能更改。
- `var`定义（不推荐使用）的变量是可变的，可以被改任意次。



**不可变性**（immutability）**是作用在变量上，而不是作用在变量所引用的实例上的**

```scala
scala> val buffer = new StringBuffer()
buffer: StringBuffer =

scala> buffer.append("hello")
res15: StringBuffer = hello

// 可以使用StringBuffer的方法（如append()方法）来修改所引用的实例
scala> buffer.append(" scala")
res16: StringBuffer = hello scala

// 不能改变buffer的引用
scala> buffer = 3
<console>:12: error: reassignment to val
       buffer = 3
              ^
```

**故而，对于一个只有`val`引用的对象，不能假定它是完全不可变的**

在Scala中，应尽可能多地使用`val`，因为它可以提升不可变性，从而减少错误，也可以增益函数式风格。

## 2.Java原始类型对应的Scala类

java 非all oop，如基础类型和对象就截然不同，java **利用自动装箱(autoboxing)机制，可以将原始类型视为对象**，然后，Java原始类型不允许方法调用，如`2.toString()`是不行的，另外自动装箱还涉及类型转换的开销也会带来一些影响。

和Java不同，**Scala将所有的类型都视为对象**。这就意味着，和调用对象上的方法一样，也可以在字面量上进行方法调用。

## 3.元组和多重赋值

**多重赋值**（multiple assignment）

**元组**是一个不可变的对象序列，创建时使用逗号分隔，如("a", "b", "c") 3个对象元祖

如下例子：

```scala
// 返回值类型也可省略
scala> def sample(pk:Int): (String, String, String) = {
     | ("Java", "Python", "Golang")
     | }
sample: (pk: Int)(String, String, String)

// 可通过val, var赋给多个变量
scala> val (java, py, go) = sample(1000)
java: String = Java
py: String = Python
go: String = Golang

scala> def sample2(pk:Int) = { ("Java", "Scala") }
sample2: (pk: Int)(String, String)

scala> val info = sample2(1)
info: (String, String) = (Java,Scala)

// 通过下划线加数字这种模式，按索引访问
// 与集合不同，访问元组的索引是从1开始的
scala> info._1
res19: String = Java

scala> info._2
res20: String = Scala

// 也可用_占位符忽略其他变量
scala> val (_, _, need) = sample(1000)
need: String = Golang
```

**元祖作用：**

- 多重赋值
- 并发编程时，用在Actor之间消息传递

## 4.参数和参数值

### 4.1 变长参数

可接受0，1或多个参数，跟Python类似，如果有多个参数，只允许最后一个参数可变长，在最后一个参数类型后面加上星号即可

```scala
scala> def pprint(values:String*) = print(values)
pprint: (values: String*)Unit

scala> pprint()
List()
scala> pprint("hello", "scala", "!")
WrappedArray(hello, scala, !)

// 求最大值
scala> def max(values: Int*) = values.foldLeft(values(0)) { Math.max }
max: (values: Int*)Int
scala> max(1,20,3,4)
res22: Int = 20
```

**当参数的类型使用一个尾随的星号声明时，Scala会将参数定义成该类型的数组。**如

```scala
// WrappedArray$ofRef 引用类型
scala> def pprint(values:String*) = println(values.getClass)
pprint: (values: String*)Unit

scala> pprint("hello", "scala", "!")
class scala.collection.mutable.WrappedArray$ofRef

// WrappedArray$ofInt
scala> def pprint(values:Int*) = println(values.getClass)
pprint: (values: Int*)Unit

scala> pprint(10, 2, 1)
class scala.collection.mutable.WrappedArray$ofInt
```

**如果可变参数传递数组则需要解压成字面上的数组类型，而不是传整个数组**，在Python里可以`max(*array)`来使用，但是在scala中要`max(array: _*)`, 这就是**数组展开标记（array explode notation）**

```scala
scala> val numbers = Array(2, 20,1,100,4)
numbers: Array[Int] = Array(2, 20, 1, 100, 4)

scala> max(numbers: _*)
res27: Int = 100
```

### 4.2 参数默认值

在Python中支持，在Java中需要用重载方法的方式省略一个或者多个参数来实现，在Scala中很容易

定义 `变量名: 类型=默认值`, 如 `title: String = "hello"`

```scala
//默认参数在前
scala> def mail(title: String="defual value", addr: String): Unit = println(s"send $addr<$title>")
mail: (title: String, addr: String)Unit
// 必须一一对应上,否则报错
scala> mail("limbo@gamil.com")
<console>:13: error: not enough arguments for method mail: (title: String, addr: String)Unit.
Unspecified value parameter addr.
       mail("limbo@gamil.com")
           ^

scala> mail("hello", "limbo@gamil.com")
send limbo@gamil.com<hello>

// 默认参数在后
scala> def mail(addr: String, title: String="defual value"): Unit = println(s"send $addr<$title>")
mail: (addr: String, title: String)Unit

scala> mail("limbo@gmail.com")
send limbo@gmail.com<defual value>
```

### 4.3 命名参数

同Python，**对参数命名更富有表现力，也不用管参数顺序了**,如上

```scala
scala> mail(addr="limbo@gamil.com", title="hi limbo")
send limbo@gamil.com<hi limbo>
```

### 4.4 隐式参数

关于赋默认值的两种方式：

1. 默认参数是由函数的创建者决定
2. 隐式参数由调用者来决定所传递的默认值

感觉`implicit`这个标记还是不太好理解，先看代码吧：

```scala
package chapter3

object ImplicitParameters extends App {

  class Wifi(name: String) {
    override def toString: String = name
  }

  // 函数定义者首先需要把参数标记为implicit，那么就像有默认值的参数了，该参数的值传递是可选的
  // 如果没有传值，Scala会在调用的作用域中寻找一个隐式变量，这个隐式变量必须和相应的隐式参数具有相同的类型
  // connectToNewWork 拥有两个参数列表，一个String常规参数，一个Wifi的隐式参数
  // 需要把隐式参数放在一个单独的参数列表而非常规参数列表中
  def connectToNewWork(user: String)(implicit wifi: Wifi): Unit = {
    println(s"User: $user connected to WIFI $wifi")
  }

  def atOffice(): Unit = {
    // implicit标记的Wifi实例
    implicit def officeNetWork = new Wifi("office-network")
    // 普通Wifi实例
    val cafeteriaNetwork = new Wifi("cafe-connect")

    // 为隐式参数wifi提供值
    connectToNewWork("guest")(cafeteriaNetwork)

    // 显式指定一个隐式定义的参数
    connectToNewWork("Jack")(officeNetWork)

    // 使用默认值，这里因为参数wifi是隐式函数，所以编译器在函数调用的作用域中寻找定义为implicit的值
    // 该函数定义中只有officeNetWork设置了implicit,所以编译器就选它了
    connectToNewWork("Joe Hacker")
  }

  atOffice()
}

```

**如果定义了一个隐式参数，那么调用者应该传递一个参数值给它，或者在作用域中已经有一个隐式参数的情况下就可以省去；否则编译器就会报错。**

## 5.字符串

### 5.1 多行字符串

- Scala 字符串就是java.lang.String, 可自动转换为`scala.runtime.RichString`
- `""" """`多行字符串，原样输出(包括空格，制表符等)，称为**原始字符串**
- `RichString`的`stripMargin`方法可以去除起始空格
- `stripMargin()`方法将起始的管道符号（`|`）前面的空白或者控制字符都去掉了

```scala
val str = """Hello
               scala
        world..."""

  println(str)

  var str2 =  """Hello
        |scala
        |world...""".stripMargin
  println(str2)
```



### 5.2 字符串插值

- `s`在双引号前，意思是s**插值器**（s-interpolator）
- f**插值器**（f-interpolator）做格式化
- 表达式的值会在插值的时候被捕获，变量的任何更改都不会影响或者改变字符串

```scala
scala> var price = 100
price: Int = 100

scala> val msg = s"got ${price * 100}"
msg: String = got 10000

// 转义
scala> val msg = s"got $$${price * 100}"
msg: String = got $10000

scala > price = 0
scala > println(msg)
got $10000

// f插值
scala> val price = 100.1234
price: Double = 100.1234

scala> val msg = f"got $$${price}%2.2f"
msg: String = got $100.12
```

### 6 运算符重载

**scala没有操作符**，+,-等属于方法，"操作符" 利用scala可忽略`.` 就用了运算符重载的幻觉（很诧异吧..)

没有操作符，那么处理这些操作符的优先级怎么搞呢？**Scala没有在操作符上定义优先级，但是它在方法上定义了优先级。**

**方法的第一个字符用来决定它们的优先级**。如果在一个表达式中两个字符的优先级相同，那么在左边的方法优先级更高。下面是第一个字母的优先级从低到高的列表：

![image-20181113193538388](https://ws1.sinaimg.cn/large/006tNbRwly1fx6o0ft4zrj30bh077aa6.jpg)

如下实例：

![image-20181113193739341](https://ws4.sinaimg.cn/large/006tNbRwly1fx6o2krfk2j30qe0tc7wh.jpg)



## 6.Scala与Java的差异

### 6.1 赋值

scala没有java或Python的 a=b=c的赋值操作,这是因为scala中赋值操作的结果值是一个`Unit`（等价`Void`)，从结果上讲，将这种值赋值给另外一个变量有可能造成类型不匹配

```scala
scala> var a = 1
a: Int = 1

scala> var b = 2
b: Int = 2

// 这样会报错
scala> a = b = 3
<console>:13: error: type mismatch;
 found   : Unit
 required: Int
       a = b = 3
             ^
// 只能这样了，确实不方便
scala> b = 3
b: Int = 3

scala> a = b
a: Int = 3

scala> a
res36: Int = 3
```

### 6.2 ==

java `==`比较**混乱**，如果基本类型则是值的比较，如果是对象，判断两者引用是否指向同一实例（是否同一身份），使用`equals()`提供对象间基于值的比较

**而scala的`==`对所有类型都一致，表示基于值的比较**；如果基于引用比较则使用`eq()`方法

```scala
scala> val str1 = "hello"  // 字面值
scala> val str2 = "hello"
scala> val str3 = new String("hello")

// 等价Java的 str1.equals(str2)
scala> str1 == str2
res37: Boolean = true
scala> str1 == str3
res38: Boolean = true

// 等价Java的 str1 == str2
scala> str1 eq str2
res39: Boolean = true
scala> str1 eq str3
res40: Boolean = false

```

## 7.默认访问修饰符



|                | scala                            | java             |
| -------------- | -------------------------------- | ---------------- |
| 默认访问修饰符 | 默认认为类、字段和方法都是公开的 | 默认为包内部可见 |
| 粒度           | 粗粒度                           | 细粒度           |
| protected      | 派生类和当前包中任意类可访问     | 只有派生类能访问 |

`private`标记私有

