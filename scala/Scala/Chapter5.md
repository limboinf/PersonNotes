## 第五章：善用类型

### 1.类型推断

跟Golang一样，变量定义都是 **变量名在前，类型在后**

```golang
// golang
var path String
```

java 都是：`String path` 这样的，scala：

```scala
val path:String = "hello"
```

在Java中是先指定变量的类型，然后是变量名，而在Scala中，恰好做了相反的操作,**为什么这样做**：

- scala暗示 变量名比标注类型更加重要
- 类型信息是可选的

**推荐使用类型推断**，这样会更加简洁：`val path = "hello"`

**在以下几种情况下，必须要显式地指定类型：**

- 当定义没有初始值的类字段时；

- 当定义函数或方法的参数时；

- 当定义函数或方法的返回类型，仅当我们使用显式的`return`语句或者使用递归时[[1\]](https://www.epubit.com/epubit/publish/reader.jsp?type=online&bookId=059C3998-CF66-487E-88C9-AE3EF6D6620E#anchor51)；

- 当将变量定义为另一种类型，而不是被直接推断出的类型时，如`val frequency: Double = 1`



针对泛型和集合的类型推断

```scala
package chapter5

import java._

object DefiningVariableWithType extends App {
  // Java ArrayList类型
  var list1:util.List[Int] = new util.ArrayList[Int]()
  var list2 = new util.ArrayList[Int]()
  var list3 = new util.ArrayList

  // print: class java.util.ArrayList
  println(list1.getClass)

  // OK
  list1 = list2

  // error, list3 as ArrayList[Nothing]
  // list2 = list3

}
```

**在Scala中，`Nothing`是所有类型的子类型**。通过将`new ArrayList`的结果看作是一个`ArrayList[Nothing]`的实例

`Any`是所有类型的基础类型



>Scala认为，没有指定参数化类型的集合是元素类型为`Nothing`的集合，并限制了跨类型的赋值。

如下：

```scala
  var list1 = new util.ArrayList[Int]()
  var list2 = new util.ArrayList[Any]()

  var ref1:Int = 1
  var ref2:Any = _

  // 把ref2赋值给ref1编译错误
  // ref1 = ref2

  // 把ref1赋值给ref2编译通过
  // 等效于在Java中将一个指向Integer的引用赋值给一个类型为Object的引用
  ref2 = ref1

  // 然而在默认的情况下，Scala不允许将一个元素类型为任意类型的集合赋值给一个指向元素类型为Any的集合的引用
  // 如list1赋值list2就会失败
  // 把list2赋值给list1编译失败, 把list1赋值给list2也会编译失败
  //list1 = list2
  //list2 = list1
```

### 2.基础类型

将学到：

1. `Any`类型
2. `Nothing`类型
3. `Option`类型
4. `Either`类型

#### 2.1 Any类型

![image-20181121144721076](https://ws2.sinaimg.cn/large/006tNbRwly1fxfomv37apj31a20hg75z.jpg)

Any:

- 是所有类型的超类型
- 可以作为任意类型对象的一个通用引用
- 是一个抽象类
- 直接后裔是`AnyVal`和`AnyRef`类型

#### 2.2 Nothing类型

书中讲的Nothing，确实没有领会到具体用处，貌似是**一个纯粹的辅助类型，用于类型推断以及类型验证**

![image-20181121150722117](https://ws3.sinaimg.cn/large/006tNbRwly1fxfp7olgu1j31f40dqqhh.jpg)

> `Any`类型是所有类型的父类型，而`Nothing`则是一切类型的子类型。

#### 2.3 Option类型

>当一个函数调用的结果可能存在也可能不存在时，`Option`类型很有用

`Option`类型可以让你更好的避免Null带来的影响，如空指针

```scala
def demo(input:String) = {
    if (input == "test") Some("good") else None
  }

for(input <- Set("test", "good")) {
    val v = demo(input)
    val vv = v.getOrElse("None....")
    println(vv)
}
```

上面方法返回的是`Some[T]`的实例或者`None`，而不是`String`的实例。这两个类都继承自`Option[T]`类。接受`Option[T]`实例的代码将会获取结果，并明确地预期结果可能并不存在（`getOrElse()`）来更好的处理

如果在Java中我们可能就(if xx == null) 来做一大堆限制，否则就`NullPointerException`了

#### 2.4 Either类型

用于从一个函数中返回两种不同类型的值之一，Either类型有两种值：

- Left：错误的
- Right：期望的

```scala
scala> def compute(input:Int) = { if(input > 0) Right(input * 2) else Left("invalid input") }
compute: (input: Int)Product with Serializable with scala.util.Either[String,Int]
```

>当接收到一个`Either`类型的值时，可以使用模式匹配来提取其中的值

```scala
def show(result:Either[String, Int]) = {
    println(s"Raw: $result")
    result match {
      case Right(value) => println(s"result: $value")
      case Left(err) => println(s"Error: $err")
    }
  }

show(compute(100))
show(compute(-100))

// output：
Raw: Right(200)
result: 200
Raw: Left(invalid input)
Error: invalid input
```



### 3.返回值类型推断

>在Scala中，在函数声明和它的主体之间使用等号（`=`）是理想的惯用风格——即使对于返回`Unit`的方法来说也是如此。
>
>Unit类似Java void

>只有当你使用等号（`=`）将方法的声明和方法的主体部分区分开时，Scala的返回值类型推断才会生效。否则，该方法将会被视为返回一个`Unit`

```scala
scala> def f1 {Math.sqrt(2)}
f1: Unit

scala> def f2 = {Math.sqrt(2)}
f2: Double

// 主体是一个简单表达式或者复合表达式可省略花括号
scala> def f3 = Math.sqrt(2)
f3: Double

scala> def f4:Double = Math.sqrt(2)
f4: Double

// 指定返回值类型，那么它必须要和方法主体的最后一个表达式产生的结果类型兼容, 否则报错
scala> def f4:String = Math.sqrt(2)
<console>:11: error: type mismatch;
 found   : Double
 required: String
       def f4:String = Math.sqrt(2)
```

### 4.参数化类型的型变

**TODO**

#### 4.1 协变和逆变

一个Java的例子

```java
package chapter5;

class Fruit {}
class Banana extends Fruit {}
class Apple extends Fruit {}

public class Trouble {
    public static void main(String[] args) {
        // 香蕉箱，要放2个香蕉
        Banana[] bananaBox = new Banana[2];
        // 放一个香蕉
        bananaBox[0] = new Banana();

        // 水果箱，由于香蕉也是水果，所以可以把香蕉箱赋给水果箱, 此时水果箱已经有一个香蕉了
        Fruit[] fruitBox = bananaBox;
        // 在水果箱放一个苹果
        // 这里会报错：Exception in thread "main" java.lang.ArrayStoreException: chapter5.Apple
        fruitBox[1] = new Apple();

        // 打印香蕉
        for (Banana banana: bananaBox) {
            System.out.println(banana);
        }
    }
}
```

上面代码编译没错，但运行就是报错，**发生错误的原因是，在运行时，我们以使用一篮子水果为托词，试图把一个苹果放到一篮子香蕉中**，但是呢Java编译器却没有报错

书上写的太晦涩，还是参考：[Scala中的协变，逆变，上界，下界等](https://colobu.com/2015/05/19/Variance-lower-bounds-upper-bounds-in-Scala/)



### 5.隐式类型转换

TODO

### 6.值类

TODO

