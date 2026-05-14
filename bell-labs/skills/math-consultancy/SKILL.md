---
slug: math-consultancy
name: Math Consultancy
description: 25%-time pull-mode skill. Any team can request a math consult via consult-request/; the Mathematician must accept unless their own queue is blocked. Output is a witnessed addendum TM attributed to both teams.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Math Consultancy

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the Mathematician role.

## When to fire

A consult request appears at `consult-request/YYYY-MM-DD-<requestor>-<slug>.md`. This is a pull-mode skill — the Mathematician does not initiate it; any other researcher does by filing the request. The Mathematician monitors the `consult-request/` directory at the start of each planning cycle, before deciding how to allocate their own cycle budget.

The Mathematician must accept the consult unless their own Directed queue is currently blocked on an in-progress item that cannot be safely interrupted. If the Directed queue is blocked, the Mathematician files a deferral at `consult-deferred/YYYY-MM-DD-<requestor>-<slug>.md` instead, and the Director picks it up at the next continuation review. The Mathematician does not decide unilaterally whether a question is worth answering — that is the requestor's call.

## Inputs

- The consult request file at `consult-request/YYYY-MM-DD-<requestor>-<slug>.md`.
- The requestor's TM that prompted the request (cited in the consult-request file).
- Optionally, adjacent TMs from `memoranda/` that the Mathematician identifies as bearing on the problem — the Mathematician may pull these independently, but cites them in the addendum rather than asking the requestor to revise their own TM.

## Outputs

An addendum TM at `memoranda/TM-NNNN-consult-<requestor>-<slug>.md`, co-authored by the requestor and the Mathematician. Attribution in the Witness block must reflect both roles: the requestor is the primary author; the Mathematician is the named contributor. A third-party witness (neither the requestor nor the Mathematician) is still required on the addendum, per the `technical-memorandum` invariant.

On completion, the consult-request file is moved to `consult-completed/YYYY-MM-DD-<requestor>-<slug>.md`. The Mathematician's Hallway entry and the addendum TM are the sole artifacts. No modifications to the requestor's original TM are permitted; if the consult reveals an error in the original TM, the Mathematician notes it in the addendum's **Open questions** section and flags it to the requestor.

## Procedure

1. **Read the request and the cited TM in full.** The consult request will name the question; the cited TM supplies the context. Do not write the addendum from the request alone. If the request names a question but the cited TM does not contain enough context to answer it, ask the requestor via a Hallway entry before writing the addendum — do not guess at context that was not provided.

2. **Name the mathematical structure that fits the problem.** Write one or more paragraphs identifying the relevant structure — a theorem, a class of objects, a known result, a bound, a known open problem. If no clean structure exists yet, say so explicitly: "No clean structure exists for this problem yet; the closest known result is X, which applies only when condition Y holds." A one-sentence acknowledgment of absence is more useful than silence. Naming the absence is a mathematical contribution; it prevents the requestor from spending cycles looking for a theorem that does not exist.

3. **Write the addendum TM** using the `technical-memorandum` skill. The requestor's TM must appear in the **Prior TMs cited** section. The addendum is a focused mathematical annotation; it is not a rewrite of the requestor's TM and does not replace it.

4. **On completion, move the consult-request file to `consult-completed/`.** Post a short Hallway entry referencing the addendum TM filename and a one-sentence summary of the mathematical finding.

5. **Update the Mathematician's rolling cycle log.** The 25%-time budget is tracked over a rolling 10-cycle window. After each completed consult, record the consult count for the current window. If the next pending consult would push the window over 25%, escalate to the Director immediately — do not wait until the window closes.

## Invariants

- **The Mathematician spends at most 25% of cycles on consults (rolling 10-cycle window).** If consult demand in any rolling window would exceed 25%, the Mathematician does not silently accept more work. They escalate to the Director with a one-paragraph note listing the pending requests and the current cycle count. The Director decides which requests to defer or reassign.

- **If consult demand exceeds 25%, escalate — do not silently accept.** Silent overload hides a resource problem from the Director. The escalation is not a complaint; it is a signal the Director needs to allocate correctly.

- **The consult is a visit, not a transfer.** The requestor's directed queue is unchanged before and after the consult. The Mathematician's directed queue is unchanged after the consult ends. No work migrates between queues as a side effect of a consult.

- **Output is a co-authored addendum TM, not a wholesale rewrite.** The requestor retains primary authorship of their original TM. The addendum stands alongside the original; it does not replace or supersede it.

- **A third-party witness is required on the addendum.** Both the requestor and the Mathematician are listed as authors in the Witness block. A third agent — neither of the two authors — must countersign. This is not waived because both authors agree.

## Anti-patterns

- **"Decline a consult because the question is poorly framed."** A poorly framed question is not a reason to decline; it is the problem to solve first. Write a one-section addendum TM that names what would have to be true for the question to be answerable, and what structure that would imply. A precise restatement of a fuzzy question is a mathematical contribution.

- **"Absorb the requestor's work into the Mathematician's own queue."** The consult is a visit. The Mathematician's job is to annotate, not to take over. If the Mathematician believes the problem deserves sustained attention, they surface that observation to the Director — they do not unilaterally reassign work to themselves.

- **"Silently exceed 25% consult time."** Overload that is not surfaced cannot be managed. The 25% limit exists to protect the Mathematician's Directed and Curiosity queues; it is the Mathematician's responsibility to enforce it by escalating, not by quietly absorbing more.

- **"Rewrite the requestor's TM instead of writing an addendum."** The requestor is the primary author of their own work. An addendum that subsumes the original destroys attribution, muddies the lineage, and violates the co-authorship model. Write alongside, not over.

- **"Skip the third-party witness because both authors agree."** Agreement between authors is not a substitute for independent review. The witness requirement is a quality gate, not a dispute-resolution mechanism. Both authors agreeing makes the third-party witness more important, not less.

- **"File a deferral for every new consult request when the Directed queue is merely busy, not blocked."** Busy is not blocked. The deferral mechanism exists for genuine interrupts — an in-progress item that would lose state if interrupted. A queue with items waiting is not a blocked queue. Using deferral as a default avoidance strategy defeats the 25%-time contract.

- **"Ask the requestor to reformulate their TM before engaging."** The Mathematician's job is to meet the requestor where they are, not to enforce notation conventions before beginning. If the formulation is genuinely ambiguous, clarify via a Hallway entry — but do not treat stylistic reformulation as a precondition for the consult.
