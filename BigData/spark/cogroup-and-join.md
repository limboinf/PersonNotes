# join
    
    
相对于SQL join, 只能两两RDD之间关联，如果需要多个则要写多个join.函数签名如下：

```python
Signature: rdd.join(other, numPartitions=None)
Docstring:
Return an RDD containing all pairs of elements with matching keys in
C{self} and C{other}.

Each pair of elements will be returned as a (k, (v1, v2)) tuple, where
(k, v1) is in C{self} and (k, v2) is in C{other}.

Performs a hash join across the cluster.
```

参数`numPartitions`用于指定结果的分区数

```python
In [20]: y = sc.parallelize([('A', 'a'), ('C', 'c'), ('D', 'd')], 2)
In [21]: x = sc.parallelize([('A', 1), ('B', 2), ('C', 3)], 2)
In [23]: x.join(y).collect()
Out[23]: [('A', (1, 'a')), ('C', (3, 'c'))]
```

# cogroup

cogroup相当于SQL中的全外关联full outer join，返回左右RDD中的记录，关联不上的为空。函数签名如下：

```python
Signature: x.cogroup(other, numPartitions=None)
Docstring:
For each key k in C{self} or C{other}, return a resulting RDD that
contains a tuple with the list of values for that key in C{self} as
well as C{other}.
```

还拿刚才x,y数据来实验：

```python
In [26]: x.join(y).collect()
Out[26]: [('A', (1, 'a')), ('C', (3, 'c'))]

In [27]: x.cogroup(y).collect()
Out[27]:
[('A',
  (<pyspark.resultiterable.ResultIterable at 0x10aa04110>,
   <pyspark.resultiterable.ResultIterable at 0x10aa06a90>)),
 ('D',
  (<pyspark.resultiterable.ResultIterable at 0x10aa06b10>,
   <pyspark.resultiterable.ResultIterable at 0x10aa06b50>)),
 ('C',
  (<pyspark.resultiterable.ResultIterable at 0x10aa06b90>,
   <pyspark.resultiterable.ResultIterable at 0x10aa06bd0>)),
 ('B',
  (<pyspark.resultiterable.ResultIterable at 0x10aa06c10>,
   <pyspark.resultiterable.ResultIterable at 0x10aa06c50>))]

In [30]: rd = x.cogroup(y)
In [32]: rd.count()
Out[32]: 4

In [34]: rd.getNumPartitions()
Out[34]: 4

In [37]: for k, v in x.cogroup(y).collect():
    ...:     print(k, [list(i) for i in v])
    ...:
    ...:
    ...:
('A', [[1], ['a']])
('D', [[], ['d']])
('C', [[3], ['c']])
('B', [[2], []])
```

来进行多个实验下:

```python
In [43]: x = sc.parallelize([('A', 1), ('B', 2), ('C', 3)], 2)

In [44]: y = sc.parallelize([('A', 'a'), ('C', 'c'), ('D', 'd')], 2)

In [45]: z = sc.parallelize([('A', 'A'), ('E', 'E')], 2)

In [48]: rdd = x.cogroup(y).cogroup(z)

In [49]: rdd
Out[49]: PythonRDD[144] at RDD at PythonRDD.scala:48

In [50]: rdd.getNumPartitions()
Out[50]: 6

In [51]: rdd.count()
Out[51]: 5

In [52]: rdd.collect()
Out[52]:
[('B',
  (<pyspark.resultiterable.ResultIterable at 0x10a9f9f90>,
   <pyspark.resultiterable.ResultIterable at 0x10aa7fed0>)),
 ('D',
  (<pyspark.resultiterable.ResultIterable at 0x10aa7f1d0>,
   <pyspark.resultiterable.ResultIterable at 0x10aa7fe10>)),
 ('A',
  (<pyspark.resultiterable.ResultIterable at 0x10aa7fd10>,
   <pyspark.resultiterable.ResultIterable at 0x10aa7f850>)),
 ('C',
  (<pyspark.resultiterable.ResultIterable at 0x10aa7f510>,
   <pyspark.resultiterable.ResultIterable at 0x10aa7f4d0>)),
 ('E',
  (<pyspark.resultiterable.ResultIterable at 0x10aa7f7d0>,
   <pyspark.resultiterable.ResultIterable at 0x10aa7fb10>))]

```


