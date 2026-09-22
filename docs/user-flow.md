# User flow

This document explains what the user does in ChatGPT and what ChatGPT automates.

## Responsibility legend

- **USER**: action the user performs manually
- **GPT**: action ChatGPT performs during setup or scheduled runs
- **USER + GPT**: ChatGPT asks, proposes, or requests approval and the user responds

## One-time setup

### Step 1 - USER - Connect Gmail and Google Drive

In ChatGPT, open `Settings > Apps` or `Settings > Plugins`, depending on the account interface.

Connect the Google account that receives job-alert emails and owns the Drive resources for this workflow.

### Step 2 - USER - Start the bootstrap prompt

1. Open `prompts/01-bootstrap.md`.
2. Copy the complete prompt.
3. Start a new normal ChatGPT conversation.
4. Paste and send the prompt.

No local application, script, terminal command, or server is required.

### Step 3 - USER + GPT - Complete conversational onboarding

The onboarding is a conversation, not a form.

The user can answer naturally and may mention several pieces of information in one message. ChatGPT extracts useful facts from each answer and skips questions that are already resolved.

The user does not need to provide a complete career biography during setup. The private profile can be improved later, so onboarding should collect enough information for useful matching without making the user feel that every detail must be finalized immediately.

If the user is unsure, cannot remember a detail, or wants to add something later, ChatGPT continues once enough evidence exists for useful matching unless the missing information is genuinely required for eligibility or core operation.

Public examples are fictional and should not reuse facts from the user's private profile, prior conversations, or Memory.

A fictional answer can look like this:

> I am mainly looking for Senior Data Analyst roles, but Analytics Engineer or BI Lead roles are also interesting when the work fits. I have about six years of experience, with the last three focused on logistics and operations analytics.

Normal questions are not labeled `Required` or `필수`. Only optional questions are marked.

#### Keep each question compact

ChatGPT does not show a setup roadmap, stage number, or `Setup progress` label.

A typical career question looks like this:

> **Tell me about your current or most recent role and what you actually owned. You can include your title, domain, and scope.**
>
> Example: I was a Senior Data Analyst on a logistics team and owned delivery-performance analytics from metric definition through dashboard rollout.
>
> Questions remaining: about 7

In Korean, the bottom line is:

`남은 질문: 약 N개`

The remaining-question count is recalculated from unresolved topics after each answer. It is intentionally approximate. Permission dialogs, connection clicks, approvals, resource creation, and tests do not count as questions.

The question itself is the visual emphasis. The remaining-question line is not emphasized.

Every career, experience, strength, preference, or constraint question includes a concise fictional answer example directly below it. Simple operational yes/no questions may omit an example when the choice is obvious.

Before the first question, ChatGPT may use one short reassurance sentence explaining that the user can answer naturally, does not need to provide everything now, and can update the profile later.

#### Understand the person before narrowing the search

ChatGPT gathers enough evidence about:

- the kind of work the user wants
- current or recent role
- relevant experience
- actual ownership and scope
- products, industries, and problem areas
- strongest skills and responsibilities
- recurring problem types
- measurable or observable impact
- decision-making under ambiguity
- cross-functional influence
- leadership or mentoring
- specialty or differentiating expertise

For experienced users, a title alone is not considered sufficient evidence. ChatGPT asks role-specific depth questions when needed to understand what actually distinguishes the person.

Depth questions are not a requirement to document every achievement immediately. If enough evidence already exists for useful matching, setup can proceed and missing details can be added later.

#### Infer search scope instead of forcing a whitelist

ChatGPT treats:

- main role direction as **Core target**
- nearby titles or broader levels as **Consider if fit**
- explicitly unwanted roles or constraints as **Hard exclude**

A user does not need to enumerate every acceptable title or level in advance. If actual responsibilities and scope fit the user's evidence, nearby roles can still be considered.

ChatGPT shows a concise interpretation summary and asks one confirmation question. The user can correct several points in one normal-language response.

