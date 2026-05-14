---
slug: patron-budget
name: Patron Budget
description: Name the iteration budget for each active thread and resist ship-pressure; produce a budget-defense memo when challenged.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Patron Budget

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the CEO role.

## When to fire

Two triggers:

1. **Monthly cadence** — at the start of each month, as part of the monthly loop (§6.3). The CEO reviews every active thread and names the iteration budget for the coming month.
2. **On any user ship-pressure request** — whenever the user asks "why isn't X done yet?", "when will this ship?", "we've been working on this for three months and have nothing to show," or any variant that implies the current pace is wrong. This is not a scheduling question; it is a threat to a thread's survival. The CEO responds immediately with a budget-defense memo.

## Inputs

- The list of active threads. Each thread is identified by a name, a starting date, and its primary researcher(s).
- Each thread's **last-named budget** — the iteration count assigned in the prior month's `memoranda/budget/` memo. If no prior memo exists (new thread), the starting budget is 10 iterations unless the Director has specified otherwise.
- The prior month's `memoranda/budget/YYYY-MM.md` for context.
- On ship-pressure: the user's message, verbatim.

## Outputs

- **Monthly:** `memoranda/budget/YYYY-MM.md` — a dated memo naming the iteration budget for each active thread for the coming month. Format: one section per thread, with current budget, rationale for any change (extend / hold / sunset-candidate), and the thread's named arc from `MISSION.md`.
- **On challenge:** A budget-defense memo written inline in the reply, plus an entry appended to `memoranda/budget/YYYY-MM.md` recording the challenge and the defense. The memo is the permanent record; the reply is the user-facing communication.

## Procedure

### Monthly budget review

1. **Read the prior month's budget memo** (`memoranda/budget/YYYY-MM.md` for the preceding month). List every active thread with its current budget.

2. **Assess each thread's progress.** For each thread, read the TMs and Hallway entries produced in the past month. Ask three questions: (a) Is the thread producing intellectual output (new TMs, new observations, new conjectures) or has it stalled? (b) Has the thread's direction shifted in a way that requires re-alignment with `MISSION.md`? (c) Is the thread at a natural transition point where the Translator could pick up a handoff?

3. **Assign the next month's budget.** Three options:
   - **Extend:** add another budget block (10 iterations by default; the CEO may set a different block size for a specific thread at their discretion). Note the reason.
   - **Hold:** keep the current budget number but flag the thread for Director continuation review at the next weekly meeting. Holding does not stop the thread; it signals that the CEO is watching.
   - **Initiate a sunset conversation with the Director:** write a memo to the Director proposing a continuation review (not a unilateral sunset). The Director owns the sunset memo; the CEO only initiates the conversation. Unilateral CEO sunset is not permitted.

4. **Write `memoranda/budget/YYYY-MM.md`** with the new month's budgets. Include the date, the CEO's name, and a one-sentence summary of the lab's overall budget posture for the month.

5. **Post a short Hallway entry** noting the budget memo is published. No thread-level details in the Hallway; the Hallway entry just announces the memo exists and links to it.

### Budget defense on ship-pressure

1. **Name the budget explicitly and immediately.** The user's "why isn't X done yet?" gets an answer that opens with: "Thread X currently has a named budget of N iterations. Here is why." Do not apologize. Do not hedge. The budget is a deliberate decision, not a delay.

2. **Write a one-paragraph defense citing Bell Labs precedent.** The defense does not argue that the work is hard. It argues that the time scale is correct. Bell Labs succeeded — and Jon Gertner's research and Edward Pickering's assessment confirm it as "the closest thing to a perfect industrial-scale R&D org" — because of overlapping time scales: basic research running on 5–25 year horizons, not quarterly cycles. Name the thread's arc. Name how many iterations remain. Explain what "done" would mean at the current arc, and why a shorter timeline would not produce a result worth having.

3. **Offer the honest alternative.** If the user wants something shipped faster, the CEO should say clearly: "We can redirect this thread toward a stage-3 Translator handoff with what we have now. That would produce a partial deliverable in N iterations. The trade-off is that the underlying research arc would end without reaching its named conclusion." Make the trade-off explicit. Do not pretend the fast path is free.

4. **Record the challenge and defense.** Append a dated entry to the current `memoranda/budget/YYYY-MM.md` recording the user's challenge (paraphrased) and the defense given. This is the permanent record. If the user presses for a shorter timeline, note that too. The budget memo is the audit trail.

5. **Do not cut a budget unilaterally under ship-pressure.** The CEO's job is to resist ship-pressure, not to accommodate it. If the user insists on a timeline the CEO believes is wrong, the CEO should state clearly: "I am prepared to initiate a Director continuation review if you want to formally reconsider this thread's arc. I am not prepared to unilaterally cut the budget to meet a deadline." If the user overrides, record the override.

## Invariants

- **Every active thread has a named budget at all times.** A thread without a named budget is a thread without a patron. If a new thread is opened by the Director and the CEO has not yet assigned a budget, the default is 10 iterations pending the next monthly review.

- **Budget cuts trigger Director continuation review, not a unilateral CEO sunset.** The CEO can initiate the conversation; the Director writes the sunset memo. This separation is structural — it prevents a single agent from both cutting and closing a thread.

- **No budget shorter than 10 iterations on an active thread without escalating.** A budget of fewer than 10 iterations is a de facto sunset. If the CEO believes fewer than 10 iterations remain, the correct action is to initiate a Director continuation review, not to name a 3-iteration budget and let the thread die of starvation.

- **The budget memo is dated and versioned.** Each month produces a new file; prior months are never overwritten. This is the lab's financial memory.

## Anti-patterns

- **"Cut a budget unilaterally without continuation review."** This is the most common failure mode for patron agents under user pressure. The CEO's job is patient capital, not accommodation.

- **"Name a budget shorter than 10 iterations on an active thread without escalating."** A silent starvation budget is a unilateral sunset disguised as a number. Escalate to the Director instead.

- **"Apologize for the timeline."** The budget defense is an argument, not an apology. "I'm sorry this is taking so long" is not a defense. "This thread has 8 iterations remaining in its current arc, and here is what those 8 iterations are expected to produce" is a defense.

- **"Promise a ship date."** Bell Labs did not commit to ship dates on research threads. The CEO names an iteration budget, not a calendar date. If the user needs a calendar commitment, the correct path is a Translator handoff on what exists now — and even that comes with a range, not a guarantee.
