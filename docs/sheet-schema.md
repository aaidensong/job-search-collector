# Google Sheet schema

Preferred new file name: `Job_Search_Collector`

Bootstrap always creates a **brand-new** Sheet using this schema. It does not search for, import, adapt, merge, or reuse an existing application tracker.

If `Job_Search_Collector` already exists, create a uniquely named new file such as `Job_Search_Collector_2` rather than asking to reuse the existing one.

Historical spreadsheet migration, if desired, is outside bootstrap and should be handled separately after setup.

Career history and job-fit rules do not live in this Sheet. They live in the private profile document described in `profile-file.md`.

## User-facing tab layout

The workbook still uses four tabs for reliability, but only `Tracker` is intended for normal user interaction.

Create the tabs in this order:

1. `Tracker`
2. `Config`
3. `Sources`
4. `Control`

After setup data is populated, hide `Config`, `Sources`, and `Control` when the available Google Sheets actions support hiding tabs. Keep `Tracker` visible, first, and active when possible.

Hiding is presentation only. The scheduled workflow must continue to read and write the hidden internal tabs by name. Never delete those tabs merely to simplify the user interface.

If tab hiding is unavailable, keep `Tracker` first and tell the user that `Tracker` is the only tab they need for normal use.

## Config

| Column | Name | Purpose |
|---|---|---|
| A | Key | Stable operational configuration key |
| B | Value | User/system value |
| C | Notes | Explanation or edge-case handling |

Required keys:

- `config_version` = `5`
- `profile_reference`
- `profile_storage_format` = `markdown_file` or `google_doc_markdown`
- `schedule_time`
- `schedule_timezone`
- `scan_window` = `catch_up_from_last_successful_scan`
- `auto_candidate_write` = `true` or `false`
- `auto_application_update` = `true` or `false`
- `module_missing_application`
- `module_response_detection`
- `module_no_response`
- `module_web_discovery`
- `web_discovery_max_queries` = `20`
- `no_response_days`
- `write_fallback` = `tsv`

Do not duplicate the user's career history or target-role rules into Config.

## Sources

| Column | Name | Purpose |
|---|---|---|
| A | Source | Human-readable source name |
| B | SenderPattern | Gmail sender address or domain/pattern |
| C | Enabled | true/false |
| D | DigestMode | true if one message can contain multiple jobs |
| E | LinkRule | Source-specific link normalization instruction |
| F | Notes | Parsing and message-classification notes |

Do not hardcode every provider in the public prompt. Let each user confirm the senders that actually reach their inbox.

A sender can produce more than one message type. Message classification must consider sender, subject, and body together. For example, the same sender can produce both job alerts and application confirmations.

## Tracker

Exactly 14 columns:

| # | Column | Name |
|---:|---|---|
| 1 | A | Status |
| 2 | B | Company |
| 3 | C | Title |
| 4 | D | Location |
| 5 | E | Salary |
| 6 | F | WorkMode |
| 7 | G | Notes |
| 8 | H | Link |
| 9 | I | ReceivedAt |
| 10 | J | AppliedAt |
| 11 | K | RespondedAt |
| 12 | L | Result |
| 13 | M | DiscoveryType |
| 14 | N | Source |

Status values:
- Candidate
- Applied
- Closed
- Excluded

`DiscoveryType` is the primary discovery method and accepts exactly `Mail` or `Search`. It exists so users can filter mail-collected and web-discovered opportunities independently.

`Source` is the concrete platform for the first discovery, for example `LinkedIn`, `Indeed`, `Greenhouse`, `Workday`, `Company Careers`, or `Recruiter email`. Do not combine multiple discovery methods or platforms into these filterable fields. If the same posting is later found through another path, preserve the original `DiscoveryType` and `Source` and add the later path to `Notes`.

Do not maintain separate ATS, resume-version, channel, or rejection-stage columns. If agency or recruiter context matters for a specific row, put that detail in `Notes`.

