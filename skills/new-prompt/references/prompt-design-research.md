# Prompt design research

Reviewed: 2026-07-03

This guide synthesizes current primary documentation from OpenAI, Anthropic, and Google. It uses provider-neutral defaults and calls out behavior that depends on a model family or API. Prompt design is empirical: treat every recommendation as a starting hypothesis and validate it on the actual model, snapshot, tools, and input distribution.

## Contents

1. [Start with the goal and output](#1-start-with-the-goal-and-output)
2. [Prompt components](#2-prompt-components)
3. [Structure for clarity and consistency](#3-structure-for-clarity-and-consistency)
4. [Reliability and controllability](#4-reliability-and-controllability)
5. [Length and level of detail](#5-length-and-level-of-detail)
6. [Iterative refinement](#6-iterative-refinement)
7. [Pitfalls and anti-patterns](#7-pitfalls-and-anti-patterns)
8. [Final audit](#8-final-audit)
9. [Primary sources](#9-primary-sources)

## 1. Start with the goal and output

A prompt is testable only when it defines both the transformation and the observable result. Start with a verb, the object being transformed, the intended audience or consumer, and the quality threshold.

| Output type | Define before drafting |
| --- | --- |
| Summary | Audience, source of truth, coverage, length, tone, evidence or citation rules, and treatment of uncertainty |
| Code generation | Language and version, repository context, interface, functional and non-functional requirements, allowed dependencies, tests, and delivery format |
| Debugging | Observed versus expected behavior, reproduction conditions, logs and code, diagnostic versus fix scope, and verification method |
| Data transformation | Input schema, output schema, field mapping, normalization rules, invalid-row policy, ordering, and completeness requirements |
| Step-by-step instructions | Reader skill level, prerequisites, environment, sequence, safety warnings, decision branches, and completion checks |
| Creative writing | Genre, audience, purpose, length, voice, required story elements, creative latitude, and prohibited content |
| Classification or evaluation | Label or scoring definitions, rubric, evidence rules, tie or abstention policy, and machine-readable output |
| Tool-using task | Desired end state, available tools, trigger conditions, permissions, confirmation boundaries, source handling, and stop conditions |

Separate the underlying goal from the requested artifact. “Analyze customer churn” is not yet an output contract; “return a five-row decision table ranking churn drivers, with evidence and confidence for each” is.

## 2. Prompt components

Not every prompt needs every component. Include a component when its omission creates a realistic ambiguity or failure mode.

| Component | Purpose | Essential when |
| --- | --- | --- |
| Objective | States the result and why it matters | Always |
| Context | Supplies domain facts, definitions, audience, environment, and source material | The model cannot infer them reliably |
| Role instruction | Selects relevant expertise, perspective, or tone | The role changes decisions or communication |
| Task specification | Defines the transformation and any consequential sequence | Always |
| Input contract | Names variable inputs, delimiters, types, and missing-data behavior | Inputs are dynamic, long, or potentially untrusted |
| Output contract | Defines format, schema, fields, length, tone, response language, and ordering | Always; exactness increases with downstream automation. Default response language to the primary input unless a fixed language is required |
| Constraints | Sets scope, permissions, exclusions, budgets, and quality boundaries | Violations would be costly or likely |
| Examples | Demonstrates format, edge cases, or nuanced judgment | Prose rules remain ambiguous or inconsistent |
| Evaluation criteria | Makes success measurable and enables self-checks and evals | Reliability matters or the task is repeated |
| Tool policy | Defines when and how tools may be called and how failures are handled | Tools or external actions are available |
| Uncertainty policy | Defines citation, abstention, assumptions, and conflict handling | Facts may be incomplete, conflicting, or consequential |

### Use roles precisely

“You are an expert” is usually too vague to change behavior. Name the relevant perspective and responsibility: “You are a PostgreSQL performance engineer reviewing query plans for correctness and latency.” Do not use a persona as a substitute for task instructions, evidence, or acceptance criteria.

### Write positive constraints

Say what the model should do, not only what it must avoid. “Use only claims supported by the supplied documents; mark unsupported fields as `null`” is more operational than “do not hallucinate.”

### Use examples deliberately

Examples are strong behavioral evidence. Keep them:

- representative of the real input distribution;
- correct and consistent with the written instructions;
- diverse enough to cover important edge cases;
- minimal enough that the model does not imitate irrelevant surface details.

Start zero-shot. Add one example for a simple format or decision boundary; add several only when observed failures justify them. Never let an example contradict a stated rule.

## 3. Structure for clarity and consistency

### Message hierarchy

When the API supports multiple message roles:

1. Put stable behavior, domain scope, global constraints, output rules, and tool policy in the system or developer message.
2. Put the concrete task, dynamic variables, and user-supplied or retrieved content in the user message or tool-result fields.
3. Never interpolate untrusted content into a higher-priority message.

System or developer messages improve consistency but do not guarantee security. Enforce authorization, data access, schema validation, and approvals in application code.

### Recommended component order

For a normal prompt:

1. Role and scope, if useful
2. Objective
3. Context and definitions
4. Task and ordered instructions
5. Constraints and uncertainty policy
6. Output format
7. Acceptance criteria
8. Examples, if needed
9. Variable input

For a long-context user message, put the documents or code before the final task and question. A practical hybrid is stable instructions in the privileged message, then `<source_material>...</source_material>` followed by `<task>...</task>` in the user message. This preserves instruction priority while putting the query after the large source block.

For prompt caching, keep stable instructions, examples, and tool definitions in a shared prefix and move request-specific content later. Exact caching behavior is provider-specific.

### Delimiters and placeholders

Use one consistent delimiter system:

- Markdown headings for human-edited prompts;
- XML-style tags for nested or mixed content;
- JSON fields when the application already serializes structured data.

Use descriptive placeholders such as `{{SOURCE_DOCUMENTS}}`, `{{TARGET_AUDIENCE}}`, and `{{MAX_WORDS}}`. Avoid vague placeholders such as `{{TEXT}}` when several text inputs exist. State whether a placeholder is required, optional, a list, or a schema.

Delimiters improve parsing but do not neutralize prompt injection. Label third-party content as untrusted data and keep it outside privileged instructions.

### Explicit steps and verbosity

Use numbered steps when:

- order matters;
- every step must be completed;
- intermediate artifacts require validation;
- a tool result controls the next action.

Do not prescribe a detailed reasoning path when the model can choose a better one. Specify checkpoints and evidence instead. Control response length with an observable budget such as “120–160 words,” “at most six bullets,” or an exact schema; “be concise” is weaker.

## 4. Reliability and controllability

### Grounding and unknowns

Tell the model:

- which sources are authoritative;
- whether outside knowledge is allowed;
- how to cite evidence;
- what to do when sources conflict;
- when to return `insufficient_information`, `null`, or a clarifying question.

For factual extraction and summarization, require each consequential claim to map to source text, an identifier, or a citation. A model self-check helps, but application-side verification remains necessary.

### Reasoning and chain-of-thought

Do not use “show your chain of thought” as a portable reliability technique.

- Current reasoning models perform internal reasoning and often expose an effort control. OpenAI advises against generic “think step by step” prompts for its reasoning models.
- Current Anthropic models use model-dependent adaptive thinking and effort controls; visible thinking may be summarized or omitted.
- Google recommends explicit plan, execute, and validate instructions for some Gemini workflows, while also recommending provider defaults for current Gemini sampling settings.

The portable pattern is:

1. select an appropriate reasoning or effort level;
2. give the model the goal, constraints, tools, and verification criteria;
3. ask it to reason internally;
4. request only a concise rationale, evidence trail, checklist, or final verification that users need.

For a classic non-reasoning model, explicit decomposition can improve a complex workflow, but test it. Distinguish “perform these verifiable stages” from “reveal private internal reasoning.”

### Stepwise decomposition and prompt chaining

Use one call when the transformation is cohesive and intermediate state has no separate consumer. Use multiple calls when you need to:

- validate or approve an intermediate artifact;
- retrieve information before drafting;
- isolate extraction from interpretation;
- generate, critique against a rubric, and revise;
- retry one stage without rerunning the full workflow;
- apply different models or permissions to different stages.

Validate the output between calls with schemas or deterministic checks. Do not pass unchecked free-form output directly into a privileged tool call.

### Structured outputs

When downstream code consumes the answer, prefer the provider's schema-constrained structured-output feature over prose that merely asks for JSON. Define:

- field types and enums;
- required versus nullable values;
- `additionalProperties: false` or its provider equivalent;
- refusal and error representation;
- units, date formats, and identifier semantics.

Still validate returned data in application code. Schema validity does not establish factual correctness.

### Tool calls

For each tool, define a clear name, when it should be used, parameter types and descriptions, required fields, and what the result means. Prefer strict schemas when available.

State:

- whether tool use is automatic, required, restricted, or forbidden;
- whether independent calls may run in parallel;
- how to handle missing parameters and tool errors;
- that the model must never invent tool results;
- which calls require user approval;
- which sources are trusted and how citations should be returned.

Keep permissions narrow. A prompt asking for confirmation is weaker than an application that technically requires approval before writes, purchases, deletions, or data disclosure.

### Model and generation settings

Settings are model-specific. Verify the selected model's current API reference before emitting exact parameters.

| Control | Starting guidance |
| --- | --- |
| Model class | Use a smaller model for simple, high-volume, well-defined tasks; use a stronger reasoning model for ambiguous, multi-step, agentic, or high-cost decisions |
| Model snapshot | Pin a production snapshot where supported; rerun evals before upgrades |
| Reasoning or effort | Low for simple extraction; medium for normal code and analysis; high for difficult debugging, planning, or agentic work |
| Temperature | Start with provider default; on classic sampling models, use roughly 0–0.3 for deterministic tasks and 0.7–1.0 for creative variation |
| `top_p` | Leave at default when tuning temperature; change one sampling control at a time |
| Frequency/presence penalties | Leave at default unless measured repetition or topic-diversity failures justify tuning; they are not correctness controls |
| Maximum output | Set enough room for the required schema or artifact, then enforce a prompt-level length contract |
| Seed | Useful for reducing variance where supported, but not a determinism guarantee |
| Structured output | Enable strict schema adherence for machine-consumed data when supported |
| Tool choice | Use automatic choice when tools are optional, required or forced choice when the task cannot succeed without a specific tool |

Current Gemini 3.x guidance strongly recommends retaining default sampling parameters because manual changes can degrade complex reasoning. Current OpenAI and Anthropic reasoning families increasingly use reasoning or effort controls rather than classic sampling as the main quality/latency tradeoff. These details will change; the task template should label them as provider-dependent.

## 5. Length and level of detail

Use the shortest prompt that preserves the contract.

### Be concise when

- the task is common and low risk;
- inputs and desired output are obvious;
- the model is a capable reasoning model;
- one clear output example replaces many rules;
- the request is interactive and easy to correct.

### Add detail when

- domain terms or policies are not standard;
- output feeds automation;
- the model must follow an exact schema or style;
- edge cases have costly consequences;
- several documents, tools, or permission boundaries are involved;
- a smaller model needs more explicit guidance;
- observed eval failures reveal a specific ambiguity.

Large context windows are capacity, not a target. Remove irrelevant documents, deduplicate policies, retrieve only useful passages, and summarize stable background where fidelity permits. More context can add conflicts, latency, cost, and distraction.

Avoid repeating the same rule in several forms. If a critical rule must appear in both a privileged message and a final task transition, keep the wording consistent.

## 6. Iterative refinement

### Build the test set first

Collect representative production-like inputs before polishing language. Include:

- normal cases;
- difficult but valid cases;
- missing and conflicting data;
- malformed inputs;
- adversarial or injection-like content when tools or retrieved documents are involved;
- cases where the correct answer is abstention.

Create a baseline using the current prompt or a minimal zero-shot prompt. Pin the model snapshot and settings for fair comparison.

### Analyze errors

Classify failures before editing:

- goal misunderstanding;
- missing context;
- instruction conflict;
- wrong format or schema;
- unsupported claim;
- tool-selection or tool-argument error;
- over-refusal or under-refusal;
- excess length;
- latency or cost regression.

Change the smallest general rule that addresses the failure. Do not add a phrase tailored to one test case unless it represents a real class of inputs.

### Run automated A/B tests

Compare candidate and baseline on the same held-out cases. Randomize presentation for human or model-judge pairwise review, repeat stochastic runs, and report sample size and variance. Change one major prompt or setting dimension at a time so the result remains interpretable.

Use a development set for iteration and a held-out set for final selection. Calibrate model judges against human labels, especially for nuanced quality or safety criteria. Prefer code-based grading for schemas, exact fields, calculations, and executable tests.

### Track metrics

Choose metrics tied to the task:

| Dimension | Example metric |
| --- | --- |
| Task fidelity | Exact match, unit-test pass rate, field-level F1, rubric pass rate |
| Grounding | Unsupported claims divided by total claims; responses containing at least one unsupported consequential claim |
| Format | Schema-valid response rate; required-field completeness |
| Consistency | Pass-rate variance across repeated runs |
| Tool behavior | Correct tool-selection rate, valid-argument rate, unnecessary-call rate, tool-error recovery |
| Safety | Unauthorized-action rate, injection-resistance pass rate, correct-abstention rate |
| Human quality | Blind pairwise win rate, calibrated Likert score, edit distance to accepted output |
| Latency | Median and p95 end-to-end response time; time to first useful token |
| Usage and cost | Input, cached, output, and reasoning tokens; tool calls; cost per successful task |

Do not optimize accuracy alone if latency or cost makes the prompt unusable. Define release thresholds and regressions that block deployment.

## 7. Pitfalls and anti-patterns

| Anti-pattern | Failure | Better approach |
| --- | --- | --- |
| “Help me with this” | No observable goal or output | State the transformation, audience, output, and success criteria |
| Vague expert role | Adds confidence without operational guidance | Name the relevant domain responsibility and evidence standard |
| Role-only prompt | Leaves task and format unspecified | Treat role as optional context, not the contract |
| Implicit assumptions | Produces plausible but wrong details | Provide facts, expose placeholders, or define abstention |
| Negative-only rules | Tells the model what to avoid but not what to produce | Pair each prohibition with desired behavior |
| Overly permissive tools | Allows unnecessary or harmful actions | Restrict tools, parameters, approvals, and stop conditions |
| Untrusted data in a privileged message | Gives injected text high instruction priority | Put it in user or tool-result data and label it untrusted |
| “Return JSON” without a schema | Produces inconsistent keys and types | Use strict structured outputs and application validation |
| Generic chain-of-thought demand | Can waste tokens or conflict with reasoning models | Use effort controls, stage criteria, and concise verification |
| Tuning temperature and `top_p` together | Makes effects hard to attribute | Keep defaults, then tune one supported control |
| Huge prompt with repeated rules | Adds cost, conflicts, and attention dilution | Keep one authoritative statement per rule |
| Too many similar examples | Encourages superficial imitation and increases tokens | Use a small, diverse, error-driven set |
| One golden test case | Overfits prompt wording | Use representative, edge, adversarial, and held-out cases |
| Model self-check as the only validator | Lets the same failure survive review | Add deterministic, human, or independently calibrated grading |
| Prompt as security control | Cannot enforce permissions or prevent all injection | Enforce authorization and validation outside the model |

## 8. Final audit

Before shipping a prompt, verify:

- A new reader can identify the exact task and output.
- Every placeholder is named, delimited, and described.
- Instructions and examples agree.
- The model knows what information is authoritative.
- Missing, conflicting, and unsupported data have defined behavior.
- Output length, shape, and verbosity are observable.
- Tool use has schemas, permissions, error handling, and stop conditions.
- Untrusted content cannot enter privileged instructions.
- Recommended settings exist for the selected model.
- Acceptance criteria can be graded on representative cases.

## 9. Primary sources

The synthesis above is based on these current official references:

- [OpenAI: Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) — message roles, prompt structure, model-specific prompting, version pinning, and evals.
- [OpenAI: Reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices) — direct prompting, delimiters, zero-shot versus few-shot, and avoiding generic chain-of-thought prompts for reasoning models.
- [OpenAI: Function calling](https://developers.openai.com/api/docs/guides/function-calling) and [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs) — strict schemas, tool choice, and machine-readable responses.
- [OpenAI: Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — task-specific evals, graders, representative data, and continuous evaluation.
- [OpenAI: Safety in building agents](https://platform.openai.com/docs/guides/agent-builder-safety) — untrusted variables, prompt injection, structured data flow, approvals, and trace grading.
- [OpenAI: Prompt caching](https://platform.openai.com/docs/guides/prompt-caching) — stable prefixes, latency, and token-cost considerations.
- [Anthropic: Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) — clear instructions, examples, XML structure, long context, tool use, reasoning, and prompt chaining.
- [Anthropic: Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) — measurable criteria, task-specific cases, grading methods, latency, and price.
- [Anthropic: Effort](https://platform.claude.com/docs/en/build-with-claude/effort) and [Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) — model-dependent reasoning controls and token tradeoffs.
- [Anthropic: Mitigate jailbreaks and prompt injections](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks) — handling third-party content and tool results as untrusted data.
- [Google: Prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) — current Gemini structure, long-context ordering, verbosity, chaining, structured output, and sampling guidance.
- [Google Cloud: System instructions](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/system-instruction-introduction) — personas, context, format, tone, and persistent behavior.
- [Google Cloud: View and interpret evaluation results](https://cloud.google.com/vertex-ai/generative-ai/docs/models/eval-python-sdk/view-evaluation) — pointwise, pairwise, computation-based metrics, means, variance, and win rates.
