---
schema: agentcompanies/v1
slug: legal-services
name: Legal Services
description: 13-agent legal company — commercial, regulatory, IP, disputes, and legal-education
  plugins from anthropics/claude-for-legal, plus a CEO that handles intake, cross-practice
  coordination, escalation, and weekly summaries. Every output is staged for attorney
  review.
version: 0.1.0
license: Apache-2.0
authors:
- name: Jannes Stubbemann
  email: jannes@paperclip.inc
goals:
- Draft legal work product (memos, redlines, claim charts, deposition outlines, review
  reports, policies, classifications) for attorney review.
- Cover the 12 practice-area plugins Anthropic shipped — commercial, corporate, employment,
  privacy, product, regulatory, AI governance, IP, litigation, plus law-student /
  legal-clinic / legal-builder-hub on the education side.
- Stage every output for attorney sign-off — no agent here files briefs, sends demand
  letters, issues legal holds, or takes legal positions on behalf of any party.
tags:
- legal
- in-house-counsel
- commercial
- privacy
- regulatory
- litigation
- ip
- employment
- ai-governance
metadata:
  upstream:
    repo: anthropics/claude-for-legal
    commit: 9cecd91b0f26f732d18315afc3c9bb5ff99e0fbb
    license: Apache-2.0
  affiliation: Community port. Not affiliated with or endorsed by Anthropic.
---
# Legal Services

13-agent legal company — commercial, regulatory, IP, disputes, and legal-education plugins from anthropics/claude-for-legal, plus a CEO that handles intake, cross-practice coordination, escalation, and weekly summaries. Every output is staged for attorney review.

## Boundaries

Nothing in this package constitutes legal advice. Every output is a draft
for attorney review — not a legal conclusion, not a substitute for a lawyer.
These agents draft work product (memos, redlines, claim charts, deposition
outlines, review reports, policies, classifications) for review by a
qualified attorney. They do not file briefs, send demand letters, issue
legal holds, or take positions on behalf of any party; every output is
staged for human sign-off. The attorney using the package — not the
package, and not Anthropic — is responsible for the legal positions taken
in their work product.

## Teams

- **Commercial & Transactions** (`teams/commercial-transactions/TEAM.md`) — Day-to-day deal docs and workforce contracts — commercial agreements, M&A diligence, employment.
- **Regulatory & Compliance** (`teams/regulatory-compliance/TEAM.md`) — Rule-tracking and compliance posture — privacy, AI governance, regulatory feeds, product launches.
- **IP & Disputes** (`teams/ip-disputes/TEAM.md`) — Offensive and defensive workstreams — IP clearance / portfolio / enforcement and full litigation lifecycle.
- **Legal Academy & Tooling** (`teams/academy-tooling/TEAM.md`) — Education and meta-tooling — law-school work, clinic operations, and discovery / evaluation of community legal skills.

