# Search-led discovery, not search-rank promises

Sources reviewed 2026-09-13. Recheck current docs before a real release.

## Known platform behavior

GitHub repository search without an `in:` qualifier searches repository name,
description and topics. README content can be searched using `in:readme`.
This does not describe GitHub code search or an external search engine.

[Official repository-search documentation](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories)

Topics help classify repositories. Documented limits are 20 topics, at most 50
characters each, lowercase letters/numbers/hyphens. A limit is not a recommendation
to fill every slot. Topics can reveal sensitive context even for private repos.

[Official topics documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics)

The public documentation also describes non-search discovery. This package has no
reliable dataset establishing that a majority of GitHub discovery comes from
search, Explore, social links, or any other channel.

[GitHub discovery guidance](https://docs.github.com/en/get-started/exploring-projects-on-github/finding-ways-to-contribute-to-open-source-on-github)

The Vercel skills CLI documents `find`, `add`, `--list`, local paths and named
agent targets. That is a separate discovery/installation surface; it is not
GitHub's repository ranking. Publication does not guarantee directory inclusion.

[Skills CLI](https://github.com/vercel-labs/skills)

## Query worksheet

For each row record: platform, exact query, date/time, observed results, relevance,
what the user expects, which implemented feature meets it, and uncertainty.

Do not convert these search hypotheses into "monthly searches":
- github publish skill
- github launch agent
- github discoverability
- README release checklist
- agent skill release preparation

Use direct user-task language. A cute name may coexist with a descriptive subtitle,
but do not claim an exact-match name guarantees rank.

Optional diagnostics:

```text
github launch skill in:name,description,topics
github publish skill in:readme
repo:OWNER/REPO
```

A result in `repo:OWNER/REPO` can help confirm discoverability by exact identity.
It does not demonstrate ranking for a competitive query. Search can be delayed or
vary over time; record context and do not promise immediate indexing.

For each candidate topic ask: would someone following this topic reasonably
expect this repository? Omit aspirational features and untested host integrations.

## README conversion is a different problem

After arrival, the README should answer: what does this do, for whom, how do I try
it, what does it cost, what is not supported? Link to actual examples and limits.
Do not keyword-stuff. A local logo/hero file does not configure GitHub's social
preview setting; report it as an asset until the setting is explicitly applied.

[Social preview documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)

## Ethical acquisition

Seek genuine directory or integration relevance and follow each venue's rules.
Drafting is not posting authorization. Do not generate fake testimonials or
coordinated engagement. Do not reward stars with access.

[GitHub acceptable-use policy](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies)
