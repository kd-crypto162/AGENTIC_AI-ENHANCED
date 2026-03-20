## Assignment 2 — Agentic AI-Enhanced DevOps Automation

### Repository

This repository contains:

- A Python **agent** that classifies **CI/CD failures from logs**
- A max-5-page **architecture + reflection report** (in `report/`)
- Evidence notes for screenshots/demos (in `evidence/`)

### Agent selection (meets requirement)

The agent performs:

1. **Planning step** (decides what to search for in logs)
+2. **Tool call step** (searches the provided log text for failure markers)
3. **Self-reflection step** (checks consistency of the classification)

Then it prints a **final answer**: failure category + recommended fix.

Run it with:

```bash
python -m agent.run_agent --log-file agent/sample_ci_log.txt
```

