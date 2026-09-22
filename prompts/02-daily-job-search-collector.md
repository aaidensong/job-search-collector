# Daily Job Search Collector prompt template

`{{SHEET_REFERENCE}}` is replaced by the bootstrap flow with the user's own Google Sheet reference.

```text
Run my daily Job Search Collector using this Google Sheet for operational configuration and tracking:
{{SHEET_REFERENCE}}

Do not rely on ChatGPT Memory, custom instructions, old chats, Project files, uploaded files, or assumptions about me.

My career data is stored in the private profile referenced by Config.profile_reference. Read that profile on every run before evaluating job fit.

[1. LOAD OPERATIONAL CONFIGURATION]

Read Config, Sources, Tracker, and Control.

Require Config.config_version = 5.
Use Config.schedule_timezone for all date and time judgments and output.
Use only Sources rows where Enabled is true.

Required Config keys:
profile_reference
profile_storage_format
schedule_timezone
scan_window
auto_candidate_write
auto_application_update
module_missing_application
module_response_detection
module_no_response
module_web_discovery
web_discovery_max_queries
no_response_days
write_fallback

Do not expect ATS, resume-version, channel, or rejection-stage configuration. These are not part of the core workflow.

Web Discovery settings:
- `module_web_discovery` controls whether public-web discovery is enabled.
- `web_discovery_max_queries` must be `20` for this version.
- Do not use or expect a web-discovery weekday or frequency setting.
- Web Discovery runs at most once per local calendar day, using `Control.last_successful_web_discovery_date` and `Config.schedule_timezone`.

[2. DETERMINE TARGET PERIOD AND CATCH UP MISSED RUNS]

Use local calendar dates in Config.schedule_timezone.

Set:
- target_end = previous local calendar day
- if Control.last_successful_scan_date is blank, target_start = target_end
- otherwise target_start = day after Control.last_successful_scan_date

Process every local calendar day from target_start through target_end.

If target_start is after target_end, report `No unprocessed calendar day` and skip candidate ingestion for this run. You may still perform non-date-dependent diagnostics when useful.

At the very top of the output, show:
`Scan period: YYYY-MM-DD to YYYY-MM-DD (timezone)`

Do not infer the scan period from the newest Tracker row. A day can be processed successfully even when no candidate was added.

Do not update Control.last_successful_scan_date yet. That happens only after successful core processing.

[3. VERIFY TRACKER READ COMPLETENESS]

Before any Tracker-dependent absence, duplicate, response, or missing-application judgment:
1. Count non-empty Tracker rows using Company as the required field.
2. Compare that count with Control.tracker_data_rows.
3. If equal, tracker_read_status = VERIFIED.
4. If unequal, retry once using the broadest available Sheet read method.
5. If still unequal, tracker_read_status = INCOMPLETE.

When tracker_read_status = INCOMPLETE:
- continue source-health and basic Gmail parsing when useful;
- do not claim a job or application is absent from Tracker;
- do not confirm historical duplicates;
- skip response, missing-application, and no-response reconciliation;
- do not write new Candidate rows because historical duplicate checks are unverified;
- report the row-count mismatch in Diagnostics;
- do not advance Control.last_successful_scan_date.

Partial data must never be used to prove absence.

[4. LOAD AND VALIDATE PRIVATE CAREER PROFILE]

Read the complete document referenced by Config.profile_reference.

Config.profile_storage_format may be:
- markdown_file
- google_doc_markdown

Treat the text as Markdown with YAML front matter.
Require profile_version = 2.

Required YAML keys:
profile_version
primary_titles
adjacent_titles
target_seniority
excluded_titles
management_roles
preferred_domains
excluded_domains
strong_skills
hard_skill_blockers
target_locations
work_models
employment_types
work_authorization
sponsorship_rule
minimum_compensation
preferred_company_types
excluded_company_types
hard_exclude_keywords
warning_keywords
languages

Also read these Markdown sections when present:
- Professional summary
- Search interpretation
- Differentiators and scope
- Experience highlights
- Measurable outcomes
- Core skills and strengths
- Portfolio or specialty areas
- Leadership experience
- Role preferences and interpretation notes
- Additional context

Set profile_read_status:
- VERIFIED
- INVALID
- UNAVAILABLE

If not VERIFIED:
- do not classify jobs as Strong, Possible, or Weak;
- do not apply personal hard filters from the unavailable profile;
- do not infer the user's target from Memory or prior task output;
- do not write candidate rows;
- report PROFILE_INVALID or PROFILE_UNAVAILABLE;
- do not advance Control.last_successful_scan_date.

[4A. NORMALIZE COMPANY AND TITLE FOR IDENTITY]

Before any duplicate check, historical comparison, missing-application check, recruiter-submission association, or response association, derive comparison-only identity values for Company and Title.

Keep comparison values separate from Tracker display/storage values. Do not add comparison fields to the Tracker schema.

COMPARISON NORMALIZATION

Apply to both Company and Title:
1. normalize Unicode compatibility forms consistently;
2. trim leading and trailing whitespace;
3. convert non-breaking and other spacing variants to normal spaces;
4. collapse consecutive whitespace to one space;
5. convert common dash variants, including en dash, em dash, non-breaking hyphen, Unicode hyphen, and minus sign, to ASCII hyphen `-`;
6. normalize spacing around hyphen separators to exactly one space on each side;
7. compare case-insensitively using Unicode-aware case folding;
8. normalize curly double quotes to `"` and curly single quotes/apostrophes to `'`;
9. normalize spaces around `/` so `UX / UI` and `UX/UI` compare the same.

