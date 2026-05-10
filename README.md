# stubbi/companies

Community-published [Paperclip](https://github.com/paperclipai/paperclip) Agent Companies, maintained by Jannes Stubbemann ([@stubbi](https://github.com/stubbi)).

## Install

Each company can be added to a Paperclip instance with:

```bash
npx companies.sh add stubbi/companies/<company-slug>
```

## Companies

### [Claude for Financial Services](./claude-for-financial-services)

```bash
npx companies.sh add stubbi/companies/claude-for-financial-services
```

Community port of [`anthropics/financial-services`](https://github.com/anthropics/financial-services) into the Agent Companies format.

- **10 agents** across 4 functional areas (coverage & advisory, research & modeling, fund admin & finance ops, operations & onboarding)
- **31 deduplicated skills**, all referenced upstream by pinned commit SHA — nothing vendored or forked
- **License:** Apache-2.0 (matches upstream); `NOTICE` preserves upstream attribution per Apache-2.0 §4

> **Community port. Not affiliated with or endorsed by Anthropic.**

> **Boundaries.** Nothing in `claude-for-financial-services` constitutes investment, legal, tax, or accounting advice. These agents draft analyst work product (models, memos, research notes, reconciliations) for review by a qualified professional. They do not make investment recommendations, execute transactions, bind risk, post to a ledger, or approve onboarding; every output is staged for human sign-off. You are responsible for verifying outputs and for compliance with the laws and regulations that apply to your firm. See the [company's Boundaries section](./claude-for-financial-services/README.md#boundaries) for full detail.

[Company README →](./claude-for-financial-services/README.md)

## License

This repository's wrapper content (top-level README, structure) is MIT-licensed. Individual companies have their own licenses — see each company's `LICENSE` file.

Where individual companies operate in regulated domains (finance, legal, medical, etc.), each company's README documents the appropriate boundaries — read those before deploying.

## Contributing

This is a personal catalog. If you'd like to publish your own community-ported or original Paperclip companies, the cleanest path is your own `<your-username>/companies` repo — `companies.sh` installs are repo-agnostic.
