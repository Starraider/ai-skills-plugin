# {{workflow-name}} — Google Agents CLI / ADK Multi-Step Workflow Specification

<!-- This specification defines a multi-step agentic workflow implemented with
     the Google Agent Development Kit (ADK) and managed via google-agents-cli.
     Commit alongside agent.py and pyproject.toml in the agent project root. -->

## Identity and Trigger

- **Workflow Name:** {{workflow-name}}
- **Responsibility:** {{one-sentence description of the multi-step automated process}}
- **Trigger:** {{schedule (cron) / PubSub event / API trigger / CLI command: agents-cli run}}
- **ADK Model:** {{gemini-2.0-flash / gemini-2.5-pro}}
- **Deployment Target:** {{Cloud Run / Google Cloud Agent Platform / Local}}

## Multi-Step Workflow Pipeline

1. **Input Ingestion & Validation:** Inspect {{INPUT_DATA_OR_EVENT}} and validate preconditions.
2. **Analysis & Step Execution:**
   - Sub-task A: {{DESCRIPTION_OF_ANALYSIS_OR_TOOL_INVOCATION}}
   - Sub-task B: {{DESCRIPTION_OF_TRANSFORMATION_OR_SYNTHESIS}}
3. **Verification & Guardrails:** Check outputs against {{POLICY_OR_EVALUATION_CRITERIA}}.
4. **Deliverable Generation:** Emit {{STRUCTURED_REPORT_OR_ARTIFACT}}.

## Tools and MCP Integrations

- {{ADK_TOOL_OR_MCP_SERVER_1}}
- {{ADK_TOOL_OR_MCP_SERVER_2}}

## Boundaries and Approvals

- Require human approval before {{EXTERNAL_WRITE_MESSAGE_OR_DEPLOYMENT}}.
- Stop and log alert if {{ANOMALY_OR_PRECONDITION_FAILURE}}.

## Scaffold and Verification

```bash
# Scaffold the ADK project
agents-cli create {{workflow-name}}

# Run evaluation suite
agents-cli eval --agent {{workflow-name}} --test-set evals/{{workflow-name}}_eval.json

# Local test execution
agents-cli run --agent {{workflow-name}}
```
