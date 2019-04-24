开启监控：`-Dflume.monitoring.type=http -Dflume.monitoring.port=1234`

访问：http://ip:1234/metrics

curl：

```bash
curl http://localhost:1234/metrics 2>/dev/null|sed -e 's/([,])\s*/\1\n/g' -e 's/[{}]/\n/g' -e 's/[“,]//g'
```



参考：[Flume监控](https://kiswo.com/article/1023)