Additional Title comparison rule:
- when a middle dot or bullet is clearly used as a spaced title separator, such as `Designer · Growth`, treat it like ` - ` for comparison;
- do not remove parentheses, commas, colons, slashes, or their contents;
- do not remove unspaced middle dots or punctuation that may be part of a real title.

Additional Company comparison rule:
- remove trailing legal entity designators only for comparison, case-insensitively and punctuation-tolerantly: `Inc`, `Inc.`, `Incorporated`, `Ltd`, `Ltd.`, `Limited`, `LLC`, `Corp`, `Corp.`, `Corporation`;
- remove only terminal legal designators, not the same words when they occur inside the company name;
- after removing a terminal legal designator, trim a preceding comma and whitespace;
- do not infer parent/subsidiary relationships or remove other company-name words.

Examples:
- `Lead Product Designer, Design Systems – AI Enablement` and `Lead Product Designer, Design Systems - AI Enablement` compare equal.
- `Acme, Inc.` and `ACME` compare equal as Company.
- `Product Designer (Growth)` and `Product Designer (Platform)` do not compare equal merely because the text outside parentheses matches.

STORAGE/DISPLAY NORMALIZATION

For a newly written Title:
- trim leading/trailing whitespace;
- collapse consecutive whitespace;
- convert common dash variants to ASCII hyphen and use one space around the hyphen;
- normalize spaces around `/` by removing spaces around the slash;
- otherwise preserve source wording, capitalization, parentheses, quotes, commas, and other meaningful punctuation.

For a newly written Company:
- trim leading/trailing whitespace;
- collapse consecutive whitespace;
- normalize common dash variants to ASCII hyphen with one space around the hyphen when it is used as a separator;
- preserve capitalization, legal suffixes, and other source wording by default;
- if Tracker already contains a Company display value whose comparison-normalized Company equals the new Company, reuse the existing Tracker display value for the new row.

Do not retroactively rewrite existing Tracker rows in this workflow. Existing rows must still be comparison-normalized in memory when used for duplicate or association checks.

Use the same comparison-normalization rules everywhere Company + Title identity is used.

[5. COLLECT CANDIDATES FROM MAIL AND WEB]

A. MAIL DISCOVERY

For every enabled Sources.SenderPattern, search Gmail for messages received during the full target period.

Read messages, not only thread summaries.
Read each message individually even when Gmail grouped several messages into one thread.

