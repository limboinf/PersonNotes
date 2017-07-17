Linux 环境变量：

- /etc/profile，/etc/bashrc 是系统全局环境变量设定
- ~/.profile，~/.bashrc用户目录下的私有环境变量设定

当login获得shell进程时，读取环境变量的步骤：

1. 首先read /etc/profile -> /etc/profile.d, /etc/inputrc
2. 其次read 当前用户home下 ~/.bash_profile, 其次读取~/.bash_login, 最后读取 ~/.profile 
3. ~/.bashrc

**~/.profile与~/.bashrc的区别:**

- 这两者都具有个性化定制功能
- ~/.profile可以设定本用户专有的路径，环境变量等，**它只能登入的时候执行一次**
- ~/.bashrc也是某用户专有设定文档，可以设定路径，命令别名，**每次shell script的执行都会使用它一次**

如：

```bash
# .bashrc
alias lm='ls -al|more'
log=/opt/applog/common_dir

# .bash_profile
export PS1='$PWD#'
```

然后可以执行： `cd $log`
