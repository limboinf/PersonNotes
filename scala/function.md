## Summary

scala 函数总结



## 变长参数

跟Java一样，只有最后一个参数是可变长的，使用方式：

```scala
(varName: dataType*) // 参数类型后加星号
```

示例：

```scala
scala> def sum(v: Int*) :Int = { v.fold(0) { (x, y) => x + y } }
sum: (v: Int*)Int

scala> sum(1,2,3,4,5)
res0: Int = 15

// 和java 不同的是不能直接将一个数组或列表作为变长参数直接传递
scala> val l = List(1,2,3,4,5)
l: List[Int] = List(1, 2, 3, 4, 5)

// 需要将数组或列表展开成离散值（数组展开标记（array explode notation）），arr:_*
scala> sum(l:_*)
res1: Int = 15
```

之前这里用总结：[https://github.com/BeginMan/PersonNotes/blob/0f5b5a40aaa9878124e5e0a6430935abf7627352/scala/Scala/Chapter3.md#41-%E5%8F%98%E9%95%BF%E5%8F%82%E6%95%B0](https://github.com/BeginMan/PersonNotes/blob/0f5b5a40aaa9878124e5e0a6430935abf7627352/scala/Scala/Chapter3.md#41-变长参数)

关于fold 可参考：

- [Scala Saturday – The foldLeft Method](<https://bradcollins.com/2015/05/30/scala-saturday-the-foldleft-method/>)
- [Scala:fold,foldLeft和foldRight区别与联系](https://www.iteblog.com/archives/1228.html)

