# 日笺

张佳昕的日记。写法和原来的 [fy-blog](https://fighteryyds.github.io/fy-blog/) 一样：MkDocs Material，日记是一篇 Markdown。

本地文件夹用图里的 **Repo2**。旧的 **Repo** 仍连着旧账号 `fighteryyds`，不要改它。新的远程仓库用 GitHub 账号 [fighteryyds-creater](https://github.com/fighteryyds-creater)。

## 一天怎么写

打开 `docs/index.md`，把新的一天放在文件最上面：

```markdown
### 2026.10.18

今天写了什么。

- 可以写列表
- 也可以写 `代码`

![ ](index/照片.jpg)
```

日期不补零，和旧博客一致，例如 `2026.10.18`、`2025.4.21`。

照片放在 `docs/index/`。也可以在仓库根目录运行：

```bash
./new-day.sh
```

它会在 `docs/index.md` 顶部补上今天的标题。今天已经有这一节时，不会再写一遍。

技术笔记在 `docs/skills/`，考研笔记在 `docs/kaoyan/`，友链在 `docs/youlian.md`。栏目和旧站相同。

## 在 Repo2 里预览

```bash
cd /path/to/Repo2
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

浏览器打开 <http://127.0.0.1:8000>。

## 接到新的 GitHub 账号

在 GitHub 账号 `fighteryyds-creater` 下新建一个空仓库，名字用 `Repo2`（不要勾选自动生成 README）。然后在本地 Repo2 文件夹里：

```bash
git init
git add .
git commit -m "日起一本新的日记"
git branch -M main
git remote add origin git@github.com:fighteryyds-creater/Repo2.git
git push -u origin main
```

推送到 `main` 或 `master` 后，`.github/workflows/ci.yml` 会安装 MkDocs 并发布到 `gh-pages`。仓库 Settings → Pages 里把来源选成 `gh-pages` 分支。站点地址是：

<https://fighteryyds-creater.github.io/Repo2/>

如果仓库不叫 `Repo2`，改 `mkdocs.yml` 里的 `site_url`、`repo_url` 和 `extra.homepage`，让它们和真实仓库名一致，否则页面上的样式路径会错。
