"""Split the 100 items into round 1 and round 2, and create blank gold label sheets.

Usage:
    python scripts/split_rounds.py

Reads:   data/all_items.csv
Writes:  data/round1_items.csv, data/round2_items.csv
         data/round1_gold.csv,  data/round2_gold.csv   (blank, for your labels)

The split is balanced: each round gets a near-equal share of every topic,
seed vs generated messages, reply style and reply model. It uses a fixed
random seed, so it comes out the same every time.

It refuses to overwrite files that already exist, so your gold labels can't
be wiped by accident. Use --force only if you really want to redo the split.
"""

import argparse
import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = 7

ITEM_FIELDS = [
    "item_id", "source", "topic", "reply_style", "reply_model",
    "customer_message", "agent_reply",
]
GOLD_FIELDS = [
    "item_id", "customer_message", "agent_reply",
    "accuracy", "resolution", "tone", "verdict", "reason",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Overwrite existing round files")
    args = parser.parse_args()

    with open(ROOT / "data/all_items.csv", newline="", encoding="utf-8") as f:
        items = list(csv.DictReader(f))

    bad = [i["item_id"] for i in items if not i["agent_reply"] or i["agent_reply"].startswith("ERROR")]
    if bad:
        raise SystemExit(f"{len(bad)} items have no reply yet: {', '.join(bad[:10])}. "
                         "Rerun generate_replies.py first.")

    outputs = [ROOT / f"data/round{n}_{kind}.csv" for n in (1, 2) for kind in ("items", "gold")]
    existing = [p.name for p in outputs if p.exists()]
    if existing and not args.force:
        raise SystemExit(f"Already exists: {', '.join(existing)}. Not overwriting. "
                         "Use --force only if you want to redo the split and lose those files.")

    # Group items that are alike, shuffle within each group, then deal them out
    # alternately so both rounds get a fair share of every kind of item.
    rng = random.Random(SEED)
    items.sort(key=lambda i: i["item_id"])
    rng.shuffle(items)
    items.sort(key=lambda i: (i["topic"], i["source"], i["reply_style"]))
    rounds = {1: [], 2: []}
    start = rng.choice([1, 2])
    for n, item in enumerate(items):
        rounds[start if n % 2 == 0 else 3 - start].append(item)

    for r, rows in rounds.items():
        rng.shuffle(rows)  # so items aren't grouped by topic while you label
        with open(ROOT / f"data/round{r}_items.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=ITEM_FIELDS, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        with open(ROOT / f"data/round{r}_gold.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=GOLD_FIELDS, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        print(f"Round {r}: {len(rows)} items")

    print("Done. Fill in data/round1_gold.csv next, before running any judges.")


if __name__ == "__main__":
    main()
