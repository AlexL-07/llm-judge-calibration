"""Compare the AI judges with the gold labels for one round.

Usage:
    python analysis/analyze.py --round 1
    python analysis/analyze.py --round 1 --exclude G-late_box-09   # leave out bad items

Reads:   data/round{N}_gold.csv, data/round{N}_judge_outputs.csv, data/round{N}_items.csv
Writes:  analysis/round{N}_report.md          (the numbers, ready to read or paste)
         analysis/round{N}_disagreements.csv  (every item where a judge differs from gold)

The disagreements file is the input to the rubric fix: read each row, tag the
cause in its blank "cause" column (rubric_gap, judge_error, gold_error, or
ambiguous), and use the rubric_gap rows to write rubric v2.
"""

import argparse
from pathlib import Path

import pandas as pd
from sklearn.metrics import cohen_kappa_score

ROOT = Path(__file__).resolve().parent.parent
DIMS = ["accuracy", "resolution", "tone"]
SCORE_COLS = DIMS + ["verdict"]


def load(round_n, exclude=()):
    gold = pd.read_csv(ROOT / f"data/round{round_n}_gold.csv", dtype=str)
    judges = pd.read_csv(ROOT / f"data/round{round_n}_judge_outputs.csv", dtype=str)
    items = pd.read_csv(ROOT / f"data/round{round_n}_items.csv", dtype=str)
    unknown = sorted(set(exclude) - set(gold["item_id"]))
    if unknown:
        raise SystemExit(f"--exclude names items not in round {round_n}: {', '.join(unknown)}")
    gold, judges, items = (df[~df["item_id"].isin(exclude)] for df in (gold, judges, items))
    for df in (gold, judges):
        for d in DIMS:
            df[d] = pd.to_numeric(df[d], errors="coerce")
        df["verdict"] = df["verdict"].fillna("").str.strip().str.capitalize()
        df.loc[~df["verdict"].isin(["Pass", "Fail"]), "verdict"] = None
    unlabeled = gold[gold[SCORE_COLS].isna().any(axis=1)]["item_id"].tolist()
    if unlabeled:
        raise SystemExit(f"{len(unlabeled)} gold rows are incomplete: {', '.join(unlabeled[:10])}")
    return gold, judges, items


def kappa(a, b, weights="linear"):
    """Weighted Cohen's kappa. Returns None when it can't be computed
    (for example, when one side gave the same score to every item)."""
    try:
        k = cohen_kappa_score(a, b, weights=weights, labels=sorted(set(a) | set(b)))
        return None if pd.isna(k) else k
    except ValueError:
        return None


def fmt(x, pct=False):
    if x is None or pd.isna(x):
        return "n/a"
    return f"{x:.0%}" if pct else f"{x:.2f}"


