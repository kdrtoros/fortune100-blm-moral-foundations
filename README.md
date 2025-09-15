# fortune100-blm-moral-foundations

Analysis of Fortune 100 companies’ tweets following George Floyd’s death (**May 26 – July 25, 2020**) using **Moral Foundations Theory**.
Includes Python scripts for preprocessing, scoring, and visualization of corporate responses to the #BlackLivesMatter movement.

---

## 📄 Dataset

Fortune 100 Tweet Dataset (BLM)
Original dataset and report available at:
👉 [https://www.kmcelwee.com/fortune-100-blm-report/site/](https://www.kmcelwee.com/fortune-100-blm-report/site/)

---

## 🛠 Repository Contents

* `prep_data.py` → filters raw dataset to focus on selected date window and required columns
* `mfd_analyze.py` → scores tweets using a Moral Foundations lexicon and aggregates daily/weekly counts
* `f100_weekly_all.py` → produces **weekly plots and CSV outputs** (stacked bar, lines, volume)
* `f100_monthly.py` → produces **monthly visualizations and summaries**
* `plot_mfd.py` → utility script for alternative plot styles
* `requirements.txt` → Python packages required to run the analysis
* `figures/` → saved plots for reporting (sample outputs included)

---

## 🔍 How to Use

### 1️⃣ Clone the repository

```bash
git clone https://github.com/kdrtoros/fortune100-blm-moral-foundations.git
cd fortune100-blm-moral-foundations
```

### 2️⃣ Set up a virtual environment (recommended)

```bash
python -m venv .venv
# On macOS/Linux
source .venv/bin/activate
# On Windows
.\.venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Place the dataset

Download from the official source:
👉 [Fortune 100 BLM Dataset](https://www.kmcelwee.com/fortune-100-blm-report/site/)

Save as:

```
fortune-100-tweets.csv
```

in the project root folder, or adjust the dataset path in the scripts.

### 5️⃣ Run the analysis

**Weekly outputs + plots:**

```bash
python f100_weekly_all.py
```

**Monthly outputs + plots:**

```bash
python f100_monthly.py
```

### 6️⃣ View results

* Figures will be saved in the `figures/` folder (create it if missing)
* CSV summaries will be written to the project root

---

## 📊 Sample Outputs

* `figures/f100_mfd_weekly_lines.png` → weekly shares of moral foundations
* `figures/f100_mfd_monthly_stacked.png` → monthly stacked bar chart (each month = 100%)

---

## 🧮 Interpretation

* **Share** = proportion of foundation-related tokens relative to all foundation tokens in that period
* **Volume** = raw count of foundation tokens
* Lexicon is minimal (can be expanded with synonyms/phrases for more coverage)

---

## ⚠️ Caveats & Limitations

* Lexicon may miss expressions (slang, multi-word phrases, etc.)
* Tweets are only from Fortune 100 companies — not general public discourse
* Dataset categories are manually coded, but foundation scores are automated and approximate
* Volume counts vary with tweet length (longer tweets = more tokens)

---

## 💡 Potential Extensions

* Expand to full **Moral Foundations Dictionary (MFD)** with phrase matching
* Compare companies (which firms emphasize Care vs Fairness, etc.)
* Explore correlation between foundations and engagement (likes/retweets)
* Extend timeline beyond May–July if larger datasets become available

---

## 🚀 License & Attribution

This work is open-source. Please cite the original dataset:

> McElwee, K. *Fortune 100 BLM Report*.
> Available at: [https://www.kmcelwee.com/fortune-100-blm-report/site/](https://www.kmcelwee.com/fortune-100-blm-report/site/)

