---
title: hive权限控制
date: 2018-10-15 10:15:20
categories: hive
tags:
	- hive
	- hue

---



hive权限控制主要是底层HDFS和hive自身对表的授权管理。

### 1.多用户启动hive

#### 1.1 非管理员身份

如以当前登录的用户进入hive cli，报错了，提示没有权限

```bash
$ hive
Exception in thread "main" java.lang.RuntimeException: java.io.IOException: Permission denied
```



> 解决办法，这个主要是由于hive配置文件中配置的一些临时或存放中间结果的目录权限设置问题，导致当前登陆hive的用户没权限访

主要涉及如下两个参数:

```xml
<property>  
  <name>hive.exec.scratchdir</name>  
  <value>hdfs://hadoop-master:9000/opt/tmp/hive</value>  
  <description>HDFS root scratch dir for Hive jobs which gets created with write all (733) permission. For each connecting user, an HDFS scratch dir: ${hive
.exec.scratchdir};username is created, with ${hive.scratch.dir.permission}</description>  
</property>
  
<property>  
  <name>hive.exec.local.scratchdir</name>  
  <value>/opt/tmp/hive_scratchdir</value>  
  <description>Local scratch space for Hive jobs</description>  
</property>  
```

<!-- more -->



需要修改对应的hdfs和本地两个目录的权限

```bash
# hdfs 
hdfs dfs -ls /opt/tmp/hive
drwx------   - hadoop     supergroup          0 2018-10-13 23:23 /opt/tmp/hive/hadoop
drwx------   - hue        supergroup          0 2017-12-08 20:47 /opt/tmp/hive/hue
drwx------   - root       supergroup          0 2018-09-19 16:50 /opt/tmp/hive/root

# 本地
ll /opt/tmp/hive_scratchdir
total 16
drwx------ 2 hadoop hadoop 4096 Nov 15  2017 164dc4ef-1442-4c67-b1e4-6c4f48f93fa8
drwx------ 2 hadoop hadoop 4096 Oct 13 20:47 42d5af9a-ecb1-4708-92fa-176ba0ca8b30
drwx------ 2 hadoop hadoop 4096 Oct 13 23:24 b54b7bc2-2156-4afa-833a-ee0b69e5c687
-rw-rw-r-- 1 hadoop hadoop    0 Oct 13 23:23 b54b7bc2-2156-4afa-833a-ee0b69e5c6875489728272456121679.pipeout
...
```

修改为666即可，**注意路径上的所有父目录路径也要有相应的访问权限!!!**

```bash
hdfs dfs -chmod -R 755 /opt
hdfs dfs -chmod -R 777 /tmp/hadoop-yarn/

chmod -R 777 /opt/tmp
```

同理参考：[Hadoop 2.7.x Permission denied: user=dr.who, access=READ_EXECUTE, inode="/tmp"问题解决](https://my.oschina.net/MIKEWOO/blog/1542194)



以管理员身份启动hive:

```bash
hive -hiveconf hive.root.logger=INFO,console
```



### 1.Hive用户对底层文件的权限

hive用户对底层文件的访问权限，主要通过设置3个参数完成:

```xml
<property>  
  <name>hive.files.umask.values</name>  
  <value>0022</value>  
  <description>当hive在hdfs上创建文件时，对应的默认掩码。此处的0022,第一个0表示八进制；剩下的022用二进制表示即000010010，然后取反得111101101，即rwxr-xr-x，这样其他用户登录hive或hdfs时候，就没权限删除该文件</description>  
</property>  
  
<property>  
  <name>hive.metastore.authorization.storage.checks</name>  
  <value>true</value>  
  <description>就是配合hive.files.umask.values参数做权限控制.</description>  
</property>  
  
<property>  
  <name>hive.metastore.execute.setugi</name>  
  <value>true</value>  
  <description>简单说就是，hadoop在非安全模式（未使用kerborers认证）时，使用hive客户端进程对应的用户和组权限操作hdfs</description>  
</property>  
```

已经在阿里EMR Hive配置上添加了该参数(*需要重启hive*)

![image-20181013233515532](https://ws3.sinaimg.cn/large/006tNbRwly1fw70q88zebj30jf04gglt.jpg)

通过以上配置，进入hive的用户就不能随意对底层文件随意操作了，必须具有相应权限。接下来可以进行hive自身类似mysql一样的权限授权管理了

### 2. Hive自身权限

开启权限

```xml
<property>   
   <name>hive.security.authorization.enabled</name>   
   <value>true</value>   
   <description>开启权限验证</description>   
</property>   
<property>   
   <name>hive.security.authorization.createtable.owner.grants</name>   
   <value>ALL</value>   
   <description>表的创建者对表拥有所有权限</description>  
</property>  
```

hive授权核心：

- 用户
- 组
- 角色

举例：

| 用户 | 组       | 描述          |
| ---- | -------- | ------------- |
| 张三 | G_db1    | 可访问db1     |
| 李四 | G_db2    | 可访问db2     |
| 王五 | G_bothdb | 可访问db1,db2 |

