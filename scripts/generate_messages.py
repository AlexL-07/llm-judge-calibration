"""Generate the 75 LLM-written customer messages, topic by topic.

Usage:
    python scripts/generate_messages.py                       # all topics
    python scripts/generate_messages.py --topics late_box allergy   # only these
    python scripts/generate_messages.py --dry-run             # print one prompt, no API call

Reads:   data/seed_messages.csv, rubric/policy.md, prompts/message_generation.md
Writes:  data/generated_messages.csv

Rerunning with --topics replaces only those topics in the CSV and keeps the
rest. If a topic still fails after 3 tries, the raw model output is saved to
data/debug/ so you can see what went wrong.

The generator is Claude Haiku. It is not one of the three judges, but it is
from the same company as the Claude judge, so the writeup notes this and
compares the Claude judge's results on seed vs generated messages.
Review every generated message by hand before using it, and fix or replace
any that are unrealistic or that mislabel the correct handling.
"""

import argparse
import csv
import json
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "data/generated_messages.csv"
DEBUG_DIR = ROOT / "data/debug"
GENERATOR_MODEL = "claude-haiku-5-5"
MAX_TOKENS = 8000
TRIES = 3
FIELDS = ["gen_id", "topic", "customer_message", "correct_handling", "why_its_tricky"]

# How many new messages per topic. Roughly matches the seed mix and adds up to 75.
TOPICS = {
    "delivery_window": (6, "When boxes arrive and what counts as on time."),
    "late_box": (12, "Boxes that arrive late, by different amounts. The 1-day line matters."),
    "missing_items": (9, "Items missing from a box, with or without a photo, reported at different times."),
    "damaged_items": (6, "Items that arrived damaged, and whether the customer wants credit or a card refund."),
    "spoiled_box": (9, "Boxes that arrived warm or might be unsafe, sometimes combined with lateness."),
    "skip_cancel": (12, "Skipping a week or cancelling, before and after the cutoff. Give the dates."),
    "allergy": (9, "Allergy and dietary safety questions about meals."),
    "credit_limit": (6, "Claims where the total is near or over $30. Give dollar amounts."),
    "not_covered": (6, "Requests the policy doesn't address at all."),
}


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def load_seeds():
    with open(ROOT / "data/seed_messages.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_existing():
    if not OUT_PATH.exists():
        return []
    with open(OUT_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def examples_for(topic, seeds):
    rows = [s for s in seeds if s["topic"] == topic]
    return "\n".join(f'- "{s["customer_message"]}"' for s in rows) or "(none)"


def build_prompt(template, policy, topic, count, description, seeds):
    return template.format(
        policy=policy,
        count=count,
        topic=topic,
        topic_description=description,
        examples=examples_for(topic, seeds),
    )


def parse_array(text):
    """Find the first valid JSON array in the response, ignoring any extra text
    or ```json fences around it. Raises ValueError if there is none."""
    decoder = json.JSONDecoder()
    i = text.find("[")
    while i != -1:
        try:
            value, _ = decoder.raw_decode(text, i)
            if isinstance(value, list) and value and isinstance(value[0], dict):
                return value
        except json.JSONDecodeError:
            pass
        i = text.find("[", i + 1)
    raise ValueError("no JSON array found")


def generate_topic(client, prompt, topic):
    """Call the model up to TRIES times. Returns a list of items, or None."""
    for attempt in range(1, TRIES + 1):
        resp = client.messages.create(
            model=GENERATOR_MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(b.text for b in resp.content if b.type == "text")
        try:
            return parse_array(text)
        except ValueError:
            DEBUG_DIR.mkdir(parents=True, exist_ok=True)
            debug_file = DEBUG_DIR / f"{topic}_attempt{attempt}.txt"
            debug_file.write_text(
                f"stop_reason: {resp.stop_reason}\n\n{text}", encoding="utf-8"
            )
            print(f"  {topic}: attempt {attempt} unreadable (stop_reason: {resp.stop_reason})")
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--topics", nargs="+", choices=list(TOPICS), help="Only (re)generate these topics")
    args = parser.parse_args()

    template = read_text(ROOT / "prompts/message_generation.md")
    policy = read_text(ROOT / "rubric/policy.md")
    seeds = load_seeds()

    if args.dry_run:
        topic, (count, desc) = next(iter(TOPICS.items()))
        print(build_prompt(template, policy, topic, count, desc, seeds))
        return

    selected = args.topics or list(TOPICS)
    # Keep rows for topics we are not regenerating.
    kept = [r for r in load_existing() if r["topic"] not in selected] if args.topics else []
    new_rows, failed = [], []

    client = anthropic.Anthropic()
    for topic in selected:
        count, desc = TOPICS[topic]
        prompt = build_prompt(template, policy, topic, count, desc, seeds)
        items = generate_topic(client, prompt, topic)
        if items is None:
            failed.append(topic)
            print(f"{topic}: FAILED after {TRIES} tries, see data/debug/")
            continue
        for i, item in enumerate(items[:count], start=1):
            new_rows.append(
                {
                    "gen_id": f"G-{topic}-{i:02d}",
                    "topic": topic,
                    "customer_message": item.get("customer_message", ""),
                    "correct_handling": item.get("correct_handling", ""),
                    "why_its_tricky": item.get("why_its_tricky", ""),
                }
            )
        print(f"{topic}: {min(len(items), count)} of {count}")

    order = {t: n for n, t in enumerate(TOPICS)}
    rows = sorted(kept + new_rows, key=lambda r: (order[r["topic"]], r["gen_id"]))
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} messages to {OUT_PATH.relative_to(ROOT)}")
    if failed:
        print("Still failing: " + " ".join(failed))
        print("Rerun with: python scripts/generate_messages.py --topics " + " ".join(failed))


if __name__ == "__main__":
    main()
