# 查看哪些端口被打开  

	netstat -anp

# 查看端口占用情况:如 80

	lsof -i tcp:80


# 打开端口号

	iptables -A INPUT -ptcp --dport  端口号 -j ACCEPT

如开启80端口：

	#方法一：
 
    /sbin/iptables -I INPUT -p tcp --dport 80 -j ACCEPT   #写入修改
    /etc/init.d/iptables save   # 保存修改
    service iptables restart    # 重启防火墙，修改生效

    #方法二：

    vi /etc/sysconfig/iptables  # 打开配置文件加入如下语句:
    -A INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT   # 重启防火墙，修改完成
 


# 关闭端口号
	
	iptables -A INPUT -p tcp --drop 端口号 -j DROP
    iptables -A OUTPUT -p tcp --dport 端口号 -j DROP


如关闭80端口：

	#方法一：
 
    /sbin/iptables -I INPUT -p tcp --dport 80 -j DROP   #写入修改
    /etc/init.d/iptables save   #保存修改
    service iptables restart     #重启防火墙，修改生效
 
    方法二：
 
    vi /etc/sysconfig/iptables  # 打开配置文件加入如下语句:
    -A INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j DROP   #重启防火墙，修改完成

# 查看端口状态

    /etc/init.d/iptables status






