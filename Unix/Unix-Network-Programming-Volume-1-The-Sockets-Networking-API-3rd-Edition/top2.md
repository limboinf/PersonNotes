第二章： 传输层:TCP、UDP和SCTP

# 一. TCP/IP协议概况
![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/tcp_ip_summary.png)

如下每个协议简介：

- IPv4: 网际协议版本4(Internet Protocol version 4), 使用32位地址
- IPv6: 网际协议版本6(Internet Protocol version 6), 使用128位地址，是IPv4替代品，通常把它两者称为”IP“
- TCP: 传输控制协议(Transmission Control Protocol).TCP是一个**面向连接**的协议，为用户进程提供**可靠**的**全双工字节流**， TCP套接字是一种**流套接字(stream sockte)**, 关心**确认**, **超时**, **重传**等细节
- UDP: 用户数据报协议(User Datagram Protocol), UDP是一个**无连接**协议， UDP套接字是一种**数据报套接字(datagram socket)**。
- SCTP：流控制传输协议(Stream Control Transmission Protocol).SCTP是一个提供**可靠全双工关联的面向连接的协议**，
- ICMP：网际控制消息协议(Internet Control Message Protocol), 处理在路由器和主机之间流通的错误和控制消息。
- ICMPv6：网际控制消息协议版本6
- IGMP: 网际组管理协议,用于多播
- ARP: 地址解析协议(Address Resolution Protocol),把IPv4地址映射成一个硬件地址(如以太网地址)
- RARP: 反地址解析协议(Reverse..), 将硬件地址映射成IPv4地址
- BPF: BSD分组过滤器

# 二. TCP通信三部曲
如下总图：

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/tcp-ip-handshark.png)

- 建立：三次握手
- 传输：超时重传、快速重传、流量控制、拥塞控制等
- 断开：四次挥手

## 2.1 三次握手(Three-Way Handshake)

1. Server 准备接受外来连接, done by calling `socket`,`bind`,`listen`.服务端被动打开
2. Client 调用`connect`主动打开(active open),  client TCP 发送"synchronize" (`SYN`)分节,告诉Server有一个Client将在(待建立)连接中发送的数据的初始化序号。通常`SYN`不携带任何数据，仅包括 an IP header, a TCP header, and possible TCP options
3. Server 应答(acknowledge (ACK)) the client's SYN, 同时自己也发送一个SYN分节，包含Server将在同一连接中发送的数据的初始化序号。服务器发送自己的SYN,并对Client's SYN确认(ACK).
4. client ACK the server's SYN

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/three_way_handshark.png)

Clinet 初始化序列号为J, Server初始化序列号为K， ACK为 SYN+1（K+1),因为SYN占据一个字节的序列号空间，所以ACK确认号则是SYN+1.

## 2.2 TCP选项
- MSS option:告诉对端的最大分节大小( maximum segment size),也就是每个TCP连接发送的最大数据量.
- Window scale option:TCP最大窗口大小为65535
- Timestamp option: 时间戳选项，在网络编程中我们无需考虑

## 2.3 TCP连接终止

1. 某个应用进程首先调用`close`(主动关闭(active close)),该端TCP发送一个FIN分节表示数据发送完毕
2. 接收端被动关闭(passive close),FIN由TCP确认，它的接收作为一个**文件结束符(end-of-file)**传递给接收端应用程序，意味着接收端再无数据可接收。
3. 一段时间后接收这个文件结束符的应用程序将调用`close`关闭其套接字，这导致它的TCP也发送一个SYN
4. 接收这个最终FIN的原发送端TCP（即主动关闭的那一端）确认这个FIN

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/tcp_connection_termination.png)

## 2.4 TCP状态转换图
TCP涉及连接和断开的操作可由TCP状态转换图来说明.TCP协议的操作可以使用一个具有11种状态,图中的圆角矩形表示状态，箭头表示状态之间的转换，各状态的描述如下所示。图中用粗线表示客户端主动和被动的服务器端建立连接的正常过程：客户端的状态变迁用粗实线，服务器端的状态变迁用粗虚线。细线用于不常见的序列，如复位、同时打开、同时关闭等。图中的每条状态变换线上均标有“事件／动作”：事件是指用户执行了系统调用（ CONNECT 、 LISTEN 、 SEND 或 CLOSE ）、收到一个报文段（ SYN 、 FIN 、 ACK 或 RST ）、或者是出现了超过两倍最大的分组生命期的情况；动作是指发送一个报文段（ SYN 、 FIN 或 ACK ）或什么也没有（用“－”表示）。

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/tcp_status_summary.jpeg)

上图粗实线表示客户的正常路径；粗虚线表示服务器的正常路径；细线表示不常见的事件。

**每个连接均开始于 CLOSED 状态。当一方执行了被动的连接原语（ LISTEN ）或主动的连接原语（ CONNECT ）时，它便会脱离 CLOSED 状态。如果此时另一方执行了相对应的连接原语，连接便建立了，并且状态变为 ESTABLISHED 。任何一方均可以首先请求释放连接，当连接被释放后，状态又回到了 CLOSED 。**

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/tcp_status.jpeg)

