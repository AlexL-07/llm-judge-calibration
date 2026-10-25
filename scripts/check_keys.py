"""Make one tiny call to every model the project uses, to confirm your keys,
billing and model access all work before the real runs.

Usage:
    python scripts/check_keys.py

Costs a fraction of a cent. Prints OK or the error for each model.
"""

import os

from dotenv import load_dotenv

from generate_messages import GENERATOR_MODEL
from generate_replies import REPLY_MODELS
from run_judges import JUDGES, call_judge

load_dotenv()

KEY_NAMES = {"claude": "ANTHROPIC_API_KEY", "gpt": "OPENAI_API_KEY", "gemini": "GEMINI_API_KEY"}


def main():
    checks = [(p, m, "judge") for p, m in JUDGES.items()]
    checks += [(p, m, "reply writer") for p, m in REPLY_MODELS.items()]
    checks.append(("claude", GENERATOR_MODEL, "message generator"))

    missing = [k for k in KEY_NAMES.values() if not os.environ.get(k)]
    if missing:
        print("Missing from .env: " + ", ".join(missing))

    failures = 0
    for provider, model, role in checks:
        if not os.environ.get(KEY_NAMES[provider]):
            print(f"SKIP  {model:<24} ({role}): no {KEY_NAMES[provider]}")
            failures += 1
            continue
        reply = call_judge(provider, model, "Reply with the single word: ok",
                           retries=2, max_tokens=200, json_mode=False)
        if reply.startswith("ERROR"):
            failures += 1
            print(f"FAIL  {model:<24} ({role}): {reply[:200]}")
        else:
            print(f"OK    {model:<24} ({role})")

    print("\nAll good, ready to run." if not failures else
          f"\n{failures} problem(s). Paste the FAIL lines to Claude if the fix isn't obvious.")


if __name__ == "__main__":
    main()
