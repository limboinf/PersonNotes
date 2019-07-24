# 第七章：特质

特质（trait）**横切关注点**（crosscutting concerns），类似Java接口

特质混入任何的类中，类似Python的Mixin模式

> 在特质中定义并初始化的`val`和`var`变量，将会在混入了该特质的类的内部被实现，任何已定义但未被初始化的`val`和`var`变量都被认为是抽象的，混入这些特质的类需要实现它们

```scala
trait Firend {
  val name:String
  def listen() = println(s"hello $name")
}
```

使用：

```scala
object Example {
  def main(args: Array[String]): Unit = {
    new Woman("Rose").listen()
    new Man("Jack").listen()
    new Dog("Tank").listen()

    // 以在混入了某个特质的类实例上调用该特质的方法，
    // 同时也可以将指向这些类的引用视为指向该特质的引用
    val mansBestFriend: Firend = new Dog("狗腿子")
    mansBestFriend.listen()
    
    // 创建实例的时候也可以混入特质
    // val angel = new Cat("Angel") with Friend
  }
  
  // 如果一个类没有扩展任何其他类，则使用extends关键字来混入特质
  class Human(override val name:String) extends Firend
  class Woman(override val name:String) extends Human(name)
  class Man(override val name:String) extends Human(name)

  class Animal()

  // 如果要混入额外的特质，要使用with关键字
  class Dog(override val name:String) extends Animal with Firend {
    // 可选择性重写方法
    override def listen(): Unit = println(s"The dog: $name listen")
  }
}
```

## Decorator pattern

使用特质实现装饰器模式，有点意思