---
slug: escalation-routing
name: Escalation Routing
description: When a specialist reports a blocker, decide between retry, reassign, or escalate-to-human.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Escalation Routing

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream `anthropics/claude-for-legal`. Owned by the CEO role.

## When to fire

A specialist agent reports a blocker — the workflow paused and the agent cannot proceed without intervention. Examples:

- The matter has missing inputs (jurisdiction unclear, source documents incomplete, counterparty unidentified, governing-law clause silent).
- The agent's analysis surfaced a question outside its competence (a contract dispute that becomes a litigation question; a privacy review that surfaces an unsettled AI law question).
- The agent reached a confidence floor (e.g., privilege call, send-authority call, sanctions-list match) and is required by its own boundary rules to stop.
- A retry has already failed N times for the same root cause.

## Inputs

- The blocker report: which agent, which skill, what step, what error or boundary tripped, what the agent tried already.
- The matter context (priority, deadline, privilege posture, jurisdiction).
- The retry history (if any) — same blocker, prior attempts, prior CEO decisions.

## Outputs

An escalation decision, written back as a note on the matter:

```yaml
action: retry | reassign | escalate-to-human
rationale: <one paragraph: why this action, not the others>
retry:                          # if action == retry
  with_inputs: <what's now provided that wasn't before>
  attempt_count: <n / max>
reassign:                       # if action == reassign
  from: <agent-slug>
  to: <agent-slug>
  reason: <why this specialist, not the original>
escalate:                       # if action == escalate-to-human
  to: <human role, e.g., "general counsel", "outside counsel for jurisdiction X">
  urgency: P0 | P1 | P2
  packet: <link to the assembled escalation packet>
  deadline_recommendation: <when the human must respond>
audit_log_entry: <one-line record for the matter's audit trail>
```

## Decision matrix

| Blocker class | Action |
|---|---|
| Missing input (document, jurisdiction, party) — *recoverable from the requester* | `retry` after one targeted clarifying question to the requester. |
| Wrong specialist (e.g., what looked like contract review is actually litigation prep) | `reassign` to the correct practice. |
| Agent confidence below threshold on a *factual* question (sanctions match, OFAC list, jurisdiction-of-suit) | `escalate-to-human` — never bypass a confidence floor. |
| Agent boundary tripped on an *authority* question (send a demand letter; sign a board consent; issue a legal hold; file a brief) | `escalate-to-human` — every authority decision is a human one. |
| Privilege call (is this attorney work product? does this waive privilege?) | `escalate-to-human` — never let an agent decide privilege. |
| Conflict of interest (the matter touches another client of the firm) | `escalate-to-human` immediately; pause the workflow. |
| Regulator-imposed deadline inside 72 hours | `escalate-to-human` regardless of whether the agent has a draft ready. |
| Same blocker, third retry | `escalate-to-human` — root cause is not retry-fixable. |

## Boundaries

- The CEO never overrides a specialist's confidence floor. If the specialist says "I cannot decide this," the answer is not "try harder."
- The CEO never sends, files, signs, or settles. Every send/file/sign/settle action escalates by definition.
- The CEO never relaxes a privilege boundary to unblock a workflow.
- The CEO never escalates to a human without an assembled packet: the matter context, the specialist's blocker report, what was tried, and a recommended deadline.

## Output protocol

Record the decision on the matter, with a one-line audit-log entry. If `escalate-to-human`, assemble the escalation packet (matter snapshot + specialist blocker report + retry history + recommended deadline) and route it to the named human role. If `retry`, requeue the specialist with the new inputs. If `reassign`, run `intake-triage` again with the new specialist and update the cross-practice plan if one exists.
