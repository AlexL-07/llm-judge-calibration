# Rubric v2

The gold labeler and every AI judge use this same rubric. It replaces v1 for round 2. See `changelog.md` for what changed and why.

Read the customer message, the policy (`policy.md`), the policy clarifications below, then the reply. Rate the reply on 3 dimensions from 1 to 3, then give an overall Pass or Fail. Every rating includes a one-sentence reason, required for any score of 1 and any Fail.

## Policy clarifications

These settle questions the policy leaves open. Apply them as if they were part of the policy.

1. **How lateness is measured.** Every box's delivery window is 8am to 8pm on the scheduled day. Customers choose a day, not a time. Lateness counts from 8pm on the scheduled day. A box is **more than 1 day late** only if it arrives after 8pm on the following day.
   - Due Tuesday, arrives Tuesday 9:15pm: late, same day. Apology only.
   - Due Tuesday, arrives Wednesday 11am or Wednesday 7:30pm: under 1 day late. Apology only.
   - Due Tuesday, arrives Wednesday after 8pm or any time Thursday: more than 1 day late. Full credit for the box.
2. **Spoiled box.** A box that arrived warm gets a full refund to the original payment method. That refund covers everything in the box, including items that were also damaged, and needs no photo.
3. **The $30 limit.** The limit applies to the total credit or refund an agent gives in one reply for missing items, damaged items, and anything given at the agent's own discretion. Two remedies are exempt and never need escalation: late-box credit (more than 1 day late) and the spoiled-box refund.
4. **Remedies the policy offers.** Account credit, a refund to the original payment method, and escalation to a supervisor. Replacement items, discounts, free boxes, extra compensation, delivery holds and subscription pauses are not in the policy.
5. **Skips and cancellations.** Agents can process a skip or cancellation that meets the cutoff.

## Decision rules

### A. Score each problem once

- **Accuracy:** does what the reply states, offers, promises or requires match the policy?
- **Resolution:** does it handle each thing the customer asked, with a clear next step?
- **Tone:** how does it read?

Put each problem in the one dimension it belongs to. Don't lower Resolution or Tone for a policy error you already scored under Accuracy.

### B. Things the reply offers or states that aren't in the policy

| Score | When |
| --- | --- |
| Accuracy 1 | Offers or hints at a remedy, compensation, exception or feature the policy doesn't give. This includes "I'll look into a credit" when no credit is owed. Also: waives a requirement (photo, 7-day window, skip cutoff), or states a rule wrongly in a way that changes what the customer gets or pays. |
| Accuracy 2 | States a rule wrongly, but the customer's outcome is still correct (for example, a wrong cutoff date that is still safe). Asks for something the policy doesn't require, but makes it optional ("send a photo if you can" for a warm box). Asserts as fact something the agent can't know ("the system was lagging"). |
| No penalty | Routine details that promise nothing: typical refund processing times, asking for an order number or delivery date, a sign-off. |

### C. Remedies the customer is owed

If the policy entitles the customer to credit or a refund, the reply must give it or clearly commit to it ("I'll apply full credit for that box as soon as I have your order number"). Leaving it out, or deferring vaguely ("I'll help make it right"), is **Accuracy 1**, because it costs the customer money.

Leaving out a detail that doesn't change what the customer gets is not an error. Examples: not saying "full," or not naming the refund method when the policy's default applies.

### D. Allergy questions

- **Required:** make no safety claim, and point the customer to the ingredient list and allergen label.
- **Accuracy 1:** says a meal is safe, or offers to confirm, verify or list which meals are safe or free of an allergen. This implies a guarantee Fernleaf can't give, so it is also an automatic Fail.
- **Accuracy 2:** makes no safety claim, but doesn't point to the ingredient list and allergen label.
- **Optional:** repeating that Fernleaf can't guarantee any meal is allergen-free. Advising the customer not to eat a meal, or to get medical help, is fine.

### E. Clear next steps

A clear next step is any of these: the action is done, the customer is told how to do it, the agent asks for information it needs, or the agent says it will check and follow up. No timeframe is needed unless the policy sets one (escalation: a reply within 1 business day).

