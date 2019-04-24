---
title: hive ranger
date: 2018-12-15 10:15:20
categories: hive
tags:
	- hive
	- hue

---



## Beeline

HiveServer2有自己的CLI叫 [Beeline](https://cwiki.apache.org/confluence/display/Hive/HiveServer2+Clients#HiveServer2Clients-Beeline%E2%80%93NewCommandLineShell)（基于JDBC的SQLLine），由于新的开发焦点在HiveServer2，那么Hive CLI将被废弃

```bash
$ beeline
beeline> !connect jdbc:hive2://localhost:10000 hadoop ""
beeline> show databases;
```

或者：

```bash
$ beeline -u jdbc:hive2://localhost:10000/stg -n hadoop -p ""
```

Hive中的用户就是用户的系统用户名



### Hadoop 安全体系

![image-20181211142116833](https://ws3.sinaimg.cn/large/006tNbRwly1fy2s9mhverj30ie08tt96.jpg)

## hive 权限管理

hive访问三种方式：

![image-20181211141031028](https://ws3.sinaimg.cn/large/006tNbRwly1fy2ryd4qadj30tm0d1ta3.jpg)



```bash
[root@beginman ~]# su - hive
[hive@beginman ~]$ hive
hive> show roles;
FAILED: Execution Error, return code 1 from org.apache.hadoop.hive.ql.exec.DDLTask. Current user : hive is not allowed to list roles. User has to belong to ADMIN role and have it as current role, for this action.
```

执行任何有关权限设置和查看的语句时都报错，这是**因为没有开启权限控制**

```xml
<!--开启hive权限认证机制-->
<property>
<name>hive.security.authorization.enabled</name>      # 开启权限认证功能
<value>true</value>
<description>enable or disable the hive client authorization</description>
</property>
 
<property>
<name>hive.server2.enable.doAs</name>
<value>false</value>
</property>
 
 
<property>
<name>hive.users.in.admin.role</name>               # admin 权限用户列表
<value>hive</value>
</property>
```

然后重启hive, 用hive 账号进入hive, 执行 `set role admin`, **将此用户设置为admin角色的用户**即可

```bash
hive> set role admin;
OK
Time taken: 0.852 seconds
hive> show roles;
OK
admin
public
```



使用Apache ranger进行权限控制：https://help.aliyun.com/document_detail/66420.html?spm=a2c4g.11186623.2.20.31d33e02PcxZsu#concept-ej3-jn3-bfb

#### Ranger与Sentry使用区别

Sentry：RBAC（role-based acess control）基于角色的管理,即：通过创建角色，将每个组件的权限授予给此角色。然后在用户中添加此角色，即用户具备此角色访问组件的权限（组也类似）

Ranger: PBAC（policy-based acess control)基于策略的管理，即：每个组件可以添加服务Service如Hive，然后添加自定义策略（如访问粒度Database，Table，Column），再添加组或用户访问权限（Select,Create,Drop等）

Ranger 权限管理流程图分析,以ranger对hive进行权限管理为例，如下图所示：鉴权过程分为五个步骤

![image-20181211145842575](https://ws2.sinaimg.cn/large/006tNbRwly1fy2tchy8hpj311k0i4n6i.jpg)

- https://ieevee.com/tech/2016/05/10/spark-7-security.html)

