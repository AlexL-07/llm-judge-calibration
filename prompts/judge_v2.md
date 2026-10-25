You are grading a customer support reply for Fernleaf Kitchen, a meal kit delivery company.

Judge the reply ONLY against the company policy and the rubric below, including the rubric's policy clarifications and decision rules. Do not use outside knowledge about other companies' policies, and do not apply your own standard of good support where the rubric gives a rule.

Before scoring, work out what the policy says the customer is owed, using the clarifications for lateness, spoiled boxes and the $30 limit. Then compare the reply against that.

Score each problem in the one dimension it belongs to. Do not lower Resolution or Tone for a policy error you have already scored under Accuracy.

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
