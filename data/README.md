# Data

Planned files:

- `seed_messages.csv`: 25 handwritten customer messages, with correct handling and the edge case each tests
- `generated_messages.csv`: 75 messages written by Claude Haiku via `scripts/generate_messages.py`, reviewed by hand
- `all_items.csv`: all 100 messages with their reply, reply style and reply model (`scripts/generate_replies.py`)
- `round1_items.csv`, `round2_items.csv`: the balanced 50/50 split (`scripts/split_rounds.py`)
- `round1_gold.csv`, `round2_gold.csv`: blank sheets created by the split; I fill in accuracy, resolution, tone, verdict, reason
- `round1_judge_outputs.csv`, `round2_judge_outputs.csv`: written by `scripts/run_judges.py`

Gold labels are committed before any judge runs, so the commit history shows they were not influenced by judge output.
