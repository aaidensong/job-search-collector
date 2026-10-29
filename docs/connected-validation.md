# Connected Scheduled Task validation

This checklist validates connected product behavior without publishing private job-search data.

Interactive ChatGPT connector capabilities do not prove that an unattended Scheduled Task exposes the same actions or approval boundaries.

## Use fictional data only

Create a temporary validation setup with:

- a fictional career profile;
- a temporary Job Search Collector Sheet using the standard 14-column Tracker schema;
- fictional company names and job-alert content;
- no real email addresses, private Sheet links, tokens, recruiter identities, application history, or personal career details in screenshots or issue comments.

Do not run a publishable validation against a real Tracker.

## What to verify

Run the current bootstrap/test flow and then execute the created Scheduled Task once.

Record whether the Scheduled Task can:

1. read the private profile referenced by `Config.profile_reference`;
2. read the full Tracker and verify it against `Control.tracker_data_rows`;
3. read the configured fictional job-alert source;
4. produce the expected 14-column candidate/update shape;
5. write the intended Tracker change without interactive approval;
6. if direct writing is unavailable or blocked, return the exact 14-column TSV fallback instead of claiming the write succeeded.

Also record the test date and the actions actually available in the Scheduled Task run.

## Pass conditions

The validation passes when:

- profile access succeeds;
- Tracker completeness is verified;
- the fictional input can be parsed;
- the output schema remains exactly 14 columns;
- the run either applies the Tracker write successfully or explicitly returns the complete TSV fallback;
- the task does not claim a write succeeded when it did not.

A TSV fallback is a valid product path. The purpose is to observe which path the current Scheduled Task environment supports.

## Failure reporting

If the run fails, record the exact boundary, such as:

- profile read unavailable;
- Tracker read incomplete;
- Gmail source unavailable;
- Sheet write requires approval;
- Sheet write action unavailable;
- fallback incomplete;
- connector action differs from interactive ChatGPT.

Do not infer product-wide behavior from a single workspace or plan. State the environment and date of the observation.

## Recording the sample run

If the same validation is used to produce README media:

- record only the fictional validation setup;
- redact account chrome, file IDs, private URLs, and identifying metadata;
- show the actual observed path;
- if Sheets writing succeeds, show the resulting Tracker row;
- if it does not, show the explicit TSV fallback;
- label the media with the verification date;
- clearly distinguish observed connected behavior from the repository's illustrative GIF.

The existing `assets/sample-workflow.gif` remains illustrative unless replaced by a genuinely observed and privacy-safe recording.

## Result template

```text
Validation date:
Environment:

Private profile read: PASS / FAIL
Full Tracker read: PASS / FAIL
Tracker completeness: VERIFIED / INCOMPLETE
Gmail source read: PASS / FAIL
Scheduled Task Sheet write: SUCCEEDED / BLOCKED / UNAVAILABLE
14-column TSV fallback: NOT NEEDED / RETURNED / FAILED
Observed path:
Documentation changes required:
Recording created: YES / NO
```

Do not publish the temporary profile, Gmail content, or private Google URLs.