- **Resolution 1:** the customer asked the agent to do something, and the reply neither does it, says how, nor explains why it can't.
- Explaining clearly why a request can't be granted counts as handling it.
- Venting questions ("what's going on?") need an apology, not an explanation.

### F. Tone

Short but complete is a 3. Give a 2 when the reply is noticeably longer than needed (restates policy the customer didn't ask about, repeats apologies), stiff, overly scripted, or leaves template text in place ("[Customer Name]").

## Dimensions

| Dimension | Question | 3 | 2 | 1 |
| --- | --- | --- | --- | --- |
| Accuracy | Does what the reply states, offers or requires match the policy and clarifications? | Everything matches. Routine details are fine. | A rule is stated wrongly but the outcome is right, an unneeded requirement is made optional, an unverifiable claim is stated as fact, or the allergy label referral is missing. | Offers or hints at something the policy doesn't give, waives a requirement, gets the outcome wrong, leaves out an owed remedy, or makes an allergy safety claim or offer to confirm. |
| Resolution | Does it handle each thing the customer asked, with a clear next step? | Handles every request and gives a clear next step. | Handles the main request but misses a secondary one. | Misses the main request, or the customer asked for an action and the reply neither does it, says how, nor explains why not. |
| Tone | Would a customer feel respected? | Warm and clear. Short is fine. | Noticeably wordy, stiff, overly scripted, or has template text left in. | Rude, dismissive, blaming, or confusing. |

## Overall verdict

- **Pass:** you would send this reply to the customer as written.
- **Fail:** it needs changes first.

## Automatic Fail (regardless of other scores)

- Any Accuracy score of 1. This covers allergy safety claims and offers to confirm safe meals.
- Gives or promises more than $30 of non-exempt credit or refunds without escalating.
- Tone score of 1.

## Worked examples

| Customer message | Reply summary | Scores | Why |
| --- | --- | --- | --- |
| My box arrived 2 days late and the chicken was warm. | Apologizes, gives full refund to card, no photo needed. | Accuracy 3, Resolution 3, Tone 3, Pass | Spoiled-box rule applied correctly. |
| Box arrived warm. It was $52, please refund my card. | Refunds the full $52 to the card, no photo, no escalation. | Accuracy 3, Resolution 3, Tone 3, Pass | Spoiled-box refunds are exempt from the $30 limit (clarification 3). |
| I forgot to skip this week, can you cancel tomorrow's box? | Apologizes, cancels the box and waives the charge. | Accuracy 1, Resolution 3, Tone 3, Fail | Past the 6-day cutoff. Agent invented an exception (rule B). Resolution is not lowered again (rule A). |
| My box was due Friday and came Saturday at 7:30pm. | Apologizes and offers a credit on the next box. | Accuracy 1, Resolution 3, Tone 3, Fail | Under 1 day late, so apology only (clarification 1). Offering credit not owed is rule B. |
| My box was 2 days late. Not great. | Apologizes, asks for the order number, says "I'll help make it right." | Accuracy 1, Resolution 3, Tone 3, Fail | Full credit is owed and the reply doesn't commit to it (rule C). |
| Two items were missing from my box, photo attached. | Offers a replacement on the next delivery or account credit. | Accuracy 1, Resolution 3, Tone 3, Fail | Replacement items are not in the policy (clarification 4). |
| I want to skip my box for the 29th. Today is the 15th. | Skips the box, but says the cutoff is "a week before." | Accuracy 2, Resolution 3, Tone 3, Pass | Rule stated wrongly, but the outcome is right (rule B). |
| I have celiac. Which meals are gluten free? | Points to allergen labels, then offers to check the meal names for them. | Accuracy 1, Resolution 3, Tone 3, Fail | Offering to check which meals are safe implies a guarantee (rule D). |
| Is the pad thai safe for my peanut allergy? | Says the pad thai has no peanuts so it is safe. | Accuracy 1, Resolution 3, Tone 3, Fail | Allergy safety claim (rule D). |
| Two items were missing from my box. | Asks for a photo, offers account credit, mentions card refund on request. Long and formal. | Accuracy 3, Resolution 3, Tone 2, Pass | Correct and complete, just stiff. |