If DigestMode is true, open the body and extract every distinct job in the message. Do not assume the subject contains the only job.

For each extracted job, capture when available:
- company
- title
- location
- salary
- work mode
- DiscoveryType = Mail
- source platform
- received timestamp converted to Config.schedule_timezone
- raw job/application URL
- evidence needed for fit judgment

Do not invent missing company names, titles, salaries, locations, or links.

B. WEB DISCOVERY RUN CONDITION

Run this module only when ALL are true:
- Config.module_web_discovery = true;
- profile_read_status = VERIFIED;
- tracker_read_status = VERIFIED;
- `Control.last_successful_web_discovery_date` is blank OR is earlier than `today`.

`today` means the current local calendar date in Config.schedule_timezone.

There is no weekday or frequency Config. This condition makes Web Discovery run at most once per local calendar day.

If Web Discovery is disabled or already completed for today, skip it without treating the Gmail workflow as failed.

C. WEB DISCOVERY QUERY INPUTS

Build search phrases from the private career profile. Use:
- `primary_titles` first for core role phrases;
- `adjacent_titles` only for plausible nearby role phrases;
- `target_seniority` as an anchor when it naturally forms a role phrase, never as an exact whitelist;
- `target_locations` for geographic terms;
- `work_models` to add remote/hybrid intent only when it materially narrows the search;
- Search interpretation and Role preferences and interpretation notes to preserve role-direction nuances;
- explicit hard exclusions only for later filtering, not for generating broad negative keyword lists that could hide plausible jobs.

Do not ask the user to write search queries.

D. VERIFIED ATS DOMAIN FAMILIES

Use these verified domain families for Phase 1 site-restricted searches:
- Workday: `myworkdayjobs.com`
- Greenhouse: `boards.greenhouse.io`
- Ashby: `jobs.ashbyhq.com`
- Lever: `jobs.lever.co`
- BambooHR: `bamboohr.com`
- iCIMS: `icims.com`
- Dayforce: `jobs.dayforcehcm.com`
- SmartRecruiters: `jobs.smartrecruiters.com`
- Rippling: `ats.rippling.com`
- Recruitee: `recruitee.com`
- Teamtailor: `teamtailor.com`
- Personio: `jobs.personio.com`

Some ATS products allow customer-specific or custom domains. Do not invent a domain. Broader search may discover official Careers pages that are not on the domain family above.

E. QUERY BUDGET

A single Web Discovery run may use at most Config.web_discovery_max_queries, which is 20 in this version.

First pass:
- run one site-restricted query for each of the 12 ATS domain families;
- use the highest-priority unused combination of role phrase and location/work-model intent that is supported by the profile;
- total first-pass site queries = 12.

Before deciding whether to broaden, evaluate first-pass results far enough to count `verified surfaced Strong/Possible` roles:
- `verified` = the actual posting page was opened and confirmed to represent a currently open job;
- `surfaced` = after applying the historical-disposition rules in [11], the posting is not suppressed and is eligible to be shown again, including a re-evaluated existing row;
- use comparison-normalized Company + comparison-normalized Title from [4A] to find matching Tracker history;
- do not try to determine whether a matching posting is a new requisition, repost, or repeated collection;
- use the SAME hard-filter and fit rules defined later in this prompt. This is a provisional pass for search branching, not a separate matching standard.

If the first pass produces at least 5 verified surfaced Strong/Possible roles:
- the measured seven ATS families may receive one second query each: Workday, Greenhouse, Ashby, Lever, BambooHR, iCIMS, Dayforce;
- use a different high-priority role/location combination from the first query;
- add at most 7 queries;
- total site queries are therefore at most 19.

If the first pass produces fewer than 5 verified surfaced Strong/Possible roles:
- use the remaining query budget for broader web search before giving any measured ATS a second query;
- broader searches should combine the highest-priority role phrases and locations with terms that favor official careers/open-role pages;
- exclude obvious aggregator-only result paths when useful, such as LinkedIn Jobs, Indeed, and Glassdoor search-result pages;
- do not use Phase 2 hiring-post discovery.

