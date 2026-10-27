# clear-tech-writing

受控技术写作 skill：中英双语，三档 × 两强度，自带检查器。
基于公开的 **ASD-STE100** 方法自行实现，与 ASD 无隶属关系，不代表通过任何认证。

> Controlled technical writing for English and Chinese. Three tiers, two strengths, form-only checkers. Based on the ASD-STE100 method. Not affiliated with ASD.

## 解决的问题

一句话：**让文本只有一种读法**。

读者是没有追问机会的另一方——维修工、非母语读者、翻译管线、半年后的你自己、另一个 agent。写错代价越高，越该用受控写法。

| 场景 | 不用它的问题 |
|---|---|
| 操作步骤 | 一句三个动作，漏做一步 |
| 错误信息 | 只说"出错了"，不说下一步 |
| 工具描述 | 模型读成另一种含义，调错参数 |
| 任务汇报 | 过程很长，结论要靠猜 |
| 中文技术文档 | 名词化、虚动词、长定语，读完不知道主干 |

## 与同类项目的三个不同

1. **保真优先，冲突可标注。** 形式规则（句长、"等"、"以上"）与事实冲突时，保真优先，并在输出末尾用"保留："列出取舍。多数同类工具只有规则，没有冲突仲裁。
2. **中英同构。** 英文侧对接 Issue 9 条号（8.1、9.3、3.7），中文侧用【必须】/【建议】，两边的档位、强度、自检项一一对应。
3. **阈值有校准。** 中文句长不是翻译英文词数，而是用两批语料实测：作者本地 68.5 万字 + 5 个开源项目 10.8 万字，脚本可复现。

## 三种档位 × 两种强度

| 档位 | 用于 | 中文上限 | 英文上限 |
|---|---|---|---|
| report 汇报 | 任务汇报、排障结论、PR 总结 | 35 字 | 25 words |
| procedure 步骤 | 部署、运维、排障操作 | 30 字（安全关键 25） | 20 words |
| descriptive 说明 | README、概念解释、工具描述、API 文档 | 40 字 | 25 words |

- **strict**：步骤、错误信息、工具描述、agent 指令、安全提示。全部规则执行。
- **flavored**：README、PR、changelog、解释性文章。结构规则全执行，词汇规则只作方向。

## 目录

```
SKILL.md                        总入口：优先级、档位、速查、自检、示例
references/
  ste-writing-rules.md          英文：Issue 9 九组要点与条号
  ste-dictionary-core.md        英文：高频批准 / 不批准对照
  chinese-adaptation.md         中文：字法、句法、篇法、保真底线、语料校准
  scenarios.md                  按文本类型落地：汇报、runbook、错误信息、API、UI、日志
  sources.md                    来源、借鉴项、许可边界
scripts/
  lint_zh.py                    中文检查器（必须 / 建议、--json、--baseline、--selftest）
  lint_en.py                    英文检查器（分号、句长、短语动词、非批准词、名词化）
  calibrate.py                  用任意语料重算句长分布
examples/
  before-after.md               四组前后对照
```

## 安装

Trae：

```
git clone https://github.com/<you>/clear-tech-writing ~/.trae-cn/skills/clear-tech-writing
```

Claude Code：

```
git clone https://github.com/<you>/clear-tech-writing ~/.claude/skills/clear-tech-writing
```

其它支持 Agent Skills 的客户端：把整个目录放进它的 skills 目录。不装也行，把 `SKILL.md` 内容贴进 system prompt。

## 快速试用

```
python scripts/lint_zh.py --selftest
python scripts/lint_zh.py --tier procedure 文档.md
python scripts/lint_en.py --tier procedure doc.md
python scripts/calibrate.py ./docs
```

输出示例：

```
docs/runbook.md:12: [SEMICOLON][必须] 分号串联完整论断，拆成两句
docs/runbook.md:18: [LONG-SENTENCE][必须] 句长 46 字，超过 procedure 档上限 30 字：……
合计：【必须】2 条，【建议】1 条。检查器只做形式首查，不证明合规。
```

只需要标准库，Python 3.8+。

## 边界

- **检查器只查形式。** 词义与词性是否合规、名词串是否可接受、指代是否清楚、改写有没有改变事实，都查不出来。命中不等于不合规（引文、术语、刻意的长句都会命中），未命中更不等于合规。
- **不含官方词典。** ISO/ASD 的约 900 批准词不可再分发，本仓库只收高频对照。
- **没有做效果实验。** 句长阈值来自语料分布，不是阅读理解实验。同类项目也没有做过。

## 许可与归属

- 文本（`SKILL.md` 与 `references/`）：CC BY 4.0，见 [LICENSE-CC-BY-4.0.md](LICENSE-CC-BY-4.0.md)
- 脚本（`scripts/`）：MIT，见 [LICENSE](LICENSE)
- 借鉴来源与逐项说明：[references/sources.md](references/sources.md)

ASD-STE100 是 ASD（欧洲航空航天与国防工业协会）的标准名与注册商标，本仓库不使用该名称作为项目名，也不暗示任何隶属或认证关系。

## 版本

1.0.0
