"""Generate the 75 LLM-written customer messages, topic by topic.

Usage:
    python scripts/generate_messages.py            # full run, 75 messages
    python scripts/generate_messages.py --dry-run  # print one prompt, no API call

Reads:   data/seed_messages.csv, rubric/policy.md, prompts/message_generation.md
Writes:  data/generated_messages.csv

The generator is a model that is NOT one of the three judges, so no judge
grades data its own model wrote. Review every generated message by hand
before using it, and fix or replace any that are unrealistic or that
mislabel the correct handling.
"""

import argparse
import csv
import json
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
GENERATOR_MODEL = "claude-haiku-5-5"

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


def load_seeds():
    with open(ROOT / "data/seed_messages.csv", newline="") as f:
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
    start, end = text.index("["), text.rindex("]") + 1
    return json.loads(text[start:end])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    template = (ROOT / "prompts/message_generation.md").read_text()
    policy = (ROOT / "rubric/policy.md").read_text()
    seeds = load_seeds()

    if args.dry_run:
        topic, (count, desc) = next(iter(TOPICS.items()))
        print(build_prompt(template, policy, topic, count, desc, seeds))
        return

    client = anthropic.Anthropic()
    rows = []
    for topic, (count, desc) in TOPICS.items():
        prompt = build_prompt(template, policy, topic, count, desc, seeds)
        resp = client.messages.create(
            model=GENERATOR_MODEL,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(b.text for b in resp.content if b.type == "text")
        try:
            items = parse_array(text)
        except (ValueError, json.JSONDecodeError):
            print(f"{topic}: could not parse output, rerun this topic")
            continue
        for i, item in enumerate(items[:count], start=1):
            rows.append(
                {
                    "gen_id": f"G-{topic}-{i:02d}",
                    "topic": topic,
                    "customer_message": item.get("customer_message", ""),
                    "correct_handling": item.get("correct_handling", ""),
                    "why_its_tricky": item.get("why_its_tricky", ""),
                }
            )
        print(f"{topic}: {min(len(items), count)} of {count}")

    out = ROOT / "data/generated_messages.csv"
    with open(out, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["gen_id", "topic", "customer_message", "correct_handling", "why_its_tricky"]
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} messages to {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
