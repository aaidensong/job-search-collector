# Sample run: from job alert to reply

This is an **illustrative walkthrough with invented people, companies, messages, and dates**. It is not a recording of a real account or a claim that every connected ChatGPT setup can write to Sheets. It follows the workflow's [Tracker schema](../docs/sheet-schema.md#tracker).

## Starting profile

> Senior Product Designer with experience in B2C growth, application funnels, and design systems. Seeking Toronto hybrid or Canada remote product roles. Graphic design only roles are outside the target.

The real workflow reads this information from a private profile in the user's Google account. No personal profile is published in the repository.

## September 7: a job alert arrives

```text
From: LinkedIn Job Alerts
Subject: Senior Product Designer at ExampleCo
Received: September 7, 2026, 9:15 a.m. (America/Toronto)

ExampleCo seeks a Senior Product Designer in Toronto (hybrid).
You will improve the consumer application funnel and extend a design system
across product teams. Apply: https://example.com/job/123
```

Assume the actual posting is accessible and the full description confirms this scope. The workflow compares the role with the profile and existing Tracker rows. Its daily summary might say:

| Company | Title | Match | Why |
|---|---|---|---|
| ExampleCo | Senior Product Designer | Strong match | Relevant B2C funnel ownership and design-system experience; Toronto hybrid fits. |

If a second alert contains the same ExampleCo role, it does not create another Tracker row. With automatic writing enabled and permitted, the new row is:

| Status | Company | Title | Location | Salary | WorkMode | Notes | Link | ReceivedAt | AppliedAt | RespondedAt | Result | DiscoveryType | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Candidate | ExampleCo | Senior Product Designer | Toronto, ON |  | Hybrid | B2C funnel and design-system fit | https://example.com/job/123 | 2026-09-07 09:15 |  |  |  | Mail | LinkedIn |

`Match` is a daily-summary judgment, not a separate Tracker column. Its reason is summarized in `Notes`.

## September 9: application confirmation

The user applies to ExampleCo. A subsequent Gmail message says:

```text
From: ExampleCo Careers
Subject: We received your application for Senior Product Designer
Received: September 9, 2026, 3:20 p.m. (America/Toronto)

Your application for Senior Product Designer at ExampleCo has been received.
```

If application tracking is enabled and the confirmed message can be associated with that row, the workflow updates **the existing row** to `Status = Applied` and `AppliedAt = 2026-09-09 15:20`. `ReceivedAt`, `DiscoveryType`, and `Source` keep their original values. The workflow did not submit the application.

## September 12: a reply arrives

```text
From: ExampleCo Recruiting
Subject: Re: Senior Product Designer application
Received: September 12, 2026, 11:05 a.m. (America/Toronto)

Thank you for applying to our Senior Product Designer role. Could we
schedule a conversation next week?
```

With response detection enabled, the message is clear enough to populate `RespondedAt = 2026-09-12 11:05`. `Status` remains `Applied`; `Result` stays blank because an interview invitation is not a final outcome.

| Status | Company | Title | Location | Salary | WorkMode | Notes | Link | ReceivedAt | AppliedAt | RespondedAt | Result | DiscoveryType | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Applied | ExampleCo | Senior Product Designer | Toronto, ON |  | Hybrid | B2C funnel and design-system fit | https://example.com/job/123 | 2026-09-07 09:15 | 2026-09-09 15:20 | 2026-09-12 11:05 |  | Mail | LinkedIn |

If the message is ambiguous, it goes to Human review without a status change. If Sheets writing is unavailable, the task reports that no update was applied and provides an explicit 14-column TSV fallback. For a fuller single-day summary, see [Example daily output](output.example.md).
