[alpine linux](https://alpinelinux.org/) 基于musl libc和busybox的面向安全的轻量级Linux发行版，官网标注：

>Small. Simple. Secure.

很小很强悍，通过docker pull 拉下来的镜像不超过5Mb，基于alpine构建的镜像，如java, node, nginx，也就是几十兆，如果通过ubuntu构建，那起码上百兆了。

![](http://beginman.qiniudn.com/2018-01-08-15153797664166.jpg)

**Alpine非常适合作为容器的基础镜像.**

alpine通过 apk来管理安装包，使用的时候最好更改下源文件 /etc/apk/repositories，如使用阿里云：

```bash
https://mirrors.aliyun.com/alpine/v3.6/main/
https://mirrors.aliyun.com/alpine/v3.6/community/
```

使用的时候先：`apk update` 更新APK软件包仓库的索引文件，然后`apk search`相关包。`apk help` 查看帮助。

在容器中，查看Alpine容器的IP地址： `ip a`

可以启动它，进去玩玩：

```bash
$ docker run --rm -it --name myalpine alpine
```

Alpine来替代ubuntu,centos等作为基础镜像是大势所趋..


