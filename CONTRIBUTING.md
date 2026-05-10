# Contributing

This is a personal catalog. It's hand-curated by one maintainer ([@stubbi](https://github.com/stubbi)) and the bar for new companies is intentionally high — bump cadence, attribution discipline, and Boundaries clarity matter more than catalog size.

## Best path: publish your own catalog

`companies.sh` installs are repo-agnostic. If you have an Agent Company you want to publish, the cleanest path is your own `<your-username>/companies` repo:

```bash
npx companies.sh add <your-username>/companies/<company-slug>
```

You keep your bump cadence, your curatorial voice, and your release schedule. No PR needed here.

## When to PR this repo

I'm happy to merge:

- **Typo / link / formatting fixes** in existing companies or the top-level README.
- **Schema drift fixes** if upstream sources change shape.
- **Upstream SHA bumps** for community-ported companies (run `make bump SHA=<new-sha>` and include the regenerated diff).
- **CI improvements** that don't add operational complexity.

I'm reluctant to merge:

- New companies (see "publish your own catalog" above).
- Refactors of `scripts/build.py` or `scripts/check.py` without a clear motivation.
- Skill renames in existing companies (these break installed deployments).
- Changes that weaken Boundaries sections in regulated-domain companies.

## How to PR

1. Fork the repo, branch off `main`.
2. Set up the company you're touching:
   ```bash
   cd <company-slug>
   python3 -m venv .venv
   source .venv/bin/activate
   pip install "pyyaml>=6.0" "pytest>=7.0"
   ```
3. If your change touches generated files (COMPANY.md, AGENTS.md, TEAM.md, SKILL.md, images/), edit the canonical source (`manifest.yaml` or hand-authored port-original SKILL.md) and re-run:
   ```bash
   make build       # regenerate artifacts
   make check       # validate schema, cross-references, content hashes
   make test        # run pytest
   ```
4. Commit the manifest change AND the regenerated artifacts together.
5. Open a PR with a clear description of what changed and why.

## Authoring port-original skills

If you're contributing a port-original (hand-authored) skill — typically owned by a CEO or coordinator role — author the SKILL.md file directly under `<company>/skills/<slug>/SKILL.md` with frontmatter:

```yaml
---
slug: <skill-slug>
name: <Skill Name>
description: <one-line description>
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: <your-name>
      added_in: <company-version>
---
```

Then add the skill to `manifest.yaml` with `port_original: true`. The build script will not overwrite your hand-authored content.

## License

Contributions are accepted under the same license as the file they touch:

- Top-level wrapper files (this `CONTRIBUTING.md`, the top-level README, CI scaffolding): MIT.
- Inside a community-ported company directory: the company's license (typically Apache-2.0 to match upstream).

By submitting a PR you agree to license your contribution accordingly.

## Code of conduct

Be kind, be specific, assume good faith. If something seems wrong, name what you observe and what you'd prefer instead.