#### Ask only material constraints

After career evidence is understood, ChatGPT asks only unresolved conditions that could materially change recommendations, such as location, work model, employment type, work authorization, explicit exclusions, or compensation limits.

Each preference question includes a concise fictional answer example.

Resume-version tracking is not part of the core workflow.

### Step 4 - GPT - Create private profile and a brand-new Tracker

ChatGPT creates:

1. a private career profile
2. a new Google Sheet Tracker using Job Search Collector's own schema

Preferred profile:
`Job_Search_Collector_Profile.md`

Fallback:
a private Google Doc containing the same Markdown text.

Preferred Sheet name:
`Job_Search_Collector`

If that name already exists, ChatGPT automatically creates a uniquely named new Sheet such as `Job_Search_Collector_2`. It does not ask to reuse the existing file.

Tabs are created in this order:
- Tracker
- Config
- Sources
- Control

`Tracker` is the only user-facing tab. After setup, ChatGPT hides `Config`, `Sources`, and `Control` when the available Google Sheets actions support tab hiding, while keeping them available to the workflow internally. `Tracker` stays visible and first, and should be left active when possible.

If hiding is unavailable, `Tracker` still stays first and the user is told once that the other tabs are internal and do not need normal interaction.

The Tracker has exactly 14 columns:

`Status, Company, Title, Location, Salary, WorkMode, Notes, Link, ReceivedAt, AppliedAt, RespondedAt, Result, DiscoveryType, Source`

There are no ATS, ResumeVersion, Channel, or RejectionStage columns.

`DiscoveryType` is `Mail` or `Search`, so users can filter how an opportunity was first discovered. `Source` stores the concrete platform such as LinkedIn, Indeed, Greenhouse, Workday, or Company Careers. If the same posting is later found through another route, the original DiscoveryType and Source stay unchanged and the later path is added to Notes.

#### Existing trackers are deliberately outside bootstrap

Bootstrap does not ask whether the user already has a spreadsheet or tracker. It does not search for, import, adapt, merge, or reuse an existing tracker.

If the user wants historical application rows migrated, that should be handled separately in another ChatGPT conversation after setup is complete.

Later Gmail-based missing-application detection is different. A scheduled run can still create an Applied row when clear confirmation or recruiter-submission evidence proves that an application occurred.

### Step 5 - USER + GPT - Configure automation and schedule

Recommended automation includes:

- add suitable jobs to Tracker
- detect clear application confirmations
- detect explicit recruiter submission evidence
- reconcile clear application status changes
- detect employer or recruiter responses
- flag no-response applications after 14 days
- optionally discover additional jobs from the public web that may not appear in email alerts

ATS and rejection-stage inference are not part of the core workflow.

Bootstrap asks one additional plain-language question about whether Web Job Discovery should be enabled. The user does not choose ATS sites, queries, query counts, weekdays, or other technical search settings.

The user chooses a daily run time and timezone in plain language. A city name is acceptable when ChatGPT can normalize it.

ChatGPT then creates the recurring Scheduled Task.

### Step 6 - GPT - Validate setup

The setup test checks profile access, Gmail access, source parsing, digest expansion, Tracker completeness, 14-column output, application-link extraction, Web Discovery availability when enabled, write capability, fit-based matching, and missed-run recovery logic.

At completion, ChatGPT tells the user that the profile does not need to be perfect today and that future career or search changes can simply be mentioned naturally in the same conversation.

## Ongoing updates after setup

The setup conversation remains useful after bootstrap.

The user does not need to know which internal field should change and does not need to say `update my profile`.

### Step A - USER - Mention a change naturally

Examples:

- a new project or responsibility
- a newly quantified outcome
- a stronger specialty the user wants to emphasize
- a change in target roles
- a new role or domain the user wants to exclude
- a location or work-model change
- a work-authorization or sponsorship change
- a change in people-management preference

The user can simply mention the new fact in normal conversation.

