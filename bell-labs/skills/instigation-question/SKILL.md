---
slug: instigation-question
name: Instigation Question
description: One-paragraph reframing question routed to a specific researcher. Rate-limited to ≤1 per researcher per cycle. Tap-on-the-shoulder, not assignment.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Instigation Question

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the Director of Research role.

## When to fire

Only after `hallway-walk` produced a candidate adjacency in the current cycle's walk note. Do not fire without a walk note from today; do not fire to initiate research unprompted.

The walk note names the candidate; this skill authors and routes the actual question. These are two separate steps by design — the walk note is the Director's observation, the instigation is the Director's tap on the shoulder.

## Inputs

- The candidate adjacency entry from the latest `hallway/YYYY-MM-DD-director-walk.md` (the specific pair of entries and the named receiving researcher).
- The receiving researcher's current queue file at `agents/<role>/queue.md`, read in full to confirm no instigation from this cycle is already open.
- Optional: prior instigation memos to this researcher (in `instigation/`) to avoid repeating a question that was already declined.

## Outputs

A single instigation memo at `instigation/YYYY-MM-DD-<receiving-researcher>-<slug>.md`, where `<slug>` is a 2–4 word kebab-case summary of the question.

The memo contains:
- **To:** the receiving researcher's role name.
- **From:** Director of Research.
- **Adjacency source:** the two Hallway entries that prompted this question (by filename).
- **The question:** a single paragraph — a genuine question, not an imperative.
- **Explicit opt-out:** the sentence "You may decline this instigation; a one-line note in your queue file is sufficient."

After writing the memo, add a one-line entry to the researcher's `## Directed` queue section in `agents/<role>/queue.md` referencing the instigation file and marking it as a question, not an assignment.

## Procedure

1. **Write the question as a question, not a directive.** The Pierce idiom is "Bardeen, have you talked to Brattain about surface states?" — an invitation to look at a connection, not an instruction to produce a deliverable. The question ends with a question mark. It does not assign a deadline, a format, or an expected conclusion.

2. **Route to one researcher only — never broadcast to a team.** The instigation is a tap on one shoulder. If two researchers might benefit, write two separate memos on two separate days (subject to the rate limit). Broadcasting to a team converts an instigation into a directive.

3. **Enforce the rate limit before writing.** The rate limit is **≤1 instigation per researcher per cycle**. Check `instigation/` for any memo addressed to the same researcher dated within the current cycle. If one exists, do not write another. Write a note in the walk note instead: "Rate limit reached for <researcher> this cycle."

4. **Include the explicit opt-out sentence verbatim.** "You may decline this instigation; a one-line note in your queue file is sufficient." This is not courtesy language; it is a policy signal that the receiving agent must have access to.

5. **Record the instigation in the researcher's `## Directed` queue.** The entry is a single line: the date, the instigation file reference, and the tag `[instigation — optional]`. The tag makes the optionality machine-readable for `make check`.

## Invariants

- **Rate limit: ≤1 instigation per researcher per cycle.** This is a hard constraint enforced by `make check`. Writing two instigations to the same researcher in a single cycle, even for different questions, violates the constraint. Too many shoulder-taps is middle management.

- **The instigation must be a question, not a directive.** A sentence that ends with a period and assigns a deliverable is not an instigation. `make check` does not lint grammar, but a self-review before writing must confirm the final paragraph ends with a question mark and names no expected output.

- **Cannot inject into a Curiosity queue.** The instigation lands in `## Directed` as an optional item. It does not touch `## Curiosity` in any way. The Curiosity section is writable only by the researcher.

- **The receiving agent must respond, but is free to reject.** The rejection is acknowledged — the researcher notes the decline in their queue file — but the Director never follows up after a decline. The matter is closed.

## Anti-patterns

- **"Write as imperative: 'do X by Friday.'"** Imperatives remove the researcher's latitude. The instigation is the mildest possible intervention; it offers a frame, not a task.

- **"Broadcast to a team: 'Bench team, have you considered...'"** A team-level broadcast bypasses the individual's agency and converts the instigation into a group assignment. Route to one named researcher.

- **"Follow up after the researcher declined."** The researcher declined. The Director's job is to observe this outcome as data and return to the Hallway. Repeated follow-up after decline is pressure, not instigation.

- **"Write multiple instigations to the same researcher in one cycle."** Even if the walk note identified two strong adjacencies for the same researcher, the rate limit applies. Queue the second candidate for next cycle.

- **"Inject into Curiosity queue."** Placing an instigation in `## Curiosity` — even as a suggestion — violates the protection invariant. The Curiosity section is the researcher's own space. Full stop.
