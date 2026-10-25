# Round 1 results

Excluded as bad items: G-late_box-09.

49 items, 3 judges. Gold: 39 Pass, 10 Fail.

1 judge outputs could not be read and are left out: G-delivery_window-06 (gemini)

## Agreement with gold

Each dimension cell is exact agreement / weighted kappa. Kappa corrects for agreement by chance: above 0.6 is usually read as substantial, below 0.4 as weak.

| Judge | Items | Accuracy | Resolution | Tone | Verdict agree | Verdict kappa |
| --- | --- | --- | --- | --- | --- | --- |
| claude | 49 | 61% / 0.45 | 39% / 0.04 | 80% / 0.33 | 78% | 0.38 |
| gemini | 48 | 58% / 0.33 | 71% / 0.24 | 83% / -0.04 | 65% | 0.27 |
| gpt | 49 | 53% / 0.31 | 73% / 0.33 | 86% / 0.29 | 61% | 0.23 |

## Failures caught

Caught: gold says Fail and the judge also said Fail. False alarm: gold says Pass, judge said Fail.

| Judge | Failures caught | False alarms |
| --- | --- | --- |
| claude | 6 of 10 | 7 of 39 |
| gemini | 8 of 10 | 15 of 38 |
| gpt | 8 of 10 | 17 of 39 |

## Leniency

Average judge score minus gold score. Positive means the judge grades easier than I do.

| Judge | Accuracy | Resolution | Tone |
| --- | --- | --- | --- |
| claude | -0.20 | -0.55 | -0.08 |
| gemini | -0.33 | -0.23 | +0.12 |
| gpt | -0.47 | -0.22 | +0.06 |

## Judge vs judge (verdict)

| Pair | Agreement |
| --- | --- |
| claude vs gemini | 79% |
| claude vs gpt | 71% |
| gemini vs gpt | 83% |

## Self-preference check

Average (judge total minus gold total) across the 3 dimensions, split by who wrote the reply. If a judge is noticeably more positive on its own company's replies, that is self-preference. With about 17 items per group, treat small gaps as noise.

| Judge | Own company's replies | Other replies |
| --- | --- | --- |
| claude | -0.82 (n=17) | -0.84 (n=32) |
| gemini | +0.12 (n=16) | -0.72 (n=32) |
| gpt | -0.75 (n=16) | -0.58 (n=33) |

## Seed vs generated messages (verdict agreement)

| Judge | Handwritten seeds | Haiku-generated |
| --- | --- | --- |
| claude | 75% (n=12) | 78% (n=37) |
| gemini | 83% (n=12) | 58% (n=36) |
| gpt | 58% (n=12) | 62% (n=37) |

## By topic (all judges pooled)

Lowest agreement first. These topics are where to look for rubric gaps.

| Topic | Items | Verdict agree | Accuracy agree |
| --- | --- | --- | --- |
| allergy | 6 | 39% | 28% |
| delivery_window | 4 | 45% | 36% |
| credit_limit | 4 | 50% | 25% |
| late_box | 7 | 71% | 67% |
| missing_items | 6 | 72% | 56% |
| spoiled_box | 6 | 72% | 56% |
| skip_cancel | 8 | 75% | 75% |
| damaged_items | 4 | 83% | 75% |
| not_covered | 4 | 100% | 92% |
