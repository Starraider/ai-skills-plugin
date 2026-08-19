# new-prompt

`new-prompt` turns a desired outcome into a ready-to-use prompt or message set for current large language models. It makes the task, inputs, output format, constraints, model controls, and success criteria explicit without adding unnecessary prompt text.

## What this skill solves

Vague requests often leave a model to infer the audience, source of truth, output shape, edge-case behavior, and definition of success. This skill resolves those gaps, separates trusted instructions from variable data, and produces a prompt that can be tested and refined.

## Use when

- Creating a prompt from a goal for code, data, summaries, procedures, creative work, evaluation, or tool use.
- Repairing a prompt that is ambiguous, inconsistent, unreliable, too verbose, or difficult to evaluate.
- Converting one large prompt into system/developer and user messages or a stepwise prompt chain.
- Adding output schemas, examples, model-setting guidance, or an evaluation plan.

For Stitch-specific UI generation prompts, use a Stitch-focused Skill when one is installed; this package does not include one.

## Expected outputs

- A paste-ready user prompt, plus a system or developer message when the runtime supports it.
- Visible placeholders for inputs the user will supply later.
- Conditional model settings that do not assume every provider supports the same parameters.
- Optional assumptions, evaluation criteria, and test guidance for production use.
- By default, prompts require the target model to answer in the same language as the primary input or source material, and this skill's delivery text follows the user's request language unless specified otherwise.

## Context requirements

The only required input is the desired goal. Results improve when the user also provides the target model or provider, audience, source material, output format, constraints, examples, available tools, and success criteria. Missing non-blocking details become explicit assumptions or descriptive placeholders.

## Installation

Install this directory in a skill location discovered by the target client:

| Client | Project scope | User scope |
| --- | --- | --- |
| Claude Code | `.claude/skills/new-prompt/` | `~/.claude/skills/new-prompt/` |
| Codex | `.agents/skills/new-prompt/` | `~/.agents/skills/new-prompt/` |
| Cursor | `.cursor/skills/new-prompt/` or `.agents/skills/new-prompt/` | `~/.cursor/skills/new-prompt/` or `~/.agents/skills/new-prompt/` |
| Antigravity | `.agents/skills/new-prompt/` | `~/.gemini/config/skills/new-prompt/` |
| OpenCode | `.opencode/skills/new-prompt/` or `.agents/skills/new-prompt/` | `~/.config/opencode/skills/new-prompt/` or `~/.agents/skills/new-prompt/` |
| Qoder | `.qoder/skills/new-prompt/` | `~/.qoder/skills/new-prompt/` |

The core skill is portable. Exact support for system/developer messages, reasoning controls, sampling parameters, structured outputs, and tool choice depends on the selected model API.

## Example prompts

- "Write a prompt that makes an LLM turn a product specification into a TypeScript implementation and tests. It must return a unified diff and flag missing requirements instead of guessing."
- "My support-ticket summarizer keeps inventing causes. Rebuild the prompt so it uses only the supplied ticket history and returns strict JSON with evidence IDs."
- "Create a reusable prompt for writing maintenance procedures for junior technicians. Include prerequisites, safety warnings, verification steps, and placeholders for the machine model."
- "Turn this rubric into a deterministic evaluator prompt that compares two answers, cites evidence for every score, and emits schema-valid JSON."

## Guidance

- [Prompt-design research](references/prompt-design-research.md) covers goals, components, structure, reliability, prompt length, iteration, metrics, and anti-patterns.
- [Annotated prompt templates](references/prompt-templates.md) provide eight task-specific templates with placeholders and recommended settings.

The research was reviewed on 2026-07-03 against current primary documentation from OpenAI, Anthropic, and Google.

## Validation

From this directory, run:

```bash
../new-skill/scripts/validate-skill.sh . \
  --clients claude,codex,cursor,antigravity,opencode,qoder

python3 -m json.tool evals/evals.json >/dev/null
```

Also confirm all relative links in `SKILL.md` and `README.md` resolve.

## Related skills

- A separately installed Stitch-focused Skill should own Stitch-specific UI prompt enhancement.
- [`new-skill`](../new-skill/) owns creation and validation of agent skills rather than task prompts.

## License

No standalone license is declared for this skill directory. Before external distribution, add or document the license required by the containing repository.
