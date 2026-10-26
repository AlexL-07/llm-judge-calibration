# Judge agreement across runs

| Run | Items | Gold Fails |
| --- | --- | --- |
| Round 1, rubric v1 | 49 | 10 |
| Round 2, rubric v1 | 50 | 27 |
| Round 2, rubric v2 | 50 | 27 |

## Verdict kappa

| Judge | Round 1, rubric v1 | Round 2, rubric v1 | Round 2, rubric v2 |
| --- | --- | --- | --- |
| claude | 0.38 | 0.80 | 0.88 |
| gemini | 0.27 | 0.76 | 0.71 |
| gpt | 0.23 | 0.76 | 0.80 |

## Verdict agreement

| Judge | Round 1, rubric v1 | Round 2, rubric v1 | Round 2, rubric v2 |
| --- | --- | --- | --- |
| claude | 78% | 90% | 94% |
| gemini | 65% | 88% | 86% |
| gpt | 61% | 88% | 90% |

## Accuracy kappa

| Judge | Round 1, rubric v1 | Round 2, rubric v1 | Round 2, rubric v2 |
| --- | --- | --- | --- |
| claude | 0.45 | 0.73 | 0.83 |
| gemini | 0.33 | 0.77 | 0.77 |
| gpt | 0.31 | 0.65 | 0.79 |

## Resolution kappa

| Judge | Round 1, rubric v1 | Round 2, rubric v1 | Round 2, rubric v2 |
| --- | --- | --- | --- |
| claude | 0.04 | 0.00 | 0.00 |
| gemini | 0.24 | 0.00 | 0.00 |
| gpt | 0.33 | 0.00 | 0.00 |

## Tone kappa

| Judge | Round 1, rubric v1 | Round 2, rubric v1 | Round 2, rubric v2 |
| --- | --- | --- | --- |
| claude | 0.33 | 0.32 | 0.65 |
| gemini | -0.04 | 0.27 | 0.57 |
| gpt | 0.29 | 0.34 | 0.50 |

## Gold Fails the judge also failed

| Judge | Round 1, rubric v1 | Round 2, rubric v1 | Round 2, rubric v2 |
| --- | --- | --- | --- |
| claude | 60% | 93% | 100% |
| gemini | 80% | 96% | 100% |
| gpt | 80% | 96% | 100% |

## Gold Passes the judge failed (false alarms)

| Judge | Round 1, rubric v1 | Round 2, rubric v1 | Round 2, rubric v2 |
| --- | --- | --- | --- |
| claude | 18% | 13% | 13% |
| gemini | 39% | 22% | 30% |
| gpt | 44% | 22% | 22% |

Kappa corrects for chance and for how many Fails each round has, so it is the fairest number to compare across rounds. Round 1 and round 2 use different items; the round 2 v1 vs v2 columns use the same items and the same gold labels, so that pair isolates the effect of the rubric change.
