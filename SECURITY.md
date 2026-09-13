# Security and privacy

Inspect any skill before granting an agent file or network access. This skill does
not add sandboxing to the host. Its read-only helper is heuristic and intentionally
limited; it is not a credential-scanner replacement or publication authorization.

Do not put live secrets in public issues. Use the repository's private vulnerability
reporting feature if the owner has explicitly enabled it; otherwise privately
contact the owner through an established channel before sharing exploit details.
No private reporting endpoint is currently configured by this package.

Unexpected file access, network calls, publication or engagement automation are
bugs, not growth features. Report sanitized reproduction steps.
