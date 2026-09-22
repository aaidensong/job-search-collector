# Architecture

## 1. ChatGPT setup layer

Runs once in a normal ChatGPT conversation after the user connects Gmail and Google Drive.

User responsibilities:
- connect Gmail and Google Drive
- paste the bootstrap prompt into a new ChatGPT chat
- answer onboarding questions naturally
- approve product permission or task-creation prompts when required

GPT responsibilities:
- verify app access
- collect career evidence and matching constraints conversationally
- show only the approximate remaining-question count at the bottom of onboarding turns
- create the private profile
- discover and confirm Gmail alert sources
- create a brand-new Tracker Sheet using the workflow's own schema
- verify read and write behavior
- create the Scheduled Task
- run a setup test

The user should not manually create, move, or wire together the profile and Tracker resources.

### Compact conversational onboarding

The setup conversation does not expose internal stages, a setup roadmap, stage numbers, stage names, or an upfront estimate of total answers.

ChatGPT asks exactly one onboarding question per turn. A natural-language answer may resolve several profile fields at once, and already resolved questions are skipped.

For career, experience, preference, and constraint questions, the question is the main visual emphasis and one concise fictional example appears directly below it.

The only progress indicator is an approximate remaining-question count at the very bottom of the message:

- Korean: `남은 질문: 약 N개`
- English: `Questions remaining: about N`

The count is recalculated from unresolved topics. Permission dialogs, approval taps, resource creation, and tests are not counted as onboarding questions.

### Fresh Tracker boundary

Bootstrap always creates a new Job Search Collector Tracker.

It does not:
- ask whether the user already has a tracker;
- search Drive for an existing tracker;
- import historical spreadsheet data;
- adapt the workflow to an arbitrary existing schema;
- reuse an existing `Job_Search_Collector` file.

If the preferred name already exists, the setup creates a uniquely named new Sheet automatically.

Historical spreadsheet migration, if desired, is a separate post-setup task that should be handled in another ChatGPT conversation.

This boundary does not affect ongoing Gmail reconciliation. A scheduled run may still create a missing Applied row from clear application-confirmation or recruiter-submission evidence.

## 2. Private profile layer

A private Markdown-formatted document owned by the user.

Preferred name:
`Job_Search_Collector_Profile.md`

The profile stores:
- main target direction and nearby roles to consider when actual fit is strong
- career background and relevant experience
- differentiators, scope, impact, and recurring problem types
- strengths and skills
- domain preferences and exclusions
- geography and work model
- employment constraints
- work authorization and sponsorship handling
- hard exclusions and warnings
- leadership evidence kept separate from direct people management

The profile uses `profile_version = 2`.
It does not track resume versions.

Public examples must be fictional and must not be derived from a user's private profile or prior conversation history.

## 3. Operational configuration layer

Google Sheet owned by the user.

The workbook is presented Tracker-first: `Tracker` is the only user-facing tab, while `Config`, `Sources`, and `Control` are internal operational tabs. When supported, the internal tabs are hidden after setup without changing their names or accessibility to the workflow. If hiding is unavailable, `Tracker` still remains first.

### Config
Stores schedule, profile reference, automation settings, and write behavior.

Current schema uses `config_version = 5`.

### Sources
Stores confirmed Gmail sender patterns plus source-specific parsing and message-classification notes.

A sender may produce more than one message type. Classification uses sender + subject + body.

### Tracker
Stores job candidates and application history in 14 columns:

`Status, Company, Title, Location, Salary, WorkMode, Notes, Link, ReceivedAt, AppliedAt, RespondedAt, Result, DiscoveryType, Source`

The Tracker intentionally does not store ATS, ResumeVersion, Channel, or RejectionStage.

`DiscoveryType` is `Mail` or `Search` and records the primary discovery method. `Source` records the concrete platform. The two fields remain separate so users can filter discovery method independently from platform. Agency or recruiter details go in Notes only when useful.

### Control
Stores verification metrics, `last_successful_scan_date`, and `last_successful_web_discovery_date`.

`last_successful_scan_date` lets the Gmail workflow catch up automatically after a skipped or failed scheduled run. `last_successful_web_discovery_date` independently prevents Web Discovery from running more than once per local calendar day. Web Discovery failure does not block the Gmail marker.

## 4. Scheduled ingestion and Web Discovery layer

Runs automatically inside ChatGPT at the configured time. The user does not manually start the daily task.

Responsibilities:
- load Config and Control
- calculate every unprocessed Gmail calendar day through yesterday
- read and validate the private profile
- read configured Gmail job-alert sources
- when enabled and due, run public-web discovery at most once for the current local calendar day
- generate search queries from the private profile
- search the Phase 1 ATS domain families first and broaden only when the verified-new Strong/Possible threshold is not met
- verify actual posting pages before normal candidate writes
- expand digest messages
- classify messages by actual content
- merge mail and web candidates into one candidate pool
- extract structured jobs
- derive comparison-normalized Company and Title identity values
- normalize links
- deduplicate within the run using normalized Company + Title

The scan marker advances only after the target period is fully processed successfully enough to produce normal output or a complete TSV write fallback.

### Phase 1 Web Discovery boundary

Web Discovery is a conditional module inside the existing Scheduled Task, not a second task. It uses a maximum of 20 search queries per run. Search and mail use the same hard-filter and fit rules.

The initial search pass covers 12 verified ATS domain families: Workday, Greenhouse, Ashby, Lever, BambooHR, iCIMS, Dayforce, SmartRecruiters, Rippling, Recruitee, Teamtailor, and Personio. If the first pass produces fewer than five verified new Strong/Possible roles, remaining query budget is used for broader web search. Hiring-post discovery is outside this Phase 1 boundary.

