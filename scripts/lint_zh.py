#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中文受控写作检查器（ASD-STE100 中文适配层的机械首查）。

只查形式项，不证明合规：
- 能查：分号、句长、虚动词、数字后端点词、相对时间、双重否定、单句"的"数量、
  半角标点、开放列举、黑话、零信息套话、称呼、含糊词。
- 查不出：定语是否过长、指代是否清楚、术语选得对不对、逻辑顺序、情态是否被改弱。

用法：
    python lint_zh.py 文件.md [更多文件]
    python lint_zh.py --tier procedure 文件.md
    python lint_zh.py --strict 文件.md      # 建议项也导致退出码 1
    type a.md | python lint_zh.py -         # 从 stdin 读

退出码：无【必须】问题为 0，否则为 1；--strict 下有【建议】问题也为 1。
"""

import argparse
import json
import re
import sys

TIER_MAX = {"report": 35, "procedure": 30, "descriptive": 40}

BUZZWORDS = [
    "赋能", "抓手", "闭环", "拉通", "打通", "沉淀", "落地", "对齐", "收口",
    "颗粒度", "组合拳", "顶层设计", "底层逻辑", "势能", "飞轮", "护城河",
    "打法", "痛点", "体感",
]
EMPTY_PHRASES = [
    "需要注意的是", "值得一提的是", "值得一提", "不难看出", "众所周知", "显而易见",
    "其实", "事实上", "实际上", "总的来说", "简单来说", "某种意义上", "在一定程度上",
    "也就是说", "换句话说", "首先我们需要", "希望对你有帮助", "希望对您有帮助",
    "如有疑问", "欢迎交流",
]
VAGUE_WORDS = ["一些", "若干", "相关", "尽量", "适当", "合适", "必要时", "大概", "大约", "左右"]
RELATIVE_TIME = ["尽快", "近期", "稍后", "下周", "明天", "近期内", "过几天"]
NOMINALIZATION = re.compile(
    r"(?:对|就|把)[^。；！？]{0,12}(?:进行|加以|作出|做出|予以)"
    r"|(?:进行|加以|予以)(?:安装|校验|核对|排查|定位|封装|重构|修改|调整|判断|决定|说明|分析|处理|检查|确认|优化|验证|测试|评估|审查|安排|部署|维护|升级|改造|统计|计算|配置|操作|设计|管理|控制|删除|清理|撤销|保留|替换|更新)"
    r"|(?:作出|做出)(?:修改|调整|判断|决定|说明|分析|处理|安排|优化|评估)"
)
RANGE_AFTER_NUM = re.compile(r"\d\s*(?:[A-Za-z%]{1,6}\s*)?(以上|以下|以内)")
DOUBLE_NEG = re.compile(r"(不得不|无不|不无|未尝不|不能不|不可不|不会不|并非不)")
OPEN_LIST = re.compile(
    r"[、，][^。；！？]{0,20}(?:(?<![相平对同])等(?!于|同|级|价|式|号|奖|待|候)|之类)(?:[^。；！？]{0,4})?(?:[，。；！？]|$)"
)
POLITE = re.compile(r"^(请|您|你(可以|需要|要))")
HALF_PUNCT = re.compile(r"[\u4e00-\u9fa5][,;:!?]")
CJK = re.compile(r"[\u4e00-\u9fa5]")
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.\-/]*")
DE = re.compile(r"的")
SENT_SPLIT = re.compile(r"[。！？!?]")
PUNCT = re.compile(r"[\s，。；：、！？「」（）()《》,.;:!?\"'“”‘’\-—…·\[\]{}*#>|`]")


def char_len(text):
    """汉字 1 字；英文词、数字、数字+单位各 1；标点与空白不计。"""
    cleaned = PUNCT.sub("", text)
    tokens = TOKEN.findall(cleaned)
    rest = TOKEN.sub("", cleaned)
    return len(CJK.findall(rest)) + len(tokens)


def strip_machine_text(lines):
    """把代码块、行内代码、front matter、表格、HTML 注释替换为等量空行。"""
    out = []
    in_fence = False
    in_front = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if i == 0 and stripped == "---":
            in_front = True
            out.append("")
            continue
        if in_front:
            if stripped == "---":
                in_front = False
            out.append("")
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append("")
            continue
        if in_fence:
            out.append("")
            continue
        if stripped.startswith("|") or stripped.startswith("<!--"):
            out.append("")
            continue
        # 行内豁免：<!-- lint-disable-line -->（用于引文、术语原话）
        if "lint-disable-line" in stripped:
            out.append("")
            continue
        # 对照块里的原文是证据，不改写，也不检查
        if stripped.startswith(("> 原稿", "> 旧版", "> 原文", "原稿：", "旧版：", "原文：")):
            out.append("")
            continue
        line = re.sub(r"`[^`]*`", "", line)
        line = re.sub(r"https?://\S+", "", line)
        out.append(line)
    return out


def split_sentences(line):
    parts = SENT_SPLIT.split(line)
    return [p.strip() for p in parts if p.strip()]


def vague_hit(line, word):
    """「相关」在正相关 / 负相关 / 相关性里是术语，不算含糊词。"""
    if word != "相关":
        return word in line
    stem = re.sub(r"(正|负)相关|相关性|相关系数", "", line)
    return "相关" in stem


def check(lines, tier):
    limit = TIER_MAX[tier]
    findings = []
    for no, line in enumerate(lines, 1):
        if not line.strip():
            continue
        if "；" in line:
            findings.append((no, "SEMICOLON", "必须", "分号串联完整论断，拆成两句"))
        if HALF_PUNCT.search(line):
            findings.append((no, "HALF-PUNCT", "必须", "中文语境用全角标点"))
        for w in BUZZWORDS:
            if w in line:
                findings.append((no, "BUZZWORD", "必须", "黑话「%s」：写具体动作或对象" % w))
        for w in EMPTY_PHRASES:
            if w in line:
                findings.append((no, "EMPTY-PHRASE", "必须", "零信息套话「%s」：删掉，直接说事" % w))
        for s in split_sentences(line):
            n = char_len(s)
            if n > limit:
                findings.append((no, "LONG-SENTENCE", "必须",
                                 "句长 %d 字，超过 %s 档上限 %d 字：%s" % (n, tier, limit, s[:20] + "…")))
            if NOMINALIZATION.search(s):
                findings.append((no, "NOMINALIZATION", "必须", "虚动词包装：直接用一个动词"))
            if RANGE_AFTER_NUM.search(s):
                if tier == "procedure":
                    findings.append((no, "RANGE-ENDPOINT", "必须", "数字后不用以上/以下：写大于、不小于、不超过"))
                else:
                    findings.append((no, "RANGE-ENDPOINT", "建议", "数字后端点词：程序档必须改写；说明档原话如此则保留，不要改掉原意"))
            if DOUBLE_NEG.search(s):
                findings.append((no, "DOUBLE-NEG", "必须", "双重否定：改成一次否定或直接陈述"))
            if OPEN_LIST.search(s):
                if tier == "procedure":
                    findings.append((no, "OPEN-LIST", "必须", "「等」结尾的开放列举：列全或写数量"))
                else:
                    findings.append((no, "OPEN-LIST", "建议", "「等」结尾：说明档原话如此则保留，删掉会变成断言列举完整"))
            if len(DE.findall(s)) > 2:
                findings.append((no, "DE-STACK", "必须", "单句「的」%d 个，超过 2 个：拆句" % len(DE.findall(s))))
            if tier == "procedure" and POLITE.search(s):
                findings.append((no, "POLITE", "必须", "操作句不写「请/您/你可以」"))
        for w in RELATIVE_TIME:
            if w in line:
                findings.append((no, "RELATIVE-TIME", "必须", "相对时间「%s」：写绝对日期或时长" % w))
        for w in VAGUE_WORDS:
            if vague_hit(line, w):
                findings.append((no, "VAGUE", "建议", "含糊词「%s」：写数值，或确认为正常泛指" % w))
    return findings


def run_selftest():
    """回归用例：改规则后先跑一遍，防止误报/漏报反复。"""
    cases = [
        ("启动泵。", "descriptive", 0),
        ("先做 A；再做 B。", "descriptive", 1),                       # 分号，所有档位
        ("文件大小在 10 MB 以内。", "procedure", 1),                  # 程序档必须
        ("文件大小在 10 MB 以内。", "descriptive", 0),                # 说明档只建议
        ("他做出一个零件。", "descriptive", 0),                       # 不是名词化
        ("对配置进行修改。", "descriptive", 1),                       # 名词化
        ("A、B 相等的情况下，继续。", "procedure", 0),                 # 不是开放列举
        ("南京理工、东莞理工等队伍。", "procedure", 1),                # 程序档必须
        ("南京理工、东莞理工等队伍。", "descriptive", 0),              # 说明档保留原意
        ("由接口的调用失败导致的配置加载的中断。", "descriptive", 1),    # 单句「的」过多
    ]
    bad = 0
    for text, tier, expect in cases:
        got = sum(1 for f in check([text], tier) if f[2] == "必须")
        ok = got == expect
        bad += 0 if ok else 1
        print("%s  [%s] %s（期望 %d，实际 %d）" % ("PASS" if ok else "FAIL", tier, text, expect, got))
    print("\n自检：%d 条用例，%d 条失败。" % (len(cases), bad))
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description="中文受控写作检查器（只提示，不证明合规）")
    ap.add_argument("files", nargs="*", help="文件路径；用 - 从 stdin 读")
    ap.add_argument("--tier", default="descriptive", choices=sorted(TIER_MAX), help="文本档位，决定句长上限")
    ap.add_argument("--strict", action="store_true", help="建议项也视为失败")
    ap.add_argument("--max-desc", type=int, help="覆盖当前档位上限")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--baseline", type=int, default=0, help="存量文档：容忍 N 条【必须】")
    ap.add_argument("--selftest", action="store_true", help="跑内置回归用例")
    args = ap.parse_args()

    if args.selftest:
        return run_selftest()

    if args.max_desc:
        TIER_MAX[args.tier] = args.max_desc

    sources = args.files or ["-"]
    must = 0
    hint = 0
    rows = []
    for path in sources:
        if path == "-":
            text = sys.stdin.read()
            label = "<stdin>"
        else:
            with open(path, encoding="utf-8") as f:
                text = f.read()
            label = path
        lines = strip_machine_text(text.splitlines())
        for no, rule, level, msg in check(lines, args.tier):
            rows.append({"file": label, "line": no, "rule": rule, "level": level, "message": msg})
            if level == "必须":
                must += 1
            else:
                hint += 1

    if args.json:
        print(json.dumps({"must": must, "hint": hint, "findings": rows}, ensure_ascii=False, indent=2))
    else:
        for r in rows:
            print("%s:%d: [%s][%s] %s" % (r["file"], r["line"], r["rule"], r["level"], r["message"]))
        print("\n合计：【必须】%d 条，【建议】%d 条。检查器只做形式首查，不证明合规。" % (must, hint))

    if must > args.baseline or (args.strict and hint):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
