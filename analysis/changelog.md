# Rubric Changelog

Each change ties back to the round 1 disagreements that caused it. Item IDs refer to `analysis/round1_disagreements.csv`.

## v1 (initial)

- Initial rubric: Accuracy, Resolution, Tone on a 1 to 3 scale, plus overall Pass/Fail and auto-fail rules.

## v2 (after round 1)

Round 1 (49 items after excluding one bad item) had 43 items with at least one judge disagreeing with my gold label. I tagged each by cause: 28 rubric gaps, 7 of my own labeling errors, 7 judge errors, and 1 genuinely debatable item. v2 targets the rubric gaps. My round 1 gold labels were not changed after seeing judge output; the 7 labeling errors are reported as a finding instead.

| Change | Why (round 1 evidence) | Items |
| --- | --- | --- |
| Rule B: offering a remedy, exception or feature not in policy is Accuracy 1; routine details like refund timelines are not penalized. Clarification 4 lists the remedies the policy offers. | Largest source of disagreement (9 items, 12 verdict flips). Judges treated replacement offers and "credit or discount" as invented policy; I often didn't. Judges also split on harmless details like refund timelines. | S07, G-missing_items-01, S01, G-late_box-08, S14, G-credit_limit-01 |
| Rule A: score each problem in one dimension only. | Judges lowered Resolution for errors already scored under Accuracy in 7 items, and I put an Accuracy problem under Resolution once. | G-spoiled_box-01, G-delivery_window-05, G-missing_items-02, G-not_covered-06, G-spoiled_box-06, S25 |
| Rule E: defines a clear next step. "I'll check and follow up" counts; no timeframe needed. Asking for an action and getting neither the action nor how-to is Resolution 1. | Claude's Resolution agreement was 39%, mostly from wanting timeframes. Judges and I split on a reply that explained cancellation but didn't cancel. | G-not_covered-01, G-spoiled_box-05, G-late_box-06, G-skip_cancel-02 |
| Rule D: allergy replies must point to the ingredient list and allergen label; offering to confirm or list safe meals is Accuracy 1; the "can't guarantee" line is optional. | Allergy was the lowest-agreement topic (39% verdict agreement). My own labels on S19 and G-allergy-08 pointed in opposite directions. | S19, G-allergy-01, G-allergy-03, G-allergy-08 |
| Clarifications 2 and 3: spoiled-box refunds cover the whole box and are exempt from the $30 limit. The limit covers the total of non-exempt amounts in one reply. | The policy didn't say. All 3 judges read spoiled-box refunds as exempt; I didn't. | G-credit_limit-02, G-damaged_items-06, G-credit_limit-05 |
| Clarification 1: lateness counts from 8pm on the scheduled day, with worked examples. Customers choose a day, not a time. | Judges and I disagreed on whether 11am or 7:30pm the next day is "more than 1 day late." | G-delivery_window-04, G-late_box-03, G-late_box-08 |
| Rule C: leaving out or vaguely deferring an owed remedy is Accuracy 1; leaving out a detail that doesn't change what the customer gets is not an error. | Replies that never committed to owed late-box credit, and replies that just didn't say "full." | G-allergy-05, S03, G-late_box-01, G-spoiled_box-03 |
| Rule B, Accuracy 2: a wrong rule with the right outcome, an optional unneeded requirement, or an unverifiable claim stated as fact. | Judges split between 1 and 2 on a wrong skip cutoff that didn't hurt the customer, and on an agent asserting "the system was lagging." | G-skip_cancel-01, G-skip_cancel-05 |
| Rule F: short but complete is a 3; noticeably wordy, stiff or template text is a 2. | Judges rarely gave Tone 2 for wordy replies; Claude sometimes gave Tone 2 for short ones. | G-allergy-02, G-late_box-04, S22, S17, G-skip_cancel-12 |
| Judge prompt v2: tells judges to work out what the customer is owed before scoring, and to apply rubric rules over their own sense of good support. | Supports the rules above. | |

## Data fix

- **G-late_box-09** is excluded from scoring. Its customer message has impossible dates (a box "due the 20th" arrived "the 23rd," but the customer says today is the 21st). Found while labeling.
