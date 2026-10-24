"""Send each item to each AI judge and save the scores to CSV.

Usage:
    python scripts/run_judges.py --round 1

Reads:   data/round{N}_items.csv   (columns: item_id, customer_message, agent_reply)
Writes:  data/round{N}_judge_outputs.csv

The model names below are placeholders. Set them to the models you choose
and add the matching API keys to your .env file.
"""

import argparse
import csv
import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent

JUDGES = {
    "claude": "MODEL_NAME_HERE",
    "gpt": "MODEL_NAME_HERE",
    "gemini": "MODEL_NAME_HERE",
}


def build_prompt(template, policy, rubric, message, reply):
    return template.format(
        policy=policy, rubric=rubric, customer_message=message, agent_reply=reply
    )


def call_judge(judge, model, prompt):
    """Call one model and return its raw text response.

    TODO: fill in each provider's SDK call. Use temperature 0 so results
    are as repeatable as possible.
    """
    if judge == "claude":
        import anthropic

        client = anthropic.Anthropic()
        resp = client.messages.create(
            model=model,
            max_tokens=300,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text
    if judge == "gpt":
        raise NotImplementedError("Add the OpenAI call here")
    if judge == "gemini":
        raise NotImplementedError("Add the Gemini call here")
    raise ValueError(f"Unknown judge: {judge}")


def parse_output(text):
    """Pull the JSON object out of a judge response. Returns None if it fails."""
    try:
        start, end = text.index("{"), text.rindex("}") + 1
        return json.loads(text[start:end])
    except (ValueError, json.JSONDecodeError):
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--round", type=int, required=True)
    parser.add_argument("--prompt-version", default="v1")
    parser.add_argument("--rubric-version", default="v1")
    args = parser.parse_args()

    template = (ROOT / f"prompts/judge_{args.prompt_version}.md").read_text()
    policy = (ROOT / "rubric/policy.md").read_text()
    rubric = (ROOT / f"rubric/rubric_{args.rubric_version}.md").read_text()

    items_path = ROOT / f"data/round{args.round}_items.csv"
    out_path = ROOT / f"data/round{args.round}_judge_outputs.csv"

    with open(items_path, newline="") as f:
        items = list(csv.DictReader(f))

    fields = ["item_id", "judge", "accuracy", "resolution", "tone", "verdict", "reason", "raw"]
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for item in items:
            prompt = build_prompt(
                template, policy, rubric, item["customer_message"], item["agent_reply"]
            )
            for judge, model in JUDGES.items():
                raw = call_judge(judge, model, prompt)
                parsed = parse_output(raw) or {}
                writer.writerow(
                    {
                        "item_id": item["item_id"],
                        "judge": judge,
                        "accuracy": parsed.get("accuracy"),
                        "resolution": parsed.get("resolution"),
                        "tone": parsed.get("tone"),
                        "verdict": parsed.get("verdict"),
                        "reason": parsed.get("reason"),
                        "raw": raw,
                    }
                )
                print(f"{item['item_id']} {judge}: {parsed.get('verdict', 'PARSE ERROR')}")


if __name__ == "__main__":
    main()
