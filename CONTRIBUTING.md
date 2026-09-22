# Contributing

Thanks for helping improve Job Search Collector. Small fixes and clear reproduction steps are useful.

## Good places to start

- Improve instructions or translations.
- Add a redacted example of a job-alert email format the workflow misses.
- Describe a matching or duplicate-detection edge case.
- Test onboarding, Scheduled Task runs, or the explicit TSV fallback.

Open an [issue](https://github.com/aaidensong/job-search-collector/issues/new/choose) for bugs, ideas, and new job-alert sources. Search existing issues first. For a substantial workflow change, describe the problem and expected behavior in an issue before editing prompts.

## Privacy in examples

Do not post your actual Gmail messages, career profile, application history, private Sheet links, tokens, or credentials. Replace names, email addresses, URLs, and identifying details with fictional values. State which parts of an example are invented.

## Pull requests

1. Fork the repository and make a focused branch.
2. Keep the English and Korean READMEs aligned when changing information shown in both.
3. If you change behavior in `prompts/`, update the relevant `docs/` reference and a fictional example. Check the 14-column Tracker schema in [`docs/sheet-schema.md`](docs/sheet-schema.md).
4. Describe what changed, why, and how you checked it. For documentation-only changes, check links, rendering, and examples; no automated test suite is required.

This repository contains prompts and templates for a connected ChatGPT workflow. Contributors do not need to connect personal accounts to fix documentation or examples. Connected behavior can differ with permissions and product changes, so report the exact observed behavior without publishing private data.
