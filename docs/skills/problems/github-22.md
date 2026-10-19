来源：<https://help.huacloud.dev/知识清单/github无法使用22端口拉取代码的解决方法>

有时，防火墙会完全拒绝允许 SSH 连接。如果使用 HTTPS 克隆凭据缓存选项，你可以尝试使用在 HTTPS 端口上建立的 SSH 连接进行克隆。大多数防火墙规则允许此操作，但代理服务器可能会干扰。GitHub Enterprise Server 用户：目前支持通过 SSH HTTPS 端口访问 GitHub Enterprise Server。

原文：<https://docs.github.com/en/authentication/troubleshooting-ssh/using-ssh-over-the-https-port>

## 测试 443 端口

要测试 SSH HTTPS 端口是否可行，请运行：

```bash
ssh -T -p 443 git@ssh.github.com
```

如果输出以下内容，则说明成功：

```text
Hi USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
```

主机名是 `ssh.github.com`，端口是 `443`。

如果成功了，就可以继续。如果没有成功，需要按照 GitHub 的故障排除指南操作。

克隆仓库：

```bash
git clone ssh://git@ssh.github.com:443/YOUR-USERNAME/YOUR-REPOSITORY.git
```

## 启用 SSH 走 HTTPS 端口

如果能够通过 `git@ssh.github.com` 的 443 端口进行 SSH 连接，可以覆盖 SSH 设置，让之后对 GitHub.com 的连接都走这个端口。

编辑 `~/.ssh/config`，加入：

```sshconfig
Host github.com
    Hostname ssh.github.com
    Port 443
    User git
```

测试：

```bash
ssh -T git@github.com
```

成功时同样会看到：

```text
Hi USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
```

## 更新已知主机

切换到端口 443 后，第一次连接 GitHub 时，可能会提示主机在 `known_hosts` 里找不到，但在另一个名称下找到了：

```text
The authenticity of host '[ssh.github.com]:443 ([140.82.112.36]:443)' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
This host key is known by the following other names/addresses:
  ~/.ssh/known_hosts:32: github.com
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

只要这里的指纹和 GitHub 公布的指纹一致，输入 `yes` 即可。指纹列表见 [GitHub 的 SSH 密钥指纹](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints)。
