4类：

- Producer API
- Consumer API
- Streams API 构建流处理接口
- Connect API 与外部系统交互API

pom.xml 如下：

```xml
<dependency>
  <groupId>org.apache.kafka</groupId>
  <artifactId>kafka_2.11</artifactId>
  <version>0.10.1.1</version>
</dependency>
<dependency>  
  <groupId>org.apache.kafka</groupId>  
  <artifactId>kafka-clients</artifactId>  
  <version>0.10.1.1</version>  
</dependency>
```

## 1. Topic API

元数据信息是注册到zk中的，有`ZkUtils`类来封装ZK操作，`AdminUtils`类调用`ZkUtils`相应方法来对kafka元数据进行管理。

```java
// 实例化ZkUtils
ZkUtils zkUtils = ZkUtils.apply(ZK_CONNECT, SESSION_TIMEOUT, CONNECT_TIMEOUT, 
        JaasUtils.isZkSecurityEnabled());
// 判断topic是否存在
AdminUtils.topicExists(zkUtils, topic)；
// 创建topic
AdminUtils.createTopic(zkUtils, topic, partition, repilca, properties);
// 删除topic
AdminUtils.deleteTopic(zkUtils, topic);
// 关闭ZkUtils
zkUtils.close();
```

## 2. Produce API

主要是`KafkaProducer`和`ProducerRecord`的操作，`Producer`接口有两个send方法

```java
public interface Producer<K, V> extends Closeable {
  // Send the given record asynchronously and return a future which will eventually contain the response information.
  // KafkaProducer默认是异步发送消息，会将消息缓存到消息缓冲区中
  // 当消息在消息缓冲区中累计到一定数量后作为一个RecordBatch再发送
  public Future<RecordMetadata> send(ProducerRecord<K, V> record);
  
  // Send a record and invoke the given callback when the record has been acknowledged by the server
  // 如果消息发送发生异常，Callback接口的onCompletion会捕获到相应异常
  public Future<RecordMetadata> send(ProducerRecord<K, V> record, Callback callback);
}
```



## 3. Consumer API

## 4. Streams API

## 5. Connect API

## 6. 扩展

## 7. 与Spring交互

