"""Send each item to each AI judge and save the scores to CSV.

Usage:
    python scripts/run_judges.py --round 1

Reads:   data/round{N}_items.csv   (columns: item_id, customer_message, agent_reply)
Writes:  data/round{N}_judge_outputs.csv

Needs ANTHROPIC_API_KEY, OPENAI_API_KEY and GEMINI_API_KEY in your .env file.

Judges are the mid-tier model from each provider, so the comparison is fair
and cheap. Model names are as of October 2026; update them if a provider
retires one.
"""

import argparse
import csv
import json
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent

JUDGES = {
    "claude": "claude-sonnet-5-5",
    "gpt": "gpt-6-sol",
    "gemini": "gemini-3.8-flash",
}

MAX_TOKENS = 400
_clients = {}


def _client(judge):
    """Create each provider's client once and reuse it."""
    if judge not in _clients:
        if judge == "claude":
            import anthropic

            _clients[judge] = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
        elif judge == "gpt":
            from openai import OpenAI

            _clients[judge] = OpenAI()  # reads OPENAI_API_KEY
        elif judge == "gemini":
            from google import genai

            _clients[judge] = genai.Client()  # reads GEMINI_API_KEY
    return _clients[judge]


def build_prompt(template, policy, rubric, message, reply):
    return template.format(
        policy=policy, rubric=rubric, customer_message=message, agent_reply=reply
    )


def _call_once(judge, model, prompt, use_temperature):
    client = _client(judge)
    if judge == "claude":
        kwargs = {"temperature": 0} if use_temperature else {}
        resp = client.messages.create(
            model=model,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )
        return "".join(b.text for b in resp.content if b.type == "text")
    if judge == "gpt":
        kwargs = {"temperature": 0} if use_temperature else {}
        resp = client.responses.create(
            model=model,
            input=prompt,
            max_output_tokens=MAX_TOKENS,
            **kwargs,
        )
        return resp.output_text
    if judge == "gemini":
        from google.genai import types

        config = types.GenerateContentConfig(
            max_output_tokens=MAX_TOKENS,
            temperature=0 if use_temperature else None,
            response_mime_type="application/json",
        )
        resp = client.models.generate_content(model=model, contents=prompt, config=config)
        return resp.text
    raise ValueError(f"Unknown judge: {judge}")


def call_judge(judge, model, prompt, retries=3):
    """Call one model and return its raw text response.

    Uses temperature 0 so results are as repeatable as possible. Some newer
    models reject a temperature setting, so if the API complains about it,
    the call is retried without one. Other errors (rate limits, timeouts)
    are retried a few times with a growing wait.
    """
    use_temperature = True
    for attempt in range(retries):
        try:
            return _call_once(judge, model, prompt, use_temperature)
        except Exception as e:  # each SDK raises its own error types
            if use_temperature and "temperature" in str(e).lower():
                use_temperature = False
                continue
            if attempt == retries - 1:
                return f"ERROR: {e}"
            time.sleep(2 ** attempt * 5)
    return "ERROR: no response"


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
    parser.add_argument("--limit", type=int, help="Only grade the first N items (for a test run)")
    args = parser.parse_args()

    template = (ROOT / f"prompts/judge_{args.prompt_version}.md").read_text(encoding="utf-8")
    policy = (ROOT / "rubric/policy.md").read_text(encoding="utf-8")
    rubric = (ROOT / f"rubric/rubric_{args.rubric_version}.md").read_text(encoding="utf-8")

    items_path = ROOT / f"data/round{args.round}_items.csv"
    out_path = ROOT / f"data/round{args.round}_judge_outputs.csv"

    with open(items_path, newline="", encoding="utf-8") as f:
        items = list(csv.DictReader(f))
    if args.limit:
        items = items[: args.limit]
        out_path = ROOT / f"data/round{args.round}_judge_outputs_test.csv"

    fields = ["item_id", "judge", "accuracy", "resolution", "tone", "verdict", "reason", "raw"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
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
