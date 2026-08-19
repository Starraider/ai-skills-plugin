# Mechanism decision guide

Use this guide only after the interview has produced a capability contract. A mechanism is an implementation choice, not the user's problem statement.

## Candidate tests

| Mechanism | Select when | Do not select merely because | Builder skill |
| --- | --- | --- | --- |
| Simple prompt | The task is one-off, exploratory, or not stable enough to maintain; all needed context can be supplied at invocation. | It is the quickest artifact to write. | `new-prompt` |
| `AGENTS.md` | Stable, evidence-backed repository or subtree facts, commands, conventions, and boundaries should guide many coding tasks. | The user wants a persona, tool permission, executable check, or procedure unrelated to the repository. | `new-agents-md` |
| Agent Skill | Reusable reasoning, domain knowledge, conditional instructions, templates, references, or scripts should load on demand. | A persistent rule, deterministic event reaction, or one-off task happens to contain instructions. | `new-skill` |
| Slash command | A user should explicitly start a compact, stable task or short procedure with useful arguments and a reviewable output. | The user used the word “command,” or the task needs automatic activation, long-lived ownership, or complex orchestration. | `new-slash-command` |
| Workflow | A repeatable multi-step process, handoff, schedule, API/event trigger, approval path, or orchestration has an observable output and stop conditions. | Any reusable checklist is called a workflow; a Skill or command may be smaller. | `new-workflow` |
| Hook | A documented lifecycle event must trigger fast, deterministic, bounded, and testable observation, transformation, or blocking. | The desired behavior requires model judgment or the target has no event at the required boundary. | `new-hook` |
| Specialized agent | A standing specialist needs a distinct responsibility, tool and permission boundary, context, model/profile, ownership, or delegation role. | A persona sounds attractive or reusable instructions would be sufficient. | `new-agent` |
| Agent Plugin | Multiple portable Skills or MCP servers need one reusable, validated distribution package. | One artifact needs behavior; a plugin is a container, not an autonomous capability. | `agent-plugin-builder` |

## Capability-to-mechanism signals

- **Stable repository context:** prefer `AGENTS.md`; use a Skill only for an invoked procedure or deeper conditional knowledge.
- **Reusable judgment:** prefer a Skill; use an agent when it also needs durable specialization, a separate capability boundary, or delegation.
- **Explicit convenience:** prefer a slash command when the target has a native form; otherwise let `new-slash-command` choose the documented alternative.
- **Automatic deterministic reaction:** prefer a hook only for a documented event and supported effect.
- **Time, external API, repository event, or multi-agent handoff:** prefer the target's workflow, automation, CI, or orchestration surface rather than pretending it is a hook.
- **New tool or data access:** the missing capability may be an MCP server, app, or native integration. An agent or prompt cannot create access. Package a portable MCP server in an Agent Plugin only when distribution is also required.
- **Standing allow/ask/deny behavior:** use the target's permission policy. Prose artifacts may document the rule but do not enforce it.
- **Cross-project distribution:** package reusable Skills or MCP servers in an Agent Plugin; do not put client-owned hooks, commands, permissions, or agents into the portable core unless the applicable specification documents them.

## Combination rules

Use multiple mechanisms only when the capability contract contains separable responsibilities. Common valid layers include:

1. `AGENTS.md` supplies stable repository facts to all coding work.
2. A Skill supplies reusable, context-dependent reasoning or a procedure.
3. A slash command supplies a manual entry point only when the target needs a distinct native shortcut and it does not duplicate the Skill.
4. A hook supplies a deterministic guard or observation at a documented lifecycle boundary.
5. A workflow coordinates steps, agents, approvals, schedules, or external triggers.
6. A specialized agent owns a durable role and its least-privilege tool boundary.
7. An Agent Plugin packages portable Skills and MCP servers after their behavior is designed and validated.

Reject a combination when two artifacts restate the same instructions, when one exists only to invoke another without user benefit, or when packaging is proposed without a distribution requirement.

## Tie-breakers

When several candidates appear viable, prefer in order:

1. documented support in the selected target;
2. smallest authority and fewest side effects;
3. simplest artifact that meets the success test;
4. lower maintenance and duplication;
5. clearer discovery, observability, and rollback;
6. portability only when the user actually needs multiple targets.

If evidence remains evenly balanced, recommend a reversible pilot with the smaller mechanism and define what result would justify adding another layer.

## Implementation-prompt mapping

The handoff prompt must explicitly name each selected builder skill and its deliverable. Examples:

- “Use the installed `new-skill` Agent Skill to create and validate the reusable review procedure described below.”
- “Use `new-agents-md` first for repository-wide facts, then `new-skill` for the invoked migration-review procedure. Do not duplicate instructions between them.”
- “Use `new-hook` to verify that Codex exposes the required pre-action event and implement the deterministic guard. If unsupported, report the limitation rather than inventing configuration.”
- “Use `new-skill` to build the portable capability, then `agent-plugin-builder` to add it to a validated Agent Plugin for distribution.”

Names are portable references to installed skills. The target client may expose them through `$name`, `/name`, `@name`, or automatic discovery; do not hard-code one invocation syntax unless the target requires it.