A web result is not treated as a normal candidate from a snippet alone. The workflow must open and validate the actual posting page and open state. Missing posted dates are noted without being guessed.

## 5. Matching layer

Two-stage decision model:

1. Hard filters remove explicit non-starters.
2. Fit matching classifies the remainder as Strong, Possible, or Weak.

Matching prioritizes actual responsibilities and demonstrated career evidence over exact title equality.

For experienced users, Strong matches should normally include a meaningful reason beyond title similarity, such as matching problem type, ownership scope, measurable impact, specialty, domain depth, or leadership evidence.

## 5A. Identity normalization layer

Company and Title identity normalization sits after extraction and before every duplicate or row-association judgment.

The workflow keeps two representations:

- comparison values: temporary, aggressively normalized enough to absorb harmless source differences such as dash variants, whitespace, case, quote style, slash spacing, and supported terminal Company legal suffixes;
- display values: conservative values written to Tracker so the source wording remains readable.

Comparison values are not Tracker columns.

The same comparison logic is used for within-run deduplication, historical Tracker comparison, Web Discovery new-role counting, application-confirmation association, recruiter-submission association, and response association.

Existing Tracker rows are not migrated or rewritten by this layer. They are normalized in memory when compared.

## 6. History and completeness layer

Before making absence or historical-history judgments, the workflow compares rows actually read from Tracker with `Control.tracker_data_rows`.

When completeness is verified, a comparison-normalized Company + Title identity match is resolved by historical disposition rather than suppressed automatically:

- AppliedAt non-empty -> suppress
- Status=Applied -> suppress
- Status=Closed -> suppress
- Status=Excluded with `Excluded: ` -> suppress
- Status=Excluded with `Fit: Weak. ` -> re-evaluate
- Status=Excluded with `Closed: ` -> re-evaluate
- Status=Excluded with other non-empty Notes -> suppress
- Status=Excluded with blank Notes -> suppress and count in Diagnostics
- otherwise, including Candidate -> re-evaluate

The workflow does not try to identify reposts or new requisitions. Re-evaluable history reuses the existing row and can surface again after current fit/hard-filter evaluation.

When completeness is not verified:
- absence claims are disabled
- historical disposition confirmation is disabled
- application/response reconciliation is skipped
- candidate writes are not applied
- `last_successful_scan_date` does not advance

## 7. Single-pass inbox reconciliation layer

Candidate alert collection uses confirmed Sources.

Application and response reconciliation can use one broad Gmail read for the target period.

The workflow classifies messages into categories such as:
- job alert
- application confirmation
- recruiter submission evidence
- employer or recruiter response
- marketing/newsletter
- unknown

It then compares relevant messages against Tracker rows.

A separate Gmail query for every Applied company is avoided by default. A targeted follow-up search is used only when needed to resolve ambiguity.

Clear recruiter statements that a profile, resume, or application was submitted for a specific role can count as application evidence. Ambiguous future-intent language requires human review.

## 8. Tracker automation layer

When Tracker completeness is verified and Google Drive write actions are available, the task can:
- append suitable new jobs as `Candidate`
- re-use and re-evaluate unapplied historical rows instead of appending duplicate rows
- preserve first-discovery ReceivedAt, DiscoveryType, and Source when a row re-surfaces
- append re-surfacing provenance to Notes
- keep an existing working Link, replacing it only when unusable and recording `Link replaced YYYY-MM-DD`
- reconcile clear application evidence to `Applied`
- fill `AppliedAt`
- fill `RespondedAt` after clear employer or recruiter responses
- close explicitly rejected applications with `Result = Rejected`
- record other explicit final outcomes in Result

ATS and rejection-stage inference are intentionally excluded from the Tracker schema. ATS names may still appear as `Source` values when a web-discovered job was found on that platform.

Ambiguous evidence is not written automatically.

If a scheduled external write cannot proceed because approval is required or a write action is unavailable, the workflow returns exact 14-column TSV as a fallback.

## 9. User application layer

The user reviews recommended links and submits applications on external sites.

Application submission is intentionally outside the core workflow because employers and application systems use different forms, authentication, consent, and submission requirements.

If an application generates no confirmation and no clear recruiter-submission evidence, the user may need to mark the row Applied manually.

## 10. Monitoring and delivery layer

The Scheduled Task result provides:
- scan period
- readable shortlist with reasons and application links
- detected applications and responses
- no-response candidates
- Tracker write results
- human-review items
- source-health checks
- diagnostics
- TSV only when automatic Tracker writing could not be applied

Enabled alert sources with zero messages are always surfaced. If all major configured sources unexpectedly return zero messages, the workflow warns that alert delivery, sender patterns, or account configuration may need review.

## Data flow

```text
USER
Connect Gmail + Google Drive
        |
        v
USER
Paste bootstrap prompt into ChatGPT
        |
        v
USER + GPT
Compact conversational onboarding
        |
        v
GPT
Create private profile + NEW Tracker + Scheduled Task
        |
        v
================ SCHEDULED RUN ================
        |
        v
Control.last_successful_scan_date -> calculate catch-up period
        |
        v
Private profile + Config + Sources + Tracker
        |
        v
Job-alert Gmail + Web Discovery -> extraction -> identity normalization -> hard filters -> fit matching
        |
        +------------------------------+
        |                              |
        v                              v
Candidate shortlist            Broad inbox reconciliation
                                       |
                                       v
                           applications + responses
        |                              |
        +---------------+--------------+
                        |
                        v
              Tracker updates when permitted
                        |
                        v
              Result + source health + diagnostics
                        |
                        v
                 USER applies externally
```