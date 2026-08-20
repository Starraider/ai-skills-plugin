# improve-my-ai-harness

`improve-my-ai-harness` diagnoses how an AI coding IDE or agent harness should be extended before anyone commits to the wrong artifact. It interviews the user over multiple short rounds, derives the required capabilities, recommends the smallest sufficient mechanism or combination, and produces a ready-to-paste implementation prompt that names this plugin's matching builder skills.

## What this skill solves

AI harness ideas often begin as “I need an agent” or “make this automatic,” even when the actual need is stable repository context, a reusable reasoning procedure, a deterministic event guard, or just a better prompt. This skill separates the problem from the proposed mechanism and makes the choice testable.

It evaluates these options:

- a simple prompt;
- an `AGENTS.md` instruction file;
- an Agent Skill;
- a slash command;
- a workflow;
- a hook;
- a specialized agent;
- an Agent Plugin;
- a justified combination with one responsibility per layer.

## Use when

- You know what keeps going wrong in an AI IDE but not which extension mechanism would fix it.
- You are choosing among prompts, persistent instructions, skills, commands, workflows, hooks, agents, and plugins.
- You want to stress-test a proposed harness architecture before implementing it.
- You need a handoff prompt that routes implementation to this plugin's relevant builder skills.

Do not use it when the artifact is already chosen and the request is to create or edit that artifact. Invoke the matching builder skill directly instead.

## Expected outputs

- A problem and success contract grounded in representative evidence.
- A capability inventory covering context, judgment, triggers, tools, permissions, persistence, coordination, and distribution.
- One recommended mechanism or a minimal layered combination, with rejected alternatives explained.
- A self-contained implementation prompt naming the exact downstream builder skills and measurable acceptance tests.

The consultation does not create, install, enable, or publish the recommended artifacts.

## Context requirements

Start with the observed problem or desired improvement. Useful context includes the target IDE/product, a failed transcript or output, repository files, existing harness configuration, intended users and scope, trigger, side effects, and success criteria. The skill asks only for material facts it cannot inspect or infer safely.

Because the interview is intentionally iterative, expect one to three focused questions per turn until the decision would no longer change with another answer.

## Installation

Install this complete directory, including `references/` and `evals/`, alongside the other skills from this plugin. Common project and user locations are:

| Client | Project scope | User scope |
| --- | --- | --- |
| Antigravity | Install the complete plugin at `.agents/plugins/ai-skills-plugin/` | Install the complete plugin at `~/.gemini/config/plugins/ai-skills-plugin/` |
| Codex | `.agents/skills/improve-my-ai-harness/` | `~/.agents/skills/improve-my-ai-harness/` |
| Zed | `.agents/skills/improve-my-ai-harness/` | `~/.agents/skills/improve-my-ai-harness/` |
| OpenCode | `.opencode/skills/improve-my-ai-harness/` or `.agents/skills/improve-my-ai-harness/` | `~/.config/opencode/skills/improve-my-ai-harness/` or `~/.agents/skills/improve-my-ai-harness/` |
| Qoder | `.qoder/skills/improve-my-ai-harness/` | `~/.qoder/skills/improve-my-ai-harness/` |
| Orca | `.agents/skills/improve-my-ai-harness/` | `~/.agents/skills/improve-my-ai-harness/` |

For ChatGPT, upload this skill directory with all supporting files through the Skills interface. The downstream builder skills referenced by the implementation prompt must also be installed and available.

## Example prompts

- “My coding agent keeps missing our migration rules and gives inconsistent reviews. Interview me and decide what I should add to the harness.”
- “I think I need an agent that formats every changed file, but I am not sure. Help me choose between a hook, workflow, command, or skill.”
- “Inspect the existing AI configuration in this repository, ask me whatever cannot be learned from the files, and propose the smallest setup that gives the team a repeatable pre-release review.”
- “We want to distribute the same review capability across several projects. Determine whether that needs a Skill, an Agent Plugin, or both, then give me an implementation prompt.”

## Validation

From the plugin root, run:

```bash
skills/new-skill/scripts/validate-skill.sh skills/improve-my-ai-harness --strict-portable
skills-ref validate skills/improve-my-ai-harness
python3 skills/agent-plugin-builder/scripts/validate_agent_plugin.py . --strict
```

Behavioral cases are maintained in [`evals/evals.json`](evals/evals.json). They cover iterative discovery, a layered recommendation, a deterministic hook decision, and a request that should route directly to another builder.

## Related skills

- [`new-prompt`](../new-prompt/README.md) implements a selected simple prompt.
- [`new-agents-md`](../new-agents-md/README.md) implements selected repository instructions.
- [`new-skill`](../new-skill/README.md) implements a selected Agent Skill.
- [`new-slash-command`](../new-slash-command/README.md) implements a selected explicit command or documented target alternative.
- [`new-workflow`](../new-workflow/README.md) implements a selected workflow or documented target alternative.
- [`new-hook`](../new-hook/README.md) implements a selected event hook or documented target alternative.
- [`new-agent`](../new-agent/README.md) implements a selected specialized agent.
- [`agent-plugin-builder`](../agent-plugin-builder/README.md) packages and validates selected portable components.

## License

Licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
