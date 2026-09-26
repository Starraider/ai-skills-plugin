# improve-skill

Review the Skills used in a completed LLM conversation and propose narrowly scoped, general-purpose updates. It learns from failures and from useful discoveries made during successful work. It is a maintenance review, not an editor: it produces a plan for approval and never changes a Skill itself.

## What this skill solves

Long conversations with a LLM can reveal defects that static review misses. A Skill may point to a stale source, recommend a tool call that no longer works, omit a recovery path, use too much context, or leave an authorization boundary unclear. They can also reveal a verified fact, a reliable technique, or a useful decision rule that belongs in a Skill even though nothing failed. This Skill evaluates every used Skill separately and turns supported findings and reusable lessons into an approval queue.

## Use when

- You have finished a substantial conversation in which one or more Skills were activated or followed.
- You want to review tool failures, user corrections, validation gaps, or unexpectedly poor results before updating those Skills.
- A successful conversation produced a verified fact, repeatable technique, or decision rule that could help the same Skill work better next time.
- You want a maintainable improvement plan rather than an immediate patch.

Do not use it to create or directly edit a Skill. Use `new-skill` for that work after approving a proposal. Do not use it in the middle of a task merely because a Skill is available in the session.

## Expected outputs

- A coverage statement that distinguishes observed evidence from unavailable or compacted history.
- An inventory of Skills actually used in the conversation.
- A separate evidence-based assessment for every used Skill, including reusable learned insights and an explicit "no change proposed" result when warranted.
- A prioritized approval queue with independent proposal IDs, proposed file targets, benefits, risks, and validation tests.

## Context requirements

Invoke the Skill in the same conversation after the work is complete so it can inspect the relevant trace. For source-level findings, the Skill also needs the applicable `SKILL.md` and linked resources in local scope. It can make a trace-only assessment when the source is unavailable, but it must label that limitation and must not invent an edit.

The review uses only the current conversation and files the user has placed in scope. It summarizes sensitive evidence instead of reproducing secrets, private content, or raw tool arguments.

## Installation

This repository packages the Skill at `skills/improve-skill/`, where compatible Agent Plugin clients discover it. For an individual installation, copy the complete `improve-skill` directory into the target client's documented Skill location; see the repository's [skill installation guide](../../skill-installation.md).

Codex reads the included `agents/openai.yaml` companion file. Keep that file with the Skill to preserve its manual-only Codex policy.

## Invocation

In Codex, invoke it explicitly at the end of the conversation:

```text
$improve-skill
```

The bundled `agents/openai.yaml` disables implicit invocation in Codex. The portable Agent Skills standard does not provide an equivalent cross-client switch. In another client, invoke it explicitly and configure that client's supported manual-only policy if one exists.

## Example prompts

- "$improve-skill. Review the Skills used in this conversation and propose changes only."
- "$improve-skill. A tool call recommended by one of the Skills failed. Determine whether the guidance, environment, or authorization caused it, then give me an approval queue."
- "$improve-skill. The work succeeded, but we learned a reusable technique. Decide whether it belongs in the Skill and propose a general update if it does."
- "$improve-skill. Audit the Skills we used to prepare this report. Keep recommendations reusable across projects and do not edit anything."

## Validation

From the plugin root, run:

```bash
bash skills/new-skill/scripts/validate-skill.sh skills/improve-skill --strict-portable
skills-ref validate skills/improve-skill
python3 skills/new-plugin/scripts/validate_agent_plugin.py . --strict
```

Exercise the representative, edge-case, and near-miss cases in `evals/evals.json`. A successful run must identify used Skills correctly, separate a genuine guidance issue from an environmental failure, recognize a supported reusable insight from successful work, preserve the no-edit boundary, and give every proposed change its own approval ID.

## Related skills

- [`new-skill`](../new-skill/README.md) creates or revises a Skill after the user approves an `improve-skill` proposal.
- [`new-plugin`](../new-plugin/README.md) validates or packages the containing Agent Plugin when that work is requested.

## License

This Skill is licensed under [CC BY 4.0](../../LICENSE).
