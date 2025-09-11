import pandas as pd
import matplotlib.pyplot as plt

INPATH = "mfd_daily_summary.csv"

# load
df = pd.read_csv(INPATH, parse_dates=["day"])

# resample by week
weekly = df.set_index("day").resample("W").sum()

# normalize to proportions
shares = weekly.div(weekly.sum(axis=1), axis=0)

# plot weekly foundation shares
shares.plot(marker="o")
plt.title("Relative Frequency of Moral Foundations in Tweets (Weekly Averages)", fontsize=14)
plt.ylabel("Proportion of Foundation-Related Tokens", fontsize=12)
plt.xlabel("Week", fontsize=12)
plt.legend(title="Moral Foundation", fontsize=10)
plt.tight_layout()
plt.savefig("mfd_weekly.png", dpi=300)
plt.show()

# also plot total volume over time
weekly.sum(axis=1).plot(marker="o")
plt.title("Volume of Moral-Foundation-Related Language in Tweets", fontsize=14)
plt.ylabel("Total Foundation Token Count", fontsize=12)
plt.xlabel("Week", fontsize=12)
plt.tight_layout()
plt.savefig("mfd_volume.png", dpi=300)
plt.show()
