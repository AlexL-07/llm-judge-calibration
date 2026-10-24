# Rubric v1

The gold labeler and every AI judge use this same rubric.

Rate each reply on 3 dimensions from 1 to 3, then give an overall Pass or Fail. Read the customer message, the policy (`policy.md`), then the reply. Every rating includes a one-sentence reason, required for any score of 1 and any Fail.

## Dimensions

| Dimension | Question | 3 | 2 | 1 |
| --- | --- | --- | --- | --- |
| Accuracy | Does the reply follow Fernleaf policy? | Everything stated matches policy. | Small error or missing detail that would not mislead the customer or cost money. | States something that contradicts policy, invents policy, or promises something the agent cannot give. |
| Resolution | Does it solve the customer's actual request? | Addresses every request and gives a clear next step. | Addresses the main request but misses a secondary one, or the next step is vague. | Misses the main request, or leaves the customer with no next step. |
| Tone | Would a customer feel respected? | Warm, clear, matches the situation. | Fine but stiff, wordy, or overly scripted. | Rude, dismissive, blaming, or confusing. |

## Overall verdict

- **Pass:** you would send this reply to the customer as written.
- **Fail:** it needs changes first.

## Automatic Fail (regardless of other scores)

- Says a meal is safe for an allergy.
- Issues more than $30 in credit without escalating.
- Any Accuracy score of 1.
- Tone score of 1.

## Worked examples

| Customer message | Reply summary | Scores | Why |
| --- | --- | --- | --- |
| My box arrived 2 days late and the chicken was warm. | Apologizes, gives full refund to card, no photo needed, says it will process in a few days. | Accuracy 3, Resolution 3, Tone 3, Pass | Spoiled box rule applied correctly. |
| I forgot to skip this week, can you cancel tomorrow's box? | Apologizes, cancels the box and waives the charge. | Accuracy 1, Resolution 2, Tone 3, Fail | Past the 6-day cutoff. Agent invented an exception. |
| Is the pad thai safe for my peanut allergy? | Says the pad thai has no peanuts so it is safe. | Accuracy 1, Resolution 2, Tone 3, Fail | Auto fail: allergy safety claim. Should point to the allergen label. |
| Two items were missing from my box. | Asks for a photo, offers account credit, mentions card refund on request. Long and formal. | Accuracy 3, Resolution 3, Tone 2, Pass | Correct and complete, just stiff. |
