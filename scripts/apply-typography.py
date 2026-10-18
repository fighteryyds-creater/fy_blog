#!/usr/bin/env python3
"""把正文整理成「排版规范化」里的写法。

代码围栏、缩进代码行、行内代码和链接地址不动。
规则来自 https://www.zhihu.com/question/41802793/answer/2435610889
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

CJK = re.compile(r"[\u4e00-\u9fff]")
TOKEN_RE = re.compile(
    r"(?P<code>``.+?``|`[^`\n]+?`)"
    r"|(?P<img>!\[[^\]]*\]\([^)\n]*\))"
    r"|(?P<link>(?<!!)\[[^\]\n]*\]\([^)\n]*\))"
    r"|(?P<html></?[A-Za-z][^>\n]*>)"
    r"|(?P<url>https?://[^\s<>)]+)"
)
UNITS = (
    r"Gbps|Mbps|Kbps|GBps|MBps|TB|GB|MB|KB|Gb|Mb|Kb|"
    r"GHz|MHz|kHz|Hz|px|dpi|bits|bit|ms|ns|mm|cm|km|kg|mAh"
)
FENCE_OPEN = re.compile(r"^(`{3,}|~{3,})")


def is_cjk(ch: str) -> bool:
    return bool(ch) and "\u4e00" <= ch <= "\u9fff"


def looks_like_code(line: str) -> bool:
    stripped = line.strip()
    return bool(
        re.search(
            r"(#include|#define|#if|printf\s*\(|fprintf\s*\(|scanf\s*\(|"
            r"\breturn\b|malloc\s*\(|;\s*$)",
            stripped,
        )
    )


def fix_quotes(text: str) -> str:
    text = text.replace("“", "「").replace("”", "」")
    text = re.sub(r"(?<=[A-Za-z])’(?=[A-Za-z])", "\uE000", text)
    chars = list(text)
    open_single = False
    for i, ch in enumerate(chars):
        if ch == "‘":
            chars[i] = "『"
            open_single = True
        elif ch == "’":
            chars[i] = "』" if open_single else "『"
            open_single = not open_single
    text = "".join(chars).replace("\uE000", "’")
    if '"' not in text or not CJK.search(text) or looks_like_code(text):
        return text
    chars = list(text)
    indexes = [i for i, ch in enumerate(chars) if ch == '"']
    if not indexes:
        return text
    if len(indexes) % 2 == 0:
        for n, i in enumerate(indexes):
            chars[i] = "「" if n % 2 == 0 else "」"
        return "".join(chars)
    for i in indexes:
        prev = chars[i - 1] if i else ""
        nxt = chars[i + 1] if i + 1 < len(chars) else ""
        if prev in "」』\\" or is_cjk(prev) or prev.isalnum():
            chars[i] = "」"
        elif is_cjk(nxt) or nxt.isalnum() or nxt == "\\":
            chars[i] = "「"
    return "".join(chars)


def fix_ellipsis(text: str) -> str:
    text = re.sub(r"。{3,}", "……", text)
    text = re.sub(r"(?<!…)…(?!…)", "……", text)

    def dots(match: re.Match[str]) -> str:
        start, end = match.span()
        before = text[start - 1] if start else ""
        after = text[end] if end < len(text) else ""
        if is_cjk(before) or is_cjk(after):
            return "……"
        return match.group(0)

    return re.sub(r"\.{3,}", dots, text)


def fix_repeat(text: str) -> str:
    text = re.sub(r"！{2,}", "！", text)
    text = re.sub(r"？{2,}", "？", text)
    text = re.sub(r"～{2,}", "～", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff])!{2,}", "！", text)
    text = re.sub(r"(?<!~)~{3,}(?!~)", "", text)
    return text


def fix_width(text: str) -> str:
    text = re.sub(r"(?<=[\u4e00-\u9fff]),", "，", text)
    text = re.sub(r",(?=\s*[\u4e00-\u9fff])", "，", text)
    text = re.sub(r"(?<=[」』])\s*,\s*(?=[\u4e00-\u9fff])", "，", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff])!+(?![\[(])", "！", text)
    text = re.sub(r"(?<![A-Za-z0-9])!(?=[\u4e00-\u9fff])", "！", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff])\?", "？", text)
    text = re.sub(r"\?(?=[\u4e00-\u9fff])", "？", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff）』」)])\s*:(?!:)", "：", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff]);", "；", text)
    text = re.sub(r";(?=[\u4e00-\u9fff])", "；", text)
    for punct in "，。！？：；、":
        text = re.sub(rf"{punct}[ \t]+(?=[\u4e00-\u9fff])", punct, text)
        text = re.sub(rf"(?<=[\u4e00-\u9fff])[ \t]+{punct}", punct, text)
    return text


def fix_parens(text: str) -> str:
    chars = list(text)
    i = 0
    while i < len(chars):
        if chars[i] != "(":
            i += 1
            continue
        k = i - 1
        while k >= 0 and chars[k] in " \t":
            k -= 1
        prev = chars[k] if k >= 0 else ""
        depth = 1
        j = i + 1
        while j < len(chars) and chars[j] != "\n":
            if chars[j] == "(":
                depth += 1
            elif chars[j] == ")":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        if j >= len(chars) or chars[j] != ")":
            i += 1
            continue
        inner = "".join(chars[i + 1 : j])
        codey = any(tok in inner for tok in (";", "{", "}", "->", "http", "://"))
        if not codey and (is_cjk(prev) or CJK.search(inner)):
            if is_cjk(prev):
                del chars[k + 1 : i]
                removed = i - (k + 1)
                i -= removed
                j -= removed
            chars[i] = "（"
            chars[j] = "）"
            i = j
        i += 1
    return "".join(chars)


def fix_proper_nouns(text: str) -> str:
    # \w 含汉字，不能用来判断英文词界。
    text = re.sub(r"(?<![A-Za-z0-9_.])[Gg]it[Hh]ub(?![A-Za-z0-9_./])", "GitHub", text)
    text = re.sub(r"(?<![A-Za-z0-9_.])GITHUB(?![A-Za-z0-9_./])", "GitHub", text)
    return text


def fix_spacing(text: str) -> str:
    text = re.sub(r"([\u4e00-\u9fff])(?! )([A-Za-z0-9])", r"\1 \2", text)
    text = re.sub(r"([A-Za-z0-9])(?! )([\u4e00-\u9fff])", r"\1 \2", text)
    text = re.sub(r"([%‰])(?! )([\u4e00-\u9fff])", r"\1 \2", text)
    text = re.sub(r"([\u4e00-\u9fff])(?! )([%‰])", r"\1 \2", text)
    text = re.sub(r"([\]\)])(?! )([\u4e00-\u9fff])", r"\1 \2", text)
    text = re.sub(r"）[ \t]+(?=[\u4e00-\u9fff])", "）", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff])[ \t]+（", "（", text)
    text = re.sub(rf"(\d)\s+({UNITS})\b", r"\1\2", text)
    text = re.sub(r"(\d)\s+%", r"\1%", text)
    return text


def transform_plain(text: str) -> str:
    text = fix_quotes(text)
    text = fix_ellipsis(text)
    text = fix_repeat(text)
    text = fix_width(text)
    text = fix_parens(text)
    text = fix_proper_nouns(text)
    text = fix_spacing(text)
    return text


def fix_sentence_period(text: str) -> str:
    """句号按整行判断，避免把 `.gitignore` 前的点收成「。」。"""
    masked: list[str] = []

    def hold(match: re.Match[str]) -> str:
        masked.append(match.group(0))
        return f"\uE001{len(masked) - 1}\uE001"

    text = re.sub(r"``.+?``|`[^`\n]+?`|https?://[^\s)]+", hold, text)
    text = re.sub(r"(?<=[\u4e00-\u9fff])\.(?=\s*[\u4e00-\u9fff])", "。", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff])\.(?=\s*$)", "。", text)

    def prose_dot(match: re.Match[str]) -> str:
        before = text[: match.start()]
        if re.fullmatch(r"\s*\d+", before):
            return match.group(0)
        return "。"

    text = re.sub(r"(?<=[A-Za-z0-9」』])\.(?=\s+[\u4e00-\u9fff])", prose_dot, text)
    text = re.sub(r"。[ \t]+(?=[\u4e00-\u9fff])", "。", text)

    def restore(match: re.Match[str]) -> str:
        return masked[int(match.group(1))]

    return re.sub(r"\uE001(\d+)\uE001", restore, text)


def needs_space(left: str, right: str, left_kind: str, right_kind: str) -> bool:
    kinds = {"code", "link", "img"}
    if left_kind not in kinds and right_kind not in kinds:
        return False
    if not left or not right:
        return False
    a, b = left[-1], right[0]
    if a.isspace() or b.isspace():
        return False
    if b in "，。！？、；：）」』】》.,!?;:)]}%‰":
        return False
    if a in "（「『【《([{<":
        return False
    if is_cjk(a) or is_cjk(b):
        return True
    if a.isalnum() and right_kind in kinds and b in "`[!":
        return True
    if b.isalnum() and left_kind in kinds and a in "`)":
        return True
    return False


def process_inline(text: str) -> str:
    parts: list[tuple[str, str]] = []
    cursor = 0
    for match in TOKEN_RE.finditer(text):
        if match.start() > cursor:
            parts.append(("plain", text[cursor : match.start()]))
        kind = match.lastgroup or "plain"
        token = match.group(0)
        if kind == "link":
            label, url = re.match(r"\[(.*)\]\((.*)\)", token).groups()
            token = f"[{transform_plain(label)}]({url})"
        elif kind == "img":
            alt, url = re.match(r"!\[(.*)\]\((.*)\)", token).groups()
            token = f"![{transform_plain(alt)}]({url})"
        elif kind == "code" and token.startswith("`") and not token.startswith("``"):
            inner = token[1:-1]
            if re.fullmatch(r"[Gg]it[Hh]ub|GITHUB", inner):
                token = "`GitHub`"
        parts.append((kind, token))
        cursor = match.end()
    if cursor < len(text):
        parts.append(("plain", text[cursor:]))
    rendered: list[tuple[str, str]] = []
    for kind, token in parts:
        if kind == "plain":
            token = transform_plain(token)
        rendered.append((kind, token))
    out = ""
    prev_kind = "plain"
    for kind, token in rendered:
        if needs_space(out, token, prev_kind, kind):
            out += " "
        out += token
        if token:
            prev_kind = kind
    return out


def process_prose(chunk: str) -> str:
    lines = []
    for line in chunk.split("\n"):
        if re.match(r"^( {4,}|\t)", line) and not CJK.search(line):
            lines.append(line)
            continue
        leading = re.match(r"[ \t]*", line).group(0)
        body = line[len(leading) :]
        body = re.sub(r"^　+", "", body)
        lines.append(leading + fix_sentence_period(process_inline(body)))
    return "\n".join(lines)


def split_fences(text: str) -> list[tuple[bool, str]]:
    lines = text.split("\n")
    parts: list[tuple[bool, str]] = []
    buf: list[str] = []
    in_fence = False
    marker = ""

    def flush(is_code: bool) -> None:
        nonlocal buf
        if buf:
            parts.append((is_code, "\n".join(buf)))
            buf = []

    for line in lines:
        if not in_fence:
            opened = FENCE_OPEN.match(line)
            if opened:
                flush(False)
                in_fence = True
                marker = opened.group(1)
                buf = [line]
            else:
                buf.append(line)
            continue
        buf.append(line)
        close = FENCE_OPEN.match(line)
        if close and close.group(1)[0] == marker[0] and len(close.group(1)) >= len(marker):
            flush(True)
            in_fence = False
            marker = ""
    flush(in_fence)
    return parts


def apply(text: str) -> str:
    out = []
    for is_code, chunk in split_fences(text):
        out.append(chunk if is_code else process_prose(chunk))
    return "\n".join(out)


def self_check() -> None:
    cases = {
        "作为Linux菜鸟": "作为 Linux 菜鸟",
        "Github于2007年10月19日正式上线。": "GitHub 于 2007 年 10 月 19 日正式上线。",
        "有15%的CPU性能提升。": "有 15% 的 CPU 性能提升。",
        "宽带有10Gbps，SSD一共有10TB。": "宽带有 10Gbps，SSD 一共有 10TB。",
        "错误地写成15 %和10 Gbps。": "错误地写成 15% 和 10Gbps。",
        "你可以前往[Linux 开源仓库](https://github.com/torvalds/linux)了解详情。": (
            "你可以前往 [Linux 开源仓库](https://github.com/torvalds/linux) 了解详情。"
        ),
        "使用github登录": "使用 GitHub 登录",
        "见github.com官网": "见 github.com 官网",
        "更多技术也随之孕育而生。。。": "更多技术也随之孕育而生……",
        "更多技术也随之孕育而生...": "更多技术也随之孕育而生……",
        "这个提议真棒！！！我喜欢~~~~": "这个提议真棒！我喜欢",
        "同学，“GitHub”的服务。": "同学，「GitHub」的服务。",
        "ex4.c文件": "ex4.c 文件",
        "使用10j向下": "使用 10j 向下",
        "4K视频和1080p电影": "4K 视频和 1080p 电影",
        "`git status`查看": "`git status` 查看",
        "在`Linux`中学习": "在 `Linux` 中学习",
        "《Lifeline: Silent Night》": "《Lifeline: Silent Night》",
        "乔布斯说「Stay hungry, Stay foolish.」": "乔布斯说「Stay hungry, Stay foolish.」",
        "核磁共振成像(NMRI)是什么原理？": "核磁共振成像（NMRI）是什么原理？",
        "我常用的是Kindle, iPad。": "我常用的是 Kindle, iPad。",
        "世界的起点是“SUMMARY OF LESS COMMANDS”,然后继续": (
            "世界的起点是「SUMMARY OF LESS COMMANDS」，然后继续"
        ),
        "### 2026.10.18": "### 2026.10.18",
        "忽略在.`gitignore`中": "忽略在.`gitignore` 中",
        "编辑.`bash_history`即可": "编辑.`bash_history` 即可",
        "6.`die` 函数": "6.`die` 函数",
        "整个hash code. 这时回来": "整个 hash code。这时回来",
        "6.1.首先安装": "6.1.首先安装",
        "1. 首先安装": "1. 首先安装",
        "在`github`上找": "在 `GitHub` 上找",
        "don’t 和注释用’#’": "don’t 和注释用『#』",
        "使用 Github 登录，不要写成 GITHUB。": "使用 GitHub 登录，不要写成 GitHub。",
    }
    fenced = "作为Linux菜鸟\n```\nman man\ncd..   #返回\n```\n见github\n"
    fenced_out = "作为 Linux 菜鸟\n```\nman man\ncd..   #返回\n```\n见 GitHub\n"
    cases_block = {fenced: fenced_out}
    failed = False
    for src, expect in {**cases, **cases_block}.items():
        got = apply(src)
        if got != expect:
            failed = True
            print("FAIL")
            print(f"  src:    {src!r}")
            print(f"  expect: {expect!r}")
            print(f"  got:    {got!r}")
    if failed:
        raise SystemExit(1)
    if apply(fenced_out) != fenced_out:
        raise SystemExit("not idempotent")


def main(argv: list[str]) -> None:
    self_check()
    if not argv:
        return
    paths: list[Path] = []
    for raw in argv:
        path = Path(raw)
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.md")))
        else:
            paths.append(path)
    for path in paths:
        original = path.read_text(encoding="utf-8")
        updated = apply(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(f"updated {path}")
        else:
            print(f"unchanged {path}")


if __name__ == "__main__":
    main(sys.argv[1:])
