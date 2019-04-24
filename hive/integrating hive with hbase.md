---
title: HBase integrated with Hive
date: 2018-10-15 10:15:20
categories: hbase
tags:
	- hbase
	- hive

---

hive limitations:  underlying  Hdfs, append-only, block-oriented storage

**To overcome this problem, Hbase is used in place of MySQL, with Hive**

Hbase Tables can be accessed like native Hive tables.

<!-- more -->

## **HBase integrated with Hive**

keyword: **Hive Storage Handler**

Hbase 创建有两个列族的table:

```bash
create 'employee','personaldetails','deptdetails'
# put data
put 'employee','eid01','personaldetails:fname','Brundesh'
put 'employee','eid01','personaldetails:Lname','R'
put 'employee','eid01','personaldetails:salary','10000'
put 'employee','eid01','deptdetails:name','R&D'
put 'employee','eid01','deptdetails:location','Banglore'

put 'employee','eid02','personaldetails:fname','Abhay'
put 'employee','eid02','personaldetails:Lname','Kumar'
put 'employee','eid02','personaldetails:salary','100000'
```

![image-20180915170307415](https://ws2.sinaimg.cn/large/006tNbRwly1fvaci1t51lj30ur05v12l.jpg)

hive

> If there are multiple columns family in HBase, we can **create one table for each column families.** In this case, we have 2 column families and hence we are creating two tables, one for each column families.

like:



```mysql
create external table employee_hbase(
    Eid String, 
    f_name string, 
    s_name string, 
    salary int)
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
with serdeproperties ("hbase.columns.mapping"=":key,personaldetails:fname,personaldetails:Lname,personaldetails:salary")
tblproperties("hbase.table.name"="employee");
```

***creating the non-native Hive table using Storage Handler, should specify the `STORED BY` clause.***

Notes:

- `hbase.columns.mapping`: hive & hbase columns mapping, 第一列必须是键列，同hbase行键列一致
- be careful rowkey

create another table



```mysql
CREATE EXTERNAL TABLE employee_dept_hbase(
    eid STRING,
    title STRING,
    `location` STRING 
)
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES ("hbase.columns.mapping"=":key,deptdetails:name,deptdetails:location")
TBLPROPERTIES("hbase.table.name"="employee");
```

query:

![image-20180915170908793](https://ws3.sinaimg.cn/large/006tNbRwly1fvaci9pfo0j310509twf5.jpg)

![image-20180915171041534](https://ws2.sinaimg.cn/large/006tNbRwly1fvacih77i7j30za0983z2.jpg)

join query

![image-20180915171231201](https://ws1.sinaimg.cn/large/006tNbRwly1fvacilvbs0j30yv0ab754.jpg)