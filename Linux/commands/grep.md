grep 命令很强大，之前我是这样查询匹配行数的：

```
$ cat data.json|grep "ZCORUM" | wc -l
     238
```

很SB，grep 可以

```bash
$ grep -c "ZCORUM" data.json
238

$ grep -cv "ZCORUM" data.json
245

$ wc -l data.json
     483 data.json
```

常用参数：

- `-o` 输出匹配行
- `-v` 输出不匹配行
- `-c` 统计次数
- `-n` 打印行号
- `-i` 忽略大小写


`grep "class" . -R -n` 递归查找

`grep -e "class" -e "vitural" file` 查找多个

`-E` 选项使用正则，如:`grep -E '[0-9]+'` 或者`egrep [0-9]+` 替代
