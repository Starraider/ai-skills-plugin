# {{agent-name}} — Google Agents CLI / ADK agent specification

<!-- This file documents the agent definition for a Google ADK agent managed
     through the Google Agents CLI (google-agents-cli). The agent logic lives
     in agent.py; this spec file captures the human-readable design contract.
     Commit alongside agent.py and pyproject.toml in the agent project root. -->

## Identity

- **Name:** {{agent-name}}
- **Responsibility:** {{one focused responsibility}}
- **ADK model:** {{gemini-2.0-flash / gemini-2.5-pro / etc.}}
- **Deployment target:** {{Cloud Run / Agent Runtime / local only}}

## Operating rules

1. Inspect {{inputs and relevant context}}.
2. {{required analysis or implementation behavior}}.
3. Return {{expected deliverable and format}}.
4. Stop when {{clear completion or escalation condition}}.

## Boundaries

- Do not {{excluded capability}}.
- Ask before {{external or destructive action}}.

## Tools and integrations

<!-- List only the ADK tools or MCP servers this agent actually requires. -->
- {{tool or integration}}

## Scaffold command

```bash
# From the workspace root, with agents-cli installed:
agents-cli create {{agent-name}}
```

## Evaluation

```bash
agents-cli eval --agent {{agent-name}} --test-set evals/{{agent-name}}_eval.json
```