`ReceivedAt` is retained so users can tell how old a discovered opportunity is even when they review or apply several days later.

Company and Title have separate comparison and display behavior:

- comparison-normalized values are temporary runtime values used for duplicate and message-association checks and are not stored as extra Tracker columns;
- new Title display values receive safe formatting cleanup such as whitespace cleanup, dash normalization, and slash-spacing normalization while preserving capitalization and meaningful punctuation;
- new Company display values receive conservative whitespace/dash cleanup, while legal suffixes and source wording are preserved by default;
- when a comparison-normalized Company matches an existing Tracker Company, reuse the existing Tracker Company display value for a new row;
- existing Tracker rows are not rewritten retroactively, but their Company and Title values are normalized in memory whenever they participate in comparisons.

The Tracker remains exactly 14 columns.

The daily task does not rely on formula columns inside Tracker.

Historical identity matches do not automatically mean suppress.

For the same comparison-normalized Company + Title:

- AppliedAt non-empty, Status=Applied, or Status=Closed -> suppress;
- Status=Candidate -> re-evaluate;
- Status=Excluded with `Excluded: ` -> suppress;
- Status=Excluded with `Fit: Weak. ` -> re-evaluate;
- Status=Excluded with `Closed: ` -> re-evaluate;
- Status=Excluded with other non-empty Notes -> suppress as a manual/legacy exclusion;
- Status=Excluded with blank Notes -> suppress and report only the count in Diagnostics.

Recognized Notes prefixes:

- `Excluded: {reason}` = hard filter;
- `Fit: Weak. {reason}` = weak-fit judgment;
- `Closed: {reason}` = posting closed, expired, removed, or unavailable.

When an unapplied historical row surfaces again, update that existing row rather than adding a duplicate. Append `Re-surfaced YYYY-MM-DD via {DiscoveryType} ({Source})` using the current re-discovery path.

`ReceivedAt` is the first-discovery timestamp and must not change on re-surfacing.

`DiscoveryType` and `Source` are also first-discovery provenance and must not change on re-surfacing. Later paths belong only in Notes.

Keep the existing Link while it works. Replace it only when it is unusable and the new Link is usable for the same posting. When replacement occurs, append `Link replaced YYYY-MM-DD` to Notes. A working Link is not replaced merely because a newly found ATS or Careers URL appears more official.

## Control

| Metric | Value | Notes |
|---|---|---|
| config_version | 5 | schema/config compatibility |
| tracker_data_rows | formula | non-empty Company rows in Tracker |
| candidate_count | formula | Status=Candidate |
| applied_count | formula | Status=Applied |
| closed_count | formula | Status=Closed |
| excluded_count | formula | Status=Excluded |
| last_successful_scan_date | date or blank | last local calendar date fully processed by the Gmail workflow |
| last_successful_web_discovery_date | date or blank | last local calendar date successfully processed by Web Discovery |

`tracker_data_rows` is the critical completeness check. The scheduled task compares the count it actually read with this value before it makes absence, duplicate, response, or untracked-application judgments.

`last_successful_scan_date` provides missed-run recovery. On each scheduled run, the task should process every local calendar day after this value through the previous local calendar day. On the first run, use only the previous local calendar day. Update the value only after the full target period was processed successfully enough to produce the normal output or an explicit write fallback.

## Web Discovery state

`module_web_discovery` is set during bootstrap from one plain-language user choice. Users do not configure ATS domains, search queries, weekdays, or query counts directly.

There is no Web Discovery frequency or weekday key. The scheduled workflow compares `Control.last_successful_web_discovery_date` with the current local calendar date in `Config.schedule_timezone`. When Web Discovery is enabled and the marker is blank or earlier than today, the module is due to run.

`web_discovery_max_queries` is `20` for Phase 1.

The Gmail and Web Discovery success markers are independent. A Web Discovery failure must not block `last_successful_scan_date` from advancing when Gmail processing itself succeeds.
