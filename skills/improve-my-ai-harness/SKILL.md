---
name: improve-my-ai-harness
description: Diagnose how to improve an AI coding IDE or agent harness by interviewing the user, identifying required capabilities, selecting a prompt, AGENTS.md, Agent Skill, slash command, workflow, hook, specialized agent, Agent Plugin, or a justified combination, and producing a paste-ready implementation prompt that invokes this plugin's relevant builder skills. Use when the desired harness improvement or mechanism is unclear; do not use when the artifact is already chosen and the user wants direct implementation.
license: CC-BY-4.0
---

# Improve My AI Harness

## Outcome

Turn a vague or recurring AI-IDE problem into an evidence-backed capability contract, the smallest sufficient harness architecture, and a paste-ready prompt for implementing it with the relevant builder skills in this plugin. Diagnose and propose only; do not create or modify the selected artifacts during this consultation.

## Workflow

1. Ground the problem before interviewing.

   Inspect any repository, harness configuration, transcripts, failed outputs, or existing prompts the user has placed in scope. Extract facts already supplied and keep a short decision ledger with:

   - target product, surface, and materially relevant version;
   - concrete failing or costly behavior and a representative example;
   - desired behavior and observable success criteria;
   - users, project or personal scope, and distribution needs;
   - invocation or event, frequency, and acceptable latency;
   - required context, tools, integrations, state, permissions, side effects, and approval boundaries;
   - need for judgment, deterministic enforcement, specialization, delegation, scheduling, or packaging;
   - existing harness artifacts that must be retained, replaced, or composed.

   Treat the user's proposed mechanism as a hypothesis unless they have already chosen it and asked for implementation. In that case, stop routing and direct the request to the matching builder skill.

   Completion: known facts and material unknowns are separated, and the diagnosis is tied to at least one real problem example rather than a feature wish alone.

2. Interview in short rounds until the capability contract is decisive.

   Ask one to three related questions per turn. Prefer questions about the observed failure, target surface, trigger, and success test before asking about artifact preferences. Do not ask for information already present in the conversation or inspectable files.

   After each answer, update the decision ledger, briefly reflect the new understanding when useful, and ask the next smallest question set. Continue across as many turns as necessary. Do not issue a final recommendation in the same turn as unresolved questions.

   The interview is complete only when all facts that could change the mechanism or permissions are known. At minimum, resolve:

   - what should improve, for whom, and how success will be observed;
   - where the behavior must run and what starts it;
   - whether it is one-off or recurring, stable or exploratory, deterministic or judgment-heavy;
   - what context, tools, integrations, persistence, and coordination it needs;
   - what it may read, edit, execute, or change externally, including approval points;
   - whether it must be shared, installed, packaged, or maintained across projects or products.

   If the user cannot supply a required fact, propose a low-risk way to collect evidence or a reversible assumption, then continue. Do not manufacture product capabilities or force a mechanism merely to end the interview.

   Completion: the problem can be stated as “for **scope**, when **trigger**, use **inputs and capabilities** to produce **outcome**, stop or ask before **boundary**, and verify with **test**.”

3. Select the smallest sufficient mechanism or layered combination.

   Read [the mechanism decision guide](references/mechanism-decision-guide.md). Score candidates against the capability contract, not against novelty. Prefer one mechanism when it covers the need without hidden duplication.

   Use a combination only when each layer owns a distinct responsibility. State the dependency order, such as repository context → reusable reasoning → explicit entry point → orchestration → distribution. Do not combine artifacts merely because a client can support them.

   Treat an Agent Plugin as packaging and distribution, not behavior by itself. Treat prompts and instruction files as guidance, not permission or security boundaries. If the target does not document a required artifact, select its supported alternative through the relevant builder skill or report that the requested capability is unsupported.

   It is valid to recommend gathering more evidence or making no harness change when the expected benefit is unproven. Never disguise CI, an MCP server, a permission policy, or a scheduler as one of the listed artifacts; identify it as a necessary complementary capability when applicable.

   Completion: every required capability has exactly one owning mechanism, every proposed artifact has a reason to exist, and target-product support is either verified by the downstream builder or explicitly left for it to verify.

4. Present the decision so it can be challenged.

   Return:

   1. **Problem and success contract** — concise statement of current failure, desired outcome, trigger, scope, and verification.
   2. **Required capabilities** — separate reasoning/context needs from tools, permissions, triggers, persistence, coordination, and distribution.
   3. **Recommendation** — primary mechanism and any necessary layers, with one responsibility per layer.
   4. **Why this fits** — map capabilities to mechanisms and explain why the closest alternatives are unnecessary or unsuitable.
   5. **Constraints and risks** — target support to verify, maintenance burden, approval boundaries, and unsupported assumptions.
   6. **Implementation prompt** — a self-contained, paste-ready prompt following step 5.

   Use calibrated language. Distinguish facts observed in the user's environment, user requirements, and inferences. Do not claim that a valid design is installed, enabled, or effective before implementation and testing.

   Completion: the user can confirm or dispute the recommendation from the stated evidence without reconstructing the interview.

5. Write the implementation prompt with exact skill routing.

   Name only the relevant installed builder skills from this plugin:

   - simple prompt → `new-prompt`
   - `AGENTS.md` → `new-agents-md`
   - Agent Skill → `new-skill`
   - slash command → `new-slash-command`
   - workflow → `new-workflow`
   - hook → `new-hook`
   - specialized agent → `new-agent`
   - Agent Plugin packaging → `new-plugin`

   For a combination, list the skills in implementation order and assign each a non-overlapping deliverable. Put `new-plugin` last when it packages artifacts created by other builders.

   Make the prompt self-contained: include the target product and scope, evidence, desired behavior, selected architecture, required inputs and capabilities, permissions and approval gates, artifacts to preserve, deliverables, and acceptance tests. Tell the implementing agent to inspect existing files and applicable repository instructions, verify current target support through the named builder skills, avoid undocumented substitutes, and report validation results. Use descriptive placeholders only for facts the user deliberately chose to defer.

   Do not tell the implementing agent to rerun this diagnostic interview unless the user asks to revisit the decision. End by inviting the user to revise or run the prompt; do not begin implementation implicitly.

   Completion: the prompt can be pasted into a clean agent session, explicitly invokes every required builder skill, contains no irrelevant builder, and has testable completion criteria.

## Safety

- This skill is read-only and advisory. Inspection of user-provided local context is allowed; artifact creation, configuration changes, installation, publication, schedules, external writes, and permission changes require a separate implementation request and the applicable approval boundary.
- Never recommend a prompt, Skill, `AGENTS.md`, command, or agent as a way to bypass sandboxing, permissions, policy, or human approval.
- Minimize privilege. Map every requested tool or integration to a required capability and place confirmation immediately before consequential external actions.
- Do not include credentials, private data, or transcript secrets in the implementation prompt. Refer to approved secret mechanisms and redact examples.

## Resources

- [Mechanism definitions, selection tests, combination rules, and builder mapping](references/mechanism-decision-guide.md)
