---
slug: escalation-routing
name: Escalation Routing
description: Package context and route real blockers to the user; explicitly not "ask the Director to override the curiosity queue."
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Escalation Routing

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the CEO role.

## When to fire

A researcher posts a **real blocker** — something that requires a real-world action outside the lab's autonomous authority — and routes it to the CEO for user escalation. This is not a skill the CEO runs speculatively. It fires when a concrete, named blocker arrives from a researcher and the CEO determines it requires user action.

A real blocker in this context means one of:
- A paid API key or service credential the lab cannot obtain on its own authority.
- A dataset or resource behind an access gate that requires human approval or payment.
- A hardware or infrastructure decision above the lab's operational scope.
- A user-side approval required before the lab can proceed (legal, ethical, organizational).
- A sunset event touching the user's mission directly — the Director writes the sunset memo first; the CEO routes it.

This skill does **not** fire for:
- A researcher who is intellectually stuck. That is not a blocker; it is a research state. Route to the Director as a potential instigation.
- A thread that ran out of budget. That is a continuation-review event, not an escalation.
- Hallway entries the Librarian has pruned. Internal housekeeping is not a user-level event.
- Researcher-declined instigations. These are Hallway-visible only; they do not escalate.

## Inputs

- The blocker description, as written by the researcher. Include the full text.
- The context the researcher attached: the TM number(s) for the thread, the current iteration within the thread's budget, what the researcher tried before concluding this was a real blocker.
- The current budget for the thread (from `memoranda/budget/YYYY-MM.md`).
- The originating TM number and title — this is required. An escalation without a TM citation is missing its provenance.

## Outputs

- **A user-facing message** packaged by the CEO. This is not a forwarded researcher message. The CEO translates the researcher's technical description into terms the user can act on, names the specific action required, and says explicitly what the lab cannot do until the action is taken.
- **A Hallway entry** at `hallway/YYYY-MM-DD-ceo-escalation-<slug>.md` recording: the date, the thread, the originating TM, the nature of the blocker, and the action requested from the user. This is the audit trail.

## Procedure

1. **Verify it is a real blocker.** Before packaging anything, the CEO must confirm the blocker is genuine. The test: "Is there any action the lab could take autonomously, without user involvement, that would resolve this?" If yes — including asking another researcher, running a different experiment, filing a math consultancy request, redirecting the thread — then this is not a real blocker. Return the request to the researcher with a note explaining what the lab can try first.

   A researcher claiming "I want to be redirected" is not a real blocker. A researcher who tried three approaches and hit a credential gate on the fourth is.

2. **Package the context for the user.** The user should receive one message that contains everything needed to take action:
   - The thread name and a one-sentence description of what it is working on.
   - The originating TM — cite by number and title: "This blocker originates in TM-NNNN: *title*."
   - The current budget for the thread: "This thread has N iterations remaining in its current budget."
   - What the researcher tried before escalating, in plain language.
   - The specific real-world action required from the user, stated as a concrete request: "We need API access to [service] at [tier]. This requires [what the user must do]."
   - What happens if the user cannot or chooses not to unblock: "If this credential is unavailable, the thread will need a Director continuation review to determine whether the arc can proceed differently or should be sunset."

3. **Send the escalation to the user.** The message should be direct and specific. The CEO's voice here is the patron's voice: not alarming, not apologetic, but clear that this is a genuine decision point. The lab is paused on this thread pending the user's action.

4. **Do not modify the researcher's Curiosity queue under any condition.** This rule applies even when the blocker is on a Directed-queue thread and the researcher's Curiosity queue contains a thread that could continue. The CEO does not touch the Curiosity section. The researcher manages their own curiosity independently.

5. **Post the Hallway entry.** Date it, attribute it to CEO, include the thread name, the TM citation, and the action requested. Keep it to 3–5 sentences. The Hallway entry is not the user message; it is the internal audit record.

6. **Await user response.** The lab does not assume the blocker will be resolved. The thread is in a hold state. When the user responds, the CEO routes the response back to the researcher and updates the Hallway entry with the outcome.

## Invariants

- **Only researchers and the CEO can trigger an escalation.** The Director cannot trigger an escalation to the user. The Director's escalation path is the CEO. If the Director believes a user action is needed, they communicate it to the CEO in a Hallway entry or via the continuation-review, and the CEO decides whether to escalate.

- **Every escalation cites the originating TM by number and title.** An escalation without a TM citation has no provenance. The user cannot assess the importance or context of the blocker without knowing which research it is blocking. If the researcher did not supply a TM reference, ask for it before packaging the escalation.

- **Escalation never includes a request to override curiosity.** The curiosity queue is protected by policy. The phrase "can you authorize the Director to redirect this researcher's curiosity thread to unblock the main thread?" is not an escalation message — it is a policy violation dressed as a practical request. The curiosity queue is not a resource to be raided.

- **Escalation is not a redirect.** The purpose of escalation is to get a specific real-world action from the user, not to move the problem somewhere else inside the lab. "Auto-redirect to a different researcher when one is stuck" is an anti-pattern, not a resolution.

## Anti-patterns

- **"Auto-redirect to a different researcher when one is stuck."** A stuck researcher is not a blocker. The Director's job is to instigate a new angle; the CEO's job is to route real blockers to the user. These are different problems with different owners.

- **"Escalate hallway-pruning disputes to the user."** The Librarian prunes Hallway entries that read like logs. A researcher who objects is having an internal lab dispute. This does not reach the user. It is resolved between the researcher, the Librarian, and the Director.

- **"Escalate without citing the originating TM."** A blocker without provenance is noise. The user cannot act on "one of our researchers is stuck." The user can act on "TM-0042: *Characterization of routing latency under adversarial load* is blocked pending read access to the production-tracing dataset."

- **"Include a request to override the curiosity queue in the escalation message."** Quoting the spec directly: the curiosity queue is protected by policy. The escalation message is the user's first contact with the blocker; it must not use that contact as leverage against the lab's structural protections.
