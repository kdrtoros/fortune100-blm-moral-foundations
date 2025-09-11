import re
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------- CONFIG ----------
INPATH = r"C:\Users\kdrto\Downloads\fortune-100-tweets.csv"  
OUTDIR = Path(".")                                           
START, END = "2020-05-25", "2020-07-26"  

MFD = {
    "care": {"care","caring","harm","hurt","violence","protect","safety","safe"},
    "fairness": {"fair","unfair","justice","equal","equality","inequal","rights","discriminate"},
    "loyalty": {"loyal","ally","allies","solidarity","together","unity","betray"},
    "authority": {"law","order","police","officer","authority","respect"},
    "purity": {"pure","clean","contaminate","impure","corrupt"},
}
FOUNDATIONS = list(MFD.keys())
CATEGORY_COLS = ["Racial Justice","BLM","Juneteenth","Money"]  


def tokenize(text: str):
    text = str(text).lower()
    text = re.sub(r"https?://\S+", " ", text)  
    text = re.sub(r"[@#]\w+", " ", text)       
    text = re.sub(r"[^a-z\s]", " ", text)      
    return [t for t in text.split() if t]

def score_foundations(tokens):
    counts = {f: 0 for f in FOUNDATIONS}
    for w in tokens:
        for f, vocab in MFD.items():
            if w in vocab:
                counts[f] += 1
    return counts

df = pd.read_csv(INPATH, encoding="utf-8")
if "Datetime" not in df.columns or "Text" not in df.columns:
    raise ValueError("Expected columns 'Datetime' and 'Text' not found. Check the file headers.")

df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce", utc=True)
df = df.dropna(subset=["Datetime"])
df = df[(df["Datetime"] >= START) & (df["Datetime"] < END)].copy()

for c in CATEGORY_COLS:
    if c in df.columns:
        df[c] = df[c].astype(str).str.strip().str.lower().isin(["1","true","t","yes","y"]).astype(int)

rows = []
for _, r in df.iterrows():
    toks = tokenize(r["Text"])
    s = score_foundations(toks)
    s["month"] = r["Datetime"].to_period("M").to_timestamp()
    for c in CATEGORY_COLS:
        if c in df.columns:
            s[c] = r[c]
    rows.append(s)

scored = pd.DataFrame(rows)

monthly_counts = scored.groupby("month")[FOUNDATIONS].sum()
monthly_totals = monthly_counts.sum(axis=1).replace(0, pd.NA)
monthly_share = (monthly_counts.T / monthly_totals).T  # proportion per month
monthly_share = monthly_share.fillna(0)

monthly_counts.to_csv(OUTDIR / "f100_monthly_foundation_counts.csv")
monthly_share.to_csv(OUTDIR / "f100_monthly_foundation_shares.csv")

if any(c in scored.columns for c in CATEGORY_COLS):
    cat_monthly = scored.groupby("month")[[c for c in CATEGORY_COLS if c in scored.columns]].sum()
    cat_monthly.to_csv(OUTDIR / "f100_monthly_categories.csv")

ax = monthly_share.plot(kind="bar", stacked=True, figsize=(10,6))
ax.yaxis.set_major_formatter(lambda x,_: f"{x:.0%}")
plt.ylabel("Proportion (each month sums to 100%)", fontsize=12)
plt.xlabel("Month", fontsize=12)
plt.title("Relative Frequency of Moral Foundations in Fortune 100 Tweets (Monthly, 2020-05-25 to 2020-07-25)", fontsize=13)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTDIR / "f100_mfd_monthly_stacked.png", dpi=300)
plt.close()

plt.figure(figsize=(8,4.5))
plt.bar(monthly_counts.index.astype(str), monthly_counts.sum(axis=1))
plt.ylabel("Total Foundation Token Count", fontsize=12)
plt.xlabel("Month", fontsize=12)
plt.title("Volume of Moral-Foundation-Related Language per Month", fontsize=13)
plt.tight_layout()
plt.savefig(OUTDIR / "f100_mfd_monthly_volume.png", dpi=300)
plt.close()

if any(c in scored.columns for c in CATEGORY_COLS):
    present = [c for c in CATEGORY_COLS if c in scored.columns]
    cat_monthly = scored.groupby("month")[present].sum()
    ax = cat_monthly.plot(kind="bar", figsize=(10,5))
    plt.ylabel("Tweet Count", fontsize=12)
    plt.xlabel("Month", fontsize=12)
    plt.title("Monthly Counts by Dataset Label", fontsize=13)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUTDIR / "f100_monthly_labels.png", dpi=300)
    plt.close()

print("[done] Wrote CSVs and figures:",
      "f100_monthly_foundation_counts.csv,",
      "f100_monthly_foundation_shares.csv,",
      "f100_mfd_monthly_stacked.png,",
      "f100_mfd_monthly_volume.png",
      "(and f100_monthly_labels.png if label columns exist)")
