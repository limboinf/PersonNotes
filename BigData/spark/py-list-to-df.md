在Python处理List转DataFrame时经常遇到，其实处理挺方便的，就拿下面的例子来说吧：

```python
In [131]: data = [('a', 1), ('b', 2)]

In [132]: rdd= sc.parallelize(data)

# 方式1
In [133]: rdd.toDF(['item', 'count'])
Out[133]: DataFrame[item: string, count: bigint]

# 方式2
In [137]: rdd.map(lambda (x, y): Row(item=x, count=y)).collect()
Out[137]: [Row(count=1, item='a'), Row(count=2, item='b')]

# 方式3
In [138]: rdd.map(lambda (x, y): dict(item=x, count=y)).toDF().collect()
Out[138]: [Row(count=1, item=u'a'), Row(count=2, item=u'b')]
```

可能还有更多方式..



