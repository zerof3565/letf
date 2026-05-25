---
description: >
  Agent helps with fast, verified English pronunciation.
---

Use the `en_sound` skill for this request.

Fast mode:
- Do not run `uv run websearch-pipeline` for ordinary pronunciation requests.
- Use the skill's fast verification order: cached/local CMUdict, then direct known dictionary or medical pages.
- Escalate to web search only when fast sources fail, conflict, or the user explicitly asks for research.

$ARGUMENTS
