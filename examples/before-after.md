# 前后对照

四组例子，覆盖两种语言、三种档位。方括号内是触发的规则。

## 1 工具描述（EN，strict）

> Before: This function will attempt to carry out a validation of the provided configuration file and ensure that all of the required fields are present, returning an error if any issue is found.

> After: `validate_config(path)` checks the configuration file. It returns `ConfigError` when a required field is missing. It returns `None` when the file is valid.

触发：句长 25 words、短语动词 carry out、名词化 validation of、ensure、非批准词 required/all of the、单句多动作。

## 2 错误信息（ZH，strict）

> 原文：抱歉，操作失败了，可能是网络问题，请您稍后重试一下；如果还是不行，请联系管理员。

> 改写：连接数据库失败（错误码 1045）：账号或密码错误。检查 `config.yaml` 中的 `db.password` 后重试。

触发：零信息套话（抱歉 / 可能是 / 请您 / 一下）、分号串联、原因与可执行动作缺失、【必须】要求写影响与下一步。

## 3 README 段落（EN，flavored）

> Before: Our powerful and flexible toolkit seamlessly leverages state-of-the-art algorithms in order to provide a comprehensive solution for developers who are looking to build robust applications.

> After: The toolkit reads CSV, JSON, and Parquet files. It converts each file to a typed record set. On a 1 GB CSV file it uses about 400 MB of memory.

触发：营销形容词（powerful / flexible / seamless / robust / comprehensive）、in order to、leverage、state-of-the-art、无数字的宣称。

## 4 任务汇报（ZH，report）

> 原文：好的我先看了一下登录相关的代码，发现问题应该是出在 token 刷新的逻辑上，大概是并发的时候两个请求同时去刷新导致的。然后我对 auth/refresh.ts 进行了修改，加了一个锁来实现串行化处理，另外顺手把一些日志之类的也优化了一下。测试基本都跑过了，应该没什么问题，不过 iOS 那边因为没有环境暂时没法验证。

> 改写：已完成：登录刷新逻辑的并发修改。iOS 端未验证。
>
> **原因**：两个请求同时刷新 token，后完成的刷新让先拿到的 token 失效。
> **改动**：`auth/refresh.ts:42` — 刷新前不检查是否已有刷新在进行。现改为同一时间只发一个刷新请求。
> **验证**：已验证：`npm test auth` — 48 项通过，含新增并发刷新测试。未验证：iOS 端 — 本机无构建环境。

触发：过程叙述、太极词（应该是 / 大概 / 基本 / 应该没什么问题）、虚动词（进行了修改 / 实现）、状态词不规范、证据不可定位。

---

想看更多：`references/scenarios.md` 按 10 类文本分别给了模板与反例。
