# fy_blog

张佳昕的日记。结构和原来的 [fy-blog](https://github.com/fighteryyds/fy-blog) 一样，站点版式也和 [fighteryyds.github.io/fy-blog](https://fighteryyds.github.io/fy-blog/) 一样。

远程仓库是 [fighteryyds-creater/fy_blog](https://github.com/fighteryyds-creater/fy_blog)。本地文件夹用 Repo2。

```
docs/index.md            主页，一天一个 ### 2026.10.18
docs/index/              日记照片
docs/skills/             技术：Linux、C 语言、文章、书籍、技术问题的解决
mkdocs.yml               顶栏：主页 / 技术
```

预览：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

写完一天后推到 `main`，Actions 会发布到 <https://fighteryyds-creater.github.io/fy_blog/>。

## 排版

正文按 [这篇回答](https://www.zhihu.com/question/41802793/answer/2435610889) 里的「排版规范化」来写：

- 中文和英文、中文和数字之间加空格：`GitHub 于 2007 年 10 月 19 日上线。`
- 数字和单位写在一起：`15%`、`10Gbps`，不写成 `15 %`、`10 Gbps`。`4K`、`1080p`、`iOS 13` 按官方写法。
- 超链接前后加空格。
- 段落不要首行缩进。
- 中文引号用「」，里面一层用『』。省略号用「……」。
- 中文句子用全角标点。整句英文，或专有名词里的标点，保持原样。
- 专有名词用官方大小写，例如 `GitHub`。
- 需要强调时用加粗，不用斜体。

已经写好的笔记可以用 `python3 scripts/apply-typography.py docs/index.md docs/skills` 再跑一遍。代码块不会改。
