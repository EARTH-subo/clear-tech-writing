#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用本地语料校准中文句长阈值。

统计一份目录里中文技术文档的句长分布，按"编号步骤 / 项目符号 / 正文描述"分开，
给出 p50 / p90 / p95 和超过 30 / 35 / 40 字的比例，用来判断档位上限定得合不合适。

用法：
    python calibrate.py <目录> [--min-chars 800] [--top 25]

只读 .md / .txt。默认跳过 node_modules、.git、dist 等目录，
以及口语转写（逐字稿 / transcript）和本 skill 的改写产物，避免循环论证。
"""

import argparse
import os
import re

CJK = re.compile(r"[\u4e00-\u9fa5]")
SENT = re.compile(r"[。！？]")
FENCE = re.compile(r"^\s*(```|~~~)")
NUM_STEP = re.compile(r"^\s*\d+[.、)]")
BULLET = re.compile(r"^\s*[-*+]\s")
EXCLUDE_PATH = re.compile(r"逐段稿|逐字稿|transcript|_受控语言版|_STC版|_我们版|_lint")
NOISE = [re.compile(r"<!--.*?-->", re.S), re.compile(r"https?://\S+"),
         re.compile(r"!\[[^\]]*\]\([^)]*\)"), re.compile(r"`[^`]*`")]
SKIP_DIRS = {"node_modules", ".git", ".pnpm-store", "dist", "build", "__pycache__",
             ".next", ".venv", "venv", "tools"}


def clean(text):
    out, fenced, front = [], False, False
    for i, line in enumerate(text.splitlines()):
        s = line.strip()
        if i == 0 and s == "---":
            front = True
            continue
        if front:
            if s == "---":
                front = False
            continue
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced or s.startswith("|"):
            continue
        out.append(line)
    text = "\n".join(out)
    for pat in NOISE:
        text = pat.sub("", text)
    return text


def sentences(text):
    res = []
    for line in text.splitlines():
        if not line.strip():
            continue
        if NUM_STEP.match(line):
            kind, body = "step", NUM_STEP.sub("", line)
        elif BULLET.match(line):
            kind, body = "bullet", BULLET.sub("", line)
        else:
            kind, body = "desc", line
        for part in SENT.split(body):
            n = len(CJK.findall(part.strip()))
            if n:
                res.append((kind, n))
    return res


def quantile(vals, q):
    vs = sorted(vals)
    return vs[int(round((len(vs) - 1) * q))] if vs else 0


def main():
    ap = argparse.ArgumentParser(description="用本地语料校准中文句长阈值")
    ap.add_argument("root", help="要扫描的目录")
    ap.add_argument("--min-chars", type=int, default=800, help="单文件最少汉字数")
    ap.add_argument("--top", type=int, default=25, help="列出前 N 个文件")
    args = ap.parse_args()

    files = []
    for dirpath, dirnames, filenames in os.walk(args.root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() not in (".md", ".txt"):
                continue
            p = os.path.join(dirpath, fn)
            if EXCLUDE_PATH.search(p):
                continue
            try:
                if not 2000 <= os.path.getsize(p) <= 400000:
                    continue
                with open(p, encoding="utf-8", errors="ignore") as f:
                    body = clean(f.read())
            except OSError:
                continue
            if len(CJK.findall(body)) < args.min_chars:
                continue
            ss = sentences(body)
            if len(ss) < 15:
                continue
            files.append({"path": p, "chars": len(CJK.findall(body)), "sents": ss})

    if not files:
        print("没有找到符合条件的文档。")
        return 1

    def show(label, vals):
        if not vals:
            print("%-6s 0 句" % label)
            return
        over = lambda t: sum(1 for n in vals if n > t) / len(vals) * 100
        print("%-6s 句数 %5d  平均 %5.1f  p50 %3d  p90 %3d  p95 %3d  最长 %3d  >30 %5.1f%%  >35 %5.1f%%  >40 %5.1f%%"
              % (label, len(vals), sum(vals) / len(vals), quantile(vals, .5), quantile(vals, .9),
                 quantile(vals, .95), max(vals), over(30), over(35), over(40)))

    print("语料：%d 个文件，汉字 %d\n" % (len(files), sum(f["chars"] for f in files)))
    for kind, label in (("step", "编号步骤"), ("bullet", "项目符号"), ("desc", "正文描述")):
        show(label, [n for f in files for k, n in f["sents"] if k == kind])
    show("合计", [n for f in files for _, n in f["sents"]])

    rows = []
    for f in files:
        desc = [n for k, n in f["sents"] if k == "desc"]
        step = [n for k, n in f["sents"] if k == "step"]
        rows.append((len(f["sents"]), f["path"], quantile(desc, .9), quantile(step, .9)))
    rows.sort(reverse=True)
    print("\n文档明细（按句数，前 %d）：" % args.top)
    print("%5s %7s %7s  %s" % ("句数", "描述p90", "步骤p90", "路径"))
    for total, path, d90, s90 in rows[:args.top]:
        print("%5d %7d %7d  %s" % (total, d90, s90, os.path.relpath(path, args.root)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