### 2.4.1 状态表：

状 态 | 描 述
----|------
CLOSED | 关闭状态，没有连接活动或正在进行  
LISTEN | 监听状态，服务器正在等待连接进入  
SYN RCVD | 收到一个连接请求，尚未确认
SYN SENT | 已经发出连接请求，等待确认
ESTABLISHED | 连接建立，正常数据传输状态
FIN WAIT 1 | （主动关闭）已经发送关闭请求，等待确认
FIN WAIT 2 | （主动关闭）收到对方关闭确认，等待对方关闭请求
TIMED WAIT | 完成双向关闭，等待所有分组死掉
CLOSING | 双方同时尝试关闭，等待对方确认
CLOSE WAIT | （被动关闭）收到对方关闭请求，已经确认
LAST ACK | 被动关闭）等待最后一个关闭确认，并等待所有分组死掉


通过下图进行分析：

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/tcp-ip-handshark.png)

### 2.4.2 TCP连接状态

1. CLOSED：起始点，在超时或者连接关闭时候进入此状态，这并不是一个真正的状态，而是这个状态图的假想起点和终点。
2. LISTEN：服务器端等待连接的状态。服务器经过 socket，bind，listen 函数之后进入此状态，开始监听客户端发过来的连接请求。此称为应用程序被动打开（等到客户端连接请求）
3. SYN_SENT：第一次握手发生阶段，客户端发起连接。客户端调用 connect，发送 SYN 给服务器端，然后进入 SYN_SENT 状态，等待服务器端确认（三次握手中的第二个报文）。如果服务器端不能连接，则直接进入CLOSED状态。
4. SYN_RCVD：第二次握手发生阶段，跟 3 对应，这里是服务器端接收到了客户端的 SYN，此时服务器由 LISTEN 进入 SYN_RCVD状态，同时服务器端回应一个 ACK，然后再发送一个 SYN 即 SYN+ACK 给客户端。状态图中还描绘了这样一种情况，当客户端在发送 SYN 的同时也收到服务器端的 SYN请求，即两个同时发起连接请求，那么客户端就会从 SYN_SENT 转换到 SYN_REVD 状态。
5. ESTABLISHED：第三次握手发生阶段，客户端接收到服务器端的 ACK 包（ACK，SYN）之后，也会发送一个 ACK 确认包，客户端进入 ESTABLISHED 状态，表明客户端这边已经准备好，但TCP 需要两端都准备好才可以进行数据传输。服务器端收到客户端的 ACK 之后会从 SYN_RCVD 状态转移到 ESTABLISHED 状态，表明服务器端也准备好进行数据传输了。这样客户端和服务器端都是 ESTABLISHED 状态，就可以进行后面的数据传输了。所以 ESTABLISHED 也可以说是一个数据传送状态。

### 2.4.3 TCP断开状态

1. FIN_WAIT_1：第一次挥手。主动关闭的一方（执行主动关闭的一方既可以是客户端，也可以是服务器端，这里以客户端执行主动关闭为例），终止连接时，发送 FIN 给对方，然后等待对方返回 ACK 。调用 close() 第一次挥手就进入此状态。
2. CLOSE_WAIT：接收到FIN 之后，被动关闭的一方进入此状态。具体动作是接收到 FIN，同时发送 ACK。之所以叫 CLOSE_WAIT 可以理解为被动关闭的一方此时正在等待上层应用程序发出关闭连接指令。前面已经说过，TCP关闭是全双工过程，这里客户端执行了主动关闭，被动方服务器端接收到FIN 后也需要调用 close 关闭，这个 CLOSE_WAIT 就是处于这个状态，等待发送 FIN，发送了FIN 则进入 LAST_ACK 状态。
3. FIN_WAIT_2：主动端（这里是客户端）先执行主动关闭发送FIN，然后接收到被动方返回的 ACK 后进入此状态。
4. LAST_ACK：被动方（服务器端）发起关闭请求，由状态2 进入此状态，具体动作是发送 FIN给对方，同时在接收到ACK 时进入CLOSED状态。
5. CLOSING：两边同时发起关闭请求时（即主动方发送FIN，等待被动方返回ACK，同时被动方也发送了FIN，主动方接收到了FIN之后，发送ACK给被动方），主动方会由FIN_WAIT_1 进入此状态，等待被动方返回ACK。
6. TIME_WAIT：从状态变迁图会看到，四次挥手操作最后都会经过这样一个状态然后进入CLOSED状态。共有三个状态会进入该状态：
	- 由CLOSING进入：同时发起关闭情况下，当主动端接收到ACK后，进入此状态，实际上这里的同时是这样的情况：客户端发起关闭请求，发送FIN之后等待服务器端回应ACK，但此时服务器端同时也发起关闭请求，也发送了FIN，并且被客户端先于ACK接收到。
	- 由FIN_WAIT_1进入：发起关闭后，发送了FIN，等待ACK的时候，正好被动方（服务器端）也发起关闭请求，发送了FIN，这时客户端接收到了先前ACK，也收到了对方的FIN，然后发送ACK（对对方FIN的回应），与CLOSING进入的状态不同的是接收到FIN和ACK的先后顺序。
	- 由FIN_WAIT_2进入：这是不同时的情况，主动方在完成自身发起的主动关闭请求后，接收到了对方发送过来的FIN，然后回应 ACK。

