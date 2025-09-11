import pandas as pd
from collections import Counter

INPATH = "blm_2020_may_jun.csv"
OUTPATH = "mfd_daily_summary.csv"


print("[info] loading dataset...")
df = pd.read_csv(INPATH, parse_dates=["Datetime"])


MFD = {
    "care": ["help", "harm", "safe", "hurt"],
    "fairness": ["equal", "justice", "rights", "fair"],
    "loyalty": ["loyal", "betray", "group", "together"],
    "authority": ["obey", "duty", "respect", "law"],
    "purity": ["pure", "clean", "corrupt", "sin"],
}

def score_text(text):
    text = str(text).lower()
    counts = {cat: 0 for cat in MFD}
    for cat, words in MFD.items():
        for w in words:
            counts[cat] += text.count(w)
    return counts

rows = []
for _, r in df.iterrows():
    scores = score_text(r["Text"])
    row = {"day": r["Datetime"].date()} | scores
    rows.append(row)

scored = pd.DataFrame(rows)


daily = scored.groupby("day").sum().reset_index()
print(f"[done] wrote {OUTPATH} with {len(daily)} days")
daily.to_csv(OUTPATH, index=False)
