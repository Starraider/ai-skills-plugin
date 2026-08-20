---
description: {{ONE_LINE_WORKFLOW_DESCRIPTION}}
# name: {{OPTIONAL_DISPLAY_NAME}}          # overrides the filename-derived invocation name
agent: agent                               # enables multi-step autonomous agentic workflow
# argument-hint: "{{ARGUMENT_HINT}}"       # placeholder displayed in the chat input box
# tools:                                   # list tools available to this workflow
#   - search
#   - codebase
#   - fetch
---

# {{WORKFLOW_TITLE}}

**Purpose:** {{ONE_SENTENCE_DESCRIPTION}}

## Inputs and Prerequisites

- {{INPUTS_OR_PREREQUISITES}}

## Procedure

1. **Inspect Evidence:** Inspect {{NAMED_FILES_OR_CONTEXT}}. Stop if {{MISSING_PRECONDITION}}.
2. **Execute Steps:**
   - {{STEP_1}}
   - {{STEP_2}}
   - {{STEP_3}}
3. **Verify:** Check {{OBSERVABLE_SUCCESS_CONDITION}}.
4. **Deliverable:** Produce {{EXPECTED_OUTPUT_FORMAT}}.

## Boundaries and Approvals

- Ask for confirmation before {{IRREVERSIBLE_ACTION_SUCH_AS_EXTERNAL_WRITE_OR_DEPLOY}}.
- Stop and escalate if {{UNRESOLVED_CONFLICT_OR_AMBIGUITY}}.
