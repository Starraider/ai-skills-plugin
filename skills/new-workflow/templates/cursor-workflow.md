# {{WORKFLOW_TITLE}}

**Purpose:** {{ONE_SENTENCE_DESCRIPTION}}

**Run when:** Explicitly invoked via `/{{WORKFLOW_NAME}}` in Cursor Chat, Agent, or Composer.

**Inputs:** {{INPUTS_OR_PREREQUISITES}}

## Procedure

1. **Preconditions & Context:** Confirm {{PRECONDITIONS}} and inspect {{FILES_OR_SYMBOLS}}. Stop if {{MISSING_PRECONDITION}}.
2. **Execute Ordered Steps:**
   - Step 1: {{STEP_1_DETAILS}}
   - Step 2: {{STEP_2_DETAILS}}
   - Step 3: {{STEP_3_DETAILS}}
3. **Verification:** Confirm {{OBSERVABLE_SUCCESS_CRITERIA}} before reporting completion.
4. **Deliverable:** Return a concise summary report with findings, diffs, or structured deliverable.

## Boundaries and Approvals

- **Approval Gate:** Stop and ask before {{DESTRUCTIVE_EDIT_TERMINAL_COMMAND_OR_EXTERNAL_WRITE}}.
- **Stop Condition:** Exit and escalate if {{UNCERTAINTY_OR_CONFLICT}}.
- Never output secrets, API keys, or unredacted tokens.