## 2.5 观察分组(Watching the Packets)

如下图展示完整的tcp分组过程包括连接，传输和终止。

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/pocktes.png)

## 2.6 TIME_WAIT状态
这是TCP网络编程中比较难理解且又重要的一个状态，这里我参考[网络编程释疑之：TCP的TIME_WAIT状态在服务器开发中的影响？](http://yaocoder.blog.51cto.com/2668309/1338567) 这篇文章：

**高并发TCP服务器中进行主动关闭的一方最好是客户端、服务器端程序最好启用SO_REUSEADDR选项**

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/203639589.jpg)

可以看出TIME_WAIT状态是执行主动关闭的那一端产生的。

**TIME_WAIT状态有两个存在的理由**:

1. 可靠地实现TCP全双工连接的终止；
2. 允许老的重复分节在网络中消逝；

第一个理由参考上图。 假设主动关闭端最终发送的ACK丢失了。对端将重新发送FIN，主动关闭端只有在维护状态信息的情况下才可以重新发送最终的那个ACK。如果不维护这个状态信息，主动关闭端将会响应一个`RST`，对端会将此响应标记为错误，所以**不能进行正常的关闭**。

第二个理由假设我们在ip A:端口B主机和ip C:端口D主机之间建立一个TCP连接。我们关闭这个连接，过一段时间在相同的IP地址和端口之间建立另一个连接。由于他们的IP地址和端口号都相同，所以如果上一个连接的老的重复分组再出现会影响新的连接。为了做到这一点，TCP将不会给处于TIME_WAIT状态的连接发起这个新的连接。这个持续时间如果大于**MSL**（IP数据报在因特网中的最大生存时间）

如果要满足以上实现，TIME_WAIT状态必须要有一定的持续时间，所以TIME_WAIT也被称为**2MSL等待状态**，一般持续时间在**1分钟到4分钟之间**。

**高并发TCP服务器中进行主动关闭的一方最好是客户端**：因为对于高并发服务器来说文件描述符资源是很重要的资源，如果对于每一个连接都要经历TIME_WAIT这个2MSL的时长，势必造成资源不能立马复用的浪费。虽然对于客户端来说TIME_WAIT状态会占用端口和句柄资源，但是客户端一般很少有并发资源限制，所以客户端执行主动关闭是比较合适的。

**服务器端程序最好启用SO_REUSEADDR选项**：我们想这样做一种情况，如果生产环境中服务端程序由于某种错误操作关闭了，我们肯定是要立马重启服务程序，但是TIME_WAIT还在占用着这些地址端口资源让你的服务起不来，那你着不着急。SOREUSEADDR这个选项正是允许地址端口的重复绑定。

## 2.7 端口号

![](https://raw.githubusercontent.com/BeginMan/BookNotes/master/Unix/media/ports.png)

## 2.8 套接字对
一个 TCP 连接由一个套接字对( Socketpair )标识,套接字对是表示 TCP 连接的两个端点的四元组: (本地 IP 地址,本地 TCP 端口号;远程 IP 地址,远程 TCP 端口号)

标识两个端点的两个值(IP地址和端口号)称为**套接字**

## 2.8 缓冲区大小和限制
主要讲IP数据报大小的限制。

- IPv4 数据报最大大小为2的16次方-1， 65535个字节(64K),这里面还包含IPv4的首部，总长度字段占16位
- IPv6 数据报最大为65575(在IPv4基础上加40), 包括40字节的IPv6首部，IPv6净荷长度字段占16位，其还有特大净荷选项能扩展至32位，这个选项需要**最大传输单元(maximum transmission unit (`MTU`))超过65535的数据链路提供支持**。
- 许多网络有一个可由硬件规定的MTU，如以太网MTU为1500字节
- 路径MTU
- 当一个IP数据报从某个接口送出时，如果大小超过相应链路的MTU则IPv4和IPv6要进行**分片**
- 最小重组缓冲区大小，是IPv4和IPv6定义的最小数据报大小
- MSS,最大分节大小，告诉对端每个分节最大能发送的TCP数据量



参考：

- [ 【Unix 网络编程】TCP状态转换图详解](http://blog.csdn.net/wenqian1991/article/details/40110703)
- [TCP连接释放与TCP状态图 ](http://blog.sina.com.cn/s/blog_417b97470100ohv1.html)







