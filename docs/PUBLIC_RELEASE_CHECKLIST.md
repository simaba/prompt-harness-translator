# Public Release Checklist

Before making this repository public:

- [ ] Confirm every source prompt, agent instruction, and example is fictional or fully sanitized.
- [ ] Remove internal system prompts, proprietary workflow instructions, private tool names, endpoints, credentials, connector details, and security/moderation policy content.
- [ ] Review all branches, git history, issues, pull requests, comments, Actions logs/artifacts, attachments, releases, and tags.
- [ ] Confirm the README and `docs/SUPPORTED_FORMATS.md` accurately describe only the formats implemented today.
- [ ] Confirm output examples visibly preserve or warn about unsupported source metadata.
- [ ] Run tests and manually inspect at least one output for each supported target.
- [ ] Create a draft release, review assets and notes, then publish a versioned snapshot.

This checklist does not prove cross-tool behavioral equivalence or replace security, privacy, legal, or employer-specific review.