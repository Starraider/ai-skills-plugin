---
description: {{when the agent should be selected}}
mode: subagent
# model: {{optional-provider/model}}
permission:
  read: allow
  glob: allow
  grep: allow
  edit: deny
  bash: deny
  websearch: deny
---

You are {{agent-name}}.

## Responsibility

{{one focused responsibility}}

1. Inspect {{inputs and context}}.
2. {{required behavior}}.
3. Return {{deliverable format}}.
4. Stop when {{escalation condition}}.
