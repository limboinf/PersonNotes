Mac sed 不是GUN sed, 所以有时候执行起来会有错误，最好gun sed:

```
# GNU sed on Mac OS X
$ brew install gnu-sed
```

- With `--with-default-names` option it installs sed to /usr/local/bin/
- Without that option it installs gsed

则可以`gsed xxx` 执行了。

比如在处理es的时候，需要在data.json 偶数行(数据)加上时间，原始数据如下：

```json
{"index":{"_index":"shakespeare","_type":"act","_id":0}}
{"line_id":1,"play_name":"Henry IV","speech_number":"","line_number":"","speaker":"","text_entry":"ACT I"}
{"index":{"_index":"shakespeare","_type":"scene","_id":1}}
{"line_id":2,"play_name":"Henry IV","speech_number":"","line_number":"","speaker":"","text_entry":"SCENE I. London. The palace."}
{"index":{"_index":"shakespeare","_type":"line","_id":2}}
....
```

那么可以这样处理：

```bash
$ gsed -i '2~2 s/{/{"timestamp":"2017-07-05 08:49:30.123",/g' data.json'
```


# Sed 简介

stream editor 流编辑器，主要就是正则匹配。

参数说明：

- s: 替换, sed 's/正则/替换值/g' file
- i: 原地修改

比如去掉html的tag标签：

```bash
# 其中的'[^>]' 指定了除了>的字符重复0次或多次。
$ sed 's/<[^>]*>//g' html.txt
```

指定行：

- 3s: 指定第三行
- 3,6s: 第3到第6行
- s/xx/xx/1: 只替换每一行的第一个xx
- s/xx/xx/2: 只替换每一行的第2个xx
- s/xx/xx/3g: 第3个以后

多个匹配：

```bash
# 第一个模式把第一行到第三行的my替换成your，第二个则把第3行以后的This替换成了That
$ sed '1,3s/my/your/g; 3,$s/This/That/g' my.txt
# 等效:
sed -e '1,3s/my/your/g' -e '3,$s/This/That/g' my.txt
```

# Sed 命令

- N命令
- a: append,如 `sed '$ a hello' my.txt ` 在最后一行添加
- i: insert ,如`sed "1 i hello" my.txt` 1i表明，其要在第1行前插入一行

还可以模式匹配：`sed "/fish/a hello" my.txt` /fish/a，这意思是匹配到/fish/后就追加一行

- c 替换匹配
- d 删除匹配， sed '/fish/d' my.txt, sed '2d' my.txt, sed '2, $d' my.txt
- p 打印
