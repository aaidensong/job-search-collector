# Observability and telemetry

## Why this exists

A small daily result can come from very different causes: low source volume, repeated discoveries, Tracker history, hard filters, weak fit, unresolved ambiguity, or closed postings. The workflow should expose enough operational evidence to distinguish those causes without requiring the user to ask follow-up questions.

## Local Collection audit

Every Scheduled Task run should calculate:

- raw Mail discoveries, including per-source counts;
- raw Web discoveries, including per-source counts when Web Discovery runs;
- within-run duplicate discoveries removed;
- unique jobs after merge;
- surfaced Strong/Possible;
- historical suppression;
- hard exclusion;
- weak fit;
- Human review / unresolved;
- closed / unavailable;
- Tracker total row count;
- Applied row count.

Accounting invariants:

`raw discoveries = within-run duplicate discoveries removed + unique jobs after merge`

`unique jobs after merge = surfaced + historical suppression + hard exclusion + weak fit + human review/unresolved + closed/unavailable`

Historical suppression should also be broken down by reason:

- AppliedAt non-empty;
- Status=Applied;
- Status=Closed;
- Excluded with `Excluded: `;
- Excluded with other non-empty Notes;
- Excluded with blank Notes.

Every historical suppression must have identifiable Tracker evidence. Accounting can show where jobs disappeared, but evidence is still required to show that a specific suppression was justified.

## User-facing output

Always show a compact Collection audit. When surfaced Strong/Possible is 3 or fewer, or an accounting invariant fails, automatically show the expanded source and disposition breakdown.

The user should not have to ask why only a small number of jobs appeared.

## Project-level telemetry status

Central telemetry is not implemented in the current project.

The project maintainer cannot currently inspect aggregate run funnels across users because each user's Gmail, profile, Tracker, and Scheduled Task remain inside that user's connected account.

Do not imply that the maintainer can see user run data.

## Requirements for future central telemetry

If central telemetry is added, it must be explicit opt-in and privacy-safe.

Allowed aggregate examples:

- anonymous or pseudonymous install identifier;
- run date bucket;
- Mail raw count;
- Web raw count;
- unique job count;
- surfaced count;
- historical suppression count and reason counts;
- hard exclusion count;
- weak fit count;
- Human review count;
- Tracker row count;
- Applied row count;
- source-zero count;
- module enabled flags;
- run success/failure;
- coarse execution duration.

Do not collect:

- email addresses;
- Gmail content;
- company names;
- job titles;
- salaries;
- application details;
- career profile text;
- Tracker rows;
- recruiter identities;
- application or response message bodies.

Telemetry failure must never block the core workflow.

Before enabling any central collection, document the endpoint, retention policy, opt-in flow, deletion path, and exact event schema.

## Product questions this data should answer

- Are users receiving too few raw opportunities, or are opportunities being filtered later?
- Which sources frequently drop to zero?
- Does historical suppression grow as the Tracker ages?
- Does Web Discovery materially increase unique surfaced opportunities?
- Which final disposition accounts for most low-result days?
- Are low-result runs caused by matching policy or source coverage?
