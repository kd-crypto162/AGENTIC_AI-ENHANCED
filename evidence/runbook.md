## Assignment 2 Evidence Runbook

### Agent demo screenshot checklist

When you run the agent, screenshot the console output showing:

- `--- Planning step ---`
- `--- Tool call step (search_log) ---`
- `--- Self-reflection step ---`
- `--- Final answer (classification) ---`

### Run command

```bash
cd assignment-2
pip install -r requirements.txt
python -m agent.run_agent --log-file agent/sample_ci_log.txt
```

Expected: the agent classifies the sample log as “Reports/Artifacts missing …”.

