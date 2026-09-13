# Experience-to-skill: a real observation log, not invented expertise

The initial experience log is empty. Repository research produces hypotheses;
local tests produce local implementation evidence. Neither equals a history of
successful public launches.

Only review results when explicitly requested. No default polling, telemetry,
traffic collection, background work, or automatic edits to installed skills.

## Store observations privately

Use `.release-private/` outside the approved publication list, or another
user-approved private location. Do not add customer/repository private analytics
to a public skill. A .gitignore alone is not a publication safeguard.

Example record (fields start unknown, not zero):

```json
{
  "experiment_id": "",
  "repository": null,
  "change": "",
  "hypothesis": "",
  "start_utc": null,
  "end_utc": null,
  "source_of_observation": null,
  "metrics": {"stars_start": null, "stars_end": null, "unique_visitors": null},
  "confounders": [],
  "result": "unmeasured",
  "causal_claim_supported": false,
  "candidate_lesson": null,
  "approved_for_skill_update": false
}
```

## Measurement constraints

GitHub traffic exposes a recent 14-day window to authorized users. Referring-site
information excludes search engines and GitHub itself in the documented UI.
It is not a full keyword/referral attribution system. Do not infer actual user
queries or the share of search traffic from it.

Store dates and intervals when using approved data. Do not sum overlapping
14-day snapshots or daily unique visitors as though they were unique people over
a longer period. Clones can include automation; stars are not active users.

[Traffic UI](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository)
[Traffic API](https://docs.github.com/en/rest/metrics/traffic)

## Decide what changes

For an installation fix, rerun the exact failing first-use path and record success.
For messaging, compare user comprehension/first result where a real study is
possible. Stars after a launch are affected by timing, external exposure, audience,
product changes and many other factors. A before/after chart alone is not causal.

At review, classify a candidate lesson:
- anecdote: one observation, keep private and scoped;
- hypothesis: needs testing;
- supported operational rule: reproduced within its stated conditions;
- contradicted/expired: revise or retire.

Do not impose an arbitrary count as proof of a universal marketing law.
Human-review the evidence, scope and proposed diff. Add a regression check where
possible. Update a source skill version only with authorization; never mutate all
installed copies. Safety and truthful-claims constraints cannot be voted away by
an engagement increase.

When nothing can be concluded, write INSUFFICIENT EVIDENCE. That is a valid result.
