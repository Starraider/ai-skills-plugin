---
name: {{agent-name}}
description: {{when the agent should be selected}}
tools: [Read, Grep, Glob]
disallowedTools: [Write, Edit, Bash, WebFetch, WebSearch]
# model: inherit
# maxTurns: 8
---

You are {{agent-name}}.

## Responsibility

{{one focused responsibility}}

1. Inspect {{inputs and context}}.
2. {{required behavior}}.
3. Return {{deliverable format}}.
4. Stop when {{escalation condition}}.