### Step B - GPT - Decide whether it matters for future matching

ChatGPT does not propose an update for every casual statement.

If the new information is stable and likely to improve or materially change future job matching, ChatGPT proactively proposes a profile update.

Example:

> This could affect future job matching. Would you like me to update your Job Search Collector profile with it?

Korean:

> 이 내용을 Job Search Collector 프로필에 업데이트할까요?

### Step C - USER - Confirm

The profile is not changed until the user confirms.

If the user explicitly asked for a profile change in the first place, that explicit request already counts as confirmation and ChatGPT should not ask redundantly.

### Step D - GPT - Update the existing private profile directly

After confirmation, ChatGPT:

1. reads the current private profile;
2. updates all affected structured fields and Markdown sections;
3. preserves unrelated information;
4. writes the complete profile back to the same private document;
5. confirms the change concisely.

Normal profile updates do not require the Scheduled Task to be recreated because the daily workflow reloads the private profile referenced by `Config.profile_reference` on every run.

### Operational settings use the same approval pattern

If the user's statement instead implies a change to run time, automation modules, Web Discovery enablement, no-response threshold, or Gmail sources, ChatGPT explains what operational setting would change and asks for confirmation.

After confirmation, ChatGPT updates the existing Config, Sources, or Scheduled Task directly when supported. The user should not be asked to copy and paste a newly generated scheduled prompt when the existing task can be updated directly.

## Daily scheduled workflow

### Step 7 - GPT - Calculate the unprocessed date range

The task uses `Control.last_successful_scan_date`.

- First run: process the previous local calendar day.
- Later runs: process every calendar day after the last successful date through yesterday.
- If a scheduled run was skipped or failed, the next successful run catches up automatically.

The task shows the scan period at the top of the result.

The success marker is updated only after the full target period was processed successfully enough to produce normal output or a complete TSV write fallback.

### Step 8 - GPT - Collect from Gmail and, when due, the public web

Candidate collection always searches the confirmed Gmail Sources for the target period.

When Web Discovery is enabled and `Control.last_successful_web_discovery_date` is blank or earlier than the current local calendar date, the same Scheduled Task also runs Web Discovery. This happens automatically at the scheduled time. The user does not manually trigger a second task.

Web Discovery first searches the configured Phase 1 ATS domain families using profile-generated queries. It verifies real posting pages and their open state. If the first pass yields fewer than five verified new Strong/Possible roles, remaining query budget is used for broader web search. Mail and web candidates then enter the same matching and deduplication pipeline.

A Web Discovery failure does not cause the Gmail workflow to fail, and its success marker is tracked separately.

### Step 9 - GPT - Read and classify Gmail messages

Candidate collection searches the confirmed Sources for the target period.

For reconciliation, ChatGPT can also read target-period inbox messages in one broad pass.

Messages are classified using sender + subject + body, not sender address alone.

Useful categories include:

- job alert
- application confirmation
- recruiter submission evidence
- employer or recruiter response
- marketing/newsletter
- unknown

One sender may produce several message types.

### Step 10 - GPT - Extract, normalize, and deduplicate jobs

ChatGPT expands digest messages, extracts individual jobs, preserves valid links, normalizes stable LinkedIn links when a job ID is explicit, and never invents missing URLs.

Within-run duplicates use comparison-normalized Company + Title, with location as a tie-breaker when needed.

Within-run deduplication is separate from historical disposition. Finding the same identity in Tracker does not automatically mean suppress.

If the same job appears through multiple routes in the current run, keep one record. Preserve the DiscoveryType and Source that first caused the row to enter Tracker, and record later discovery paths in Notes.

If company identity is ambiguous, ChatGPT does not guess the parent company. Suspected duplicates go to Human review rather than being merged automatically.

### Step 11 - GPT - Evaluate actual fit

Hard exclusions are applied first.

Remaining jobs are judged using actual responsibilities, required scope, ownership, ambiguity, leadership, problem type, differentiators, domain, skills, outcomes, and practical constraints.

