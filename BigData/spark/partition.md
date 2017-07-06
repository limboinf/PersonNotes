spark rdd 是分区的，关于分区操作有：

- coalesce()
- repartition()

这两个方法可参考：[Spark算子：RDD基本转换操作(2)–coalesce、repartition](http://lxw1234.com/archives/2015/07/341.htm)

这样需要弄明白：

- [ ] 窄依赖
- [ ] 宽依赖


有这篇文章[通过分区(Partitioning)提高Spark的运行性能](https://www.iteblog.com/archives/1695.html) 讲的非常牛逼。

- 动手实践一遍
- 学着看 spark history UI 来分析问题
- 分区的设置确实对性能影响很大。

>在Spark中，只要job需要在分区之间进行数据交互，那么一个新的stage将会产生（如果使用Spark术语的话，分区之间的数据交互其实就是shuffle）。Spark stage中每个分区将会起一个task进行计算，而这些task负责将这个RDD分区的数据转化(transform)成另外一个RDD分区的数据。

对于`map`, 将一个RDD中的每个数据项，通过map中的函数映射变为一个新的元素。**输入分区与输出分区一对一，即：有多少个输入分区，就有多少个输出分区。**。如下：

```scala
val m = 10
scala> sc.parallelize(2 to m, 2).map(x => (x, (2 to (m/x)))).collect()
res4: Array[(Int, scala.collection.immutable.Range.Inclusive)] = Array((2,Range(2, 3, 4, 5)), (3,Range(2, 3)), (4,Range(2)), (5,Range(2)), (6,Range()), (7,Range()), (8,Range()), (9,Range()), (10,Range()))

```

`sc.parallelize(2 to n, 2)` Spark使用分区机制将数据很好地分成2组，2~6,一组，6~10 一组，然而我们的map函数将这些数转成(key,value)pairs，而value里面的数据大小变化很大（key比较小的时候，value的值就比较多，从而也比较大）。每个value都是一个list。比如说 当key较小为2时，对应的value list就越多。那么第一个分区拥有大部分的数据，它的计算花费了最多的时间。从stage运行来看，工作负载并没有均衡到所有的task中。解决办法就是**将map数据重新分区**

对RDD调用.repartition(numPartitions)函数将会使Spark触发shuffle并且将数据分布到我们指定的分区数中。

```scala
scala> val n = 2000000
n: Int = 2000000

# 这里repartition(8)重新分区
scala> val comp = sc.parallelize(2 to n, 8).map(x => (x, (2 to (n/x)))).repartition(8).flatMap(kv => kv._2.map(_ * kv._1))
comp: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[22] at flatMap at <console>:26

scala> val p = sc.parallelize(2 to n, 8).subtract(comp)
p: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[27] at subtract at <console>:28

scala> p.collect()
```

参考：

- [Spark Rdd coalesce()方法和repartition()方法](http://www.cnblogs.com/fillPv/p/5392186.html)
- [通过分区(Partitioning)提高Spark的运行性能](https://www.iteblog.com/archives/1695.html)

