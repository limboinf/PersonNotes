Scala match case:

```scala
scala> val times = 1
times: Int = 1

scala> times match {
     | case 1 => "one"
     | case 2 => "two"
     | case 3 => "three"
     | }
res2: String = one

scala> val arrs = Array("1","2","3")
arrs: Array[String] = Array(1, 2, 3)

scala> arrs match {
     | case Array(a, b, c) => (a, c, b)
     | case _=> "default"
     | }
res4: java.io.Serializable = (1,3,2)
```

