spark k-v pair 在Python里是一tuple.

```python
rdd = sc.parallelize([('a', 1), ('b', 1), ('a', 1)])
```

对这个kv pair常用操作是 `groupByKey`和`groupBy`

# groupBy

```python
# Return an RDD of grouped items.
rdd.groupBy(f, numPartitions=None, partitionFunc=<function portable_hash at 0x10335d2a8>)
```

元素item 通过函数返回一个key, key + item 组成 k-v, 然后将key相同的item组成一组：

```python
rdd = sc.parallelize([1, 1, 2, 3, 5, 8])
In [23]: rdd.groupBy(lambda x: x % 2).collect()
# 这里 0 和 1 为通过函数 f 返回的key
# key 对应的value是一个ResultIterable 对象，里面包含相同key的item
Out[23]:
[(0, <pyspark.resultiterable.ResultIterable at 0x10375c4d0>),
 (1, <pyspark.resultiterable.ResultIterable at 0x10375c990>)]

In [24]: for i, v in rdd.groupBy(lambda x: x % 2).collect():
    ...:     print(i)
    ...:     print(list(v))
    ...:
0
[2, 8]
1
[1, 1, 3, 5]
```

# groupByKey

签名如下：

```python
rdd.groupByKey(numPartitions=None, partitionFunc=<function portable_hash at 0x10335d2a8>)

"""
Docstring:
Group the values for each key in the RDD into a single sequence.
Hash-partitions the resulting RDD with numPartitions partitions.

.. note:: If you are grouping in order to perform an aggregation (such as a
    sum or average) over each key, using reduceByKey or aggregateByKey will
    provide much better performance.

"""
```

对Key-Value形式的RDD的操作。与groupBy类似。但是其分组所用的key不是由指定的函数生成的，而是采用元素本身中的key。

```python
In [25]: rdd = sc.parallelize([('a', 1), ('b', 1), ('a', 1)])

In [26]: rdd.groupByKey().collect()
Out[26]:
[('a', <pyspark.resultiterable.ResultIterable at 0x103751b50>),
 ('b', <pyspark.resultiterable.ResultIterable at 0x103787050>)]

In [27]: for i in rdd.groupByKey().collect():
    ...:     print(i[0], list(i[1]))
    ...:
('a', [1, 1])
('b', [1])

In [28]: rdd.groupByKey().mapValues(len).collect()
Out[28]: [('a', 2), ('b', 1)]
```

    
# mapValues

一般有`groupByKey`就有`mapValues`, 因为groupByKey只是把相同key组合起来(list -> value), mapValues就要对这些k-v pair的value(list) 进行操作。

函数签名如下：

```python
"""
Signature: rdd.mapValues(f)
Docstring:
Pass each value in the key-value pair RDD through a map function
without changing the keys; this also retains the original RDD's
partitioning.
"""

>>> x = sc.parallelize([("a", ["apple", "banana", "lemon"]), ("b", ["grapes"])])
>>> def f(x): return len(x)
>>> x.mapValues(f).collect()
[('a', 3), ('b', 1)]
``` 


