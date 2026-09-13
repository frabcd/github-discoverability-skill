# GitHub Discoverability Skill

**Turn “push it to GitHub” into a release people can find, understand and try.**

An agent skill for GitHub launch preparation, search-aware repository metadata,
evidence-backed READMEs, and a reviewed upload handoff. It works on an **existing
project**; it is not an app builder or a promise of viral growth.

[中文说明](README.zh-CN.md) · [Read the skill](skills/github-discoverability/SKILL.md) · [Research and alternatives](docs/research.md) · [Local evidence](docs/validation.md)

## What you get

| Input | Output |
|---|---|
| A working local project | A concrete task/value statement, not a new invented product |
| Real search questions | A dated query-to-feature map with unknown demand kept unknown |
| Current project evidence | Factual README/About/topics and limitations |
| Approved public snapshot | Local hygiene report, file hashes and upload instructions |
| Real post-launch observations | A reviewed, scoped lesson proposal—not made-up growth wisdom |

## A useful first request

```text
Use github-discoverability on this repository.
Prepare its GitHub launch, but do not publish or change application code.
Research three close alternatives, improve the README and proposed metadata,
check the first-use instructions, and produce an exact upload handoff.
Mark every untested claim. Do not promise stars.
```

Upload only is a separate mode. It checks and publishes an already authored,
explicitly approved file set; it does not tell the agent to build a new product.

## Install

Inspect [SKILL.md](skills/github-discoverability/SKILL.md) and its resources first.
The package follows the Agent Skills directory format. Real client activation
and live distribution tests are listed separately in [validation](docs/validation.md).

After this repository is publicly available, the intended third-party CLI route is:

```bash
npx skills add frabcd/github-discoverability-skill --skill github-discoverability
```

Select your agent in the installer. This route uses the external skills CLI and
network access; its documented behavior is not an end-to-end test of this release.
A release agent must test and record the actual remote route before claiming it works.

For local use, copy the entire `skills/github-discoverability` folder to a
project's `.agents/skills/` for Codex or `.claude/skills/` for Claude Code, avoiding
an existing skill with the same name. These are documentation-based paths;
client behavior can change and has not been exercised here.

## Try the helper without an agent

Python 3.10+; no pip dependencies, credentials or network needed.

```bash
python skills/github-discoverability/scripts/preflight.py . --json
python scripts/demo.py
python -m unittest discover -s tests -v
```

The demo checks synthetic before/after fixtures. It is not a customer case or
evidence of improved search rank. The checker does not write files or execute
the target project. It does not scan Git history, every secret type, all media,
or external links, and it does not judge whether a README is persuasive.

Before the repository identity is bound, the package audit correctly reports
REVIEW. That is not a hidden failure: see [publishing instructions](UPLOAD_ONLY_PROMPT.md).

## Search-aware, not search spam

GitHub's documented default repository search matches name, description and
topics; README search is available with `in:readme`. The skill checks these as
separate surfaces. It does not know GitHub's ranking formula, keyword volume, or
the share of users coming from search. See [sources](docs/sources.md).

Do not use unrelated topics, fake metrics, auto-stars, promotional PR spam, or
hidden keywords. A successful upload is not evidence of adoption.

## Limits and alternatives

Generic GitHub publishing and launch skills already exist, including close
alternatives with privacy review and adoption feedback. This is an original,
compact implementation—not a claimed new category. Read the dated
[comparison](docs/research.md) before choosing it.

The local helper needs only Python. The surrounding agent can have model costs
and provider data processing; this package makes no fully-offline agent claim.
The optional publication path needs authenticated GitHub access and explicit
permission. A clean audit is never permission to publish.

## Contribute an actual lesson

Report a reproducible installation failure or a consented, sanitized release
observation. See [contribution rules](CONTRIBUTING.md). “It got stars, therefore
this caused them” is not adequate evidence. No private user analytics are bundled.

## Status

Version 0.1.0. Locally authored and tested as recorded; no external user study,
real launch outcome, search-rank result or 5K-star achievement is claimed.

## License

[MIT](LICENSE). Research sources are linked, not copied into the skill.
Not affiliated with GitHub, OpenAI, Anthropic or Vercel.
