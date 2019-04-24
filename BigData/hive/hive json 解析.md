---
title: hive解析json数据
date: 2018-10-15 10:15:20
categories: hive
tags:
	- json
---

这里使用[Read - Write JSON SerDe for Apache Hive](https://github.com/rcongiu/Hive-JSON-Serde) 来在hive里使用json

分两个theme:

- hive
- hadoop

Hive这块安装：

```bash
$ cd $HIVE_HOME/lib
$ wget http://www.congiu.net/hive-json-serde/1.3.8/cdh5/json-serde-1.3.8-jar-with-dependencies.jar
$ wget http://www.congiu.net/hive-json-serde/1.3.8/cdh5/json-udf-1.3.8-jar-with-dependencies.jar
```

<!-- more -->

数据结构是这样的：

```json
{
    "_ip":"39.107.245.223",
    "ua":"Windows NT 6.1; WOW64",
    "timestamp":1536649070251,
    "message":{
        "event":"trace"
    },
    "uid":"abcde"
}
```

创建schema

```mysql
CREATE EXTERNAL TABLE `demo`( 
    `ua` string,
    `timestamp` string,
    `message` map<string, string>,
    `uid` string
)
PARTITIONED BY (`dt` string) 
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES ("ignore.malformed.json" = "true")
STORED AS TEXTFILE;
```

添加jar到hive classpath中

```bash
hive> add jar /opt/hive/apache-hive-2.2.0-bin/lib/json-udf-1.3.8-jar-with-dependencies.jar;
hive > add jar /opt/hive/apache-hive-2.2.0-bin/lib/json-serde-1.3.8-jar-with-dependencies.jar;
```

添加分区：

```mysql
alter table demo add partition(dt=20180911) LOCATION '/data/events/demo/dt=20180911'
```

**Hadoop需要直接把jar包放在$HADOOP_HOME/share/hadoop/mapreduce/下即可**，否则会出现如下问题，如聚合查询hive

```bash
hive> SELECT count(*) FROM demo WHERE dt='20181010';

Caused by: java.lang.ClassNotFoundException: Class org.openx.data.jsonserde.JsonSerDe not found
        at org.apache.hadoop.conf.Configuration.getClassByName(Configuration.java:2103)
        at org.apache.hadoop.hive.ql.plan.PartitionDesc.getDeserializer(PartitionDesc.java:177)
        at org.apache.hadoop.hive.ql.exec.MapOperator.getConvertedOI(MapOperator.java:295)
        ... 24 more
```



