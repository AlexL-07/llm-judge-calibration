"""Write one AI support reply for each of the 100 customer messages.

Usage:
    python scripts/generate_replies.py            # all items (skips ones already done)
    python scripts/generate_replies.py --limit 5  # test on 5 items
    python scripts/generate_replies.py --dry-run  # print one prompt, no API call

Reads:   data/seed_messages.csv, data/generated_messages.csv,
         prompts/reply_generation.md, rubric/policy.md
Writes:  data/all_items.csv

Each item gets a reply STYLE (careful, rushed or generous, from
prompts/reply_generation.md) so reply quality varies the way real support
quality does. Each item also gets a REPLY MODEL: the small model from each of
the three judge providers, rotated evenly. That way no judge grades only its
own company's writing, and the analysis can check whether each judge favors
replies from its own provider (self-preference bias).

Safe to rerun: items that already have a reply are skipped, so an
interrupted run picks up where it stopped. Assignments are fixed by a random
seed, so they come out the same every time.
"""

import argparse
import csv
import random
import re
from pathlib import Path

from run_judges import call_judge  # same API code the judges use

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "data/all_items.csv"
SEED = 42
MAX_TOKENS = 2000

# provider -> small model used to WRITE replies (the judges use mid-tier models)
REPLY_MODELS = {
    "claude": "claude-haiku-5-5",
    "gpt": "gpt-6-luna",
    "gemini": "gemini-3.5-flash-lite",
}

# share of items per style: mostly careful, so there are plenty of good replies
STYLE_SHARES = {"A": 0.4, "B": 0.3, "C": 0.3}
STYLE_NAMES = {"A": "careful", "B": "rushed", "C": "generous"}

FIELDS = [
    "item_id", "source", "topic", "customer_message", "correct_handling",
    "why_its_tricky", "reply_style", "reply_model", "agent_reply",
]


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_style_prompts():
    """Split reply_generation.md into its '## Style X: name' sections."""
    text = (ROOT / "prompts/reply_generation.md").read_text(encoding="utf-8")
    parts = re.split(r"^## Style ([A-Z]):[^\n]*\n", text, flags=re.M)
    styles = {parts[i]: parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}
    missing = set(STYLE_SHARES) - set(styles)
    if missing:
        raise SystemExit(f"reply_generation.md is missing styles: {sorted(missing)}")
    return styles


def load_messages():
    rows = []
    for s in read_csv(ROOT / "data/seed_messages.csv"):
        rows.append({"item_id": s["seed_id"], "source": "seed", **_shared(s)})
    gen_path = ROOT / "data/generated_messages.csv"
    if not gen_path.exists():
        raise SystemExit("data/generated_messages.csv not found. Run generate_messages.py first.")
    for g in read_csv(gen_path):
        rows.append({"item_id": g["gen_id"], "source": "generated", **_shared(g)})
    return rows


def _shared(r):
    return {k: r[k] for k in ("topic", "customer_message", "correct_handling", "why_its_tricky")}


def assign(rows):
    """Give every item a style and a reply model, evenly and repeatably."""
    order = sorted(rows, key=lambda r: r["item_id"])
    random.Random(SEED).shuffle(order)
    n = len(order)
    styles = []
    for style, share in STYLE_SHARES.items():
        styles += [style] * round(n * share)
    styles = (styles + ["A"] * n)[:n]  # pad or trim for rounding
    providers = list(REPLY_MODELS)
    for i, row in enumerate(order):
        row["reply_style"] = styles[i]
        row["reply_model"] = providers[i % len(providers)]
    return {r["item_id"]: r for r in order}


def load_done():
    if not OUT_PATH.exists():
        return {}
    return {
        r["item_id"]: r
        for r in read_csv(OUT_PATH)
        if r.get("agent_reply") and not r["agent_reply"].startswith("ERROR")
    }


def write_all(items):
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for item_id in sorted(items):
            writer.writerow({k: items[item_id].get(k, "") for k in FIELDS})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, help="Only write replies for N items (test run)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    policy = (ROOT / "rubric/policy.md").read_text(encoding="utf-8")
    styles = load_style_prompts()
    items = assign(load_messages())

    if args.dry_run:
        item = next(iter(items.values()))
        print(f"[{item['item_id']} | style {item['reply_style']} | {item['reply_model']}]\n")
        print(styles[item["reply_style"]].format(policy=policy, customer_message=item["customer_message"]))
        return

    done = load_done()
    for item_id, row in done.items():
        if item_id in items:
            items[item_id]["agent_reply"] = row["agent_reply"]

    todo = [i for i in items.values() if not i.get("agent_reply")]
    if args.limit:
        todo = todo[: args.limit]
    print(f"{len(done)} already done, writing {len(todo)} replies")

    errors = 0
    for n, item in enumerate(todo, start=1):
        prompt = styles[item["reply_style"]].format(
            policy=policy, customer_message=item["customer_message"]
        )
        provider = item["reply_model"]
        reply = call_judge(
            provider, REPLY_MODELS[provider], prompt,
            max_tokens=MAX_TOKENS, json_mode=False, temperature_zero=False,
        ).strip()
        item["agent_reply"] = reply
        errors += reply.startswith("ERROR")
        print(f"{n}/{len(todo)} {item['item_id']} ({STYLE_NAMES[item['reply_style']]}, {provider})"
              + ("  ERROR" if reply.startswith("ERROR") else ""))
        write_all(items)  # save after every reply so nothing is lost

    print(f"Saved to {OUT_PATH.relative_to(ROOT)}")
    if errors:
        print(f"{errors} replies failed. Run the same command again to retry just those.")


if __name__ == "__main__":
    main()
