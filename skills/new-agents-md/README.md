# new-agents-md

`new-agents-md` creates or improves a focused `AGENTS.md` for Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca.

## What this skill solves

An `AGENTS.md` is a repository instruction file, not a generic prompt or a replacement for linting, tests, Skills, or native agent definitions. This skill inspects the actual project, writes only guidance that an agent needs, and accounts for each product's different loading behavior.

## Use when

- Creating a new project or personal `AGENTS.md` for one supported product.
- Refreshing an existing instruction file after build commands, conventions, or project structure changed.
- Splitting a monorepo's root instructions from genuinely different package-level instructions.
- Auditing an `AGENTS.md` for duplicated, stale, vague, unsafe, or unenforceable guidance.

Do not use it to create a reusable Skill, a custom agent, an Antigravity Rule, a Qoder subagent, or a ChatGPT custom GPT unless an `AGENTS.md` is specifically required.

## Expected outputs

- A plain-Markdown `AGENTS.md` placed at the correct project or personal location for the selected product.
- Concise, evidence-backed instructions: exact commands, non-obvious architecture and conventions, boundaries, and verification requirements.
- Product-specific discovery instructions and any limitation for a surface that does not document automatic loading.

## Context requirements

- A selected target: Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca.
- The intended scope: project, subdirectory, or personal guidance.
- Access to the repository or authoritative project facts. The skill asks when it cannot establish an important command, rule, or target surface.

For ChatGPT, state whether the work will run through a Codex-backed coding surface. A general ChatGPT Project, custom GPT, or Workspace Agent is not assumed to read local files automatically.

## Installation

Install the whole `new-agents-md/` directory as an Agent Skill. In this repository it is located at `skills/new-agents-md/`; compatible clients discover it through the enclosing Agent Plugin. See the repository [installation guidance](../../README.md#install-in-supported-ides-and-agents).

## Example prompts

- "Create a **Codex** repository-root `AGENTS.md`. Inspect this TypeScript monorepo and include only verified install, lint, test, and package-specific rules."
- "Audit our **OpenCode** `AGENTS.md`; remove anything repeated from CI or the formatter and retain the migration safety rules."
- "Create a **Zed** project `AGENTS.md` for the `apps/mobile` subtree. It has different test commands from the root; do not change the root file."
- "I use **ChatGPT Desktop with Codex** for this repository. Create the project guidance it will load, and tell me how to verify it."
- "We use **Orca** to launch Codex workers. Add only the root `AGENTS.md` instructions needed by the workers, not an Orca-only configuration."

## Validation

Run the structural validation from the repository root:

```bash
skills/new-skill/scripts/validate-skill.sh skills/new-agents-md \
  --clients codex,antigravity,opencode,qoder
```

Then follow the selected product's harmless discovery check in [target support and verification](references/target-support.md). Confirm that the agent can summarize the loaded guidance before relying on it for a real task.

## Sources

The target behavior and writing guidance were checked on 2026-08-20 using the primary documentation linked in [target support and verification](references/target-support.md), the open [AGENTS.md format](https://agents.md/), and Microsoft’s concise-instruction guidance for agent context files. The skill treats unverified product behavior—especially a generic ChatGPT file loader—as unsupported rather than inferring it.

## Related skills

- [`new-agent`](../new-agent/README.md) for a specialized product-native agent.
- [`new-skill`](../new-skill/README.md) for a reusable Agent Skill instead of always-on repository guidance.

## License

No standalone license is declared for this skill directory. Before external distribution, apply the license required by the containing repository.
