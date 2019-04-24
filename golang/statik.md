---
title: golang statik静态资源二进制打包 
date: 2018-10-15 10:15:20
categories: avro
tags:
	- 序列化
	- avro

---

[statik](https://github.com/rakyll/statik) 是golang 将静态资源编译进二进制文件的一个库，有很多databoard等web component通过这个工具来处理，如 https://github.com/BeginMan/ElasticHD 还是很cool的。

官方给的例子也不错：https://github.com/rakyll/statik/tree/aa8a7b1baecd0f31a436bf7956fcdcc609a83035/example



**基于此能做什么呢？**

1. 将静态资源打包进去
2. 打包前后端成一个可执行程序

