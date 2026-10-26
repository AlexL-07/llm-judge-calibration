# Round 2 results (v1 judge run)

50 items, 3 judges. Gold: 23 Pass, 27 Fail.

## Agreement with gold

Each dimension cell is exact agreement / weighted kappa. Kappa corrects for agreement by chance: above 0.6 is usually read as substantial, below 0.4 as weak.

| Judge | Items | Accuracy | Resolution | Tone | Verdict agree | Verdict kappa |
| --- | --- | --- | --- | --- | --- | --- |
| claude | 50 | 78% / 0.73 | 26% / 0.00 | 72% / 0.32 | 90% | 0.80 |
| gemini | 50 | 84% / 0.77 | 56% / 0.00 | 84% / 0.27 | 88% | 0.76 |
| gpt | 50 | 78% / 0.65 | 56% / 0.00 | 84% / 0.34 | 88% | 0.76 |

## Failures caught

Caught: gold says Fail and the judge also said Fail. False alarm: gold says Pass, judge said Fail.

| Judge | Failures caught | False alarms |
| --- | --- | --- |
| claude | 25 of 27 | 3 of 23 |
| gemini | 26 of 27 | 5 of 23 |
| gpt | 26 of 27 | 5 of 23 |

## Leniency

Average judge score minus gold score. Positive means the judge grades easier than I do.

| Judge | Accuracy | Resolution | Tone |
| --- | --- | --- | --- |
| claude | -0.02 | -0.82 | -0.22 |
| gemini | -0.02 | -0.54 | +0.12 |
| gpt | -0.06 | -0.50 | +0.08 |

## Judge vs judge (verdict)

| Pair | Agreement |
| --- | --- |
| claude vs gemini | 94% |
| claude vs gpt | 90% |
| gemini vs gpt | 92% |

## Self-preference check

Average (judge total minus gold total) across the 3 dimensions, split by who wrote the reply. If a judge is noticeably more positive on its own company's replies, that is self-preference. With about 17 items per group, treat small gaps as noise.

| Judge | Own company's replies | Other replies |
| --- | --- | --- |
| claude | -0.88 (n=17) | -1.15 (n=33) |
| gemini | -0.19 (n=16) | -0.56 (n=34) |
| gpt | -0.29 (n=17) | -0.58 (n=33) |

## Seed vs generated messages (verdict agreement)

| Judge | Handwritten seeds | Haiku-generated |
| --- | --- | --- |
| claude | 92% (n=13) | 89% (n=37) |
| gemini | 92% (n=13) | 86% (n=37) |
| gpt | 85% (n=13) | 89% (n=37) |

## By topic (all judges pooled)

Lowest agreement first. These topics are where to look for rubric gaps.

| Topic | Items | Verdict agree | Accuracy agree |
| --- | --- | --- | --- |
| damaged_items | 3 | 67% | 67% |
| delivery_window | 4 | 75% | 67% |
| spoiled_box | 6 | 78% | 78% |
| late_box | 8 | 83% | 75% |
| skip_cancel | 8 | 88% | 88% |
| missing_items | 6 | 100% | 44% |
| allergy | 6 | 100% | 100% |
| credit_limit | 4 | 100% | 100% |
| not_covered | 5 | 100% | 100% |
