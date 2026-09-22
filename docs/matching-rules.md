# Matching rules

## Core principle

Judge the actual job, not the title label alone.

A user's stated target title or career level is an anchor for matching, not automatically a whitelist. If the posting's responsibilities, required experience, product context, and scope are supported by the user's career evidence, the role can still be a valid match even when the title uses a different label.

Only explicit hard exclusions should close that door.

Fictional examples:

- A user mainly targeting `Senior Data Analyst` can still receive an `Analytics Engineer` or `BI Lead` role when the actual scope is supported by their experience.
- A role should not be excluded merely because `Analytics Engineer` or `BI Lead` was not explicitly listed during onboarding.
- A `Data Analytics Manager` role can be excluded when the user explicitly does not want people-management roles.
- A role whose title sounds close but whose required technical or ownership scope is materially unsupported should be downgraded or excluded for that evidence-based reason, not for the title label by itself.

Public examples in this document are generic and fictional. Do not derive examples from a user's private profile, Memory, or prior conversations.

## Use differentiators, not title-only similarity

For experienced candidates, matching should use the user's distinctive evidence whenever available.

Examples of high-signal evidence:

- recurring problem types the user is especially good at solving;
- end-to-end ownership;
- decision-making scope;
- measurable or observable outcomes;
- cross-functional influence;
- leadership or mentoring;
- systems or process improvements;
- domain or product depth;
- specialty areas the user wants to be hired for next.

A job should not be called a Strong match merely because its title resembles the user's title.

For example, two `Senior Data Analyst` roles can differ materially:

- one may emphasize operational metrics, SQL, data modeling, and stakeholder decision support;
- another may emphasize marketing attribution, experimentation statistics, and ad-platform data.

Use the user's `Differentiators and scope`, experience highlights, outcomes, skills, and specialty evidence to decide which one is actually stronger.

## Decision order

1. Read and validate the private career profile.
2. Parse the posting.
3. Derive comparison-normalized Company and Title values.
4. Apply explicit hard exclusions.
5. Deduplicate within the current run using the comparison values.
6. Compare with Tracker history using the same comparison values when completeness is verified.
7. Evaluate actual fit using career evidence, differentiators, and job scope.
8. Extract and validate the best usable application link.
9. Apply storage/display normalization before writing a new row.
10. Produce shortlist and Tracker rows.

## Company and Title normalization

Comparison normalization and Tracker display normalization are separate concerns.

### Comparison-only values

Derive temporary comparison values for Company and Title. These values are used only for identity checks and are not stored as additional Tracker columns.

Apply to both Company and Title:

- normalize Unicode compatibility forms consistently;
- trim leading and trailing whitespace;
- convert non-breaking and other spacing variants to normal spaces;
- collapse repeated whitespace to one space;
- convert common dash variants, including en dash, em dash, Unicode hyphen, non-breaking hyphen, and minus sign, to ASCII hyphen;
- use exactly one space around hyphen separators;
- compare case-insensitively using Unicode-aware case folding;
- normalize curly double quotes to straight double quotes and curly single quotes/apostrophes to straight single quotes;
- remove spaces around slash so variants such as `UX / UI` and `UX/UI` compare consistently.

For Title only:

- when a middle dot or bullet is clearly used as a spaced separator, treat it like a hyphen separator for comparison;
- preserve parentheses and their contents;
- preserve commas, colons, slashes, and other punctuation that can distinguish real roles;
- do not normalize unspaced middle dots that may be part of a real name or title.

For Company only:

- ignore these terminal legal designators for comparison, case-insensitively and punctuation-tolerantly: `Inc`, `Inc.`, `Incorporated`, `Ltd`, `Ltd.`, `Limited`, `LLC`, `Corp`, `Corp.`, `Corporation`;
- remove only terminal legal designators, plus a preceding comma and whitespace when present;
- do not remove the same words when they occur inside the company name;
- do not infer parent, subsidiary, or brand relationships.

Example:

`Lead Product Designer, Design Systems – AI Enablement`

and

`Lead Product Designer, Design Systems - AI Enablement`

must produce the same comparison-normalized Title.

### Tracker storage/display values

Do not store the lowercased or legal-suffix-stripped comparison value in Tracker.

For newly written Title values:

- trim and collapse whitespace;
- normalize common dash variants to ASCII hyphen with one space around the separator;
- remove spaces around slash;
- otherwise preserve source capitalization and meaningful punctuation.

