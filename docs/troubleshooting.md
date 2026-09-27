# Troubleshooting

## The private profile cannot be read

Symptoms:
- `PROFILE_UNAVAILABLE`
- the scheduled run can see the Sheet but cannot open `Config.profile_reference`

Checks:
- confirm Google Drive is connected to the same account that owns or can access the profile;
- confirm the stored profile reference still points to the intended file/document;
- confirm the profile is not only a Project upload or task attachment;
- if a raw `.md` file is not readable in the current environment, use the Google Doc Markdown fallback and update `Config.profile_storage_format` and `Config.profile_reference`.

Do not fall back to ChatGPT Memory or infer the profile from previous task results.

## The profile is marked invalid

Symptoms:
- `PROFILE_INVALID`
- YAML fields cannot be parsed reliably

Checks:
- keep the `---` YAML delimiters;
- preserve the required field names from `profiles/profile.template.md`;
- ensure list fields remain valid YAML lists;
- keep `profile_version: 2` unless the repository schema is intentionally upgraded.

Use `prompts/04-update-profile.md` to repair the file while preserving existing factual content.

## Tracker count mismatch

If the rows read from Tracker do not equal `Control.tracker_data_rows`, the task must mark history as incomplete.

It may still parse current Gmail job-alert messages for diagnostics, but it must not claim that a job or application is absent from Tracker, confirm historical duplicates, reconcile application state, write new Candidate rows, or advance `last_successful_scan_date`.

## A scheduled run was skipped

The workflow uses `Control.last_successful_scan_date` instead of assuming that yesterday was always processed.

On the next run, it should process every local calendar day after the last successful date through yesterday.

If the date did not advance after a failed run, that is expected. The next successful run should catch up automatically.

Do not use the newest Tracker `ReceivedAt` value as a substitute for the successful-scan marker. A day can be processed successfully even when no candidate was added.

## No job alerts found

Check Source health and Diagnostics.

Possible causes:
- the sender pattern is wrong;
- the source stopped sending alerts;
- Gmail is connected to a different account;
- the calculated scan period or timezone is wrong;
- messages are being delivered under a new sender address.

Every enabled source with zero messages should be listed.
If all major sources unexpectedly return zero messages, review alert delivery, sender patterns, and account configuration.

## Too few jobs surfaced

Do not assume a small result means the alert sources are broken.

Read the run's Collection audit in this order:

1. Check raw Mail discoveries and the per-source Mail counts.
2. Check whether Web Discovery ran and how many raw Web discoveries it contributed.
3. Compare raw discoveries with unique jobs after within-run merging.
4. Review the final-disposition breakdown.
5. Review historical suppression by reason.
6. Check Tracker total rows and Applied rows to see whether long-running history may be contributing to suppression.

Interpretation examples:

- Low raw Mail and low raw Web: source coverage or market-volume issue.
- One Mail source suddenly at zero: sender pattern, alert delivery, or source-specific issue.
- High raw discoveries but low unique jobs: repeated discovery across messages/platforms.
- High unique jobs but low surfaced count: inspect historical suppression, hard exclusions, weak fit, and Human review.
- Historical suppression growing with Tracker size: the history policy may be reducing surfaced results over time.

Do not change matching thresholds merely to raise the count. First identify the stage responsible for the loss.

A historical suppression should be treated as trustworthy only when the run can identify the matching Tracker record that caused it.

## A sender produced the wrong kind of message

A sender address does not define one permanent message type.

For example, one sender may send both job recommendations and application confirmations.

The workflow should classify messages from sender + subject + body before deciding how to use them.

If classification is wrong, update `Sources.Notes` with stable content clues rather than creating a separate sender solely to represent the message type.

## Links are missing

A blank link is preferable to a fabricated link.

Check whether:
- the digest contains a direct job URL;
- the source changed its email markup;
- the URL is only a tracking redirect that cannot be safely associated with a posting;
- the job expired or was removed.