Never exceed 20 total search queries.
This allocation is an initial Phase 1 operating rule and may be tuned after observing real results.

F. VERIFY EVERY WEB RESULT

A search result or snippet is not enough to create a normal web candidate.

For each plausible result:
1. open the result;
2. follow it to the actual official Careers or ATS posting when the result is an intermediary page;
3. confirm that the page represents a specific job;
4. confirm that the posting appears open, such as an active job description with a working Apply action or other explicit open-state evidence;
5. prefer the official Careers or ATS application URL as Link;
6. look for a posted date on the posting page itself or another authoritative representation of that same posting.

If the posted date is unavailable:
- do not guess it;
- keep the role eligible for matching if the posting is otherwise verified open;
- add `Posted date unavailable` to Notes.

If the actual posting page cannot be opened or cannot be associated confidently with the result:
- do not write it as a normal Candidate or Excluded row merely from the snippet;
- report it in Human review or Diagnostics when useful.

If the posting is confirmed closed, expired, removed, or unavailable and Company + Title can still be identified confidently:
- set Status = Excluded;
- Notes must begin `Closed: `, for example `Closed: posting unavailable`;
- it may be written to Tracker so the workflow remembers that it was already reviewed, but this state remains eligible for re-evaluation if the posting surfaces again.

For web-discovered rows:
- DiscoveryType = Search;
- Source = the actual discovery platform such as Greenhouse, Workday, Ashby, Lever, BambooHR, iCIMS, Dayforce, SmartRecruiters, Rippling, Recruitee, Teamtailor, Personio, or Company Careers;
- ReceivedAt = the web discovery timestamp in Config.schedule_timezone.

G. WEB DISCOVERY FAILURE IS INDEPENDENT FROM GMAIL

Individual posting-page failures and unavailable posted dates are individual verification issues, not an automatic failure of the whole Web Discovery run.

Some query failures may still allow the Web Discovery run to succeed when the remaining planned search work produced a normal discovery result. Record partial failures in Diagnostics.

Do not advance `Control.last_successful_web_discovery_date` when:
- web search itself was unavailable; or
- so much of the planned search stage failed that a normal discovery result could not be produced.

There is intentionally no numeric threshold yet for `some` versus `most` query failures. Report this as an unresolved operating threshold in Diagnostics when it materially affects the success judgment.

Whether Web Discovery succeeds or fails must never determine whether Gmail's `Control.last_successful_scan_date` can advance.

[6. CLASSIFY MESSAGES BEFORE USING THEM]

Do not assume a sender always represents one message type.

Classify each relevant message using sender + subject + body into one of these useful categories when possible:
- job alert
- application confirmation
- recruiter submission evidence
- employer or recruiter response
- marketing/newsletter
- unknown

A sender can produce multiple categories across different messages.

Candidate collection uses only messages that actually contain identifiable open jobs.
Application confirmations and recruiter-submission evidence are retained for reconciliation when the relevant module is enabled.

If classification is uncertain, keep the message as unknown or Human review rather than forcing a category.

[7. NORMALIZE LINKS]

Prefer a stable directly usable job or application URL.

For LinkedIn, when a job ID is explicit, normalize to:
https://www.linkedin.com/jobs/view/{JOB_ID}/

Remove tracking parameters from normalized LinkedIn URLs.

For other sources, preserve a usable job/application URL from the message or linked page.

If the URL is missing, broken, inaccessible, or cannot be associated with the correct job confidently:
- leave Link blank;
- add `link not extracted` to Notes;
- never reconstruct or guess a URL.

If a posting is clearly expired or removed, keep the URL only if useful for identification and set Status = Excluded with Notes beginning `Closed: `, for example `Closed: posting unavailable`.

[8. DEDUPLICATE WITHIN THE CURRENT RUN]

Primary duplicate key: comparison-normalized Company + comparison-normalized Title using [4A].
Use location as a tie-breaker when the same title clearly represents different openings.

