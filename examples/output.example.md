# Example daily output

Scan period: 2026-09-07 to 2026-09-07 (America/Toronto)

## Collection audit

- Raw Mail discoveries: 5
- Raw Web discoveries: 3
- Within-run duplicate discoveries removed: 0
- Unique jobs after merge: 8
- Surfaced Strong/Possible: 1

Because only 1 job surfaced, the expanded breakdown is shown automatically:

- Historical suppression: 2
  - AppliedAt non-empty: 1
  - Status=Applied: 1
- Hard exclusion: 1
- Weak fit: 3
- Human review / unresolved: 1
- Closed / unavailable: 0
- Tracker rows: 42
- Applied rows: 9

Check: 8 unique jobs = 1 surfaced + 2 historical suppression + 1 hard exclusion + 3 weak fit + 1 human review + 0 closed/unavailable.

## Best matches

| Company | Title | Location | Work mode | Salary | Match | Why | Source | Apply |
|---|---|---|---|---|---|---|---|---|
| ExampleCo | Senior Product Designer | Toronto, ON | Hybrid |  | Strong match | B2C funnel ownership and design-system experience match the profile's strongest evidence | LinkedIn | https://example.com/job/123 |

## Excluded or low priority

| Company | Title | Reason | Source |
|---|---|---|---|
| Example Studio | Graphic Designer | Explicit excluded title family | Indeed |

## Applications detected

None.

## Responses detected

None.

## No-response candidates

None.

## Tracker updates

- Added `ExampleCo - Senior Product Designer` as `Candidate`.
- Automatic Tracker write: applied.

## Human review

None.

## Source health

- LinkedIn Alerts: 2 messages
- Indeed Alerts: 1 message
- Glassdoor Alerts: 0 messages

## Diagnostics

- Config version: 5
- Profile version: 2
- Previous last_successful_scan_date: 2026-09-06
- Resulting last_successful_scan_date: 2026-09-07
- Previous last_successful_web_discovery_date: 2026-09-06
- Resulting last_successful_web_discovery_date: 2026-09-07
- Web Discovery: completed, 12 site queries, broader search not needed
- Tracker read: VERIFIED, 42 rows read / 42 expected
- Extracted postings before filtering: 8
- Discovery accounting: VERIFIED
- Historical suppressions with identifiable Tracker evidence: 2 / 2
- Automatic Tracker write: applied
- Link extraction failures: 1

## Manual Tracker fallback example

This section appears only when an automatic Sheet write could not be applied.

```tsv
Candidate\tExampleCo\tSenior Product Designer\tToronto, ON\t\tHybrid\tB2C funnel and design-system fit\thttps://example.com/job/123\t2026-09-07 09:15\t\t\t\tMail\tLinkedIn
```

The Tracker schema has exactly 14 columns:

`Status, Company, Title, Location, Salary, WorkMode, Notes, Link, ReceivedAt, AppliedAt, RespondedAt, Result, DiscoveryType, Source`