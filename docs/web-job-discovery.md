# Web Job Discovery Phase 1

This document defines the Phase 1 public-web discovery module for Job Search Collector.

## Scope

Phase 1 adds a second candidate-discovery path beside Gmail alerts.

```text
Gmail alerts ----\
                  > unified candidate pool -> matching -> dedupe -> Tracker
Web Discovery ---/
```

The module runs inside the existing Scheduled Task. It is not a separate task.

Hiring-post discovery, Canadian job-board expansion, recruiter discovery, hiring-manager discovery, and outreach are outside this Phase 1 scope.

## User experience

Bootstrap asks one additional plain-language question:

English:

> Would you like Job Search Collector to also search the public web for additional jobs that may not appear in your email alerts?

Korean:

> 메일 알림에 없는 공고도 Job Search Collector가 웹에서 추가로 찾아보게 할까요?

Recommended default: enabled.

The user does not configure ATS domains, search queries, weekdays, frequency, or query counts.

## Config

Phase 1 uses `config_version = 5`.

New Config keys:

- `module_web_discovery`: true or false from the bootstrap choice
- `web_discovery_max_queries`: 20

Do not create a Web Discovery weekday or frequency key.

## Control

Add:

- `last_successful_web_discovery_date`

The date uses `Config.schedule_timezone`.

Web Discovery is due when it is enabled and the marker is blank or earlier than the current local calendar date.

This means Web Discovery can run at most once per local calendar day.

Its marker is independent from Gmail's `last_successful_scan_date`.

## Query generation

Build query phrases from the private career profile.

Use:

- `primary_titles` first for core role phrases
- `adjacent_titles` for plausible nearby role phrases
- `target_seniority` only when it naturally contributes to a title phrase
- `target_locations` for geographic intent
- `work_models` when remote or hybrid intent materially narrows results
- Search interpretation and role-preference notes to preserve user intent

Hard exclusions are applied during evaluation rather than converted into a large negative-query list that could hide plausible jobs.

## Phase 1 ATS domain families

First-pass site-restricted search covers these 12 domain families:

| ATS | Search domain family |
|---|---|
| Workday | `myworkdayjobs.com` |
| Greenhouse | `boards.greenhouse.io` |
| Ashby | `jobs.ashbyhq.com` |
| Lever | `jobs.lever.co` |
| BambooHR | `bamboohr.com` |
| iCIMS | `icims.com` |
| Dayforce | `jobs.dayforcehcm.com` |
| SmartRecruiters | `jobs.smartrecruiters.com` |
| Rippling | `ats.rippling.com` |
| Recruitee | `recruitee.com` |
| Teamtailor | `teamtailor.com` |
| Personio | `jobs.personio.com` |

Some ATS products allow customer-specific or custom domains. The workflow must not invent an ATS domain. Broader search can discover official company Careers pages that do not match these domain families.

## Query budget

Maximum per Web Discovery run: 20 queries.

First pass:

- one site-restricted query for each of the 12 ATS domain families
- total: 12

Before choosing the second stage, first-pass results must be evaluated enough to count verified surfaced Strong/Possible jobs.

Definitions:

- `verified`: the actual posting page was opened and confirmed to represent a currently open job
- `surfaced`: after applying the shared historical-disposition rules, the posting is not suppressed and is eligible to be shown, including a re-evaluated existing row
- identity lookup uses comparison-normalized Company + comparison-normalized Title from `docs/matching-rules.md`
- do not try to classify a match as a repost, new requisition, or repeated collection

If first pass yields at least 5 verified surfaced Strong/Possible roles:

- measured ATS families may receive a second query: Workday, Greenhouse, Ashby, Lever, BambooHR, iCIMS, Dayforce
- maximum 7 additional queries
- maximum 19 site queries total

If first pass yields fewer than 5 verified surfaced Strong/Possible roles:

- use the remaining query budget for broader web search
- broader search has priority over a second query for the measured ATS families
- favor official Careers and open-role pages
- avoid aggregator-only result pages when useful
- do not perform hiring-post discovery

Never exceed 20 total queries.

This allocation is an initial Phase 1 rule and is expected to be tuned after operating data is available.

## Shared identity normalization

Web Discovery does not define its own duplicate-normalization rules. After a posting is parsed, use the shared Company and Title comparison normalization from `docs/matching-rules.md` before deciding whether the posting is new.

This is required for Search-to-Search and Mail-to-Search comparisons. For example, a Title using an en dash and the same Title using a hyphen must not become separate opportunities solely because of that character difference.

