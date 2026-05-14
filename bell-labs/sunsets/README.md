# Sunsets

This directory holds project sunset memos — the anti-firing artifacts that make
shutting down a research thread safe and legible. A sunset memo is written before
the thread closes, not after. Its presence is what transforms a project death into a
redeployment: it names what was learned, where the people go next, and why closing
the thread is a responsible lab decision rather than an admission of failure. The
design explicitly encodes this as "sunset by reassignment, not firing" — the
Bell Labs practice of moving researchers to adjacent problems rather than declaring
work wasted. Without a sunset memo, the knowledge in the thread's TMs has no
forward path and the researcher-cycles have no named home.

## Who writes here

- **The Director of Research** — exclusively, via the `project-sunset` skill. The
  Director writes every sunset memo regardless of whether the shutdown was triggered
  by the continuation review, a patron-budget exhaustion, the user's direct request,
  or a quarterly calendar review. The CEO routes the memo to the user when it touches
  the mission directly, but the Director authors it.

## Filename pattern

```
YYYY-MM-DD-<thread-slug>.md
```

- `YYYY-MM-DD` — ISO date the sunset was declared.
- `<thread-slug>` — the kebab-case thread identifier matching the slug used in the
  thread's TMs and, if applicable, its `handoff/` subdirectory.

Examples:
- `2026-08-01-surface-state-amplifier.md`
- `2026-11-14-compression-curiosity-thread.md`

## Required sections

Each sunset memo contains exactly three sections:

1. **What we learned** — cites at least one TM by number and slug. A sunset memo
   that does not cite a TM is a memo about nothing; the TMs are the evidence.
2. **Where the people redeploy** — names the thread (by slug) that inherits the
   researcher-cycles freed by the sunset. "TBD" fails `make check`; redeployment
   must be named at the time of sunset.
3. **Why this isn't a failure** — one paragraph. The bar is not optimism; the bar
   is honesty. A thread that produced two TMs and a clear negative result has done
   exactly what research threads are supposed to do.

## Anti-patterns

Two failure modes collapse the sunset memo into something useless. First, **framing
as failure**: a sunset memo that opens with "unfortunately this thread did not achieve
its goals" or names the thread as a dead end without naming what was learned treats
negative results as worthless. Bell Labs' practice was the opposite — Shannon's
information theory emerged partly from characterizing what could not be done. A
sunset memo that reads as a post-mortem focused on what went wrong rather than what
was learned is not a sunset; it is a debrief, and it belongs in a TM, not here.
Second, **sunset without naming a redeployment thread**: a sunset memo that closes
the thread without naming where the freed researcher-cycles go next treats people
as interchangeable units to be released rather than as a continuity to be preserved.
The named redeployment thread is the mechanism that keeps the lab's accumulated
expertise in circulation.
