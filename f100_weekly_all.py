# f100_weekly_all.py
import re
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -------- CONFIG --------
INPATH = r"C:\Users\kdrto\Downloads\fortune-100-tweets.csv"  
OUTDIR = Path(".")                                          
START, END = "2020-05-26", "2020-07-26"  
MFD = {
    "care": {"care","caring","harm","hurt","violence","protect","safety","safe"},
    "fairness": {"fair","unfair","justice","equal","equality","inequal","rights","discriminate"},
    "loyalty": {"loyal","ally","allies","solidarity","together","unity","betray"},
    "authority": {"law","order","police","officer","authority","respect"},
    "purity": {"pure","clean","contaminate","impure","corrupt"},
}
FOUNDATIONS = list(MFD.keys())
# ------------------------

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
    raise ValueError("Expected columns 'Datetime' and 'Text' not found in the CSV.")

df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce", utc=True)
df = df.dropna(subset=["Datetime"])
df = df[(df["Datetime"] >= START) & (df["Datetime"] < END)].copy()

rows = []
for _, r in df.iterrows():
    toks = tokenize(r["Text"])
    s = score_foundations(toks)
    s["week"] = r["Datetime"].to_period("W-SUN").to_timestamp()
    rows.append(s)

scored = pd.DataFrame(rows)

weekly_counts = scored.groupby("week")[FOUNDATIONS].sum()
weekly_counts.index = pd.to_datetime(weekly_counts.index).sort_values()

weekly_totals = weekly_counts.sum(axis=1).replace(0, pd.NA)
weekly_shares = (weekly_counts.T / weekly_totals).T.fillna(0)

weekly_counts.to_csv(OUTDIR / "f100_weekly_foundation_counts.csv")
weekly_shares.to_csv(OUTDIR / "f100_weekly_foundation_shares.csv")


ax = weekly_shares.plot(kind="bar", stacked=True, figsize=(12,6))
ax.yaxis.set_major_formatter(lambda x,_: f"{x:.0%}")
plt.ylabel("Share of Tweets Containing Foundation-Related Language", fontsize=12)
plt.xlabel("Week (Ending Sunday)", fontsize=12)
plt.title("Relative Frequency of Moral Foundations in Fortune 100 Tweets\n(May 26 – July 25, 2020)", fontsize=13)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(OUTDIR / "f100_mfd_weekly_stacked.png", dpi=300)
plt.close()

plt.figure(figsize=(12,6))
for f in FOUNDATIONS:
    plt.plot(weekly_shares.index, weekly_shares[f], marker="o", linewidth=2, label=f.title())
plt.gca().yaxis.set_major_formatter(lambda x,_: f"{x:.0%}")
plt.ylabel("Share of Tweets Containing Foundation-Related Language", fontsize=12)
plt.xlabel("Week (Ending Sunday)", fontsize=12)
plt.title("Relative Frequency of Moral Foundations in Tweets (Weekly Averages)", fontsize=13)
plt.grid(True, alpha=0.3)
plt.legend(title="Moral Foundation")
plt.tight_layout()
plt.savefig(OUTDIR / "f100_mfd_weekly_lines.png", dpi=300)
plt.close()

plt.figure(figsize=(12,4.5))
plt.bar(weekly_counts.index.astype(str), weekly_counts.sum(axis=1))
plt.ylabel("Number of Foundation-Related Tokens", fontsize=12)
plt.xlabel("Week (Ending Sunday)", fontsize=12)
plt.title("Volume of Moral-Foundation-Related Language in Tweets\n(May 26 – July 25, 2020)", fontsize=13)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(OUTDIR / "f100_mfd_weekly_volume.png", dpi=300)
plt.close()

print("[done] wrote:",
      "f100_weekly_foundation_counts.csv,",
      "f100_weekly_foundation_shares.csv,",
      "f100_mfd_weekly_stacked.png,",
      "f100_mfd_weekly_lines.png,",
      "f100_mfd_weekly_volume.png")
