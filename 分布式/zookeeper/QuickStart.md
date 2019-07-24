> Zookeeper highly reliable distributed coordination.(高可用分布式协调服务)

如下架构

![image-20190429135928888](http://limbo.oss-cn-beijing.aliyuncs.com/2019-04-29-055929.png)

说明：

- ZooKeeper服务器组。形成ensemble所需的最小节点数为3
- Leader节点，启动时被选举
- Follower节点：跟随leader指令的服务器节点
- Observer节点：观察者节点，不参与选举



数据结构

类似文件系统，每个节点称为znode, znode可以存储数据，可以CRUD

![image-20190429141253396](http://limbo.oss-cn-beijing.aliyuncs.com/2019-04-29-061301.png)

适用场景：

- 状态同步
- 分布式应用配置项
- 分布式锁
- 集群管理