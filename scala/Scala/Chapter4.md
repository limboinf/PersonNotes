## 第四章 处理对象

### 1.创建并使用类

#### 1.1 创建实例

同Java，`new`后面附上类名和它的构造器参数，但如果构造器没有参数，Scala允许在创建实例时省略`()`

```scala
new StringBuilder
```

#### 1.2 创建类

Scala将类定义浓缩在了**主构造器（primary constructor）**上，如下

```scala
/ 类定义没有主体可省略{}
// 具备信息：
//  1.两个字段
//  2.一个构造器
//  3.不可变的number的getter
//  4.一个可变的creditLimit的getter和setter
class CreditCard (val number:Int, var creditLimit:Int)
```

如果Java实现需要：

```java
public class CreditCardJava {

    private final Integer number;
    private Integer creditLimit;

    public CreditCardJava(Integer number, Integer creditLimit) {
        this.number = number;
        this.creditLimit = creditLimit;
    }

    public Integer getNumber() {
        return number;
    }

    public Integer getCreditLimit() {
        return creditLimit;
    }

    public void setCreditLimit(Integer creditLimit) {
        this.creditLimit = creditLimit;
    }

```

可以查看编译器产生的代码

```bash
scalac CreditCard.scala
javap -private CreditCard
```

**Scala会执行主构造器中任意表达式和直接内置在类定义中的可执行语句**

```scala
package chapter4

object Construct extends App {

  // Scala会执行主构造器中任意表达式和直接内置在类定义中的可执行语句
  class Construct(param:String) {
    // 这段代码作为构造器调用的一部分会被执行
    println(s"...$param ...")
  }

  new Construct("Jack")
  // 输出：...Jack ...
}
```

#### 1.3 定义字段，方法和构造器

除了用**主构造器**参数声明的字段，还可以定义其他字段、方法和**辅助构造器（auxiliary constructor）**`this()`方法就是一个辅助构造器

```scala
package chapter4

object Person extends App {

  // 主构造器（primary constructor）接收两个参数
  class Person(val firstName:String, val lastName:String) {

    // Scala会执行主构造器中任意表达式和直接内置在类定义中的可执行语句
    // 类中定义为var的字段将会映射到一个private, 并附带相应的getter和setter方法
    // 用下划线初始化var变量, Scala要求变量在使用前必须初始化
    // 下划线表示相应类型的默认值，所以对于Int来说，是0，而对于Double来说，则是0.0；对于引用类型来说，是null
    // 用val声明的变量就没法使用下划线这种方便的初始化方法了，因为val变量创建后就无法修改了。故必须在初始化的时候就给定一个合理的值
    var position:String = _
    println(s"Creating $toString")



    // this方法是辅助构造器（auxiliary constructor）接收3个参数
    // 方法中不需要val或var
    def this(firstName:String, lastName:String, positionHeld:String) {
      // 调用主构造器来初始化
      // Scala强制规定：辅助构造器的第一行有效语句必须调用主构造器或者其他辅助构造器。
      this(firstName, lastName)
      position = positionHeld
    }

    override def toString: String = {
      s"User: $firstName $lastName live $position"
    }
  }

  val jack = new Person("Jack", "Kook", "Shanghai")
  println(jack)
  val rose = new Person("Rose", "Pink")
  println(rose)
}

// 输出
Creating User: Jack Kook live null
User: Jack Kook live Shanghai
Creating User: Rose Pink live null
User: Rose Pink live null
```

有点不好的是所生成的访问器方法的名字并不遵循JavaBean惯例

### 2.遵循JavaBean惯例

上面提到过，scala生成的不是JavaBean规范，如果要把scala和java混合编程的话，需要遵循javabean

只要在相应的期望字段声明上标记`scala.beans.BeanProperty`注解,scala解释器就会自动处理成JavaBean风格访问器，以及Scala风格的访问器

```scala
import scala.beans.BeanProperty

class Dube(@BeanProperty val firstName:String, val lastName:String) {
    @BeanProperty var position: String = _
}
```

再看下,生成JavaBean风格的访问控制器了