Update the corresponding Sources.LinkRule only when a stable parsing rule is known.

## A recruiter said they submitted me, but the Tracker was not updated

Clear recruiter language can count as application evidence when it explicitly states that the user's application, profile, or resume was submitted or forwarded for a specific company and role.

Ambiguous statements such as `I may submit you` or `I can send your profile` should not trigger an automatic status change.

If the evidence is ambiguous, the workflow should put it in Human review.

## Company names look different for what may be the same job

Do not guess a parent company from an unfamiliar subsidiary, brand, or legal entity name.

Preserve the source wording.
If the records look related but identity cannot be verified confidently, mark a suspected duplicate for Human review instead of merging automatically.

## Scheduled task cannot use a connected app

Connected-app availability and supported actions depend on plan, workspace settings, permissions, and app capabilities.

Verify the user connected their own Gmail and Google Drive. A shared task does not inherit the original creator's credentials or files.

Durable matching information must live in the private Drive profile referenced by Config.profile_reference.

## Tracker did not update automatically

Symptoms:
- the Scheduled Task found suitable jobs but returned `Manual Tracker fallback`;
- Diagnostics says `approval required` or `write unavailable`.

Checks:
- confirm Google Drive is connected to the account that owns the Tracker;
- confirm the connected Google account has edit access to the Sheet;
- confirm the relevant Google Drive write actions are available;
- review whether the workspace requires approval for external data changes.

The workflow must not claim a write succeeded when it did not. When an unattended write is blocked, use the exact 14-column TSV fallback.

## I applied but the row still says Candidate

Job Search Collector normally learns that an application was submitted from clear Gmail evidence such as an application-confirmation email or an explicit recruiter-submission message.

If neither exists, there may be no reliable evidence that the application happened. In that case, manually change the Tracker row to `Applied` and enter `AppliedAt` if desired.

Do not infer an application merely because the user opened an application link.

## Where are ATS, ResumeVersion, Channel, and RejectionStage?

They are intentionally not part of the current Tracker schema.

The core workflow keeps only fields that materially help users find, review, apply to, and track opportunities.

`DiscoveryType` separates `Mail` from `Search`. `Source` stores the concrete platform such as LinkedIn, Indeed, Greenhouse, Workday, or Company Careers. ATS is not a separate column because an ATS name can already be the Source for a search-discovered job.

If recruiter or agency context matters for a specific application, put that detail in Notes.

## Web Discovery did not run

Web Discovery runs inside the same Scheduled Task only when it is enabled and `Control.last_successful_web_discovery_date` is blank or earlier than the current local calendar date in `Config.schedule_timezone`.

Check:
- `Config.module_web_discovery` is true;
- `Config.web_discovery_max_queries` is 20;
- the private profile and Tracker were readable and valid;
- web search was available to the scheduled run;
- the web-discovery marker was not already set to today.

Do not create a separate Scheduled Task just to compensate for a skipped Web Discovery run.

## A web search result looks relevant but was not added

A search snippet is not enough. The workflow must open the actual posting page and verify that it represents a currently open job before a normal Candidate or Weak row is written.

If the posting page cannot be opened or associated confidently with the search result, the item may appear in Human review or Diagnostics instead of Tracker.

A missing posted date alone does not block a verified open role. Notes should say `Posted date unavailable` rather than inventing a date.

## Eligibility requirement is unclear

Do not infer citizenship, security clearance, licensing, or another eligibility fact that is not present in the private profile.

Only auto-exclude when a known profile fact clearly conflicts with the requirement. Otherwise keep the role eligible for fit evaluation and add a concise confirmation note.

## Web Discovery partially failed

Partial web-search failures are reported separately from Gmail processing. Web Discovery failure must not prevent `Control.last_successful_scan_date` from advancing when the Gmail workflow itself succeeded.

`Control.last_successful_web_discovery_date` advances only when enough of the planned web search completed to produce a normal discovery result. The exact numeric threshold between partial and majority query failure is intentionally not fixed yet.
