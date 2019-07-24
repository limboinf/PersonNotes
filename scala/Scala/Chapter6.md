# 第六章 函数和闭包

## 匿名的**即时函数**（just-in-time function）

`inputType=>outputType` 方式，以接收一个函数值，如下：

```scala
def main(args: Array[String]): Unit = {
    println(cal(4, i=>i))
    println(cal(4, i=>if (i % 2 == 0) i else 0))
    println(cal(4, i=>fn(i)))

    println(inject(4, (v1, v2) => v1 + v2))
  }

  def fn(i: Int):Int= {
    i * 1 * 2 * 3
  }

  // 单值
  def cal(v:Int, codeBlock: Int=>Int): Int= {
    var res = 0
    for (i<- 1 to v) {
      res += codeBlock(i)
    }
    res
  }

  // 多值
  def inject(v: Int, op: (Int, Int) => Int) : Int = {
    v + op(1, 2000)
  }
```

好处：

- 减少函数创建
- 减少代码噪音
- 可以实现更多策略，高阶函数实现中间层

## currying

上面 inject 函数 改下下：

```scala
// 柯里化
def currying(v:Int) (op: (Int, Int) => Int) : Int = {
  v + op(1, 2000)
}

// 调用
currying(1)( (v1, v2) => v1 + v2 )
// 或者
currying(1){ (v1, v2) => v1 + v2 }
```

