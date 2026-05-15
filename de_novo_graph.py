# ============================
# Imports
# ============================
import re
import argparse
import yaml
import pandas as pd
import matplotlib.pyplot as plt

# ============================
# Argument parser
# ============================
parser = argparse.ArgumentParser(
    description="Plotting the de novo mutation counts"
)

parser.add_argument("--config", "--yaml",
                    required=True,
                    help="YAML configuration file")

parser.add_argument("--input", "--counts",
                    required=True,
                    help="Input CSV file with mutation counts")

parser.add_argument("--output", "--output_pdf",
                    required=True,
                    help="Output PDF file")

args = parser.parse_args()

yaml_file = args.config
csv_file = args.input
output_pdf = args.output

# ============================
# Load YAML
# ============================
with open(yaml_file, "r") as f:
    config = yaml.safe_load(f)

species = config.get("SPECIES")
if species is None:
    raise ValueError("YAML file does not contain SPECIES field")

# ============================
# Load CSV
# ============================
df = pd.read_csv(csv_file)

# First column = labels
labels = df.iloc[:, 1].astype(str)

# CLEAN LABELS: remove parentheses + content inside
clean_labels = labels.str.replace(r"\s*\(.*?\)", "", regex=True)

# Last column = counts
counts = df.iloc[:, -1]

# ============================
# Plot
# ============================
plt.figure(figsize=(13, 7))

# 3) Use cleaned string labels on x-axis (no numbers)
plt.plot(clean_labels, counts, color="deeppink", linewidth=2)

# Square-plus marker
plt.scatter(clean_labels, counts, marker='P', s=120, color="deeppink")

# 1) Add numbers next to each dot, offset so the line doesn’t cover them

for x, y in zip(clean_labels, counts):
    plt.annotate(
        str(y),            # the number to print
        xy=(x, y),         # anchor at the dot
        xytext=(5, 5),     # shift 5 points to the right and up
        textcoords='offset points',
        ha='left', va="bottom",       # text extends to the top right of the dot
        fontsize=10,
        color="black"
    )

plt.xticks(ticks=range(len(clean_labels)), labels=clean_labels, rotation=45, ha="right")
plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5, alpha=0.6)
plt.title(f"{species}: De Novo Mutations")
plt.xlabel("Filters")
plt.ylabel("Count")
plt.tight_layout()

# ============================
# Save PDF
# ============================
plt.savefig(output_pdf)
print("Saved plot to:", output_pdf)