For newly written Company values:

- trim and collapse whitespace;
- normalize common dash variants when used as separators;
- preserve capitalization, legal suffixes, and source wording by default;
- if Tracker already contains a Company display value with the same comparison-normalized Company, reuse that existing display value for a new row.

Existing Tracker rows are not rewritten retroactively as part of this rule. They are still comparison-normalized in memory whenever they participate in duplicate or message-association checks.

### Where the comparison rule applies

Use the same Company + Title comparison normalization for:

- Web Discovery `new` counting;
- Mail-to-Mail, Search-to-Search, and Mail-to-Search deduplication within a run;
- historical Tracker duplicate checks;
- missing-application detection;
- application-confirmation association;
- recruiter-submission association;
- employer/recruiter response association.

Do not use raw string equality for these identity checks.

## Historical duplicate and re-surfacing rules

A comparison-normalized Company + Title identity match does not automatically mean suppress.

When matching Tracker history is found, apply this order:

1. AppliedAt non-empty -> suppress.
2. Else Status = Applied -> suppress.
3. Else Status = Closed -> suppress.
4. Else Status = Excluded:
   - Notes begins `Excluded: ` -> suppress as a hard exclusion.
   - Notes begins `Fit: Weak. ` -> re-evaluate.
   - Notes begins `Closed: ` -> re-evaluate.
   - any other non-empty Notes -> suppress as a manual/legacy exclusion.
   - blank Notes -> suppress and report only the count in Diagnostics.
5. Otherwise, including Status = Candidate -> re-evaluate.

Do not attempt to determine whether a matching posting is a repost, a new requisition, or repeated collection. Do not use job ID, URL differences, or posting date to decide that.

For a re-evaluated row, use the current profile and posting:

- Strong or Possible -> Status = Candidate and surface it again.
- Weak -> Status = Excluded with Notes beginning `Fit: Weak. `.
- hard exclusion -> Status = Excluded with Notes beginning `Excluded: `.
- posting closed, expired, removed, or unavailable -> Status = Excluded with Notes beginning `Closed: `.

Re-use the existing Tracker row rather than appending a duplicate.

Preserve these first-discovery values:

- ReceivedAt
- DiscoveryType
- Source

Record the new path only in Notes using:

`Re-surfaced YYYY-MM-DD via {DiscoveryType} ({Source})`

Link policy for a historical row:

- keep the existing Link while it works;
- replace it only when the existing Link is unusable and the newly found Link is usable for the same posting;
- do not replace a working link merely because the new route is an official ATS or Careers page;
- if replaced, append `Link replaced YYYY-MM-DD` to Notes.

The three recognized Excluded-note prefixes have distinct meanings:

- `Excluded: {reason}` = hard filter and future suppress.
- `Fit: Weak. {reason}` = fit judgment and future re-evaluation.
- `Closed: {reason}` = unavailable/expired/removed/closed posting and future re-evaluation.

## Hard exclusions

Use only explicit profile rules or unambiguous posting facts.

Examples:

- title family explicitly listed in `excluded_titles`
- internship when internships are explicitly disallowed
- location outside an allowed region when location is a hard rule
- required sponsorship mismatch when configured as hard
- explicitly excluded domain
- a user-defined blocking keyword
- a required skill listed as a hard blocker when the posting clearly requires it
- people-management responsibility when `management_roles = unacceptable`

Missing information is not automatically a hard exclusion.

For eligibility requirements such as citizenship, security clearance, licensing, or similar conditions, automatically exclude only when the private profile contains a clear fact that conflicts with the requirement. If the profile does not establish whether the user qualifies, do not guess. Keep the role eligible for fit evaluation and add a concise confirmation note such as `Eligibility requirement needs confirmation: Canadian citizenship required.`

`target_seniority` is not a hard exclusion list. Treat it as a reference point unless the profile explicitly says a level must be excluded.

## Fit dimensions

### Role scope and responsibilities

Compare what the person would actually do with the user's demonstrated responsibilities and experience.

This dimension matters more than exact title wording.

### Career level and scope

Compare required years, ownership, decision-making scope, leadership expectations, strategic responsibility, and people-management requirements with the user's evidence.

Do not assume that title labels such as Senior, Staff, Lead, Principal, Manager, or Director mean the same thing at every company.

