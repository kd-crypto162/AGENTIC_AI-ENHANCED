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

### Architecture diagram screenshot checklist (Before / After)

Create both diagrams in `draw.io` or `Lucidchart` (as the assignment requests), then:

- Screenshot (or export PNG) of the **Before (legacy monolith)** architecture diagram.
- Screenshot (or export PNG) of the **After (cloud-native microservices)** architecture diagram.

Where to include these in your PDF:
- In `report/report.md` under **“Modernisation Analysis (Before / After)”**.

