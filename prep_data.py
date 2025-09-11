import pandas as pd
INPATH = r"C:\Users\kdrto\Downloads\fortune-100-tweets.csv"
OUTPATH = "blm_2020_may_jun.csv"
df = pd.read_csv(INPATH, encoding="utf-8")
print("[info] columns in file:", list(df.columns))
df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")
mask = (df["Datetime"] >= "2020-05-01") & (df["Datetime"] <= "2020-06-30")
df = df.loc[mask]
print(f"[done] saved {len(df)} rows to {OUTPATH}")
df.to_csv(OUTPATH, index=False)
