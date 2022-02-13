# GOS

# 前言

GOS是一个GTAV进程快速结束工具，能做到一键结束进程、一键结束全部队友进程，能阻止GTA数据上传，有效提升GTAV犯罪之神任务的通过率。

# 服务端搭建

GOS需要一个服务器或有公网IP的主机来搭建一个服务端，通过服务端协同各个用户。

## Linux

克隆项目到本地：

```bash
git clone https://github.com/MRKKmrkk/GOS.git
```

进入GOS目录后执行以下命令开启服务端

```bash
nohup python3 gos/gosServer.py ip port &
```

## Windows

暂未开发，小伙伴们可以自行研究

## 客户端使用GOS

将GOS压缩包下载解压到本地后，进入gos目录，双击gosClient.exe即可运行GOS，会出现以下界面:

![Untitled](Scala%20%E4%B8%AD%E7%9A%84%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E7%89%B9%E6%80%A7%20bf05f82bd1994b58abac11737d9e00b7/Untitled.png)

在server host和server port 文本框中，输入服务端对应的IP和端口，点击connect即可和服务端进行链接，如若出现 ”`connect success!`”则表示链接成功。

链接成功后，单机”Kill GTAV"按钮即可向服务端发送关闭指令，服务端会向所有连接成功的用户发送关闭指令，达到关闭全部队友GTAV进程的效果。

也可以单机”only Kill my GTAV”按钮，此时只会关闭自己电脑上的GTAV进程。此按钮无线与服务器建立链接也能使用。