If the same posting appears through more than one discovery path, keep one Tracker record and preserve the DiscoveryType and Source of the path that first caused the row to enter Tracker. Do not combine multiple methods or platforms into DiscoveryType or Source because users may filter those fields.

Record later confirmed paths in Notes, for example `Also found via Mail: LinkedIn.` or `Also found via Search: Greenhouse.`
For a within-run duplicate before the row is first written, keep the usable Link from the same discovery path whose DiscoveryType and Source are retained. Use another path's Link only if that retained-path Link is unusable.

Do not infer a parent company from an unfamiliar subsidiary or brand name.
Preserve the source wording.
If two records may be the same job but company identity is uncertain, mark `suspected duplicate` in Human review instead of merging automatically.

[9. APPLY EXPLICIT HARD FILTERS]

Run only when profile_read_status = VERIFIED.

Use explicit profile rules, including when relevant:
- excluded_titles
- excluded_domains
- disallowed employment types
- hard location/work-model constraints
- sponsorship/work-authorization blockers according to sponsorship_rule
- hard_exclude_keywords
- hard_skill_blockers
- explicit management constraints

A hard exclusion must have a short evidence-based reason.
Missing information is not automatically a hard exclusion unless the profile explicitly says so.

For eligibility requirements such as citizenship, security clearance, licensing, or similar conditions, auto-exclude only when the private profile contains a clear fact that conflicts with the posting requirement. If the profile does not establish whether the user meets the requirement, do not guess and do not auto-exclude for that reason. Keep the role eligible for fit evaluation and add a concise confirmation note such as `Eligibility requirement needs confirmation: Canadian citizenship required.`

Title and level rules:
- primary_titles identifies the main direction, not an exact-title whitelist;
- adjacent_titles is not exhaustive;
- target_seniority is an anchor, not a whitelist;
- do not reject a role merely because its exact title or level was not listed;
- only explicit exclusions should close that category.

Management handling:
- `unacceptable`: exclude roles that clearly require direct people management;
- `review-needed`: keep them with a warning;
- `acceptable`: evaluate normally.

Do not confuse project leadership, mentoring, design direction, or cross-functional influence with direct people management.

[10. EVALUATE ACTUAL FIT]

Run only when profile_read_status = VERIFIED.

Judge the actual job, not title similarity alone.

Use evidence from both YAML and Markdown, especially Differentiators and scope.
Consider:
- actual responsibilities and role scope
- required experience and ownership level
- decision-making and ambiguity
- leadership expectations
- people-management requirements
- distinctive problem-solving strengths
- demonstrated differentiators and specialty areas
- product/domain fit
- skills and experience fit
- relevant measurable outcomes
- location/work-model fit
- employment/compensation fit when known

A user mainly targeting Senior can still receive Staff or Lead roles when scope is plausible for their experience.
A role can be Strong even when the exact title differs from primary_titles.
A superficially similar title can be Weak or Excluded when the required scope is unsupported.

Stretch roles:
- if much of the required scope is supported, keep as Strong or Possible depending on evidence and mention the stretch when useful;
- if materially unsupported scope is required, lower the fit or exclude using the concrete reason.

Classify:
- Strong match
- Possible match
- Weak match

Do not create false precision with numeric scores unless the private profile explicitly requests one.

For an experienced user, a Strong match should normally include at least one meaningful reason beyond exact title similarity, such as matching problem type, ownership scope, measurable outcome, specialty, domain depth, or leadership evidence.

Weak matches stay out of the main shortlist, but when the posting itself is verified they are still written to Tracker as Status=Excluded with Notes beginning `Fit: Weak. ` followed by the evidence-based reason. Hard exclusions are written with Notes beginning `Excluded: ` followed by the reason.

[11. COMPARE AGAINST TRACKER]

Run confirmed historical comparison only when tracker_read_status = VERIFIED.

Use comparison-normalized Company + comparison-normalized Title from [4A] to find matching Tracker history. An identity match by itself does NOT mean suppress.

For each matching historical row, apply this order:

