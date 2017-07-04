ssh config -> control SSH Session. 位置：

- 用户配置文件 (~/.ssh/config)
- 系统配置文件 (/etc/ssh/ssh_config)

通过`Host`来加载不同segment. SSH配置项：

- Host 别名
- HostName 主机名, 指定远程主机名，可以直接使用数字IP地址。如果主机名中包含 `%h` ，则实际使用时会被命令行中的主机名替换。
Port 端口
User 用户名, 指定登录用户名。
IdentityFile 密钥文件的路径
IdentitiesOnly 只接受SSH key 登录
PreferredAuthentications 强制使用Public Key验证

```bash
'%d' 本地用户目录
'%u' 本地用户名称
'%l' 本地主机名
'%h' 远程主机名
'%r' 远程用户名
```

如下实例：

```bash
# config
Host elk
  HostName ip-10-1-11-39
  Port 22
  User root
  IdentityFile  ~/.ssh/id_rsa
  IdentitiesOnly yes
Host hadoop
  HostName ip-10-1-19-39
  Port 22
  User root
  IdentityFile  ~/.ssh/id_rsa
  IdentitiesOnly yes
```

则可直接：`ssh elk` 或 `ssh hadoop`登录指定远程主机。

在使用Git多账号的时候也会用到，如：

```bash
$ cat ~/.ssh/config
# coding.net
Host myCoding
HostName coding.net
User git
IdentityFile /Users/fangpeng/.ssh/id_rsa

# github
Host github.com
HostName github.com
User git
IdentityFile /Users/fangpeng/.ssh/id_rsa

# gitlab
host beginman.com.cn
HostName beginman.com.cn
RSAAuthentication yes
User git
IdentityFile /Users/fangpeng/.ssh/id_rsa_gitlab

### check ########################################
## ~ ssh -T git@github.com
## Hi BeginMan! You've successfully authenticated, but GitHub does not provide shell access.
##
## ~ ssh -T git@gitlab.com
## Welcome to GitLab, BeginMan!
##
## ~ ssh -T git@git.coding.net
## Hello beginman You've connected to Coding.net by SSH successfully!
##
### check ########################################

```

ref: https://www.hi-linux.com/posts/14346.html



