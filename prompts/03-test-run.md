# Test-run prompt

Use this after bootstrap or after changing the profile, sources, or schema.

```text
Run Job Search Collector in TEST MODE only.

Use the configured Job Search Collector Google Sheet, the private profile referenced by Config.profile_reference, and the configured Gmail sources.
Do not create, edit, delete, or append Tracker rows.
Do not change the recurring schedule.
Do not update Control.last_successful_scan_date or Control.last_successful_web_discovery_date in test mode.

Require Config.config_version = 5 and profile_version = 2.

Use the same scan-period logic as the daily workflow:
- target end = previous local calendar day in Config.schedule_timezone;
- if Control.last_successful_scan_date is blank, target start = target end;
- otherwise target start = day after last_successful_scan_date;
- if the resulting period contains no day, report that there is no unprocessed calendar day and use the nearest recent 24-hour window with enabled-source mail only for parsing validation.

Return:
1. Config version and whether required Config values were readable;
2. profile reference, storage format, profile readability, and profile version;
3. whether the Markdown career-evidence sections were readable, including Search interpretation and Differentiators and scope;
4. whether an experienced user's profile contains enough evidence beyond title and years to explain meaningful fit differences;
5. Control.last_successful_scan_date and the calculated target period;
6. enabled Sources and message count for each in the test period;
7. one example of a digest email expanded into individual jobs, if available;
8. Tracker row count read vs Control.tracker_data_rows;
9. up to three extracted jobs with parsed application URLs;
10. hard-filter result and match class for those examples when profile validation passes;
11. for every Strong or Possible example, the specific profile evidence used to justify the match;
12. whether plausible nearby titles were evaluated by actual scope rather than title label alone;
13. whether messages from the same sender were classified by sender + subject + body rather than sender alone;
14. if response or missing-application detection is enabled, whether a single-pass inbox scan can be performed for the target period without running a separate company search for every Applied row;
15. whether clear application-confirmation or recruiter-submission evidence can be distinguished from ambiguous evidence;
16. whether Web Discovery is enabled, whether it is due today under `last_successful_web_discovery_date < today`, and whether web search is available;
17. when Web Discovery is due, validate the first-pass query plan against the 12 ATS domain families without exceeding 20 total queries, and report whether broader search would be triggered by the verified-surfaced Strong/Possible threshold;
18. verify that a web result is not accepted from a search snippet alone and that a real posting page/open state is checked;
19. verify that mail rows use DiscoveryType=Mail and web rows use DiscoveryType=Search, with Source reserved for the concrete platform;
20. verify that unknown eligibility details are flagged for confirmation rather than guessed as hard exclusions;
21. whether automatic Tracker writing is available when enabled, or whether TSV fallback would be required;
22. Company/Title normalization checks showing that:
   - en dash, em dash, Unicode hyphen variants, and hyphen compare consistently;
   - leading/trailing, repeated, and non-breaking whitespace do not create false differences;
   - case differences do not create false differences;
   - curly vs straight quote variants do not create false differences;
   - `UX / UI` and `UX/UI` compare consistently;
   - supported trailing Company legal suffix variants such as `Inc.` vs no suffix compare consistently;
   - meaningful parentheses content remains distinct;
23. historical-disposition regression checks showing that:
   - Candidate + blank AppliedAt is re-evaluated rather than suppressed;
   - non-empty AppliedAt suppresses even if Status is not Applied;
   - Status=Applied suppresses;
   - Status=Closed suppresses;
   - Status=Excluded with `Excluded: ` suppresses;
   - Status=Excluded with `Fit: Weak. ` is re-evaluated;
   - Status=Excluded with `Closed: ` is re-evaluated;
   - Status=Excluded with other non-empty Notes suppresses;
   - Status=Excluded with blank Notes suppresses and is counted in Diagnostics;
   - a re-surfaced row reuses the existing row and does not append a duplicate;
   - ReceivedAt remains unchanged;
   - DiscoveryType and Source remain unchanged;
   - Notes receives `Re-surfaced YYYY-MM-DD via {DiscoveryType} ({Source})`;
   - a working existing Link is preserved even when a newly found ATS/Careers link is available;
   - Link is replaced only when the existing Link is unusable and the replacement is usable for the same posting;
   - a Link replacement records `Link replaced YYYY-MM-DD`;
   - `Closed: posting unavailable` is eligible for re-evaluation when the posting surfaces again;
24. all permissions, profile, parsing, source, web-discovery, normalization, historical-disposition, or completeness failures.

Pass criteria:
- private profile readable and valid
- Gmail readable
- Sheet readable
- Tracker completeness verified, or an explicit INCOMPLETE diagnostic is produced without unsupported absence claims
- enabled-source search works
- digest extraction works when a digest exists
- no fabricated application link
- Tracker output schema is exactly 14 columns
- DiscoveryType and Source are separate fields; DiscoveryType is only Mail or Search
- no ATS, ResumeVersion, Channel, or RejectionStage field is produced
- plausible nearby titles are evaluated by actual scope, not title label alone
- Strong matches for experienced users use at least one meaningful evidence signal beyond exact title similarity when that evidence is available
- missed-run catch-up period is calculated correctly
- Web Discovery never advances or blocks the Gmail successful-scan marker
- Web Discovery marker is not changed in test mode
- normalization is applied before within-run dedupe, historical Tracker dedupe, missing-application association, recruiter-submission association, and response association
- comparison normalization does not require or add Tracker columns
- existing Tracker rows are not rewritten in test mode
- historical identity matches are tested as suppress vs re-evaluate decisions rather than automatically treated as duplicates
- re-surfacing preserves first-discovery provenance and ReceivedAt

Do not say the setup passed if the profile, Gmail, or Sheet required permission failed.
```