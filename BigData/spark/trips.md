---
title: spark trips
date: 2018-10-15 10:15:20
categories: spark
tags:
	- trips

---

### datasets of spark Row into string

```java
public class SparkSample {
    public static void main(String[] args) {
        SparkSession spark = SparkSession
            .builder()
            .appName("SparkSample")
            .master("local[*]")
            .getOrCreate();
    //create df
    List<String> myList = Arrays.asList("one", "two", "three", "four", "five");
    Dataset<Row> df = spark.createDataset(myList, Encoders.STRING()).toDF();
    df.show();
    //using df.as
    List<String> listOne = df.as(Encoders.STRING()).collectAsList();
    System.out.println(listOne);
    //using df.map
    List<String> listTwo = df.map(row -> row.mkString(), Encoders.STRING()).collectAsList();
    System.out.println(listTwo);
  }
}
```



### Service 'sparkDriver' could not bind on port 0. 解决方案

`hostname`命令看下hostname 添加到 /etc/hosts https://stackoverflow.com/questions/34601554/mac-spark-shell-error-initializing-sparkcontext



未完待续...

<!-- more -->

### Ref

- [Apache Spark Dataset and SQL in Java](https://mydevgeek.com/apache-spark-dataset-and-sql-in-java/)