NoSQL（Not Only SQL，不限于SQL）数据模型分类：

- K-V
- BigTable
- Document
- Graph DB


图数据库面向『图』这种数据结构，包含：节点、边（关系），节点和关系都有属性（存储数据）。图数据结构如下：

```bash
G(V, E)
//V: vertex 边
//E: Edge
```

![](http://upload-images.jianshu.io/upload_images/3503486-a2268f9d41b00752?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

图数据库内部存储结构一般为**邻接矩阵或邻接表**的方式

![](http://beginman.qiniudn.com/2017-07-13-14999461234986.jpg)

*图片来源：http://www.jianshu.com/p/83d6188a26d4*

有个典型的图数据库需包含：

- 存储系统
- 计算系统

![](http://beginman.qiniudn.com/2017-07-13-14999462920702.jpg)

![](http://beginman.qiniudn.com/2017-07-13-14999465734273.jpg)

一些术语：

- 关系型数据库世界中的联机事务处理（Online Transactional Processing，OLTP）
- 联机分析处理（Online Analytical Processing，OLAP）

[OLTP vs. OLAP](http://datawarehouse4u.info/OLTP-vs-OLAP.html)



