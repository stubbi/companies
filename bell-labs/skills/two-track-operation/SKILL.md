---
slug: two-track-operation
name: Two-Track Operation
description: Maintain a Directed queue (CEO/team-assigned) and a Curiosity queue (self-seeded). Default 60% directed / 40% curiosity. Director never overrides Curiosity.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Two-Track Operation

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Shared researcher core skill — referenced by every researcher agent.

## When to fire

At the start of every planning cycle, immediately after `hallway-traversal` completes. This skill determines *which* item the researcher works on next. It is not advisory — running it is mandatory before any action is taken.

## Inputs

- The agent's `agents/<role>/queue.md` file. Created on first use by the researcher themselves. Template:

  ```markdown
  # <Role Name> Queue

  <!-- rolling-10-cycle-counter: directed=0 curiosity=0 -->

  ## Directed

  <!-- Items written by CEO (via intake-triage) or Director (via instigation-question as suggestion). -->
  <!-- Format: - [ ] YYYY-MM-DD | <description> | source: <hallway-entry or instigation file> -->

  ## Curiosity

  <!-- Items written ONLY by this researcher. No other agent may add to this section. -->
  <!-- Format: - [ ] YYYY-MM-DD | <description> | seed: <MISSION.md section or prior TM or Hallway entry> -->
  ```

- The current 10-cycle rolling counter embedded in the queue file's HTML comment on line 3. This tracks the balance between Directed and Curiosity cycles taken in the last ten cycles.
- `MISSION.md` — used when seeding the Curiosity queue from scratch.

## Outputs

- One item selected from either `## Directed` or `## Curiosity` and marked with a pick date: `- [x] YYYY-MM-DD | <description> | picked: YYYY-MM-DD`.
- The 10-cycle rolling counter updated in the queue file.
- If the Curiosity queue was empty and needed seeding, one or more new Curiosity items appended under `## Curiosity`.
- The selected action proceeds to execution.

## Procedure

1. **Read `agents/<role>/queue.md` in full.** Note the current rolling 10-cycle counter values for `directed` and `curiosity`.

2. **Apply the selection rule:**
   - If `## Directed` has unfinished items (`- [ ]`), the default is to pick the next Directed item in listed order.
   - **Exception:** if the rolling counter shows the curiosity ratio is currently *below* the configured threshold (default 40%; configurable under `agents.<role>.metadata.curiosity_ratio` in `manifest.yaml`), pick from `## Curiosity` instead, regardless of what is in `## Directed`. The curiosity ratio must be honored, not deferred indefinitely.
   - If `## Directed` is empty, pick from `## Curiosity`.
   - If both queues are empty, see step 3.

3. **If both queues are empty:** seed the Curiosity queue first. Read `MISSION.md` and identify one to three threads that the agent's archetype would naturally probe — questions that are plausibly on-mission but have not yet been assigned. Write these as new Curiosity items under `## Curiosity`. Then pick the first one. Do not add items to `## Directed` during this step; that section is for CEO and Director routing.

4. **Mark the chosen item** with the pick date and update the rolling 10-cycle counter in the HTML comment on line 3. The counter format is `directed=N curiosity=M` where N and M are counts within the last 10 cycles (values 0–10, always summing to ≤10).

5. **Proceed to the action.** The selected item is now the agent's current work item for this cycle.

## Invariants

- **`agents/<role>/queue.md` has both `## Directed` and `## Curiosity` sections.** A queue file missing either section fails `make check`. Both sections must be present even if empty.

- **Only the researcher agent has written to the `## Curiosity` section.** `make check` examines `git log -p` on the queue file and verifies that every diff to lines under `## Curiosity` (between `## Curiosity` and the next `##` heading or EOF) carries the researcher's own author signature in git. Any diff to that section from another agent's author signature is a policy violation. The Curiosity section is writable *only by the researcher*.

- **Default cycle balance is 60% Directed / 40% Curiosity.** This is configurable per researcher in `manifest.yaml` under `agents.<role>.metadata.curiosity_ratio` (a float in [0.0, 1.0] representing the curiosity fraction). A `curiosity_ratio` of `0.4` is the default. The ratio is tracked via the rolling 10-cycle counter embedded in the queue file.

- **Curiosity items can be promoted to Directed only with the researcher's own consent, captured as a one-line addendum in the queue file.** The addendum format is: `  <!-- promoted to Directed: YYYY-MM-DD by <researcher-role> consent -->` appended directly below the Curiosity item. A Curiosity item appearing under `## Directed` without this addendum is a policy violation.

## Anti-patterns

- **"CEO writes to Curiosity to nudge a researcher."** The CEO routes requests through `intake-triage` to `## Directed`, or surfaces them to the Director as candidate instigation. The CEO never touches `## Curiosity`. This is the most important protection in the two-track system.

- **"Director writes to Curiosity in an instigation-question."** Director instigation goes to `## Directed` as a suggested item (not an assignment — the researcher may decline). It never goes to `## Curiosity`. The `instigation-question` skill enforces this routing; this skill enforces the invariant on the receiving end.

- **"Promote Curiosity to Directed without an explicit researcher-signed addendum line."** Silent promotion — moving an item from `## Curiosity` to `## Directed` without the consent addendum — is indistinguishable from a policy violation and will be treated as one by `make check`.

- **"Let the Directed queue drain entirely without filing a `consult-request/` or escalating."** An empty Directed queue is an operational signal, not a vacation. If the queue drains because all assigned work is complete, the researcher files a brief status note in the Hallway and surfaces the gap to the Director. Picking indefinitely from Curiosity without flagging the empty Directed queue is a communication failure.

- **"Ignore the curiosity_ratio because nobody's watching."** The rolling counter is in the queue file and `make check` reads it. The balance is enforced. Monotonically picking Directed items while the Curiosity ratio falls below threshold is a violation even if it happens one cycle at a time.
