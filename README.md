# fy_blog

张佳昕的日记。结构和原来的 [fy-blog](https://github.com/fighteryyds/fy-blog) 一样，站点版式也和 [fighteryyds.github.io/fy-blog](https://fighteryyds.github.io/fy-blog/) 一样。

远程仓库是 [fighteryyds-creater/fy_blog](https://github.com/fighteryyds-creater/fy_blog)。本地文件夹用 Repo2。

```
docs/index.md            主页，一天一个 ### 2026.10.18
docs/index/              日记照片
docs/youlian.md          友链
docs/skills/             技术：Linux、c语言、文章、书籍、github&git
docs/kaoyan/             考研：题目、思想
docs/habit/painting.md   习惯
mkdocs.yml               顶栏：主页 / 技术 / 考研
```

预览：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

写完一天后推到 `main`，Actions 会发布到 <https://fighteryyds-creater.github.io/fy_blog/>。
