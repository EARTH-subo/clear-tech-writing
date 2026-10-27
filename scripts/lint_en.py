#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""English controlled-language checker (ASD-STE100 mechanical first pass).

Checks form only. It does not prove compliance:
- Checks: semicolons, sentence length, phrasal verbs, non-approved words,
  nominalization ("do an inspection of"), passive voice, "-ing" as a modifier,
  weak modals.
- Cannot check: approved meaning, part of speech, noun-cluster acceptability,
  technical-term validity, or whether a rewrite changed the facts.

Usage:
    python lint_en.py FILE [MORE...]
    python lint_en.py --tier procedure FILE
    python lint_en.py --json FILE
    python lint_en.py --baseline 12 FILE     # legacy file: tolerate 12 must-findings
    type a.md | python lint_en.py -

Exit code: 0 when must-findings <= baseline (default 0); otherwise 1.
--strict also fails on hints.
"""

import argparse
import json
import re
import sys

TIER_MAX = {"report": 25, "procedure": 20, "descriptive": 25}

BANNED = [
    "utilize", "utilizes", "utilized", "ensure", "ensures", "commence", "commences",
    "initiate", "initiates", "terminate", "terminates", "facilitate", "facilitates",
    "approximately", "additional", "sufficient", "numerous", "regarding",
    "concerning", "subsequent", "subsequently", "methodology", "leverage",
    "functionality", "prior to", "in order to", "due to the fact that",
    "in the event that", "it is recommended", "and/or", "etc.", "e.g.", "i.e.",
]
PHRASAL = [
    "turn on", "turn off", "switch on", "switch off", "carry out", "put back",
    "set up", "take off", "shut down", "find out", "look into", "come back",
    "pick up", "give up", "break down", "run out", "check out", "figure out",
    "come up with", "go on",
]
NOMINALIZATION = re.compile(
    r"\b(?:do|does|did|perform|performs|performed|conduct|conducts|conducted|make|makes|made)\s+"
    r"(?:a|an|the)\s+\w+(?:ion|ment|ance|ence|al|ure)\b",
    re.I,
)
PASSIVE = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ed|known|made|done|given|taken|shown|"
    r"written|built|sent|kept|held|found|put|read|run|set)\b",
    re.I,
)
ING_MODIFIER = re.compile(r"\b(?:the|a|an)\s+\w+ing\s+[a-z]+", re.I)
MODAL = re.compile(r"\b(should|shall|would|might|could)\b", re.I)
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'\-_/.]*")


def protect_decimals(text):
    return re.sub(r"(\d)\.(\d)", r"\1<DOT>\2", text)


def restore(text):
    return text.replace("<DOT>", ".")


def word_count(sentence):
    # Hyphenated compounds and numbers count as one word each.
    return len(WORD.findall(sentence))


def strip_machine_text(lines):
    out = []
    in_fence = False
    in_front = False
    for i, line in enumerate(lines):
        s = line.strip()
        if i == 0 and s == "---":
            in_front = True
            out.append("")
            continue
        if in_front:
            if s == "---":
                in_front = False
            out.append("")
            continue
        if s.startswith("```") or s.startswith("~~~"):
            in_fence = not in_fence
            out.append("")
            continue
        if in_fence:
            out.append("")
            continue
        if s.startswith("|") or s.startswith("<!--"):
            out.append("")
            continue
        # Quoted before-text in comparison blocks is evidence, not prose.
        if s.startswith(("> Before", "> Original", "> 原稿", "> 旧版", "Before:", "Original:")):
            out.append("")
            continue
        line = re.sub(r"`[^`]*`", "", line)
        line = re.sub(r"https?://\S+", "", line)
        out.append(line)
    return out


def check(lines, tier):
    limit = TIER_MAX[tier]
    findings = []
    for no, line in enumerate(lines, 1):
        if not line.strip():
            continue
        low = line.lower()
        if ";" in line:
            findings.append((no, "SEMICOLON", "必须", "Semicolons are not permitted (8.1). Split the sentence."))
        for w in BANNED:
            if w.endswith("."):
                hit = w in low
            else:
                hit = re.search(r"\b" + re.escape(w) + r"\b", low)
            if hit:
                findings.append((no, "BANNED-WORD", "必须", "Non-approved word: %s" % w))
        for w in PHRASAL:
            if re.search(r"\b" + re.escape(w) + r"\b", low):
                findings.append((no, "PHRASAL-VERB", "必须", "Phrasal verb: %s. Use one approved verb (9.3)." % w))
        protected = protect_decimals(line)
        for sent in SENT_SPLIT.split(protected):
            sent = restore(sent).strip()
            if not sent:
                continue
            n = word_count(sent)
            if n > limit:
                findings.append((no, "LONG-SENTENCE", "必须",
                                 "%d words, over the %s limit of %d: %s" % (n, tier, limit, sent[:40] + "…")))
            m = NOMINALIZATION.search(sent)
            if m:
                findings.append((no, "NOMINALIZATION", "必须",
                                 "Use the verb, not its noun: %s (3.7)" % m.group(0)))
            if PASSIVE.search(sent):
                findings.append((no, "PASSIVE", "建议",
                                 "Passive voice. Use active unless the agent is unknown (3.6)."))
            m = ING_MODIFIER.search(sent)
            if m:
                findings.append((no, "ING-MODIFIER", "建议",
                                 "-ing used as a modifier: %s (3.5)" % m.group(0)))
            m = MODAL.search(sent)
            if m:
                findings.append((no, "WEAK-MODAL", "建议",
                                 "Weak modal: %s. Use must, or state the fact." % m.group(0)))
    return findings


def run_selftest():
    """Regression cases. Run after changing any rule."""
    cases = [
        ("Start the pump.", 0),
        ("Turn on the pump.", 1),                       # phrasal verb
        ("Perform an inspection of the filter.", 1),    # nominalization
        ("The system reads the file at startup.", 0),
        ("Prior to the test, close the valve.", 1),     # non-approved word
        ("The valve is closed.", 0),                    # passive is a hint only
        ("Close the valve; then start the pump.", 1),   # semicolon
    ]
    bad = 0
    for text, expect in cases:
        got = sum(1 for f in check([text], "descriptive") if f[2] == "必须")
        ok = got == expect
        bad += 0 if ok else 1
        print("%s  %s (expected %d, got %d)" % ("PASS" if ok else "FAIL", text, expect, got))
    print("\nSelf-test: %d cases, %d failed." % (len(cases), bad))
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description="English controlled-language checker (hints only)")
    ap.add_argument("files", nargs="*", help="file paths; use - for stdin")
    ap.add_argument("--tier", default="descriptive", choices=sorted(TIER_MAX))
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--baseline", type=int, default=0, help="tolerate N must-findings (legacy files)")
    ap.add_argument("--strict", action="store_true", help="hints also fail the run")
    ap.add_argument("--selftest", action="store_true", help="run built-in regression cases")
    args = ap.parse_args()

    if args.selftest:
        return run_selftest()

    sources = args.files or ["-"]
    must = hint = 0
    rows = []
    for path in sources:
        if path == "-":
            text, label = sys.stdin.read(), "<stdin>"
        else:
            with open(path, encoding="utf-8") as f:
                text = f.read()
            label = path
        for no, rule, level, msg in check(strip_machine_text(text.splitlines()), args.tier):
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
        print("\nTotal: %d must, %d hints. Form checks only, not a compliance statement." % (must, hint))

    if must > args.baseline or (args.strict and hint):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
