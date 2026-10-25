# Round 1 results

50 items, 3 judges. Gold: 40 Pass, 10 Fail.

1 judge outputs could not be read and are left out: G-delivery_window-06 (gemini)

## Agreement with gold

Each dimension cell is exact agreement / weighted kappa. Kappa corrects for agreement by chance: above 0.6 is usually read as substantial, below 0.4 as weak.

| Judge | Items | Accuracy | Resolution | Tone | Verdict agree | Verdict kappa |
| --- | --- | --- | --- | --- | --- | --- |
| claude | 50 | 60% / 0.45 | 38% / 0.04 | 80% / 0.33 | 76% | 0.35 |
| gemini | 49 | 57% / 0.33 | 69% / 0.22 | 84% / -0.04 | 63% | 0.26 |
| gpt | 50 | 52% / 0.31 | 72% / 0.31 | 86% / 0.29 | 60% | 0.22 |

## Failures caught

Caught: gold says Fail and the judge also said Fail. False alarm: gold says Pass, judge said Fail.

| Judge | Failures caught | False alarms |
| --- | --- | --- |
| claude | 6 of 10 | 8 of 40 |
| gemini | 8 of 10 | 16 of 39 |
| gpt | 8 of 10 | 18 of 40 |

## Leniency

Average judge score minus gold score. Positive means the judge grades easier than I do.

| Judge | Accuracy | Resolution | Tone |
| --- | --- | --- | --- |
| claude | -0.22 | -0.56 | -0.08 |
| gemini | -0.35 | -0.24 | +0.12 |
| gpt | -0.48 | -0.24 | +0.06 |

## Judge vs judge (verdict)

| Pair | Agreement |
| --- | --- |
| claude vs gemini | 80% |
| claude vs gpt | 72% |
| gemini vs gpt | 84% |

## Self-preference check

Average (judge total minus gold total) across the 3 dimensions, split by who wrote the reply. If a judge is noticeably more positive on its own company's replies, that is self-preference. With about 17 items per group, treat small gaps as noise.

| Judge | Own company's replies | Other replies |
| --- | --- | --- |
| claude | -0.82 (n=17) | -0.88 (n=33) |
| gemini | +0.00 (n=17) | -0.72 (n=32) |
| gpt | -0.75 (n=16) | -0.62 (n=34) |

## Seed vs generated messages (verdict agreement)

| Judge | Handwritten seeds | Haiku-generated |
| --- | --- | --- |
| claude | 75% (n=12) | 76% (n=38) |
| gemini | 83% (n=12) | 57% (n=37) |
| gpt | 58% (n=12) | 61% (n=38) |

## By topic (all judges pooled)

Lowest agreement first. These topics are where to look for rubric gaps.

| Topic | Items | Verdict agree | Accuracy agree |
| --- | --- | --- | --- |
| allergy | 6 | 39% | 28% |
| delivery_window | 4 | 45% | 36% |
| credit_limit | 4 | 50% | 25% |
| late_box | 8 | 62% | 58% |
| missing_items | 6 | 72% | 56% |
| spoiled_box | 6 | 72% | 56% |
| skip_cancel | 8 | 75% | 75% |
| damaged_items | 4 | 83% | 75% |
| not_covered | 4 | 100% | 92% |
