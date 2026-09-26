---
name: improve-skill
description: Review and propose general-purpose updates to skills used in the current conversation. Use only when explicitly invoked at the end of a completed LLM conversation after skills or skill-guided tool calls were used. Correlate each skill's instructions with outcomes, failures, and reusable lessons learned; produce an approval-ready plan without modifying skills. Do not use for direct skill authoring; use new-skill instead.
license: CC-BY-4.0
---

# Improve Skill

## Outcome

Produce an evidence-backed, individually approvable plan for improving each Skill actually used in the current conversation. The plan identifies which source instructions, references, tool recommendations, validation steps, or documentation could be updated because of a problem or a reusable lesson learned during successful work, but it does not change any Skill.

## Workflow

1. Establish the review scope and evidence coverage.

   Review the current conversation only, plus Skill source files and artifacts the user has placed in scope. Inventory a Skill as used only when the conversation shows that the agent activated, read, or followed it. Do not count a Skill merely because it was listed as available.

   For every used Skill, record its name, source path or supplied text, invocation evidence, relevant task segment, and available evidence: instructions, tool calls, outputs, errors, retries, user corrections, final result, successful techniques, newly verified facts, and reusable observations. If the conversation was compacted or a source file is unavailable, state the exact coverage limit.

   Completion: every assessment is tied to a named Skill and the review distinguishes full source-and-trace evidence from trace-only evidence.

2. Correlate Skill guidance with execution and lessons learned.

   For each used Skill, identify consequential instructions and recommendations, especially suggested tool calls, validation commands, references, permission boundaries, and expected outputs. Compare them with what happened in the conversation.

   Treat a failed call as evidence of a Skill problem only when its failure plausibly follows from incorrect, stale, ambiguous, incomplete, or incompatible guidance. Do not blame the Skill for an unavailable service, denied permission, missing user authorization, malformed user input, or a one-off environment error unless its instructions should have anticipated or handled that condition.

   When a potentially stale external claim materially affected the result, verify it against a current primary source if available. Cite the source and date checked. Otherwise mark the claim unverified; do not guess that it is outdated.

   Also identify useful insights that arose even when the execution succeeded. Examples include a verified current fact, a repeatable technique that produced a better result, a decision rule that avoided unnecessary work, a missing validation that would increase confidence, or a recurring user need that falls within the Skill's existing scope. Treat an insight as a change candidate only when its evidence is credible, it would help comparable future uses, and it can be added without duplicating existing guidance or expanding the Skill's boundary.

   Completion: each issue or insight names the relevant instruction or gap, observed evidence, causal or applicability assessment, and confidence level.

3. Assess every used Skill independently.

   Evaluate the Skill's trigger boundary, factual accuracy, currentness, ordered workflow, tool guidance, safety and authorization boundaries, validation, references, and context cost. Check whether the instructions helped produce the result, caused wasted work, ambiguity, failed calls, skipped checks, or misleading claims, or omitted a reusable lesson that would improve future results.

   Classify each finding as one of: incorrect or stale information, failed or incompatible tool guidance, missing decision rule or recovery path, unclear scope or authorization boundary, missing validation, unnecessary context, reusable learned finding, or no actionable issue. Include a "no change proposed" assessment when the evidence does not justify a revision.

   Completion: every used Skill has its own assessment, including Skills that performed correctly.

4. Design only general-purpose improvements.

   Convert supported findings and reusable learned insights into the smallest portable improvement that would help comparable future conversations. Do not copy project names, private data, absolute paths, one-off APIs, or instructions tailored solely to this conversation. Prefer a clearer rule, a focused reference, a recovery condition, a validation step, or a deterministic helper only when the evidence supports it.

   Keep distinct changes separate. For each proposed change, assign a stable ID and state the target file, concise proposed edit, rationale, expected benefit, risk or trade-off, evidence, and a test that would show the change worked. If a source is unavailable, propose only an external recommendation; do not invent a patch for it.

   Completion: every proposal is general-purpose, traceable to evidence, and small enough for the user to authorize or reject independently.

5. Return a review plan and stop before implementation.

   Return these sections in order:

   1. **Review scope and limitations** - conversation coverage, evidence gaps, and any unverified claims.
   2. **Skill inventory** - used Skills only, with invocation and evidence status.
   3. **Per-Skill assessments** - one subsection per Skill containing observed outcome, reusable learned insights, findings, applicability or causal confidence, and either proposed changes or "no change proposed."
   4. **Approval queue** - one row per proposed change with ID, target, trigger type, summary, benefit, trade-off, and validation.
   5. **Next step** - ask the user to authorize specific proposal IDs. Do not edit a Skill, run a mutation, or bundle a release in this review.

   Completion: the user can accept, reject, or defer every change without reconstructing the conversation.

## Safety

- This Skill is advisory and read-only. Do not modify Skill files, plugin metadata, documentation, releases, installations, settings, or external systems.
- Do not expose secrets, private conversation content, tool arguments, or raw error output in the plan. Summarize or redact sensitive evidence.
- Use only evidence in the current conversation and explicitly scoped files. Ask for missing source material rather than implying a source-level review.
- Do not treat an invocation policy or tool recommendation as permission to perform a consequential action. A later implementation request must obtain authorization at the actual mutation boundary.