Tracker storage/display values remain separate from these comparison-only values.

## Posting verification

A search result snippet is never sufficient for a normal candidate write.

For each plausible web result:

1. open the result
2. follow it to the actual official Careers or ATS posting when needed
3. confirm that it is a specific job posting
4. confirm that it appears currently open
5. prefer the official Careers or ATS application URL
6. look for a posted date on the posting page or another authoritative representation of the same posting

Useful open-state evidence includes an active job description with a working Apply action or another explicit indication that applications are open.

If the posted date cannot be found:

- do not guess
- the role may still be used when otherwise verified open
- add `Posted date unavailable` to Notes

If the posting page cannot be opened or cannot be associated confidently with the search result:

- do not write it as a normal Candidate or Weak row from the snippet alone
- surface it in Human review or Diagnostics when useful

If the posting is confirmed closed, expired, removed, or unavailable and Company + Title remain identifiable:

- set Status = Excluded
- Notes begin `Closed: `, for example `Closed: posting unavailable`
- it may be written to Tracker so later discovery can recognize that it was reviewed
- this state remains eligible for re-evaluation if the posting surfaces again

## Fit and eligibility

Mail and Search candidates use the same matching rules.

Web provenance does not lower a fit classification by itself.

Match-to-Tracker mapping:

- Strong -> Candidate
- Possible -> Candidate
- Weak -> Excluded
- hard Excluded -> Excluded

Weak Notes must begin:

`Fit: Weak. {reason}`

Hard-exclusion Notes must begin:

`Excluded: {reason}`

For citizenship, security clearance, licensing, and similar eligibility requirements:

- auto-exclude only when the private profile contains a clear fact that conflicts with the posting
- if eligibility cannot be determined from the profile, do not guess and do not auto-exclude for that reason
- add a concise confirmation note instead

Example:

`Eligibility requirement needs confirmation: Canadian citizenship required.`

## Tracker schema and provenance

The Tracker has 14 columns:

1. Status
2. Company
3. Title
4. Location
5. Salary
6. WorkMode
7. Notes
8. Link
9. ReceivedAt
10. AppliedAt
11. RespondedAt
12. Result
13. DiscoveryType
14. Source

`DiscoveryType` is exactly:

- Mail
- Search

`Source` stores the concrete platform.

Examples:

- DiscoveryType = Mail, Source = LinkedIn
- DiscoveryType = Mail, Source = Indeed
- DiscoveryType = Search, Source = Greenhouse
- DiscoveryType = Search, Source = Workday
- DiscoveryType = Search, Source = Company Careers

These fields remain separate so users can filter discovery method independently from platform.

If a matching historical row surfaces again:

- keep the first-discovery DiscoveryType and Source unchanged
- keep the first-discovery ReceivedAt unchanged
- add the later path only to Notes as `Re-surfaced YYYY-MM-DD via {DiscoveryType} ({Source})`
- keep the existing Link while it works
- replace Link only when the existing Link is unusable and the new Link is usable for the same posting
- if Link is replaced, add `Link replaced YYYY-MM-DD` to Notes
- do not combine multiple values inside DiscoveryType or Source

## ReceivedAt

For Mail rows:

- use the original job-alert timestamp in `Config.schedule_timezone`

For Search rows:

- use the web discovery timestamp in `Config.schedule_timezone` when the row first enters Tracker

ReceivedAt is never changed when an existing row re-surfaces.

A posting date, when available, belongs in Notes rather than replacing ReceivedAt.

## Failure handling

Individual posting-page failures do not automatically fail the whole Web Discovery run.

A missing posted date does not fail the whole run.

Partial query failures are reported in Diagnostics and may still count as a successful Web Discovery run when the remaining search work produces a normal result.

Do not advance `last_successful_web_discovery_date` when:

- web search itself is unavailable
- most of the planned search stage cannot be completed well enough to produce a normal result

The exact numeric boundary between partial and majority query failure is not yet defined.

Zero discovered jobs is not itself a failure.

Web Discovery failure never blocks Gmail processing or advancement of Gmail's `last_successful_scan_date`.

## Completion criterion

Phase 1 is functionally complete when ATS and broader web discovery can place verified jobs into the unified Tracker, suppress already-applied or intentionally excluded history, and allow unapplied re-evaluable opportunities to surface again without creating duplicate rows.

Operational quality should then be evaluated using:

- proportion of closed postings discovered
- proportion of dead or unusable links
- duplicate miss rate
- number of genuinely new jobs discovered per day