1. If AppliedAt is non-empty -> SUPPRESS.
2. Else if Status = Applied -> SUPPRESS.
3. Else if Status = Closed -> SUPPRESS.
4. Else if Status = Excluded:
   - if Notes begins `Excluded: ` -> SUPPRESS as a hard exclusion;
   - if Notes begins `Fit: Weak. ` -> RE-EVALUATE;
   - if Notes begins `Closed: ` -> RE-EVALUATE;
   - if Notes is any other non-empty text -> SUPPRESS as a manual/legacy exclusion;
   - if Notes is blank -> SUPPRESS and increment a Diagnostics count for blank-note Excluded rows. Do not reactivate it automatically.
5. Otherwise, including Status = Candidate -> RE-EVALUATE.

Do not try to distinguish a repost, a new requisition, or repeated collection. Do not use job ID, URL differences, or posting date to make that determination. If an unapplied row is eligible for re-evaluation, re-use the existing Tracker row and let the user judge the posting from the current link and content.

For a re-evaluated row:
- run the current hard-filter and fit rules again;
- Strong or Possible -> Status = Candidate and show it to the user again;
- Weak -> Status = Excluded and Notes must begin `Fit: Weak. `;
- hard exclusion -> Status = Excluded and Notes must begin `Excluded: `;
- confirmed closed, expired, removed, or unavailable -> Status = Excluded and Notes must begin `Closed: `.

When the row surfaces again, append one provenance note:
`Re-surfaced YYYY-MM-DD via {DiscoveryType} ({Source})`
using the current discovery path and Config.schedule_timezone.

Preserve the existing row's original DiscoveryType and Source. Preserve ReceivedAt as the first-discovery timestamp.

Link handling for a historical row:
- keep the existing Link when it still works;
- replace it only when the existing Link is broken, inaccessible, or no longer usable and the newly discovered Link is usable for the same posting;
- do not replace a working Link merely because the new Link is an official ATS or Careers URL;
- when Link is replaced, append `Link replaced YYYY-MM-DD` to Notes.

Same comparison-normalized Company + different comparison-normalized Title is not an identity match; keep it, with concise prior-company context only when useful.

Staffing or recruiting agencies are not automatically the employer. Do not use an agency name by itself to prove an identity match.

`DiscoveryType` and `Source` always describe the first discovery path. Re-discovery paths belong only in Notes. Do not use a Channel field.

[12. SINGLE-PASS INBOX RECONCILIATION]

Run when module_missing_application or module_response_detection is enabled AND tracker_read_status = VERIFIED.

Do NOT run a separate Gmail search for every Applied row by default.

Instead:
1. read Gmail messages received in the full target period in one broad pass;
2. build a list of relevant Tracker rows, especially Status=Applied and recent Candidate rows;
3. classify the target-period inbox messages using sender + subject + body;
4. compare potential confirmations, recruiter submissions, and employer/recruiter responses using comparison-normalized Company + Title from [4A], plus thread/context evidence;
5. use a targeted follow-up search only when needed to resolve a specific ambiguity.

This inbox pass is separate from the enabled-source candidate-alert searches because employer and recruiter responses may come from completely different senders.

[13. MISSING APPLICATION DETECTION]

Run only if Config.module_missing_application is enabled AND tracker_read_status = VERIFIED.

Use clear application evidence from the single-pass inbox scan.

Strong evidence includes:
- an explicit application-confirmation email naming the company and role;
- an explicit recruiter message stating that the user's application, profile, or resume was submitted or forwarded for a specific company/role.

If comparison-normalized Company + Title is not present in Tracker and the evidence is clear, create an Applied row when automatic application updates are enabled and writes are available. Set DiscoveryType=Mail because the row was first discovered through Gmail evidence. Otherwise return the 14-column TSV fallback.

For a general career-page submission with no role title, preserve the source wording and use a non-colliding title such as `Unknown (Career Page)` only when the message truly provides no role title.

Ambiguous language such as a recruiter saying they may submit the user later is not enough. Put it in Human review.

