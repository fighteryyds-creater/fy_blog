#!/usr/bin/env bash
# 在 docs/index.md 最上面补上今天的日期标题，格式与旧博客一致：### 2026.10.18
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
file="$root/docs/index.md"
year="$(date +%Y)"
month="$((10#$(date +%m)))"
day="$((10#$(date +%d)))"
heading="### ${year}.${month}.${day}"

if grep -qxF "$heading" "$file"; then
  printf '今天已经有一页：%s\n' "$heading"
  exit 0
fi

tmp="$(mktemp)"
{
  printf '%s\n\n\n' "$heading"
  cat "$file"
} >"$tmp"
mv "$tmp" "$file"
printf '已写在 docs/index.md 顶部：%s\n' "$heading"