### Differentiators

Compare the posting with the user's high-signal strengths and recurring work patterns.

Questions include:

- Does this role need the kind of problems the user is especially good at solving?
- Does the required ownership resemble the user's demonstrated scope?
- Does the role reward the user's distinctive domain or product experience?
- Is the user's strongest evidence directly relevant to the work?
- Does the role offer the kind of work the user said they want to be hired for next?

### Impact and evidence

Use measurable results when available, but do not require a metric for every strength.

Concrete non-numeric evidence can include:

- leading a major launch;
- reducing delivery risk;
- establishing a reusable system;
- improving team process;
- influencing a key decision;
- mentoring or cross-functional leadership.

### Domain

Is the product or industry close to the user's experience or stated target direction?

### Skills

Does the posting emphasize strengths supported by the private career profile, including concrete responsibilities, outcomes, leadership evidence, or specialty areas?

### Location and work model

Does the stated location and remote, hybrid, or on-site model match the user's constraints and preferences?

### Employment and compensation

Is the employment type acceptable, and does known compensation meet any explicit rule?

## Interpreting target titles

Use three conceptual buckets internally. The user does not need to fill these out as a form.

### Core target

The main role family or direction the user is actively seeking.

Usually represented by `primary_titles`.

### Consider if fit

Nearby titles, different title labels, or broader career levels that should still be evaluated when the actual job scope fits the user's evidence.

This can be represented by `adjacent_titles` plus natural-language notes in the profile.

Do not require every plausible title to be enumerated in advance.

### Hard exclude

Roles the user explicitly does not want regardless of otherwise positive fit.

Usually represented by `excluded_titles`, management rules, excluded domains, hard blockers, or explicit interpretation notes.

## Stretch roles

A role that appears somewhat above or outside the user's usual title should not be rejected automatically.

If the user's evidence supports much of the required scope:

- keep it as Strong or Possible depending on the evidence;
- mention the scope difference briefly when useful;
- let the user decide whether to apply.

If the posting requires materially unsupported scope, such as large-team management, executive ownership, or specialized expertise the user clearly lacks, lower the match or exclude it using that concrete reason.

## Match classes

### Strong match

Clear fit across the important dimensions with no major unresolved conflict.

Exact title equality is not required.

For experienced users, a Strong match should normally be explainable using at least one piece of high-signal evidence beyond title similarity, such as relevant scope, differentiator, outcome, specialty, or domain depth.

### Possible match

Plausible fit, but one or more material details are missing, ambiguous, somewhat outside preference, or represent a reasonable stretch.

### Weak match

Not a hard exclusion, but meaningfully outside the user's target or unsupported by the user's evidence.

Omit it from the main shortlist, but for a verified posting write it to Tracker with `Status = Excluded` so future discovery paths can recognize that the role was already reviewed. Notes must begin `Fit: Weak. ` followed by the evidence-based reason.

A hard exclusion also uses `Status = Excluded`, but Notes must begin `Excluded: ` followed by the reason. This keeps Weak and hard exclusion distinct without adding a new Tracker column.

## Explanation standard

Every Strong or Possible match should have a short evidence-based reason.

Fictional examples:

- `Strong match: the role emphasizes SQL, operational metrics, and cross-functional KPI ownership, which directly matches the user's demonstrated logistics analytics work.`
- `Possible match: the BI Lead title is broader than the user's usual title, but the role remains hands-on and the required stakeholder ownership is supported.`

Avoid generic reasons such as:

- `great fit`
- `same title`
- `senior-level role`

without pointing to actual scope, differentiators, domain, skills, outcomes, or constraints.

## Invalid or unreadable profile

If the private profile cannot be read, its YAML is materially malformed, or the content is too incomplete to determine the user's target:

- do not use ChatGPT Memory or old chats as a substitute;
- do not assign Strong/Possible/Weak fit;
- report `PROFILE_UNAVAILABLE` or `PROFILE_INVALID` in Diagnostics;
- continue only with source-health and non-profile-dependent parsing checks when useful.

## Discovery-method independence

Mail and Web Discovery use the same hard-filter and fit rules. Do not lower a match simply because it was found through web search.

`DiscoveryType` records how the row first entered Tracker, using `Mail` or `Search`. `Source` records the concrete platform. These fields describe provenance, not fit quality.
