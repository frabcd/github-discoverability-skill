# GitHub 可发现性与发布 Skill

**把“上传到 GitHub”变成：别人找得到、看得懂、试得起来。**

这个项目本身就是可安装的 Skill，不是让编码 Agent 再开发一个平台的需求文档。
适用于已有项目：研究搜索意图、准备 README/仓库元数据、形成明确上传范围，
并在有真实发布数据时提炼经过审核的经验。

[English](README.md) · [Skill 本体](skills/github-discoverability/SKILL.md) · [调查](docs/research.md) · [本地验证](docs/validation.md)

## 使用

在已授权工作区中要求 Agent：

```text
用 github-discoverability 帮这个项目准备 GitHub 发布。
不要改核心代码，不要公开上传。先研究真实同类，改进 README 和拟用元数据，
校验首次使用路径，给出明确上传范围。未测试的兼容性和增长结论必须标明。
```

公开之后的预期安装入口：

```bash
npx skills add frabcd/github-discoverability-skill --skill github-discoverability
```

这使用第三方安装器；公开远端安装与真实客户端激活未在这里测试。
也可先将整个 Skill 文件夹复制进支持的项目级 Skill 目录。说明见英文 README。

## 只上传，不再开发

把本发布包与 [UPLOAD_ONLY_PROMPT.md](UPLOAD_ONLY_PROMPT.md) 交给 Agent。
它只检查文件、绑定经你确认的 OWNER/REPO、提交允许的文件、设置元数据、读回验证。
身份、可见性、发布范围不明确时一次询问。不会自动发帖、买星或改业务代码。

## 免费的本地检查

```bash
python skills/github-discoverability/scripts/preflight.py . --json
python scripts/demo.py
python -m unittest discover -s tests -v
```

Python 3.10+，零 pip 依赖。检查器只读，结果不包含匹配到的密钥内容。
这是有限文件检查，不检查完整 Git 历史，不证明没有秘密或版权问题，也不预测爆火。

## 为什么不写“保证 5K”

GitHub 搜索、技能目录发现、使用、Star 是不同环节。
搜索优先是产品策略，不能据此宣称 GitHub 大多数用户来自搜索。
泛化发布和增长 Skill 已经有同类；本项目不宣称全球首创。

5K+ stars 是目标，不是完成状态或承诺。经验库最初为空；调研不是亲自做成的增长案例。
本版本没有真实外部用户或增长验证，具体本地执行证据见 validation。
