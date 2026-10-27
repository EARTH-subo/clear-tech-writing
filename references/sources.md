# 来源、借鉴与许可

本 skill 的规则结构来自 ASD-STE100 Issue 9，中文侧的分级、阈值与特有规则借鉴了 6 个社区项目。
此表用于两件事：追溯每条规则的出处；标清哪些内容可以直接复用、哪些只能借鉴做法。

## 标准本身

| 项 | 说明 |
|---|---|
| ASD-STE100 Issue 9 | 2025-01-15 发布，ASD（欧洲航空航天与国防工业协会）所有，STEMG 维护。53 条规则 9 个章节，约 900 批准词 + 约 1200 不批准词 |
| 获取 | https://asd-ste100.org/STE_downloads.html （免费索取，表单提交后邮件给链接） |
| 再分发 | **词典不可再分发**。本 skill 只复述规则类别与高频对照，不含官方正文与词表 |
| 术语 | Issue 9 起用 "standard"，不再用 "specification"；不是 ISO/IEC 国际标准 |

## 社区项目

| 项目 | 许可 | 本 skill 借鉴了什么 |
|---|---|---|
| [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill) | MIT | 英文原件。"结构规则可核对 / 词汇规则只是方向"的切分；Strict / STE-flavored 两档；把读者换成 agent 的场景框架（工具描述、错误信息、agent 间指令、system prompt） |
| [lemonhall/asd-ste100-skill-zh](https://github.com/lemonhall/asd-ste100-skill-zh) | 上游 MIT，本仓库另标（沿用上游许可） | 中文对应物。不翻译而按中文失败模式重写；"情态是内容，不得改"；默认只输出正文、要才给规则表；不声称合规的边界写法 |
| [mzopedia/simplified-technical-chinese](https://github.com/mzopedia/simplified-technical-chinese)（STC 0.2） | 规范与词表 CC BY 4.0，脚本与测试 MIT | 【必须】/【建议】两级；句长按 350 万字真实文档校准（90 分位：操作 33 字、描述 41 字）；中文特有一词一义（以上/以下端点、可以 vs 支持、打开/启用/启动）；"等"结尾的开放列举；范围端点、相对时间、倍数与百分点；检查器的"只提示不证明" |
| [KonglingDaDa/zh-ste100-jev-skill](https://github.com/KonglingDaDa/zh-ste100-jev-skill) | 未核实 | 篇法·句法·字法三层结构；report / procedure / descriptive 三档及 35 / 25 / 40 字；首句给死结论、禁太极词与免责叠甲；竹节短句、单句"的"≤2；剥欧化介词壳；真动词替弱动词 |
| [dualface/ste-zh](https://github.com/dualface/ste-zh) | 未核实 | 汇报档的状态词固定（10 个）；工作状态与验证状态分开；证据可定位；不叙述过程；选项编号 +（推荐）；不编造与"待确认" |
| [Fenng/Tech-Doc-Style-Chinese](https://github.com/Fenng/Tech-Doc-Style-Chinese) | 未核实 | 事实保真清单（不新增数字、时限、能力、结论）；"自动检查边界"的写法；明确"不是 ASD-STE100 中文版"的免责 |
| [mrtsels/skills · tech-writing-style](https://github.com/mrtsels/skills/tree/main/writing/tech-writing-style) | 未核实 | 冲突时的优先级顺序（事实 > 项目约定 > 术语与机器可读 > 结构 > 排版）；撰写/改写/校对/审阅四种任务模式；机器可读内容白名单；按内容类型（入口页、API、UI 文案、runbook）分别给要求 |

## 检查器

`scripts/lint_zh.py` 与 `scripts/lint_en.py` 是本 skill 自建的，不来自上述任何项目，规则按本 skill 的条目实现。
输出格式（`文件:行号: [规则][级别] 说明`）、`--baseline`、行内 `lint-disable-line`、跳过代码与 URL 这几种做法，
参考了 STC 的 `check.py`、lemonhall 的 `ste-lint-zh.py` 与 mrtsels 的三个检查脚本。

它只做形式首查。不要把"检查器通过"当作"符合 ASD-STE100"——标准要求逐词查 Part 2 词典，本 skill 没有也不分发该词典。

## 使用约定

- 本仓库名 `clear-tech-writing` 与 ASD、ASD-STE100 均无关系，不使用标准名作为项目名，也不暗示隶属或认证。
- 上表标"未核实"的项目，本 skill **只借鉴做法与结构，未复制原文**。若要整段复用其文本，先确认许可证并按其要求署名。
- STC 的规则与词表为 CC BY 4.0：如引用其具体条目，需保留署名与许可证说明。
- ASD 的词典与正文不得复制进任何仓库；本 skill 的 `ste-dictionary-core.md` 是高频改写对照，不是官方词表。
- 中文侧的句长阈值来自公开的语料校准结果，不是官方条文；引用时说明来源是适配层，不是 ASD 标准。
