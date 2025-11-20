"""
TITANIC DATASET - FULL EDA + PDF REPORT (VS CODE READY)
Run: python demo.py
Make sure Titanic_Dataset.csv is in SAME FOLDER as this file.
"""

# ------------------- IMPORTS -------------------
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF
from pathlib import Path

# ------------------- LOAD DATA -------------------
CSV_FILE = "Titanic-Dataset.csv"  # SAME folder me hona chahiye

try:
    df = pd.read_csv(CSV_FILE)
except:
    raise FileNotFoundError("❌ Titanic_Dataset.csv same folder me rakho bhai!")

print("✔ CSV Loaded:")
print(df.head())

# ------------------- BASIC EDA -------------------
OUTPUT_DIR = Path("output")
PLOT_DIR = OUTPUT_DIR / "plots"
OUTPUT_DIR.mkdir(exist_ok=True)
PLOT_DIR.mkdir(exist_ok=True)

df.info()
basic_stats = df.describe()
missing_data = df.isnull().sum()

# SAVE SUMMARY TEXT
summary_text = f"""
TITANIC DATASET - EDA SUMMARY
====================================
Rows: {df.shape[0]} | Columns: {df.shape[1]}

MISSING VALUES:
{missing_data.to_string()}

NUMERIC SUMMARY:
{basic_stats.to_string()}

Outcome:
Gain skill in finding patterns, trends, and anomalies.
"""

with open(OUTPUT_DIR / "summary.txt", "w") as f:
    f.write(summary_text)

# ------------------- VISUALS -------------------
sns.set_style("whitegrid")

# Pairplot
try:
    sns.pairplot(df.dropna(), hue="Survived")
    plt.savefig(PLOT_DIR / "pairplot.png", bbox_inches="tight")
    plt.close()
except:
    pass

# Heatmap
try:
    plt.figure(figsize=(8,6))
    sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.savefig(PLOT_DIR / "heatmap.png", bbox_inches="tight")
    plt.close()
except:
    pass

# Histogram
df.hist(figsize=(10,8), bins=30)
plt.tight_layout()
plt.savefig(PLOT_DIR / "histograms.png")
plt.close()

# Boxplot: Age vs Pclass
if "Pclass" in df.columns and "Age" in df.columns:
    sns.boxplot(x="Pclass", y="Age", data=df)
    plt.title("Age by Pclass (Boxplot)")
    plt.savefig(PLOT_DIR / "boxplot_age_pclass.png")
    plt.close()

# Scatterplot
if "Age" in df.columns and "Fare" in df.columns:
    sns.scatterplot(x="Age", y="Fare", hue=df["Survived"], data=df)
    plt.title("Age vs Fare (Survived)")
    plt.savefig(PLOT_DIR / "scatter_age_fare.png")
    plt.close()

print("✔ Plots Saved:", len(list(PLOT_DIR.glob('*.png'))))

# ------------------- PDF REPORT -------------------
pdf = FPDF()
pdf.add_page()

# Title
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "TITANIC EDA REPORT", align="C", ln=True)

# Summary
pdf.set_font("Arial", size=11)
pdf.multi_cell(0, 6, summary_text)

# Add images
for img in PLOT_DIR.glob("*.png"):
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Figure: {img.name}", ln=True)
    pdf.image(str(img), x=10, w=180)

final_pdf = OUTPUT_DIR / "Titanic_EDA_Report.pdf"
pdf.output(str(final_pdf))
print("✔ FINAL PDF GENERATED:", final_pdf)
