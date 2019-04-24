## 第二章：体验Scala

## 1思维导图

![image-20181113140010324](https://ws1.sinaimg.cn/large/006tNbRwly1fx6ebfbnpej314s0jewhj.jpg)

## 2.编译

**scalac工具**

```scala
package chapter2

//扩展了App特质(trait)名为Sample的object
//App指示编译器生成必需的main()方法，以使Sample成为起始类
object Sample extends App {
  println("hello scala!")
}

```

```bash
$ scalac Sample.scala 

$ ll
total 16
-rw-r--r-- 1 fangpeng staff 2376 Nov 13 13:47 'Sample$.class'
-rw-r--r-- 1 fangpeng staff  729 Nov 13 13:47 'Sample$delayedInit$body.class'
-rw-r--r-- 1 fangpeng staff  925 Nov 13 13:47  Sample.class
-rw-r--r-- 1 fangpeng staff   56 Nov 13 13:47  Sample.scala

$ scala Sample       
hello scala!

$ java -classpath /usr/local/opt/scala@2.11/libexec/lib/scala-library.jar:. Sample                                    
hello scala!
```

