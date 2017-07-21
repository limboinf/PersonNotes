# 表达式

Scala的表达式有值和类型。

```scala
// 值为1 类型为Int
scala> if (x >1) 1 else 2
res5: Int = 1

// 如果缺少else 则默认为 (), 也就是 Util类
scala> if (x >2) 1
res0: AnyVal = ()

scala> if (x >2) 1 else ()
res3: AnyVal = ()

// 如果if else有不同类型分支，则类型为Any, 也就是公共超类型
scala> if (x >2) 2 else "str"
res6: Any = str

// 多个if else可简写
scala> if (x > 3) {
     |   1
     | } else if (x==1) {
     |   1
     | } else if (x==2) {
     |   2
     | } else "Unknown"
res8: Any = 2

scala> if (x > 3) 1 else if (x ==1) 1 else if (x == 2) 2 else "Unknown"
res7: Any = 2
```

# 循环

scala的for与Python类似, 如：

```scala
scala> for (i<-1 to 5)
     | println(i)
1
2
3
4
5
```

`for (i <- 表达式)`, 让`i`遍历`<-` 右边表达式的所有值。


