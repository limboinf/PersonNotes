```java
//一次从kafka中poll出来的数据条数
//max.poll.records条数据需要在在session.timeout.ms这个时间内处理完,默认值：10000 (10s)
props.put("max.poll.records","100");
```

max.poll.records 配置) 变量限制了每次 poll 的消息条数，不管 consumer 对应多少个 partition，从所有 partition 拉取到的消息条数总和不会超过 `maxPollRecords`。

max.poll.interval.ms 参数设置大一点可以增加两次 poll 之间处理消息的时间。

0.11.0 Kafka 的默认配置是

- max.poll.interval.ms=5min
- max.poll.records=500

即平均 600ms 要处理完一条消息，如果消息的消费时间高于 600ms，则一定要调整 max.poll.records 或 max.poll.interval.ms。

