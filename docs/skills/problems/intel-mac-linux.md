Intel Mac 用的是 Broadcom Wi-Fi 芯片，而 Broadcom 对 Linux 极度不友好。

绝大部分普通笔记本用的是：

- Intel Wi-Fi（Linux 原生驱动，稳定）
- Realtek Wi-Fi（Linux 驱动一般，但可用）

Intel MacBook 用的是 Broadcom BCM4360 / BCM43xx 系列。这个厂商的特点是：

- 不开放驱动源码
- 不支持 Linux 内核直接驱动
- 需要闭源专用驱动（`bcmwl-kernel-source`）
- Ubuntu 默认不带这类驱动（版权问题）

## 解决方案

最稳定的方式是安装 Broadcom 驱动 `bcmwl-kernel-source`。

你现在需要一个临时网络，可以通过：

- 手机 USB 网络共享（最简单）
- 有线 USB 网卡
- 临时借别人开热点

有网络后（用有线数据线连接手机，手机开热点，以太网连接，手机相当于一个路由器），在终端输入：

```bash
sudo apt update
sudo apt install bcmwl-kernel-source
sudo reboot
```
