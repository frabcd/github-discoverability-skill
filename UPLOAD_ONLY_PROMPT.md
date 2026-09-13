# Upload-only handoff prompt

将本文件和完整项目文件夹交给有 GitHub 权限的编码 Agent。
这是上传任务，不是让 Agent 再开发本项目。目录中已经包含实际 Skill、脚本、测试与说明。
下面没有默认授权公开仓库；目标和可见性必须由用户明确确认。

---

你现在是本发布包的上传执行者，不是产品开发者。

## 目标与权限

只发布 `github-discoverability-skill` 这份已完成初版的 Skill 仓库。
不回到以前任何产品，不造网站、安装器、CLI、Agent 平台或新功能。
不重新写 Skill、增长战略或 README，不扩大本任务。

先检查用户是否已经明确给出：
- GitHub OWNER/REPO；
- 新建还是已有仓库；
- public 或 private；
- 可公开发布当前文件和 MIT 许可的授权。

如有缺失，一次询问这些必要字段。不要用已登录账号推断公开授权。
不要要求用户把 token 粘贴到对话；使用已授权的 GitHub connector 或本机 GitHub CLI 登录。
若当前主机提供 GitHub connector，按其实际 schema 使用；否则使用已安装且获授权的 gh。
不因这份文件而绕过主机权限。

## 本地检查

1. 在独立目录解压，检查文件，不要混入任何旧项目或其 Git 历史。
   存在用户未提交修改时不得覆盖。不要执行不相关仓库脚本。
2. 阅读 README、docs/validation.md、release/metadata.json 和 public-files.json。
3. 运行已有命令，不安装新的依赖：

```bash
python scripts/package.py verify
python -m unittest discover -s tests -v
python scripts/demo.py
python skills/github-discoverability/scripts/preflight.py . --json
```

系统使用 `python3` 或 Windows `py -3` 时可以等价替换。
未绑定仓库身份前 REVIEW 属预期；其余异常必须如实报告。
检查器不是完整秘密扫描或版权审查，仍须审查实际计划公开的文件。

4. 用户确认目标后，只运行现成绑定工具：

```bash
python scripts/package.py bind OWNER/REPO
python scripts/package.py verify
python skills/github-discoverability/scripts/preflight.py . --json
```

绑定工具只替换两份 README 和 release/metadata.json 中的仓库身份，
并更新同一文件清单的哈希。不授权修改核心内容或给已有仓库改名。
如发生其他问题，停止并报告；不要为了测试变绿删检查或开发新功能。

## 上传范围

只允许 `public-files.json` 中列出的文件，再加这个 manifest 文件本身。
上传前显示精确待提交列表，检查 staged diff。
不得执行 blanket `git add .` / `git add -A`，不得上传私密工作日志、缓存、token或原始参考截图。
manifest 是一致性检查，不是来自受信任签名者的安全保证。

新建仓库：仅初始化这份经过审查的快照，使用用户已确认的可见性。
已有仓库：先检查远端与分支，使用用户批准的 branch/PR 范围。
不能 force push、覆盖历史、删除文件、换许可证或把 private 改 public。
必要时只为该仓库使用经用户确认的 Git 作者信息，不修改全局配置。
GitHubCLI 认证状态可用 gh auth status 检查；不要运行输出 token 的命令。

## GitHub 设置与读回

按 release/metadata.json 设置真实 About 描述和相关 topics。
这个 JSON 文件上传成功不代表 GitHub 设置已经生效。
不要顺便创建 Release tag、Pages、包发布、外部推广或自动化定时任务；这些需要独立授权。
没有生成/配置 social preview 时，不宣称已经设置。

上传后读取并核实：
OWNER/REPO、实际 public/private、branch、commit、文件列表、README、About、topics。
若有权限和网络条件，再测试 README 中真实公开安装路径；
未经实际执行，兼容性与远端安装继续标 UNVERIFIED。
网络受限或工具缺失时明确说明，不自行绕过限制。

## 交付

只返回：
1. 仓库链接、真实可见性、分支和 commit；
2. 上传的文件范围及实际通过的检查；
3. About/topics 是否真实读回；
4. 未验证/被阻塞项；
5. 真实安装命令（未测试就明确标注）。

禁止宣称：已被搜索收录、已出现在目录、用户在使用、必达5Kstars，除非分别获得证据。
不自动发帖、买星、互刷、批量私信或给其他仓库提交宣传 PR。
上传完就结束本任务，不进入新一轮产品开发。