A Strong match for an experienced user should normally have a meaningful reason beyond title similarity.

### Step 12 - GPT - Compare with Tracker

Before absence or historical-history judgments, ChatGPT verifies that the number of Tracker rows read matches `Control.tracker_data_rows`.

If the read is incomplete, it does not claim that a row is absent and skips history-dependent reconciliation.

For the same comparison-normalized Company + Title, historical disposition follows this order:

1. AppliedAt non-empty -> suppress.
2. Else Status=Applied -> suppress.
3. Else Status=Closed -> suppress.
4. Else Status=Excluded:
   - `Excluded: ` -> suppress.
   - `Fit: Weak. ` -> re-evaluate.
   - `Closed: ` -> re-evaluate.
   - other non-empty Notes -> suppress as a manual/legacy exclusion.
   - blank Notes -> suppress and report the count in Diagnostics.
5. Otherwise, including Candidate -> re-evaluate.

The workflow does not try to determine whether a posting is a repost or a new requisition. Re-evaluable rows are judged again using the current posting and profile.

### Step 13 - GPT - Reconcile applications and responses in one inbox pass

When enabled, ChatGPT reads target-period inbox messages once and compares likely application confirmations, recruiter submissions, and employer/recruiter responses against relevant Tracker rows.

It does not run a separate Gmail search for every Applied company by default.

A targeted follow-up search is used only when a specific ambiguity needs resolution.

Clear application evidence can include an explicit recruiter statement that a profile, resume, or application was submitted for a specific company and role.
Ambiguous future-intent language goes to Human review.

### Step 14 - GPT - Update Tracker

When writes are permitted:

- suitable new jobs are added as Candidate
- re-evaluable historical rows reuse the existing row instead of creating a duplicate
- a re-surfaced Strong/Possible row returns to Candidate and is shown again
- ReceivedAt, DiscoveryType, and Source remain fixed to first discovery
- Notes records `Re-surfaced YYYY-MM-DD via {DiscoveryType} ({Source})` using the current re-discovery path
- a working existing Link is kept; it is replaced only when unusable, and replacement adds `Link replaced YYYY-MM-DD` to Notes
- clear application evidence can set Status=Applied and AppliedAt
- clear replies can fill RespondedAt
- explicit rejection can set Status=Closed and Result=Rejected
- other explicit final outcomes can be stored in Result

No ATS or rejection-stage field is stored.

If an automatic write is blocked, ChatGPT returns exact 14-column TSV as a fallback.

### Step 15 - USER - Apply to jobs

The user opens recommended links and completes applications on external sites.

Job Search Collector does not claim to submit applications on the user's behalf.

### Step 16 - GPT - Monitor no-response cases and source health

When enabled, ChatGPT identifies Applied rows with no response after the configured number of days.

It also reports enabled job-alert sources with zero messages and warns when all major sources unexpectedly return zero messages.

No-response rows are not automatically closed by default.

## Simplified flow

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
Compact natural-language onboarding
        |
        v
GPT
Build fit-based profile with real differentiators
        |
        v
GPT
Create private profile + NEW 14-column Tracker
        |
        v
GPT
Create and test Scheduled Task
        |
        v
USER
Later mentions career/search changes naturally
        |
        v
GPT
Offers profile update when it matters
        |
        v
USER
Confirms
        |
        v
GPT
Updates the same private profile directly
        |
        v
================ DAILY ================
        |
        v
GPT
Calculate catch-up scan period
        |
        v
GPT
Read alerts + run Web Discovery when due
        |
        v
GPT
Verify web postings + classify messages
        |
        v
GPT
Merge candidates + deduplicate + evaluate actual fit
        |
        v
GPT
Single-pass application/response reconciliation
        |
        v
GPT
Write Tracker updates when permitted
        |
        v
GPT
Return shortlist + source health + diagnostics
        |
        v
USER
Open links and apply
```