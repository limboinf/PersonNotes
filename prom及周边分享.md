# Summary

主题：

- Prometheus

- 时序数据库

- Burrow
- burrow exporter

- Grafana

## Prometheus 架构

![image-20190423173805952](http://limbo.oss-cn-beijing.aliyuncs.com/2019-04-23-093806.png)

<https://github.com/prometheus/prometheus/>

> Prometheus是一套开源的监控&报警&时间序列数据库的组合

pull vs push 模型

Prometheus pull mode, 通过HTTP协议采集指标，ES 是push mode

架构图

![img](https://prometheus.io/assets/architecture.svg)

组件：

- Prometheus server：核心，采集与存储，PromQL支持
- Push Gateway：job主动推送指标的中间网关
- exporters：类似 agent
- alertmanager: 报警模块

![Image result for prometheus metrics](https://docs.cloudposse.com/assets/324asd-Prometheus_architecture.png)

## Prometheus 数据模型

每条时序数据由一个指标名称(metrics name)和一组标签(label, k=v)组成，如：

```
kafka_burrow_total_lag{cluster="production",group="flume",instance="127.0.0.1:9190",job="kafka"}
```

kafka_burrow_total_lag是指标名称，`{k=v, k1=v1, ..}`是一组标签，类别关系型数据库：

- kafka_burrow_total_lag: 表名
- 标签是字段
- timestamp 主键



## 延伸：时序数据库

两个问题：

1. 为什么会存在这个时序数据库？
2. 为什么要用？

存在的原因是，万物皆联网的时代，我们需要一种衡量事物随时间的变化的数据形式，这里的时间不只是一个度量标准，而是一个坐标的主坐标轴。为啥要用呢？因为需要大规模、高效可用

> 时间序列数据之所以如此强大，是因为将系统的每个变化都记录为新的一行，从而可以去*衡量变化*：分析过去的*变化*，监测现在的*变化*，以及预测未来将如何*变化*。



时序数据(Time Series Database)是基于时间的一系列的数据，以时间为坐标，与RDBMS 对比

| 时序数据库         | 关系型数据库 |                                                             |
| ------------------ | ------------ | ----------------------------------------------------------- |
| metric，度量       | table        |                                                             |
| data point, 数据点 | row          |                                                             |
| timestamp, 时间戳  | PK, 主键     | timestamp加上所有的tags可以认为是table的primary key。       |
| field，度量字段    | field        | 在时序数据库中，field 随着时间戳的变化而变化的数据          |
| tag, 标签          |              | 在时序数据库中，表示附加信息， 随着时间戳的变化不变化的数据 |

![image-20190425141452503](http://limbo.oss-cn-beijing.aliyuncs.com/2019-04-25-061751.png)

![image-20190425142412298](http://limbo.oss-cn-beijing.aliyuncs.com/2019-04-25-062412.png)

应用场景：

- 监控系统(互联网、物联网)
- 事件应用程序
- BI
- ...

类别：

- InfluxDB
- OpenTsdb，底层使用Hbase作为其分布式存储引擎
- Druid



### Prometheus metric

```
<metric name>{<label name>=<label value>, ...}
```

- Counter：计数,一直增加或减少，按时间趋势
- Gause: 内存或CPU变化，可大可小，瞬时变化
- Histogram：一段时间内采样分组聚合统计
- Summary：与Histogram类似，只不过通过百分比表示



### Prometheus target & job

![image-20190429164510216](http://limbo.oss-cn-beijing.aliyuncs.com/2019-04-29-084510.png)

```bash
- target1: xxxx
   - instance
```



###  PromQL

PromQL (Prometheus Query Language) 是 Prometheus 自己DSL语言

具体细节参考：<https://songjiayang.gitbooks.io/prometheus/content/promql/summary.html>

查询方式与sql对比：<https://songjiayang.gitbooks.io/prometheus/content/promql/sql.html>



查询结果类型：

1. 瞬时数据 (Instant vector): 包含一组时序，每个时序只有一个点
2. 区间数据 (Range vector): 包含一组时序，每个时序有多个点
3. 纯量数据 (Scalar): 纯量只有一个数字，没有时序

如下查询kafka集群production，groupid为指定的group 消费堆积量

```bash
# 瞬时查询
kafka_burrow_total_lag{cluster="production",group="console-consumer-10175",instance="127.0.0.1:9190",job="kafka"}	
value 10841748

# 区间查询，查询5分钟堆积量
kafka_burrow_total_lag{cluster="production",group="console-consumer-10175",instance="127.0.0.1:9190",job="kafka"}[5m]
value
10841748 @1556527978.172
10841748 @1556527993.171
10841748 @1556528008.171
10841748 @1556528023.172
10841748 @1556528038.171
10841748 @1556528053.172
10841748 @1556528068.171
10841748 @1556528083.172
10841748 @1556528098.172
10841748 @1556528113.171
10841748 @1556528128.172
10841748 @1556528143.171
10841748 @1556528158.172
10841748 @1556528173.171
10841748 @1556528188.172
10841748 @1556528203.172
10841748 @1556528218.172
10841748 @1556528233.172
10841748 @1556528248.172
10841748 @1556528263.171

# 查询总量
sum(kafka_burrow_total_lag{cluster="production",group="console-consumer-10175",instance="127.0.0.1:9190",job="kafka"})
value 10841748
```

还有些内置函数，如kafka topic 5分钟内平均每秒写入量：

```bash
sum(rate(kafka_burrow_partition_current_offset{cluster="production",group="1v1_room_event_data",instance="127.0.0.1:9190",job="kafka",topic="qoe_room_event"}[5m]))
```

Graph展示

![image-20190429170713911](http://limbo.oss-cn-beijing.aliyuncs.com/2019-04-29-090714.png)

但是一般图形化展示用Grafana

## Grafana

做数据和监视可视化的时候，Grafana + Prometheus 来配合，grafana是go开发的可视化工具

## Exporter

是个agent, 按照一定文本格式，http请求，保留 /metrics 接口就行

文本格式：<https://songjiayang.gitbooks.io/prometheus/content/exporter/text.html>

简单的exporter实现：<https://songjiayang.gitbooks.io/prometheus/content/exporter/sample.html>

有很多第三方exporter 如：

- [MySQL server exporter](https://github.com/prometheus/mysqld_exporter) 负责收集 Mysql Sever 信息
- [MongoDB exporter](https://github.com/dcu/mongodb_exporter) 负责收集 MongoDB 信息
- [InfluxDB exporter](https://github.com/prometheus/influxdb_exporter) 负责收集 InfluxDB 信息
- [JMX exporter ](https://github.com/prometheus/jmx_exporter)负责收集 Java 虚拟机信息

如配合cadvisor 监控Docker

## goroutine

内存消耗，线程8MB, 协程2KB,一台普通的服务器就可以支持百万协程。

TODO

## Burrow

消费__consumer_offsets 解析数据：<https://github.com/BeginMan/kafka-0.10.1.1-src/blob/981e19c188d7c8448aed9e1701cd9504f69055f9/examples/src/main/java/kafka/examples/MetaDataConsumer.java>

架构：

![image-20190505221116087](http://limbo.oss-cn-beijing.aliyuncs.com/2019-05-05-141214.png)



## 其他

- [热加载配置](<https://songjiayang.gitbooks.io/prometheus/content/qa/hotreload.html>)
- [TODO: flask项目加监控： Prometheus exporter for Flask applications](https://github.com/rycus86/prometheus_flask_exporter)

# 参考

- [我们为什么需要一个时序数据库？](<https://www.infoq.cn/article/2017/07/Why-time-series-database>)
- [Grafana全面瓦解](<https://www.jianshu.com/p/7e7e0d06709b>)