```bash
$ scalac Dude.scala 
$ javap -private Dube                                                             
Compiled from "Dude.scala"
public class Dube {
  private final java.lang.String firstName;
  private final java.lang.String lastName;
  private java.lang.String position;
  public java.lang.String firstName();
  public java.lang.String lastName();	// lastName没加注解
  public java.lang.String position();
  public void position_$eq(java.lang.String);
  public void setPosition(java.lang.String);   // setXXX
  public java.lang.String getFirstName();		// getXXX
  public java.lang.String getPosition();		// getXXX
  public Dube(java.lang.String, java.lang.String);
}
```

### 3.类型别名

用`Cop`来起一个别名

```scala
type Cop = OtherClassBalabala	// 口语化的Cop别名只是在这个文件的作用域有效
val copInst = new Cop(...)  // 传递构造参数
println(copInst.getClass) // class OtherClassBalabala  实例的类型仍旧反映它的真正身份
```

### 4.扩展一个类

- override必须带上
- 在扩展一个类时，必须将派生类的参数传递给基类某个构造器
- 只有主构造器能传递参数给基类的构造

觉得还是有点懵，看下代码吧

```scala
package chapter4

/**
  * 类的继承
  * override关键字必须有，只有主构造器能传递参数给基类的构造器。
  */

object Vehicle extends App {

  class Vehicle(val id:Int, val year:Int) {
    override def toString: String = s"ID:$id, YEAR:$year"
  }

  /**
    * 继承Vehicle，id, year派生自基类，因此需要在类Car的主构造器相应参数前加上override
    * scala编译器看到这个关键字就不会为这两个属性生成字段，而是会将这些属性的访问器方法路由到基类的相应方法
    * extends Vehicle(id, year):
    *   在扩展一个类时，必须将派生类的参数传递给基类的某个构造器。
    *   因为只有主构造器才能调用一个基类的构造器，
    *   所以我们把这个调用直接放在extends声明之后的基类名后面。
    * @param id
    * @param year
    * @param fueLevel
    */
  class Car(override val id:Int, override val year:Int, var fueLevel:Int)
    extends Vehicle(id, year) {
    override def toString: String = s"${super.toString}, FUELEVEL:$fueLevel"
  }

  val car = new Car(1001, 2018, 1)
  println(car)
}
```



### 5.参数化类型

其实就是**泛型**

> 在Java中，尖括号（`<>`）被用于指定泛型。在Scala中我们使用方括号（`[]`）来替代

实例：

```scala
package chapter4

// 参数化类型
object Parameterized extends App {

  // 记号[T]告诉编译器后面提到的类型T 是一个参数化类型。
  def echo[T](a:T, b: T) = {
    println(s"got a: $a, ${a.getClass}, b: $b, ${b.getClass}")
  }

  echo("hello", "world")
  echo(1, 2)
  // 传入的参数是同一种类型的,但是下面这样也行，因为scala所有类型都派生自Any
  echo("hi", 2)
  // 为了防止混用不同参数类型，可以指定T的类型
  // echo[Int]("hi", 2)  会编译失败
  echo[Int](1, 2)

  def echo2[T1, T2](a:T1, b:T2) = {
    println(s"got a: $a, ${a.getClass}, b: $b, ${b.getClass}")
  }

  echo2("hi", 100)
  echo2(1, 2)
  echo2[Int, String](1, "hello")


  class Message[T](val ctx: T) {
    override def toString: String = s"got message: $ctx"
    def is(value: T):Boolean = value == ctx
  }

  // 类型推断
  val msg = new Message("hi")
  println(msg)
  println(msg.is("hi"))

  // 显式指定Message类型的变量
  val msg2: Message[String] = new Message[String]("hello")
  println(msg2)
}
```



### 6.单例对象和伴生对象

#### 6.1单例对象

在scala中实现单例是很容易的，**创建一个单例要使用关键字`object`而不是`class`。因为不能实例化一个单例对象，所以不能传递参数给它的构造器。**

```scala
package chapter4
import scala.collection._


object Singleton extends App {

  class Marker(val color:String) {
    println(s"color: $color")
    override def toString = s"marker color $color"
  }

  object MarkerFactory {
    private val markers = mutable.Map(
      "red" -> new Marker("red"),
      "green" -> new Marker("green"),
      "yellow" -> new Marker("yellow")
    )

    def getMarker(color:String):Marker = {
      markers.getOrElseUpdate(color, new Marker(color))
    }
  }

  println(MarkerFactory getMarker("red"))
  println(MarkerFactory getMarker "red")
  println(MarkerFactory getMarker "green")
  println(MarkerFactory getMarker "green")
  println(MarkerFactory getMarker "blue")
  println(MarkerFactory getMarker "blue")

  /**output:
    * color: red
    * color: green
    * color: yellow
    * marker color red
    * marker color red
    * marker color green
    * marker color green
    * color: blue
    * marker color blue
    * marker color blue
    */
}
```



