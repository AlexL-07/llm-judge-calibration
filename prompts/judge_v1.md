You are grading a customer support reply for Fernleaf Kitchen, a meal kit delivery company.

Judge the reply ONLY against the company policy and rubric below. Do not use outside knowledge about other companies' policies.

## Company policy

{policy}

## Rubric

{rubric}

## Item to grade

Customer message:
{customer_message}

Agent reply:
{agent_reply}

## Output

Return only valid JSON in exactly this format, with no other text:

{{
  "accuracy": 1-3,
  "resolution": 1-3,
  "tone": 1-3,
  "verdict": "Pass" or "Fail",
  "reason": "One sentence explaining the most important factor in your scores."
}}
