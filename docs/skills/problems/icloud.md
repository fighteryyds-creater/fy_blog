## Obsidian 在 iCloud 中的位置

`~/Library/Mobile Documents/iCloud~md~obsidian/Documents`

## iCloud 的位置

```bash
cd ~/Library/Mobile Documents/com~apple~CloudDocs
```

短名字能直接 `cd`，靠的是符号链接。从当前目录里有一个叫 `obsidian` 的入口时，`cd obsidian` 就会进去，不用再打那一长串真实路径。

建立这个入口用的是 `ln -s`，不是 `link`：

```bash
ln -s /很长/的/真实路径 ~/obsidian
```

之后在家目录里执行 `cd obsidian`，实际进入的就是那条长路径。`ls -l ~/obsidian` 会显示箭头，例如 `obsidian -> /很长/的/真实路径`。

如果希望在任何目录都能一句进库，用别名更合适：

```bash
alias obsidian 'cd "/Users/zhangjiaxin/Library/Mobile Documents/iCloud~md~obsidian/Documents"'
```

在终端直接输入 `obsidian` 即可。
