# Round 2 results

50 items, 3 judges. Gold: 23 Pass, 27 Fail.

## Agreement with gold

Each dimension cell is exact agreement / weighted kappa. Kappa corrects for agreement by chance: above 0.6 is usually read as substantial, below 0.4 as weak.

| Judge | Items | Accuracy | Resolution | Tone | Verdict agree | Verdict kappa |
| --- | --- | --- | --- | --- | --- | --- |
| claude | 50 | 88% / 0.83 | 90% / 0.00 | 88% / 0.65 | 94% | 0.88 |
| gemini | 50 | 84% / 0.77 | 86% / 0.00 | 90% / 0.57 | 86% | 0.71 |
| gpt | 50 | 86% / 0.79 | 98% / 0.00 | 82% / 0.50 | 90% | 0.80 |

## Failures caught

Caught: gold says Fail and the judge also said Fail. False alarm: gold says Pass, judge said Fail.

| Judge | Failures caught | False alarms |
| --- | --- | --- |
| claude | 27 of 27 | 3 of 23 |
| gemini | 27 of 27 | 7 of 23 |
| gpt | 27 of 27 | 5 of 23 |

## Leniency

Average judge score minus gold score. Positive means the judge grades easier than I do.

| Judge | Accuracy | Resolution | Tone |
| --- | --- | --- | --- |
| claude | -0.04 | -0.12 | -0.08 |
| gemini | -0.18 | -0.14 | +0.10 |
| gpt | -0.12 | -0.02 | -0.10 |

## Judge vs judge (verdict)

| Pair | Agreement |
| --- | --- |
| claude vs gemini | 88% |
| claude vs gpt | 88% |
| gemini vs gpt | 92% |

## Self-preference check

Average (judge total minus gold total) across the 3 dimensions, split by who wrote the reply. If a judge is noticeably more positive on its own company's replies, that is self-preference. With about 17 items per group, treat small gaps as noise.

| Judge | Own company's replies | Other replies |
| --- | --- | --- |
| claude | -0.29 (n=17) | -0.21 (n=33) |
| gemini | +0.06 (n=16) | -0.35 (n=34) |
| gpt | -0.12 (n=17) | -0.30 (n=33) |

## Seed vs generated messages (verdict agreement)

| Judge | Handwritten seeds | Haiku-generated |
| --- | --- | --- |
| claude | 85% (n=13) | 97% (n=37) |
| gemini | 85% (n=13) | 86% (n=37) |
| gpt | 85% (n=13) | 92% (n=37) |

## By topic (all judges pooled)

Lowest agreement first. These topics are where to look for rubric gaps.

| Topic | Items | Verdict agree | Accuracy agree |
| --- | --- | --- | --- |
| damaged_items | 3 | 78% | 78% |
| spoiled_box | 6 | 78% | 83% |
| late_box | 8 | 83% | 83% |
| skip_cancel | 8 | 88% | 83% |
| delivery_window | 4 | 92% | 100% |
| missing_items | 6 | 94% | 61% |
| allergy | 6 | 100% | 94% |
| credit_limit | 4 | 100% | 100% |
| not_covered | 5 | 100% | 100% |
