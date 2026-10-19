学长的博客搭建笔记：<https://cs.haohaha.cn/03-blog/01-init/tutorial/>

## 搭建过程疑问的解决笔记

我通常在 Repo 这个文件夹及其子文件设置了与 GitHub 的连接，其中 fy-blog 文件夹用来写博客，GitHub 也有同名仓库。现在我在 Obsidian 文件夹下将 Repo 拷贝了过来，然后用这个新的 Repo 作为我与 GitHub 建立连接的文件树根。我正在尝试重新将新的 fy-blog 连接至远程仓库，但 GitHub 报错，说已经存在 fy-blog 这个仓库。是不是需要删除这个仓库，然后重新输入这些连接命令？

```text
fy-blog on master [!]
git config --global user.name "fighteryyds"
git config --global user.email "1591715509@qq.com"
git remote add fy-blog GITHUB_REMOTE
error: remote fy-blog already exists.
```

你本地的新 fy-blog 目录里已经拷贝了原仓库的 `.git`，所以远端别名 fy-blog 也一起复制过来了。`git remote add fy-blog …` 会提示已存在，就是因为这个别名本来就在。不需要删除 GitHub 上的仓库。

现在的远端配置已经指向 `git@github.com:fighteryyds/fy-blog.git`（`git remote -v` 里能看到），所以直接用它推送即可，例如：

```bash
git push fy-blog master
```

如果只是想确认或修改远端地址，可以用：

```bash
git remote set-url fy-blog git@github.com:fighteryyds/fy-blog.git
```

要换个别名也可以：

```bash
git remote rename fy-blog origin
```

总之无需重建仓库，把之前的连接信息继续沿用就能推送。

## 什么是 .git，为什么可以直接沿用之前的连接信息？

`.git` 是 Git 仓库的「配置和历史档案库」。它是一个隐藏目录，里面保存了所有提交历史、对象文件、分支指针、暂存区、钩子脚本，以及仓库级的配置（比如 `.git/config` 中的远端地址）。当你把整个项目文件夹拷贝到新位置时，如果连同 `.git/` 一起复制，就等于完整搬运了整个仓库，包括远端信息和所有提交历史。因此在新位置打开仓库时，Git 会继续使用 `.git/config` 里记下的远端 fy-blog，你无需重新设置。只有在把 `.git/` 删掉或刻意新建仓库时，才需要重新 `git init` 并手动添加远端。
