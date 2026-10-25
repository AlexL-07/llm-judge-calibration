"""Compare judge agreement across runs: round 1 vs round 2, and v1 vs v2 rubric
on the same round 2 items.

Usage:
    python analysis/compare.py 1 2:v1 2 --exclude G-late_box-09

Each run is ROUND or ROUND:TAG. "2:v1" reads data/round2_judge_outputs_v1.csv,
the round 2 items judged with the v1 rubric. --exclude drops bad items from
whichever round they belong to.

Writes: analysis/comparison.md
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze import DIMS, ROOT, SCORE_COLS, fmt, kappa, load, table  # noqa: E402

LABELS = {"1": "Round 1, rubric v1", "2:v1": "Round 2, rubric v1", "2": "Round 2, rubric v2"}


def run_metrics(spec, exclude):
    rnd, _, tag = spec.partition(":")
    gold, judges, _ = load(int(rnd), [e for e in exclude if e in set(load_ids(int(rnd)))], tag)
    ok = judges.dropna(subset=SCORE_COLS)
    m = ok.merge(gold[["item_id"] + SCORE_COLS], on="item_id", suffixes=("", "_gold"))
    out = {"n": len(gold), "fails": int((gold["verdict"] == "Fail").sum())}
    for j, g in m.groupby("judge"):
        gf, gp = g[g["verdict_gold"] == "Fail"], g[g["verdict_gold"] == "Pass"]
        out[j] = {
            "verdict_agree": (g["verdict"] == g["verdict_gold"]).mean(),
            "verdict_kappa": kappa(g["verdict_gold"], g["verdict"], weights=None),
            **{f"{d}_kappa": kappa(g[d + "_gold"], g[d]) for d in DIMS},
            "caught": (gf["verdict"] == "Fail").mean() if len(gf) else None,
            "false_alarm": (gp["verdict"] == "Fail").mean() if len(gp) else None,
        }
    return out


def load_ids(rnd):
    import pandas as pd
    return pd.read_csv(ROOT / f"data/round{rnd}_gold.csv", dtype=str)["item_id"].tolist()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("runs", nargs="+", help="e.g. 1 2:v1 2")
    parser.add_argument("--exclude", nargs="+", default=[])
    args = parser.parse_args()

    results = {s: run_metrics(s, args.exclude) for s in args.runs}
    names = [LABELS.get(s, s) for s in args.runs]
    judges = sorted({j for r in results.values() for j in r if j not in ("n", "fails")})

    lines = ["# Judge agreement across runs", ""]
    lines.append(table([[LABELS.get(s, s), r["n"], r["fails"]] for s, r in results.items()],
                       ["Run", "Items", "Gold Fails"]))
    metrics = [
        ("verdict_kappa", "Verdict kappa", False),
        ("verdict_agree", "Verdict agreement", True),
        ("accuracy_kappa", "Accuracy kappa", False),
        ("resolution_kappa", "Resolution kappa", False),
        ("tone_kappa", "Tone kappa", False),
        ("caught", "Gold Fails the judge also failed", True),
        ("false_alarm", "Gold Passes the judge failed (false alarms)", True),
    ]
    for key, title, pct in metrics:
        rows = [[j] + [fmt(results[s].get(j, {}).get(key), pct) for s in args.runs] for j in judges]
        lines += ["", f"## {title}", "", table(rows, ["Judge"] + names)]
    lines += ["", "Kappa corrects for chance and for how many Fails each round has, so it is the fairest "
              "number to compare across rounds. Round 1 and round 2 use different items; the round 2 "
              "v1 vs v2 columns use the same items and the same gold labels, so that pair isolates "
              "the effect of the rubric change."]

    out = ROOT / "analysis/comparison.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nWrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
