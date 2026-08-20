# {{WORKFLOW_TITLE}}

**Purpose:** {{ONE_SENTENCE_DESCRIPTION}}

**Run when:** Manually invoked via `/{{WORKFLOW_NAME}}` in Cascade chat.

**Inputs:** {{INPUTS_OR_PREREQUISITES}}

## Procedure

1. **Preconditions & Context:** Confirm the requested scope and inspect {{NAMED_EVIDENCE_OR_FILES}}. Stop if {{MISSING_PRECONDITION}}.
2. **Execute Primary Workflow:** {{PRIMARY_ORDERED_ACTIONS}}
3. **Optional Sub-workflows:** If {{CONDITION}}, call `/{{SUB_WORKFLOW_NAME}}`.
4. **Verification:** Verify {{OBSERVABLE_SUCCESS_CONDITION}}.
5. **Deliverable:** Return a concise summary of results, affected files, and next actions.

## Approval and Stop Conditions

- **Ask before:** {{IRREVERSIBLE_ACTION_SUCH_AS_DESTRUCTIVE_EDIT_OR_DEPLOY}}. Explain the impact and wait for explicit confirmation.
- **Stop and escalate if:** {{ERROR_CONDITION_OR_POLICY_CONFLICT}}.
- Never output secrets, passwords, or unredacted credentials.
