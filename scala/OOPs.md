# Summary

class - object - method - property

Encapsulation(封装) - Inheritance(继承) - Polymorphism(多态) - Abstraction(抽象)

# Encapsulation

- 基于对象封装：
  - c 或 go `struct`
- 基于类的封装：
  - python / java /scala `class`

# OOP

Java not pure oop, `int`, `long` 等无属性和方法

Scala pure oop, all things has method or properities，原因在于scala 类型结构

Java 所有对象父类型是`java.lang.Object`, 但是`int`,`long`等**原始类型** 排除外，Scala 是`Any`, 包含所有([*scala类型*]([https://github.com/BeginMan/PersonNotes/blob/6bbab0700f8841fe0c5d9b730a3adb946be5b14d/scala/Scala/Chapter5.md#2%E5%9F%BA%E7%A1%80%E7%B1%BB%E5%9E%8B](https://github.com/BeginMan/PersonNotes/blob/6bbab0700f8841fe0c5d9b730a3adb946be5b14d/scala/Scala/Chapter5.md#2基础类型)))

- 顶类型：Any
- 底类型：Nothing

```scala
Nothing -> [Int] -> AnyVal -> Any
```

# null

null是所有引用类型的子类型

```scala
scala> def fn(f:Boolean) = { if (f) "1" else null }
fn: (f: Boolean)String

scala> def fn(f:Boolean) = { if (f) 1 else null }
fn: (f: Boolean)Any
```



# Ref

- [从 Java 到 Scala（一）：面向对象谈起](<https://scala.cool/2018/03/java-2-scala-1/>)
- [从 Java 到 Scala（二）：object](<https://scala.cool/2018/08/java-2-scala-2/>)
- [从 Java 到 Scala（三）：object 的应用](<https://scala.cool/2018/09/java-2-scala-3/>)
- [从 Java 到 Scala（四）：Traits](<https://scala.cool/2018/11/java-2-scala-4/>)

