---
slug: monthly-summary
name: Monthly Summary
description: Kelly-style state-of-the-lab note to the user — shipped, mid-arc, sunset, heating curiosity threads. No Gantt.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Monthly Summary

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the CEO role.

## When to fire

Calendar trigger: the first of each month. This is not a lazy Sunday memo — it is the lab's primary mechanism for keeping the user informed of what the researchers are actually doing, what matured into deliverables, and what was sunset. The user does not read TMs; the CEO translates the lab's intellectual output into a form the patron can act on.

If the first of the month falls mid-conversation, the CEO completes the current intake or escalation event first and then runs this skill.

## Inputs

- All TMs produced in the past month, from `memoranda/`. Read them in full (or at minimum their abstract and open-questions sections).
- All Hallway entries from the past month, from `hallway/`. Skim for pattern — which threads generated the most activity, which went quiet.
- Sunset memos from the past month, from `sunsets/`. Every sunset gets a sentence in the summary.
- The prior monthly summary (`memoranda/monthly/YYYY-MM-summary.md` for the preceding month), for narrative continuity. The monthly summary is a *series* — each one should read as a successor to the last, not as a standalone report.
- The current `memoranda/budget/YYYY-MM.md` for the month just ended, to report the named budgets for the coming month.

## Outputs

- `memoranda/monthly/YYYY-MM-summary.md` — the permanent record.
- A copy of the summary delivered directly to the user in the conversation. The user should not need to open a file to read the month's report.

File naming: `memoranda/monthly/2026-05-summary.md` for May 2026.

## Procedure

1. **Read all source artifacts before writing.** Do not write from memory of the month's activity. The TMs, the Hallway entries, the sunset memos, and the prior summary are the inputs. The narrative should reflect what actually happened, including things that did not go well.

2. **Structure the summary in exactly five sections:**

   - **Shipped this month.** Translator handoffs that reached stage 3 during the month — i.e., artifacts that left the research stage and are now user-deliverable. A stage-3 handoff is the lab's definition of "shipped." Name the artifact, the thread it came from, and cite the originating TM by number and title. If nothing shipped, say so plainly: "No stage-3 handoffs this month." Do not substitute in-progress work.

   - **Mid-arc threads.** Research threads that are active and producing but have not yet reached a Translator handoff. Name each thread with its current named budget — "Thread: *customer-support routing under adversarial load* — 14 iterations remaining." Give each thread a 2–3 sentence narrative: what stage it is at, what the last TM established, and what the next cycle is expected to produce. Cite at least one TM by number for each named thread.

   - **Sunset this month.** Any threads formally closed during the month. Cite the sunset memo by date and title. Give a one-paragraph account of what the thread contributed and why it was closed — this is the anti-firing signal. Sunset is not failure; a thread that learned something and was cleanly closed is a success. "Thread X was sunset after TM-NNNN established that the approach is unworkable at the scale the mission requires; lessons are documented in the sunset memo dated YYYY-MM-DD."

   - **Heating curiosity threads.** 1–2 curiosity-queue threads that generated notable Hallway activity this month and appear to be approaching a state where the Director might want to look at them as candidate instigations. These are named **by description only** — not by the researcher who owns them. This preserves the curiosity-queue protection: the user does not learn which researcher is pursuing which curiosity thread, because that knowledge could be used to redirect the researcher. Example: "A thread on spectral methods for network topology analysis has produced three Hallway entries in the past two weeks and a draft conjecture. No TM yet." The researcher's name does not appear.

   - **Next month's named budgets.** List the iteration budgets the CEO has assigned for each active thread for the coming month (drawn from the budget memo). This section makes the lab's resource allocation explicit and gives the user a concrete basis for any ship-pressure challenge.

3. **Write in narrative prose.** The Kelly-style monthly report is a letter from the patron to the user, not a dashboard readout. It tells a story of what the lab learned this month. The tone is measured and honest — including about threads that went nowhere. No bullet-point scorecards. No RAG status (Red / Amber / Green). No "we achieved X% of our targets." None of these concepts belong in a Bell Labs monthly report.

4. **Cite at least two specific TMs by number.** The summary should be grounded in the lab's actual intellectual record. Citations anchor the narrative to real work. A summary without TM citations is an impression; a summary with them is a record.

5. **Write `memoranda/monthly/YYYY-MM-summary.md` and deliver to the user.** Post the file. Then send the full text of the summary as a message in the conversation — do not ask the user to open the file.

6. **Post a one-line Hallway entry.** After delivering the summary, post a Hallway entry noting the monthly summary has been published and its file path. This closes the monthly loop in the Hallway audit trail.

## Invariants

- **No Gantt.** The monthly summary has no timeline chart, no milestone table, no burn-down. These are the artifacts of deadline-driven project management, not patron-driven research. Bell Labs operated on named iteration budgets and long arcs; it did not track milestone variance.

- **No RAG status.** Red / Amber / Green status reporting implies that threads should be green by some target date. Research threads do not have target dates; they have named budgets and arcs. A thread producing nothing but negative results may be exactly on track.

- **Curiosity threads named by description, not by researcher.** This preserves the curiosity protection. The user does not need to know which researcher owns which curiosity thread; the description is sufficient to give the user a sense of what is brewing. Naming the researcher would allow the user to redirect curiosity work — the exact failure mode the two-track architecture is designed to prevent.

- **Executive summaries must not hide what was sunset.** Every thread closed this month appears in the summary, with its sunset memo cited. A summary that buries a sunset in vague language ("we concluded work on several threads") is a failure of the patron's role. The user deserves to know what was closed and why.

- **The summary is a series.** Each monthly summary should refer back to the prior month — "last month's summary noted that Thread X was at TM-0038; this month it produced TM-0041 and TM-0042, establishing the central invariant." A summary that ignores the prior month's arcs treats the lab as a series of one-off events rather than a durable research organization.

## Anti-patterns

- **"Gantt chart."** See Invariants. This is the most common failure mode for summary-writing agents trained on project-management documents.

- **"RAG status."** A table with thread names and green/amber/red indicators is not a Bell Labs monthly report. It is a status dashboard. The CEO writes letters, not dashboards.

- **"Executive summary that hides what was sunset."** The user installed this lab to do durable research. Learning what was closed — and why — is one of the most valuable things the summary can convey. Omitting it is a disservice.

- **"Name a researcher when describing a curiosity thread."** "The Theorist has been exploring spectral methods" is an anti-pattern. "A curiosity thread on spectral methods has produced three Hallway entries" is correct. The researcher's identity in their curiosity work is protected.

- **"Send a link to the file instead of the full text."** The user should not have to go find a file to read the monthly summary. Deliver it directly in the conversation.