#### 6.2 独立对象和伴生对象

前面的`MarkerFactory`是一个**独立对象**（stand-alone object），所谓的**伴生对象**（companion object）就是将一个单例关联一个类，对象和类名一致，相应的类被称为**伴生类**

**类与其伴生对象间没有边界——它们可以相互访问私有字段和方法**

如下对上面MarkerFactory的改造成伴生对象

```scala
package chapter4
import scala.collection._

// 伴生对象

object Marker extends App {

  // 主构造器，也可以标记为private,表示私有构造器
  // 但它的伴生对象可以访问它，除此之外，外界访问就会失败
  class Marker private (val color:String) {
    println(s"create color: $this")

    override def toString: String = s"maker color: $color"
  }

  // 伴生对象
  object Marker {
    private val markers = mutable.Map(
      "red" -> new Marker("red"),
      "green" -> new Marker("green"),
      "yellow" -> new Marker("yellow")
    )

    def getMarker(color:String):Marker = {
      markers.getOrElseUpdate(color, new Marker(color))
    }
  }

  println(Marker getMarker("red"))
  println(Marker getMarker "red")
  println(Marker getMarker "green")
  println(Marker getMarker "green")
  println(Marker getMarker "blue")
  println(Marker getMarker "blue")

  /**
    * output:
    * create color: maker color: red
    * create color: maker color: green
    * create color: maker color: yellow
    * maker color: red
    * maker color: red
    * maker color: green
    * maker color: green
    * create color: maker color: blue
    * maker color: blue
    * maker color: blue
    */
}
```



#### 6.3 Scala中的`static`

Scala没有`static`关键字，可以通过伴生对象来实现

```scala
package chapter4

import scala.collection._

object Static extends App {

  class Marker private (val color: String) {
    override def toString: String = s"marker color: $color"
  }

  object Marker {
    private val markers = mutable.Map(
      "red" -> new Marker("red"),
      "green" -> new Marker("green"),
      "yellow" -> new Marker("yellow")
    )

    def supportColors:Iterable[String] = markers.keys
    def apply(color:String):Marker = markers.getOrElseUpdate(color, new Marker(color))
  }

  println(Marker apply "red")
  println(Marker.supportColors)
  println(Marker supportColors)
}
```



### 7.创建枚举类

scala可以直接用java枚举，也可自己创建

**TODO: 还没搞明白**

看下代码：

```scala
// 枚举是一个扩展了Enumeration类的对象
object Currency extends Enumeration {

  // Value在定义中表示枚举的类型
  type Currency = Value
  // val 定义枚举实例
  val CNY, GBP, INR, JPY, NOK, PLN, SEK, US = Value

}
```

```scala
package chapter4

import chapter4.Currency.Currency

object Money extends App {

  // 构造器中接收一个Currency作为一个参数
  // 将val currency: Currency中的单词Currency视作一个实例就讲不通了。它应该被视为一种类型。
  // 现在你就知道type Currency = Value这一行的作用了，它是在告诉编译器将单词Currency视作一个类型而不是一个实例
  class Money(val price:Int, val currency: Currency) {
    println(s"price: $price $currency")
  }

  // 枚举名作为任何一种枚举值的通用引用
  new Money(1000, Currency.US)
  // output: price: 1000 US
}
```



### 8.包对象

|        | java                     | scala                                                        |
| ------ | ------------------------ | ------------------------------------------------------------ |
| 包范围 | 只有接口、类、枚举、注解 | scala除此之外还有变量和函数                                  |
| 使用   | package                  | 它们都被放在一个称为**包对象**（package object）的特殊的**单例对象**中 |
| 定义   | package                  | `package`两种用途：1.定义一个包，2.定义一个包对象            |

scala包对象和Python有点类似

![image-20181115144854354](https://ws4.sinaimg.cn/large/006tNbRwly1fysnjuspffj31s80nm4qq.jpg)

包对象：

![image-20181115144947386](/Users/fangpeng/Library/Application%20Support/typora-user-images/image-20181115144947386.png)

