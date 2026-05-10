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

[Company README →](./claude-for-financial-services/README.md)

## License

This repository's wrapper content (top-level README, structure) is MIT-licensed. Individual companies have their own licenses — see each company's `LICENSE` file.

## Contributing

This is a personal catalog. If you'd like to publish your own community-ported or original Paperclip companies, the cleanest path is your own `<your-username>/companies` repo — `companies.sh` installs are repo-agnostic.