def table(rows, headers):
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--round", type=int, required=True)
    parser.add_argument("--exclude", nargs="+", default=[], help="Item IDs to leave out (bad items)")
    args = parser.parse_args()
    r = args.round

    gold, judges, items = load(r, args.exclude)
    # Parse failures are reported, then left out of the agreement numbers.
    failed = judges[judges[SCORE_COLS].isna().any(axis=1)]
    ok = judges.drop(failed.index)
    m = ok.merge(gold[["item_id"] + SCORE_COLS], on="item_id", suffixes=("", "_gold"))
    m = m.merge(items[["item_id", "source", "topic", "reply_style", "reply_model"]], on="item_id", how="left")
    judge_names = sorted(m["judge"].unique())

    lines = [f"# Round {r} results", ""]
    if args.exclude:
        lines.append(f"Excluded as bad items: {', '.join(args.exclude)}.\n")
    lines.append(f"{len(gold)} items, {len(judge_names)} judges. "
                 f"Gold: {(gold['verdict'] == 'Pass').sum()} Pass, {(gold['verdict'] == 'Fail').sum()} Fail.")
    if len(failed):
        lines.append(f"\n{len(failed)} judge outputs could not be read and are left out: "
                     + ", ".join(f"{a} ({b})" for a, b in failed[["item_id", "judge"]].values[:10]))

    # 1. Headline: agreement with gold
    rows = []
    for j in judge_names:
        g = m[m["judge"] == j]
        row = [j, len(g)]
        for d in DIMS:
            row.append(f"{fmt((g[d] == g[d + '_gold']).mean(), True)} / {fmt(kappa(g[d + '_gold'], g[d]))}")
        row.append(fmt((g["verdict"] == g["verdict_gold"]).mean(), True))
        row.append(fmt(kappa(g["verdict_gold"], g["verdict"], weights=None)))
        rows.append(row)
    lines += ["", "## Agreement with gold", "",
              "Each dimension cell is exact agreement / weighted kappa. Kappa corrects for agreement by chance: "
              "above 0.6 is usually read as substantial, below 0.4 as weak.", "",
              table(rows, ["Judge", "Items", "Accuracy", "Resolution", "Tone", "Verdict agree", "Verdict kappa"])]

    # 2. Failures caught and false alarms
    rows = []
    for j in judge_names:
        g = m[m["judge"] == j]
        gold_fail, gold_pass = g[g["verdict_gold"] == "Fail"], g[g["verdict_gold"] == "Pass"]
        caught = (gold_fail["verdict"] == "Fail").sum()
        false_alarm = (gold_pass["verdict"] == "Fail").sum()
        rows.append([j, f"{caught} of {len(gold_fail)}", f"{false_alarm} of {len(gold_pass)}"])
    lines += ["", "## Failures caught", "",
              "Caught: gold says Fail and the judge also said Fail. False alarm: gold says Pass, judge said Fail.", "",
              table(rows, ["Judge", "Failures caught", "False alarms"])]

    # 3. Leniency
    rows = [[j] + [f"{(m[m['judge'] == j][d] - m[m['judge'] == j][d + '_gold']).mean():+.2f}" for d in DIMS]
            for j in judge_names]
    lines += ["", "## Leniency", "",
              "Average judge score minus gold score. Positive means the judge grades easier than I do.", "",
              table(rows, ["Judge"] + [d.capitalize() for d in DIMS])]

    # 4. Judge vs judge
    rows = []
    wide = m.pivot_table(index="item_id", columns="judge", values="verdict", aggfunc="first")
    for i, a in enumerate(judge_names):
        for b in judge_names[i + 1:]:
            both = wide[[a, b]].dropna()
            rows.append([f"{a} vs {b}", fmt((both[a] == both[b]).mean(), True)])
    lines += ["", "## Judge vs judge (verdict)", "", table(rows, ["Pair", "Agreement"])]

    # 5. Self-preference: does each judge go easier on replies its own company wrote?
    rows = []
    for j in judge_names:
        g = m[m["judge"] == j].copy()
        g["diff"] = sum(g[d] - g[d + "_gold"] for d in DIMS)
        own, other = g[g["reply_model"] == j], g[g["reply_model"] != j]
        rows.append([j, f"{own['diff'].mean():+.2f} (n={len(own)})", f"{other['diff'].mean():+.2f} (n={len(other)})"])
    lines += ["", "## Self-preference check", "",
              "Average (judge total minus gold total) across the 3 dimensions, split by who wrote the reply. "
              "If a judge is noticeably more positive on its own company's replies, that is self-preference. "
              "With about 17 items per group, treat small gaps as noise.", "",
              table(rows, ["Judge", "Own company's replies", "Other replies"])]

    # 6. Seed vs generated (the Claude judge shares a company with the message generator)
    rows = []
    for j in judge_names:
        g = m[m["judge"] == j]
        row = [j]
        for src in ("seed", "generated"):
            s = g[g["source"] == src]
            row.append(f"{fmt((s['verdict'] == s['verdict_gold']).mean(), True)} (n={len(s)})")
        rows.append(row)
    lines += ["", "## Seed vs generated messages (verdict agreement)", "",
              table(rows, ["Judge", "Handwritten seeds", "Haiku-generated"])]

    # 7. By topic: where disagreement concentrates
    rows = []
    for topic, g in m.groupby("topic"):
        rows.append([topic, g["item_id"].nunique(), (g["verdict"] == g["verdict_gold"]).mean(),
                     (g["accuracy"] == g["accuracy_gold"]).mean()])
    rows.sort(key=lambda x: (x[2], x[3]))
    rows = [[a, b, fmt(c, True), fmt(e, True)] for a, b, c, e in rows]
    lines += ["", "## By topic (all judges pooled)", "",
              "Lowest agreement first. These topics are where to look for rubric gaps.", "",
              table(rows, ["Topic", "Items", "Verdict agree", "Accuracy agree"])]

    report = ROOT / f"analysis/round{r}_report.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Disagreements file: one row per item and judge where anything differs.
    diff_mask = sum((m[c] != m[c + "_gold"]).astype(int) for c in SCORE_COLS) > 0
    d = m[diff_mask].copy()
    d["n_judges_disagreeing"] = d.groupby("item_id")["judge"].transform("count")
    def show(v):
        return str(int(v)) if isinstance(v, float) else str(v)
    d["what_differs"] = d.apply(lambda x: ", ".join(
        f"{c} {show(x[c + '_gold'])}->{show(x[c])}" for c in SCORE_COLS if x[c] != x[c + "_gold"]), axis=1)
    d = d.merge(gold[["item_id", "reason"]].rename(columns={"reason": "gold_reason"}), on="item_id")
    d["cause"] = ""
    cols = ["item_id", "topic", "judge", "n_judges_disagreeing", "what_differs",
            "gold_reason", "reason", "cause"]
    d = d.rename(columns={"reason": "judge_reason"})
    cols[cols.index("reason")] = "judge_reason"
    d.sort_values(["n_judges_disagreeing", "item_id", "judge"], ascending=[False, True, True])[cols].to_csv(
        ROOT / f"analysis/round{r}_disagreements.csv", index=False, encoding="utf-8")

    print("\n".join(lines))
    print(f"\nWrote {report.relative_to(ROOT)} and analysis/round{r}_disagreements.csv "
          f"({d['item_id'].nunique()} items with at least one disagreement)")


if __name__ == "__main__":
    main()
