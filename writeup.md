# LLM Judge Calibration: What I Found

I built a 100-item customer support eval set, labeled it myself as the gold standard, and tested whether three AI judges grade the way I do. Over two rounds, verdict agreement with my labels (Cohen's kappa, averaged across the three judges) went from 0.29 to 0.80. A controlled rerun showed that most of that gain came from clearer labels and items, not the rubric itself. The rubric changes still mattered where they were specific: on the same items, they lifted Accuracy kappa from 0.72 to 0.80, Tone kappa from 0.31 to 0.57, and every judge caught all 27 failing replies.

## Setup

- **Task:** grade AI-written replies to customer support messages for a fictional meal kit company, Fernleaf Kitchen, against a written policy.
- **Data:** 25 messages I wrote by hand, 75 generated with Claude Haiku and reviewed by hand. Replies were written by each provider's small model in three styles (careful, rushed, overly generous) so quality varied.
- **Gold labels:** I scored every reply on Accuracy, Resolution and Tone (1 to 3) plus Pass or Fail, before any judge ran. Labels were committed to git first.
- **Judges:** Claude Sonnet 5.5, GPT-6 Sol, Gemini 3.8 Flash, each with the same rubric and prompt.
- **Rounds:** round 1 used 50 items and rubric v1. I tagged every disagreement by cause and wrote rubric v2. Round 2 used 50 new items, judged twice: once with v1 and once with v2, so the rubric's effect could be measured on the same items.

## Results

Verdict kappa, judge vs my labels (above 0.6 is usually read as substantial):

| Judge | Round 1, rubric v1 | Round 2, rubric v1 | Round 2, rubric v2 |
| --- | --- | --- | --- |
| Claude | 0.38 | 0.80 | 0.88 |
| GPT | 0.23 | 0.76 | 0.80 |
| Gemini | 0.27 | 0.76 | 0.71 |
| **Average** | **0.29** | **0.77** | **0.80** |

On the same round 2 items, rubric v2 compared with v1:

| Measure, averaged across judges | Rubric v1 | Rubric v2 |
| --- | --- | --- |
| Accuracy kappa | 0.72 | 0.80 |
| Tone kappa | 0.31 | 0.57 |
| Failing replies caught | 95% | 100% |

Full numbers are in `analysis/comparison.md` and the per-round reports.

## What I learned

1. **Most of the improvement came before the rubric changed.** Judged with the old v1 rubric, round 2 already scored 0.77. Two things likely changed between rounds: the round 2 items had more clear-cut failures, and my own labeling got more consistent after working through round 1's disagreements. I can't separate those two with this design. Without the v1 rerun on round 2, I would have credited the rubric with the whole jump.
2. **Specific rules beat general ones.** The rules that moved numbers were concrete: how to measure lateness from 8pm, which remedies the policy actually offers, and what counts as a clear next step. Round 1 had 28 disagreements I traced to rubric gaps; round 2 had 4.
3. **The judges caught my mistakes.** In round 1, 7 of the 43 items with a disagreement were errors in my own labels, usually where all three judges agreed. I kept those labels unchanged so the round 1 baseline stayed honest, and reported them instead.
4. **Gemini went easier on Google-written replies, in both rounds.** Compared with my labels, Gemini scored replies from Google's model 0.84 points closer than other replies in round 1, and 0.41 points closer in round 2. Claude and GPT showed no consistent gap. With about 17 items per group per round, this is a lead worth testing on more data, not a conclusion.
5. **What's left is mostly judges being strict about tone.** Of 27 round 2 items with any disagreement, 18 were judge errors and 10 differed only on Tone. Only 9 items had a different Pass/Fail verdict.
6. **More rules can make a judge stricter, not better.** With v2, Gemini's false alarms rose from 5 to 7 of 23 passing replies, and its verdict kappa dipped slightly. Claude's and GPT's held steady or improved.

**The judge I'd use:** Claude Sonnet, with rubric v2. It agreed with me on 94% of round 2 verdicts (kappa 0.88), caught 27 of 27 failures, and flagged 3 of 23 good replies.

## Limitations

- Small samples: 50 items per round, about 17 per group in the self-preference check.
- One labeler. I can't measure how consistent my own labels are without a second person labeling the same items.
- I labeled round 2 after studying round 1's disagreements, so my labels may have moved toward the judges' reading.
- The message generator (Claude Haiku) is from the same company as the Claude judge. Claude's agreement on handwritten vs generated messages showed no consistent gap across rounds.
- Resolution kappa is not meaningful in round 2: I gave almost every reply a 3, and kappa breaks down when one score dominates. Exact agreement on Resolution was 86% to 98%.

## What I'd do next

- Fix the 4 remaining rubric gaps: whether "you're eligible for credit" counts as committing to it, whether agents may offer a choice of refund method, how to score template text that replaces a needed answer, and late-box card refunds.
- Have a second person label 20 items, to measure human agreement as a ceiling for the judges.
- Rerun the self-preference check on a larger, balanced set.
