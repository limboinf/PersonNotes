---
title: hive管理
date: 2018-10-15 10:15:20
categories: hive
tags:
	- hive
	- hue

---



metastore启动脚本

```bash
cat hive-metastore.sh
#!/bin/bash
# 添加metastore启动脚本

nohup ./hive --service metastore >> metastore.log 2>&1 &
echo $! > hive-metastore.pid
```

hiveserver2启动脚本

```bash
cat hive-server.sh
#!/bin/bash
#添加hive server启动脚本
nohup ./hive --service hiveserver2 >> hiveserver2.log 2>&1 &
echo $! > hiveserver2.pid
```

启动：

```bash
./hive-metastore.sh
./hive-server.sh
```



未完待续...

