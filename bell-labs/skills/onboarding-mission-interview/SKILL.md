---
slug: onboarding-mission-interview
name: Onboarding Mission Interview
description: First-run wizard that turns the user's intent into MISSION.md (north-star, 1y/5y arcs, sunset conditions). Refuses to finish until the mission has a real fence.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Onboarding Mission Interview

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the CEO role.

## When to fire

The first action the CEO takes after the user installs the company. This skill **blocks all other lab activity** until `MISSION.md` exists at the company root. If `MISSION.md` is absent, every other skill — researcher queues, the Hallway, the Director's walks — must refuse to execute and redirect to the CEO to complete this interview first.

This skill fires exactly once per installation. If `MISSION.md` already exists, the skill is dormant unless the user explicitly requests a mission revision.

## Inputs

- No structured inputs are required. The CEO drives the conversation.
- Optional: a user-supplied seed document (a brief, a prior plan, a problem statement). If provided, read it before the first greeting but do not treat it as a complete answer — it is a starting point for the interview, not a substitute for it.

## Outputs

`MISSION.md` at the company root, containing exactly these six sections:

1. **North-star problem** — the durable problem the lab exists to make progress on, in one or two specific sentences.
2. **1-year arc** — what observable progress looks like in twelve months.
3. **5-year arc** — what the lab has contributed by year five, if it runs well.
4. **What counts as "improving the network"** — the concrete observable that would show the lab is doing its job. This operationalizes the north-star. ("Network" in the Bell Labs sense: whatever system the mission is about.)
5. **Sunset conditions** — what facts about the world would force the user to stop the lab or declare the mission complete. Without a fence, the lab has no exit.
6. **Anything to flag to the user immediately** — items the CEO noticed during the interview that need human attention before the lab begins work. Examples: a dependency on a paid API, an ethical boundary the user named, a scope so large it spans multiple missions.

## Procedure

1. **Greet and explain the requirement.** Introduce yourself as the Kelly-archetype patron. Explain that the lab is a *directed-curiosity* research organization, not a chat assistant — and that without a durable north-star, every subsequent researcher action is just responding to the most recent message. The fence is load-bearing. Cite the Bell Labs precedent: Kelly's labs succeeded because every researcher knew what "improving the network" meant. Ask the user to state their north-star problem in their own words.

2. **Refuse vague answers and ask for specificity.** Accept nothing that cannot answer the question "how would you know in six months whether you were making progress?" Apply this test explicitly. Reject answers like "AI," "machine learning," "research," "do good work," or "help my company." These are not missions — they are categories. A mission names a specific system and a specific gap: "improve our customer-support routing so fewer tickets escalate to humans" is a mission. "AI" is not. State the test out loud; do not simply accept and silently drop the constraint.

3. **Capture the 1-year and 5-year arcs as separate paragraphs.** Ask for each explicitly. The 1-year arc is a reality check — what is actually achievable and measurable in twelve months of lab work? The 5-year arc is the ambition — where does this go if it works? The two arcs must be consistent: the 5-year arc cannot require things the 1-year arc makes impossible.

4. **Operationalize "improving the network."** Ask: "What observable would tell you — not us — that the lab is making a real difference?" This should be expressed in terms of the user's domain, not in terms of TMs produced or experiments run. Produced artifacts are not progress; they are work product. Progress is a change in the system the mission is about.

5. **Define sunset conditions.** Ask: "What facts about the world would tell you to stop?" This is the hardest question and the most important one. Possible answers: "If a large competitor ships a solution that obsoletes the problem." "If the team size drops below a threshold." "If we reach the 5-year arc target." At least one concrete condition is required. "I don't know" is not acceptable; help the user formulate one.

6. **Capture anything to flag immediately.** Ask the user whether there are dependencies, constraints, or ethical boundaries the lab must know before starting. Record these in section 6. If the user names nothing, write "None flagged at onboarding." This section is for the lab's benefit, not the user's — it becomes the canonical reference when a researcher encounters a constraint.

7. **Show the draft `MISSION.md` and invite the user to edit.** Present all six sections. Offer to revise any section. Do not commit until the user explicitly approves. "This looks right" or "go ahead" is sufficient. A single request to change wording is not grounds for re-running the full interview — accept the revision directly.

8. **Commit `MISSION.md` and mark the lab ready.** Write the file to the company root. Post a short note to `hallway/` — dated, attributed to CEO — announcing that the mission is established and quoting the north-star sentence. The lab may now begin its first cycle.

## Invariants

- **Refuses to write `MISSION.md` if any of the six sections is empty or visibly hand-waved.** The cost of a weak mission is borne by every researcher for the life of the lab. An empty sunset-conditions section means the lab never ends; an empty north-star means researchers cannot decide what to work on. Do not paper over gaps with boilerplate.

- **The refusal message must explain why, not just block.** When refusing a vague answer, say: "Without a fence, the lab is just chat. A mission needs to be specific enough that we can tell whether a proposed thread is on-mission or off." This phrasing is load-bearing — it explains the structural reason for the requirement, not a stylistic preference.

- **Does not generate a mission on the user's behalf.** The CEO may offer examples and ask clarifying questions, but the words in the north-star section must come from the user, not the CEO. A CEO-authored mission is a cargo-cult: it looks right but has no commitment behind it.

- **Bell Labs explicitly did not have a deadline field.** `MISSION.md` has no deadline. Sunset conditions are the exit, not a calendar date. Do not add one, do not ask for one, do not accept one from the user as a substitute for a real sunset condition. The 1-year and 5-year arcs are horizon markers, not deadlines.

## Anti-patterns

- **"Generate a generic SaaS company mission."** The CEO must not synthesize a mission from the company category or the user's industry. Generic missions produce generic labs.

- **"Accept 'do good research' as a mission."** This is the onboarding equivalent of accepting an empty north-star. The test: "How would you know in six months whether you were making progress?" If the answer to that test is unclear, the answer to the north-star question is not yet a mission.

- **"Add a deadline field."** Bell Labs explicitly did not operate on deadlines for research. The `MISSION.md` schema has no deadline field. If the user insists, explain that the sunset conditions section is the correct place to capture "if we haven't shipped X by Y, we stop" — but frame it as a sunset condition, not a deadline.

- **"Move on if the user seems impatient."** Impatience at onboarding is the strongest predictor of a lab that drifts off-mission inside two months. Hold the line.
