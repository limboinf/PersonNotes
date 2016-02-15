这里接上节，一篇总结太多太啰嗦，故而多篇分而治之。

# 一.TIME_WAIT状态

- TIME_WAIT存在的两个原因
- 坚持2MSL的原因
- 有时候避免使用TIME_WAIT的原因，如果关闭后需要立即重用，TIME_WAIT状态占用着端口不能复用，客户端重启失败。这里说的是服务器端，因为客户端使用的端口是系统
随机生成的，如果服务器端主动关闭连接后异常终止，则因为服务器使用的是知名端口，则在TIME_WAIT状态时，它不能立即重启。

# 二.复位报文段
`RST`标识：复位报文段，通知对方关闭连接或重新建立连接。适用下面三种场景：

## 1.访问不存在的端口

    #只监听发送和接收至54321端口TCP报文段
    tcpdump -nt -i eth1 port 54321
    
    #访问
    telnet 192.168.0.120 54321

如上测试访问120机器上不存在的端口号54321，则抓取如下：

    Trying 192.168.0.120...
    telnet: connect to address 192.168.0.120: Connection refused
    telnet: Unable to connect to remote host

120机器：

    IP 192.168.0.103.58705 > 192.168.0.120.54321: Flags [S], seq 2755519932, win 65535, options [mss 1460,nop,wscale 5,nop,nop,TS val 279283203 ecr 0,sackOK,eol], length 0
    IP 192.168.0.120.54321 > 192.168.0.103.58705: Flags [R.], seq 0, ack 2755519933, win 0, length 0

看到了`R`标识，且复位报文段的接收通告窗口大小为0，所以可以预见：收到复位报文段的一端应该关闭连接或者重新连接，而不能回应这个复位报文段。当端口处于TIME_WAIT状态时也会出现复位报文段。

## 2.异常终止连接

当一端发送复位报文段后就会触发异常终止连接，发送端所有排队待发送的数据都会被丢弃。

## 3.处于半打开连接

半打开状态可以发生在服务器或客户端，往往是网络故障导致的，一端还连着呢，另一端已经丢弃了该连接，则写入时会对方则回应一个复位报文段。

书上例子用`nc`命令模拟，然后拔掉网线中断服务器模拟半打开状态。`nc`命令很强大啊，参考[nc命令详解](http://www.cnblogs.com/wenbiao/p/3375811.html).

# 三. TCP交互数据流
这里在120机器上执行：

    # 模拟回显服务器
    nc -l 12345

    # 监听
    tcpdump -nt -i eth1 port 12345

在103机器上远程访问回显服务器并发送数据：

    telnet 192.168.0.120 12345
    Trying 192.168.0.120...
    Connected to 192.168.0.120.
    Escape character is '^]'.
    good

则可看到120抓取的数据如下：

    IP 192.168.0.103.59450 > 192.168.0.120.italk: Flags [S], seq 500556981, win 65535, options [mss 1460,nop,wscale 5,nop,nop,TS val 282013680 ecr 0,sackOK,eol], length 0
    IP 192.168.0.120.italk > 192.168.0.103.59450: Flags [S.], seq 2945537075, ack 500556982, win 14480, options [mss 1460,sackOK,TS val 3546530879 ecr 282013680,nop,wscale 9], length 0
    IP 192.168.0.103.59450 > 192.168.0.120.italk: Flags [.], ack 1, win 4117, options [nop,nop,TS val 282013681 ecr 3546530879], length 0
    IP 192.168.0.103.59450 > 192.168.0.120.italk: Flags [P.], seq 1:7, ack 1, win 4117, options [nop,nop,TS val 282017633 ecr 3546530879], length 6

# 四.TCP成块数据流
如ftp传递大文件发送方会连续发送多个TCP报文段，接收方可以一次确认所有这些报文段。

# 五.拥塞控制

>TCP一个重要的功能是提高网络利用率，减低丢包率，保证每条数据流的公平性，这就是拥塞控制。

拥塞控制的四部分：

- 慢启动
- 拥塞避免
- 快速重传
- 快速恢复

over

