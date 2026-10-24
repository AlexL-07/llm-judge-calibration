# LLM Judge Calibration Pilot

A small, solo evaluation project: can AI judges grade customer support replies the way a careful human would, and does a better rubric close the gap?

## What this project does

1. Builds a 100-item eval set: customer support messages for a fictional meal kit company, **Fernleaf Kitchen**, each paired with an AI-written reply.
2. I label every reply by hand using a written rubric and company policy. These are the gold labels.
3. Three AI judges from different providers grade the same replies with the same rubric.
4. I measure how well each judge agrees with the gold labels, trace disagreements back to rubric gaps, and revise the rubric and judge prompt.
5. Round 2 runs on 50 fresh items to see whether agreement improved.

## Repo structure

```
data/        Customer messages, AI replies, gold labels, and judge outputs (CSV)
rubric/      Company policy, rubric versions, and the changelog between them
prompts/     Prompts used to generate replies and to instruct the AI judges
scripts/     Python scripts that call model APIs and save results
analysis/    Notebook and SQL queries for agreement metrics and charts
```

## Metrics

- Exact agreement with gold labels, per judge and per dimension
- Weighted Cohen's kappa, judge vs gold (headline number)
- Pass/fail agreement, including auto-fail cases caught
- Leniency: each judge's average score vs mine
- Judge vs judge agreement

## Status

- [x] Policy and rubric v1 drafted
- [ ] Dataset built
- [ ] Round 1: gold labels, judge runs, analysis
- [ ] Rubric v2 and changelog
- [ ] Round 2: gold labels, judge runs, analysis
- [ ] Writeup

## Running it

```bash
pip install -r requirements.txt
cp .env.example .env   # then add your API keys
```

## Results

Coming after round 2.
