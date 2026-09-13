# Approved upload procedure

Read this only for publication work. Publishing is an external side effect.

## Decisions required

Resolve exact owner/repository, new versus existing repository, public/private,
branch, license approval, staged public files and requested remote actions.
Ask one combined question for remaining required fields. Do not make a private
repository public by inference. Owner authorization also matters for org repos.
Do not change repository topics before publication scope is agreed.

## New repository

1. Inspect the reviewed export, manifest/hashes and local Git state.
2. Use a clean working directory; do not push another directory's history.
3. Authenticate through the existing authorized connector or `gh auth status`.
   Never print token values or ask the user to paste a token into a README.
4. Check whether the destination exists. Distinguish not-found from auth/network
   errors. An existing destination is not permission to overwrite it.
5. Initialize only the approved snapshot. Stage exact public files, inspect the
   staged list and diff, and make a local commit. Do not use blanket `git add .`.
6. Create the repository with explicitly approved visibility and publish.
7. Set the approved About description/topics. Creating a source file called
   metadata.json does NOT apply GitHub repository settings.
8. Read back repository identity, visibility, branch and commit. Read the remote
   README; compare uploaded file paths and, where available, content hashes.
9. Record what was actually published and what remains unverified.

## Existing repository

Do not overwrite history or licenses. Use the approved branch/PR scope. Compare
base and intended diff. Preserve protections. A force push, deletion, renaming,
visibility change, release tag or Pages deployment needs separate explicit scope.

## Interface details

Prefer a host's authorized GitHub connector if available; inspect its actual
function schema. Otherwise use an installed authenticated GitHub CLI. Commands
below name relevant operations, not an unconditional shell script:

```text
gh auth status
gh repo view OWNER/REPO --json nameWithOwner,visibility,url,defaultBranchRef
gh repo create OWNER/REPO --source . --remote origin --public --push
gh repo edit OWNER/REPO --description "approved factual description"
gh repo edit OWNER/REPO --add-topic "approved-topic"
```

Use `--private` instead of `--public` when private is approved. Read current help
before execution. Supplying `--public` in this guide is not permission to use it.

[Create](https://cli.github.com/manual/gh_repo_create)
[Edit](https://cli.github.com/manual/gh_repo_edit)
[View](https://cli.github.com/manual/gh_repo_view)
[Releases](https://cli.github.com/manual/gh_release_create)

No package registry publication, external promotion, scheduled collection,
GitHub Pages, marketplace submission or automated starring is implicit.

## Receipt

Record owner/repo, URL, actual visibility, commit, branch, allowed actions,
completed actions, omitted actions, checks, observed remote metadata and remaining
unknowns. Keep credentials, private file contents and personal data out.
Publish a receipt only after reviewing its separate public scope.
"Uploaded" does not mean indexed, installed, used, recommended or viral.
