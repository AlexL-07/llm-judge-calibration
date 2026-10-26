"""Send each item to each AI judge and save the scores to CSV.

Usage:
    python scripts/run_judges.py --round 1
    python scripts/run_judges.py --round 2 --prompt-version v2 --rubric-version v2
    python scripts/run_judges.py --round 2 --tag v1     # v1 rubric on round 2, saved separately
    ...add --retry-errors to any of these to regrade only the rows that came back unreadable

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
import re
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

MAX_TOKENS = 2000  # roomy, since some models spend tokens thinking before they answer
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


def _call_once(judge, model, prompt, use_temperature, max_tokens=MAX_TOKENS, json_mode=True):
    client = _client(judge)
    if judge == "claude":
        kwargs = {"temperature": 0} if use_temperature else {}
        resp = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )
        return "".join(b.text for b in resp.content if b.type == "text")
    if judge == "gpt":
        kwargs = {"temperature": 0} if use_temperature else {}
        resp = client.responses.create(
            model=model,
            input=prompt,
            max_output_tokens=max_tokens,
            **kwargs,
        )
        return resp.output_text
    if judge == "gemini":
        from google.genai import types

        config = types.GenerateContentConfig(
            max_output_tokens=max_tokens,
            temperature=0 if use_temperature else None,
            response_mime_type="application/json" if json_mode else None,
        )
        resp = client.models.generate_content(model=model, contents=prompt, config=config)
        return resp.text or ""  # None when the model returns no text
    raise ValueError(f"Unknown judge: {judge}")


def call_judge(judge, model, prompt, retries=3, max_tokens=MAX_TOKENS, json_mode=True, temperature_zero=True):
    """Call one model and return its raw text response.

    Also used by generate_replies.py, which passes json_mode=False and
    temperature_zero=False to get natural, varied replies.

    Uses temperature 0 so results are as repeatable as possible. Some newer
    models reject a temperature setting, so if the API complains about it,
    the call is retried without one. Other errors (rate limits, timeouts)
    are retried a few times with a growing wait.
    """
    use_temperature = temperature_zero
    for attempt in range(retries):
        try:
            return _call_once(judge, model, prompt, use_temperature, max_tokens, json_mode)
        except Exception as e:  # each SDK raises its own error types
            if use_temperature and "temperature" in str(e).lower():
                use_temperature = False
                continue
            if attempt == retries - 1:
                return f"ERROR: {e}"
            time.sleep(2 ** attempt * 5)
    return "ERROR: no response"


def parse_output(text):
    """Pull the JSON object out of a judge response. Returns None if it fails
    or if any score is missing or out of range."""
    if not isinstance(text, str):
        return None
    try:
        start, end = text.index("{"), text.rindex("}") + 1
    except ValueError:
        return None
    body = text[start:end]
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        # Models sometimes leave a comma after the last field, e.g. "reason": "...",}
        try:
            parsed = json.loads(re.sub(r",\s*([}\]])", r"\1", body))
        except json.JSONDecodeError:
            return None
    if not isinstance(parsed, dict):
        return None
    for d in ("accuracy", "resolution", "tone"):
        try:
            parsed[d] = int(parsed.get(d))
        except (TypeError, ValueError):
            return None
        if parsed[d] not in (1, 2, 3):
            return None
    verdict = str(parsed.get("verdict", "")).strip().capitalize()
    if verdict not in ("Pass", "Fail"):
        return None
    parsed["verdict"] = verdict
    return parsed


def grade(judge, model, prompt, tries=3):
    """Ask one judge, retrying when the answer can't be read.
    Returns (parsed or None, raw text of the last attempt)."""
    raw = ""
    for _ in range(tries):
        raw = call_judge(judge, model, prompt)
        parsed = parse_output(raw)
        if parsed:
            return parsed, raw
    return None, raw


def make_row(item_id, judge, parsed, raw):
    parsed = parsed or {}
    return {
        "item_id": item_id,
        "judge": judge,
        "accuracy": parsed.get("accuracy"),
        "resolution": parsed.get("resolution"),
        "tone": parsed.get("tone"),
        "verdict": parsed.get("verdict"),
        "reason": parsed.get("reason"),
        "raw": raw,
    }


FIELDS = ["item_id", "judge", "accuracy", "resolution", "tone", "verdict", "reason", "raw"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--round", type=int, required=True)
    parser.add_argument("--prompt-version", default="v1")
    parser.add_argument("--rubric-version", default="v1")
    parser.add_argument("--limit", type=int, help="Only grade the first N items (for a test run)")
    parser.add_argument("--tag", default="", help="Save to a separate file, e.g. --tag v1 writes round2_judge_outputs_v1.csv")
    parser.add_argument("--retry-errors", action="store_true",
                        help="Only regrade rows in the existing output file that have no scores")
    args = parser.parse_args()

    template = (ROOT / f"prompts/judge_{args.prompt_version}.md").read_text(encoding="utf-8")
    policy = (ROOT / "rubric/policy.md").read_text(encoding="utf-8")
    rubric = (ROOT / f"rubric/rubric_{args.rubric_version}.md").read_text(encoding="utf-8")

    items_path = ROOT / f"data/round{args.round}_items.csv"
    suffix = f"_{args.tag}" if args.tag else ""
    out_path = ROOT / f"data/round{args.round}_judge_outputs{suffix}.csv"

    with open(items_path, newline="", encoding="utf-8") as f:
        items = list(csv.DictReader(f))
    if args.limit:
        items = items[: args.limit]
        out_path = ROOT / f"data/round{args.round}_judge_outputs{suffix}_test.csv"

    def prompt_for(item):
        return build_prompt(template, policy, rubric, item["customer_message"], item["agent_reply"])

    if args.retry_errors:
        if not out_path.exists():
            raise SystemExit(f"{out_path.relative_to(ROOT)} not found. Run without --retry-errors first.")
        with open(out_path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        by_id = {i["item_id"]: i for i in items}
        todo = [r for r in rows if not parse_output(
            json.dumps({k: r[k] for k in ("accuracy", "resolution", "tone", "verdict")}))]
        print(f"{len(todo)} rows to regrade")
        for r in todo:
            # First try re-reading the answer already saved, so no new API call is needed.
            parsed, raw = parse_output(r["raw"]), r["raw"]
            how = "re-read saved answer"
            if not parsed:
                parsed, raw = grade(r["judge"], JUDGES[r["judge"]], prompt_for(by_id[r["item_id"]]))
                how = "asked again"
            r.update(make_row(r["item_id"], r["judge"], parsed, raw))
            print(f"{r['item_id']} {r['judge']}: {parsed['verdict'] + ' (' + how + ')' if parsed else 'STILL UNREADABLE'}")
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        return

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for item in items:
            prompt = prompt_for(item)
            for judge, model in JUDGES.items():
                parsed, raw = grade(judge, model, prompt)
                writer.writerow(make_row(item["item_id"], judge, parsed, raw))
                f.flush()
                print(f"{item['item_id']} {judge}: {parsed['verdict'] if parsed else 'PARSE ERROR'}")


if __name__ == "__main__":
    main()
