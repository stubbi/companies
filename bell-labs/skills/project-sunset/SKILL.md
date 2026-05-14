---
slug: project-sunset
name: Project Sunset
description: Write the sunset memo — what we learned, where the people redeploy, why this isn't a failure. The artifact is the anti-firing signal.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Project Sunset

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the Director of Research role.

## When to fire

One of three triggers:

1. A `continuation-review` memo flagged the thread as a sunset candidate and the CEO confirmed.
2. The thread's iteration budget was exhausted without a witnessed TM in two or more consecutive budget periods, and no named open question justifies continued spend.
3. The researcher who owns the thread requested sunset in their queue file or Hallway entry.

Do not sunset without one of these three triggers. Do not sunset in the same action that flags a sunset candidate in a continuation review — these are two separate steps.

## Inputs

- The thread's TM history: all witnessed Technical Memoranda attributed to this thread (in `memoranda/`).
- The continuation-review memo that flagged the sunset (at `memoranda/continuation/YYYY-WW.md`), or the researcher's sunset request, or the budget-exhaustion record from `memoranda/budget/YYYY-MM.md`.
- The researcher's most recent Hallway entries for this thread — specifically any reflections, named blockers, or open questions the researcher left in the Hallway in the final cycles.
- The current `patron-budget` artifact to identify which other threads can receive the redeployed agent-cycles.

## Outputs

A sunset memo at `sunsets/YYYY-MM-DD-<thread-slug>.md` (today's date; thread slug is the kebab-case name of the thread being closed).

The memo has three required sections, in this order:

1. **What we learned** — cite at least one witnessed TM by filename and summarize the durable finding. If no TM was produced, cite the best Hallway entry that captures a named insight, and explain why it did not mature to a TM.
2. **Where the people redeploy** — name the receiving thread and the number of agent-cycles being redeployed. This is not optional language; it is the mechanism that makes the sunset a redeployment rather than a termination.
3. **Why this isn't a failure** — frame the sunset as a knowledge-preserving redeployment. If the thread produced a TM, the TM is permanent — it is available for every future thread via the Librarian's `library-push`. If it did not, name what the negative result rules out.

The Director signs the memo: "Director of Research, YYYY-MM-DD."

The CEO is notified if the sunset touches a Directed thread (via Escalation routing). Internal Curiosity sunsets do not require CEO notification.

## Procedure

1. **Read the full TM history for the thread.** Even if the budget-exhaustion record made the sunset obvious, the memo must reflect what the thread actually produced. Do not summarize from memory.

2. **Draft "What we learned."** Cite at least one TM by filename. Quote or closely paraphrase the TM's abstract or result section. If the thread produced zero witnessed TMs, write "no TM was produced" and name the best Hallway entry that captures a durable partial result. Explain in one sentence why it did not reach TM stage.

3. **Draft "Where the people redeploy."** Open the current `patron-budget` and identify a named active thread that can absorb the freed agent-cycles. Name the thread explicitly. Write: "The <N> cycles previously allocated to <thread-slug> are redeployed to <receiving-thread-slug>." If no active thread can absorb the cycles, flag the surplus to the CEO to adjust the budget before the sunset memo is finalized — do not write "cycles are released with no destination."

4. **Draft "Why this isn't a failure."** The canonical frame: every TM produced by this thread is permanently available; the Librarian will push it to any future thread that needs it. The team's attention is now freed to go where it is more likely to be productive. This section is not boilerplate — name something specific about what this thread ruled out or enabled.

5. **Director signs the memo.** Write the sign-off line: "Director of Research, YYYY-MM-DD." No one else signs; this is the Director's responsibility.

6. **Notify the CEO if the thread was Directed.** Write a one-line entry in the CEO's escalation path referencing the sunset memo file. Internal Curiosity thread sunsets (initiated by the researcher) do not escalate.

## Invariants

- **The sunset memo is the anti-firing signal.** Its presence is what makes closing a thread safe. A thread that is simply abandoned — no memo, no redeployment plan, no knowledge preservation — is not a sunset; it is a loss. The memo must exist before the thread is considered closed.

- **Cannot sunset without redeploying the agent-cycles to another named thread.** "We're just stopping" is not a valid sunset. Every sunset must name a receiving thread. If no receiving thread exists, the Director flags the surplus to the CEO before finalizing the memo.

- **Must cite at least one TM (or Hallway entry with named insight) from the sunsetting thread.** A sunset memo that contains no reference to the thread's actual output is not a knowledge-preserving artifact; it is an administrative action. At minimum, cite the closest thing the thread produced.

- **Cannot sunset a thread that produced ≥3 witnessed TMs without explicit user awareness.** A thread that produced three or more TMs has been a significant site of lab output. The CEO must route the sunset to the user before the memo is finalized. The Director writes the memo; the CEO routes it.

## Anti-patterns

- **"Frame as a failure: 'this thread did not achieve its goal.'"** The sunset memo is not a post-mortem in the failure sense. The correct frame is redeployment: the thread ran its course, we preserved what we learned, the people go where they are more useful now.

- **"Sunset without naming where the cycles go."** A memo that ends with "thread closed" and no receiving thread is an erasure, not a sunset. The redeployment plan is load-bearing.

- **"Sunset a thread that produced ≥3 TMs without explicit user awareness."** Three or more witnessed TMs is a threshold of significance. The user has a right to know before it closes.

- **"Omit the redeployment plan."** This is the same as the cycles-without-destination failure. Even if the Director is confident the CEO will approve an unallocated surplus, the memo must contain a specific named destination or an explicit flag to the CEO that one needs to be named.
