# ASD-STE100 Writing Rules（9 组要点 + 可查条号）

> 来源：ASD-STE100 Issue 9（2025-01-15），ASD 所有，STEMG 维护。
> 本文件是 9 组规则的**要点摘要**，条号按官方 Issue 9 标注；**不是 53 条全文**。
> 引用逐字条文时以官方文本为准（免费索取：https://asd-ste100.org/STE_downloads.html）。
> 条号无法确证的地方只标所属章节，不编号码。

## Group 1 — Words 词（1.1–1.14）

- **1.1** 每个词只能来自两处：批准词典（Part 2），或合规的技术名词 / 技术动词。
- **1.2** 词典里的词只按词典给的词性用。
- **1.3** 词典里的词只按词典给的含义用。例：fall（动词）只表示受重力下落，"数值下降"用 decrease。
- **1.4** 只用词典认可的词形。
- **1.5–1.8** 技术名词必须能归入允许类别（部件与设备名、材料名、工具名、行业术语、专有名称、商标等）；**词难不等于技术名词**；技术名词不得当动词用；优先用行业或公司已统一的名称。
- **1.9–1.10** 同类技术名词里选短的、易懂的那个；口语、俚语、行话不做技术名词。
- **1.11** 同一个东西全篇只有一个技术名词。
- **1.12–1.13** 技术动词仅限特定类别；技术动词不得当名词用。
- **1.14** 拼写按美式英语（Merriam-Webster），除有强制规定。

> 词典结构：约 900 个批准词 + 约 1200 个不批准词（附替换建议）。改写时先查不批准词那张表，命中率最高。

## Group 2 — Noun phrases 名词短语（2.1–2.2）

- **2.1** 名词串最多 3 个词，超了加介词、改写或拆句。
  - ✗ fuel system component inspection procedure
  - ✓ procedure to inspect the components of the fuel system
- **2.2** 超过 3 词的技术名词：首次写全，之后用短形式，或用连字符连接紧密部分。
  - ✓ engine-driven fuel pump（首现写全）→ 后文 fuel pump
- 技术名词的原文拼写与形式不改。

## Group 3 — Verbs 动词（3.1–3.7）

- **3.1–3.2** 只用批准词形：不定式、祈使式、一般现在、一般过去、一般将来、过去分词作形容词。
- **3.3** 过去分词作形容词描述状态，不算被动语态。
  - ✓ the valve is closed（状态）
- **3.4** 不叠助动词：不用现在完成、过去完成、进行时，也不用情态动词连用。
  - ✗ The system has been updated. → ✓ The system is updated.
  - ✗ The pump will be able to start. → ✓ The pump can start.
- **3.5** -ing 形式只允许出现在技术名词里或作其修饰语，不作动词、不作后置从句。
  - ✗ the engine running at idle → ✓ the engine at idle
- **3.6** 主动语态。程序性文本**必须**主动；描述性文本只在施动者未知或不重要时用被动。
- **3.7** 动作用动词，不用其名词化形式。
  - ✗ Do an inspection of the pump. → ✓ Examine the pump.
- 情态阶梯：should（强制要求）→ must；should（建议）→ 删掉或写成事实；may / might / could（可能性）→ can；may（许可）→ can。

## Group 4 — Sentences 句子（Section 4）

- 一句一个主要意思；一个指令一个句子。
- 不为了缩短句子省掉主语、谓语或冠词。官方明确说省掉成分会造成歧义，不是简洁。
  - ✗ Remove bolt and install new one. → ✓ Remove the bolt. Then install the new one.
- 条件 / 前提放句首，用逗号与主句分开。
  - ✓ If the pressure is more than 3 bar, stop the pump.

## Group 5 — Instructions 程序写作（5.1–5.4）

- **5.1–5.3** 指令句 ≤ 20 words；一个句子一个指令（只有同时发生的动作才可合并）；用祈使句。
- **5.4** 读者需要的条件放指令之前，用逗号分开。
- 步骤编号，层级连续；子步骤缩进。
- 不用位置描述代替动作指令（The switch is on the left. 不是一步操作）。
- WARNING / CAUTION / NOTE 放在相关步骤之前，格式全篇统一。

## Group 6 — Explanations 描述写作（6.1–6.6）

- **6.1–6.6** 描述句 ≤ 25 words；一段一个主题，≤ 6 句；信息渐进给出，先概述后细节。
- 以一般现在时为主；不用完成时与进行时。
- 不用隐喻、成语、幽默、修辞性表达。

## Group 7 — Safety 安全表达（Section 7）

| 类型 | 适用 | 结构 |
|---|---|---|
| **WARNING** | 可能造成人员伤亡 | 类型词 + 危险 + 后果 + 规避动作 |
| **CAUTION** | 可能造成设备损坏 | 类型词 + 危险 + 后果 + 规避动作 |
| **NOTE** | 补充信息，无安全后果 | 一句话说明 |

- 放相关内容之前，全篇格式统一。
- 安全指令的句首必须是明确动作或条件，不能埋在中段。

## Group 8 — Punctuation and word counting 标点与计数（8.1–8.6）

- **8.1** 只用标准英文标点，**分号（;）完全禁用**。两个完整论断拆成两句。
- 圆括号只放补充信息，不放必要信息；冒号只用于引入列表。
- 缩略语首次出现给全称 + 缩略语，之后只用缩略语。
- 数字与单位之间留空格（3 mm）。
- **8.6** 词数按标准口径统计，空白分词只是近似。本文件的执行约定：
  - 连字符复合词、缩写、数字、数字 + 单位各计 **1 个词**（engine-driven = 1，3 mm = 1）。
  - 代码、命令、表格单元格、图注不计入句长。
- 数超没超限前先删冗余词（very、properly、correctly、in order to），再判断要不要拆句。

## Group 9 — Writing practices 写作实践（Section 9）

- **9.2** 每个批准词按批准含义与批准词性使用。
- **9.3** **不用短语动词**（动词 + 介词 / 副词）。改用单个动词。
  - ✗ turn on → ✓ start；✗ switch off → ✓ stop
  - ✗ carry out → ✓ do / examine；✗ put back → ✓ install
- **9.4** 同一事物全篇同一名称；同义词只留一个。
- 保持文本尽可能短——能删则删。
- 复杂流程配图、表、流程图。
- 不用读者不熟悉的缩略语。
