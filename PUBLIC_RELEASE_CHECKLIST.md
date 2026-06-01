# Public Release Checklist

Use this checklist before changing the repository visibility to public.

## Required before publishing

- [ ] Confirm examples are fictional and public-safe.
- [ ] Confirm no internal system prompts, private agent instructions, or proprietary prompt packs are committed.
- [ ] Confirm no customer-specific workflows, confidential tool names, endpoints, connector details, moderation rules, or escalation policies are included.
- [ ] Confirm no API keys, tokens, credentials, account identifiers, private paths, or emails are present.
- [ ] Confirm generated examples do not accidentally expose private operating logic.
- [ ] Confirm the README does not imply provider endorsement or full semantic equivalence across harnesses.
- [ ] Confirm the license, README, and quick-start commands are accurate.

## Recommended before promotion

- [ ] Add a compatibility matrix for supported source and target formats.
- [ ] Add warnings for lossy conversions.
- [ ] Add before/after examples with explanations.
- [ ] Add tests for unsupported or partially supported fields.
- [ ] Run tests locally after a fresh clone.

## Final manual review

Before publishing, search the repo for private prompts, hidden instructions, tool endpoints, connector names, customer names, employer names, emails, tokens, keys, and private paths.

This checklist is a publication aid, not a security or compatibility guarantee.