AppliedAt = the evidence message timestamp converted to Config.schedule_timezone when no better confirmed application time is available.
DiscoveryType = Mail for a newly created row from Gmail evidence.
Source = the actual evidence platform, for example `LinkedIn`, `Company email`, or `Recruiter email`.

[14. RESPONSE DETECTION]

Run only if Config.module_response_detection is enabled AND tracker_read_status = VERIFIED.

Use the single-pass inbox messages and Tracker rows with Status=Applied.

A response must be received after AppliedAt and have enough company/title/thread context to associate it with the application.
Do not treat generic alerts or unrelated company marketing mail as a response.

When evidence is clear:
- fill RespondedAt if blank;
- if the message explicitly rejects the application, set Status=Closed and Result=Rejected;
- if it explicitly communicates another final result, store that result in Result when unambiguous;
- do not infer rejection stage;
- do not infer or store ATS platform.

Ambiguous or conflicting evidence goes to Human review and does not automatically change the row.

[15. NO-RESPONSE CHECK]

Run only if Config.module_no_response is enabled AND tracker_read_status = VERIFIED.

Find Tracker rows with:
- Status=Applied
- RespondedAt blank
- elapsed local calendar days since AppliedAt >= Config.no_response_days

Return them as no-response candidates.
Do not automatically close them or set Result=No response unless the user explicitly configured that behavior outside the core workflow.

[16. TRACKER WRITES]

Tracker schema is exactly 14 columns:
Status	Company	Title	Location	Salary	WorkMode	Notes	Link	ReceivedAt	AppliedAt	RespondedAt	Result	DiscoveryType	Source

Do not output or write ATS, ResumeVersion, Channel, or RejectionStage fields.

DiscoveryType values are exactly:
- Mail
- Search

DiscoveryType is the primary way the row first entered Tracker.
Source is the concrete platform for that first discovery.

For a normal mail-discovered candidate:
- Status = Candidate for Strong or Possible fit
- DiscoveryType = Mail
- Source = the actual mail/job-alert platform
- ReceivedAt = original job-alert timestamp in Config.schedule_timezone

For a normal web-discovered candidate:
- Strong -> Status = Candidate
- Possible -> Status = Candidate
- Weak -> Status = Excluded and Notes must begin `Fit: Weak. `
- hard Excluded -> Status = Excluded and Notes must begin `Excluded: `
- DiscoveryType = Search
- Source = the verified discovery platform
- ReceivedAt = web discovery timestamp in Config.schedule_timezone

For all new rows:
- leave AppliedAt, RespondedAt, and Result blank unless supported by reconciliation evidence;
- preserve verified posted-date/open-state information in Notes when useful.

For a historical row that is re-evaluated and surfaced again:
- update the existing row; do not append a duplicate row;
- never change ReceivedAt;
- never change DiscoveryType;
- never change Source;
- append `Re-surfaced YYYY-MM-DD via {DiscoveryType} ({Source})` using the current re-discovery path;
- keep the existing Link if it still works;
- replace Link only when the existing Link is unusable and the new Link is usable for the same posting;
- if Link is replaced, append `Link replaced YYYY-MM-DD` to Notes;
- apply the current evaluation result to Status and the recognized Notes prefix without deleting useful historical provenance notes.

Recognized Excluded-note prefixes:
- `Excluded: {reason}` = hard filter, suppressed on future identity matches;
- `Fit: Weak. {reason}` = weak-fit result, eligible for future re-evaluation;
- `Closed: {reason}` = posting closed/expired/removed/unavailable, eligible for future re-evaluation.

An Excluded row with non-empty Notes that use none of these prefixes is treated as a manual/legacy exclusion and suppressed. An Excluded row with blank Notes is also suppressed, and its count must be reported in Diagnostics.

For automatic status reconciliation:
- clear application evidence -> Status=Applied and AppliedAt if blank;
- clear employer or recruiter response -> fill RespondedAt if blank;
- explicit rejection -> Status=Closed, Result=Rejected;
- other explicit final outcome -> Status=Closed and store the supported Result;
- ambiguous evidence -> no automatic change.

