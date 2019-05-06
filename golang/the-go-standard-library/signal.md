## 信号量

"os/signal", 主要是`signal.Notify( chan<- os.Signal, sig ...os.Signal)`

监听信号，将信号传递给channel c, 如果没传sig, 默认监听全部

示例：Signal 实现程序优雅退出

```go
package main

import (
    "fmt"
    "os"
    "os/signal"
    "syscall"
)

func main() {
    done := make(chan os.Signal, 1)
    // SIGINT: Ctrl-C，SIGTERM: terminate
    signal.Notify(signalChan, syscall.SIGINT, syscall.SIGTERM)
    <-done 
    // 可在下面做些回收处理工作
    fmt.Println("exit...") 
}
```

golang的信令处理感觉比Python干净利索，Python 程序优雅退出示例：

```python
import sys
import time
import signal


class GracefulExit:
	
	running = True

	def __init__(self):
		signal.signal(signal.SIGINT, self.exit_gracefully)
		signal.signal(signal.SIGTERM, self.exit_gracefully)


	def exit_gracefully(self, sig, frame):
		self.running = False


def main():
	print("starting ...")
	app = GracefulExit()
	while 1:
		time.sleep(1)
		print("main loop ...")
		if app.running is False:
			break

	print("finished ...")
	# 清理工作


if __name__ == '__main__':
	main()
```



案例：

- [burrow-exporter.go](<https://github.com/BeginMan/burrow_exporter/blob/master/burrow-exporter.go>)
- [从burrow学主函数控制]([https://github.com/BeginMan/PersonNotes/blob/55ea3bdff2e3d639bba5438fc9864c895651a320/golang/%E4%BB%8Eburrow%E5%AD%A6%E4%B8%BB%E5%87%BD%E6%95%B0%E6%8E%A7%E5%88%B6.md](https://github.com/BeginMan/PersonNotes/blob/55ea3bdff2e3d639bba5438fc9864c895651a320/golang/从burrow学主函数控制.md))
- [python rq 消息队列框架 worker.py](<https://github.com/rq/rq/blob/0d593f40e1efcf2bead67b8bade91d0f3477bf61/rq/worker.py#L358>)

