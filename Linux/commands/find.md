find multiple query:

```bash
$ find . \( -name "*.py" -o -name "*.txt" \) -print
```

Notes: `()` 内留空格且`\`

`!` 否定参数：

```bash
$ find . ! -name "*.txt" -print
```

善用`file`命令：

```bash
$ file haha.jpg
haha.jpg: JPEG image data, JFIF standard 1.01

# 查找所有JPG
$ ls -lrt | awk '{print $9}'|xargs file|grep JPEG|awk '{print $1}'|tr -d ':'
```

**按时间搜索**

- atime 访问时间 (单位是天，分钟单位则是-amin，以下类似）
- mtime 修改时间 （内容被修改）
- ctime 变化时间 （元数据或权限变化）

更多内容参考：http://man.linuxde.net/find