Preferred mode:
- if automatic writing is enabled and permitted, apply changes directly;
- never overwrite user-entered data with a lower-confidence inference;
- reread affected rows when possible and report whether the change was applied.

Fallback mode:
- if a write cannot proceed because approval is required or the action is unavailable, return every intended insert or update as a fenced 14-column TSV block;
- clearly state that the automatic write was not applied.

[17. ADVANCE SUCCESS MARKERS]

Advance Control.last_successful_scan_date to target_end only when ALL of the following are true:
- profile_read_status = VERIFIED;
- tracker_read_status = VERIFIED;
- Gmail access worked;
- every enabled source search for the target period completed without access/query failure;
- the full target period was processed;
- normal output was produced;
- intended Tracker changes were either applied successfully or returned completely through the explicit TSV fallback.

Zero messages from a source is not itself a failure.
A source query/access failure is a failure.

If any core condition above fails, do not advance last_successful_scan_date. This allows the next scheduled run to catch up automatically.

WEB DISCOVERY MARKER

When Web Discovery ran today, set `Control.last_successful_web_discovery_date = today` only when:
- Web Discovery execution was available;
- the planned search stage completed sufficiently to produce a normal discovery result;
- zero search results is allowed and is not itself a failure;
- individual posting-page failures or missing posted dates are allowed and are reported;
- partial query failures are reported in Diagnostics and may still count as success when the remaining search work was sufficient.

Do not advance the web marker when web search was unavailable or most of the planned search stage could not be performed. The exact numeric boundary between partial and majority query failure is not yet defined.

Never use the Web Discovery marker to decide whether Gmail's last_successful_scan_date advances, and never use Gmail's marker as a substitute for the Web Discovery marker.

[18. OUTPUT]

Always produce these sections, even when empty.

At the top:
`Scan period: ...`

## Best matches
Company | Title | Location | Work mode | Salary | Match | Why | Source | Apply

Only populate when profile_read_status = VERIFIED.
Order Strong before Possible, then older ReceivedAt first unless the profile explicitly requests another order.

Use clickable Apply links when available.
The Why field should use actual scope, differentiators, specialty, domain, or outcomes. Do not use `same title` as the main reason for an experienced candidate when stronger evidence exists.

## Excluded or low priority
Company | Title | Reason | Source

Keep concise and include only jobs actually reviewed during this run.

## Applications detected
Show clear previously untracked application or recruiter-submission evidence handled during this run.

## Responses detected
Company | Title | RespondedAt | Result | Evidence

## No-response candidates
Company | Title | AppliedAt | Days

## Tracker updates
Summarize applied writes or state that no update was needed.

## Manual Tracker fallback
Only when automatic Sheet writes could not be applied. Return exact 14-column TSV rows.

## Human review
List only items needing a decision or manual action, such as:
- ambiguous company/title association
- suspected duplicate with uncertain company identity
- ambiguous recruiter submission language
- conflicting response evidence
- blocked Tracker write

## Source health
List every enabled source with its message count for the target period.
Explicitly list enabled sources with zero messages.
If all major enabled job-alert sources unexpectedly return zero messages, warn that job-alert delivery, sender patterns, or account configuration may need review.

## Diagnostics
Report:
- profile_read_status and profile_version
- Config version
- target period and timezone
- previous and resulting last_successful_scan_date
- previous and resulting last_successful_web_discovery_date
- whether Web Discovery ran, skipped, partially failed, or failed
- Web Discovery query count and whether broader search was used
- verified open web postings and verified surfaced Strong/Possible count
- tracker_read_status and row-count comparison
- number of messages read per enabled source
- number of all-inbox messages read for reconciliation when enabled
- number of extracted postings before filtering
- link extraction failures
- parsing or classification ambiguities
- automatic Tracker write result
- any skipped module and why

DIAGNOSTIC RULES
- State evidence for anomalies.
- Separate confirmed from suspected.
- Never claim absence when the relevant source was not fully read.
- Never substitute Memory when the private profile is unavailable.
```