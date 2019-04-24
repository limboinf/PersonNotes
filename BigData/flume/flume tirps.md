## hdfs.batchSize & capacity & transactionCapacity

- batchSize: 在将文件刷新到HDFS之前写入文件的事件数
- channel capacity: 通道中存储的最大事件数
- channel transactionCapacity: 每个事务通道从源或提供给接收器的最大事件数

```bash
capacity >= transactionCapacity >= batchsize
```

