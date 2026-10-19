## 方法一

```bash
vim ~/.bash_profile
```

```bash
alias proxy="
    export http_proxy=socks5://127.0.0.1:7890;
    export https_proxy=socks5://127.0.0.1:7890;
    export all_proxy=socks5://127.0.0.1:7890;
    export no_proxy=socks5://127.0.0.1:7890;
    export HTTP_PROXY=socks5://127.0.0.1:7890;
    export HTTPS_PROXY=socks5://127.0.0.1:7890;
    export ALL_PROXY=socks5://127.0.0.1:7890;
    export NO_PROXY=socks5://127.0.0.1:7890;"
alias unproxy="
    unset http_proxy;
    unset https_proxy;
    unset all_proxy;
    unset no_proxy;
    unset HTTP_PROXY;
    "
```

## 方法二

NAT + TUN。虚拟机处于 NAT 模式时，Ubuntu 发出的连接由宿主机上的虚拟机进程代为发出。Clash 以管理员身份开启 TUN 后，会在 Windows 里建立一张虚拟网卡并接管本机出站流量，虚拟机进程的连接也在其中，于是被转进代理。Ubuntu 自己没有代理配置，它只是把流量交给了 NAT。

## 方法三

桥接 + 指向 Windows 的局域网 IP。桥接后，虚拟机和 Windows 是同一局域网里的两台机器，Ubuntu 能直接访问 Windows 的局域网地址。打开 ALLOW LAN，让 Clash 的代理端口监听在这块网卡上，而不只是本机回环地址。Ubuntu 把 `http_proxy`、`https_proxy` 指到 Windows 局域网 IP 和端口后，认代理的程序会主动把请求发给 Clash，再由 Clash 转发出去。
