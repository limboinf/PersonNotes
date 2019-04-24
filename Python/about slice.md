---
title: Python切片的一些高级特性
date: 2019-01-02 13:40:14
categories: python
tags:
	- 切片

---



## 1.Overview

切片（Slice）的概念，顾名思义，但是要理解应用在什么身上，切什么片呢？这个先留着我们后面说。在Python里提供**切片操作符**，注意是操作符，使用起来极为方便。

<!-- more -->

## 2.语法

语法很简单：`[start:end:step]`, 其中step是步长，如下例子：

```python
In [52]: l[0:10:1]
Out[52]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

In [53]: l[0:10]
Out[53]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

In [54]: l[:10]
Out[54]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

start默认0，step默认1，可省略不填

```python
In [63]: start, end, step = -10, 100, 1

In [64]: l[start:end:step]
Out[64]: [90, 91, 92, 93, 94, 95, 96, 97, 98, 99]

In [65]: l[-10:]
Out[65]: [90, 91, 92, 93, 94, 95, 96, 97, 98, 99]

In [66]: l[-10:100]
Out[66]: [90, 91, 92, 93, 94, 95, 96, 97, 98, 99]

In [67]: l[-1]
Out[67]: 99

In [68]: l[-1:]
Out[68]: [99]

In [69]: l[-1:100]
Out[69]: [99]
```

倒数第一个元素的索引是`-1`

只写`[:]`就可原样复制一个list

## 3.python 切片实现机制

看下下面的例子，在py3中取字典keys()或values()进行切片

```python
In [73]: r = rs.keys()

In [74]: r[:1]
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-74-9e1ba94155c3> in <module>()
----> 1 r[:1]

TypeError: 'dict_keys' object is not subscriptable

In [75]: list(r)[:1]
Out[75]: ['08:00:00']
```

报错提示：*object is not subscriptable*，**也就是说切片必须在对象是subscriptable的时候才能使用**，那么什么是subscriptable？**只有实现了`__getitem__`方法才符合**，常见的如string，list, tuple, dict，字典也可以的，如：

```python
{"a":1, "b":2, "c":3}["c"] == 3
```

切片操作都是由解释器调用的list.__getitem__(x)特殊方法进行的

```python
In [76]: list.__getitem__?
Docstring: x.__getitem__(y) <==> x[y]
Type:      method_descriptor
```



## 4.切片常用操作

```python
In [91]: l = list(range(10))

In [92]: l
Out[92]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

In [93]: l[::2]
Out[93]: [0, 2, 4, 6, 8]

In [94]: l[1::2]
Out[94]: [1, 3, 5, 7, 9]

In [95]: l[::2]  # 取偶数索引位置
Out[95]: [0, 2, 4, 6, 8]

In [96]: l[1::2]  # 取奇数索引位置
Out[96]: [1, 3, 5, 7, 9]

In [97]: l[:]  # 浅复制，等价list.copy()
Out[97]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

In [98]: l[::-1] # 逆序
Out[98]: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

In [99]: l[:0]
Out[99]: []

In [100]: l[:0] = ['a', 'b', 'c']  # 插入

In [101]: l
Out[101]: ['a', 'b', 'c', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

In [102]: l[0:3] = ['3', '2', '1']   # 替换切片

In [103]: l
Out[103]: ['3', '2', '1', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

In [104]: del l[0:3]  # 删除切片

In [105]: l
Out[105]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

还有些常用的就是切成多少子片，如l = [1,2,3,4,5,6]切成2个子list，[[1,2,3],[4,5,6]]

```python
def slice_it(l, cols=2):
    """将一个列表拆分cols块
    >> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >> list(slice_it(l,3))
    [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    start = 0
    for i in range(cols):
        stop = start + len(l[i::cols])
        yield l[start:stop]
        start = stop
```

上面代码的重点在于如何确定下一个子list能有多少个元素，通过`len(l[i::cols])`来看下个子list能分片的量来确定stop边界

还有常用的就是chunk,切成多少份，如下：

```python
def chunks(l, n=3):
    """
    >> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >> list(chunk(l))
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    for i in range(0, len(l), n):
        yield l[i: i + n]
```

