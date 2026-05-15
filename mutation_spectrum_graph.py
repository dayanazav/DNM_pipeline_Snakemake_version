# ---------------------------------------
# Imports
# ---------------------------------------
import argparse
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# ---------------------------------------
# Mutation order + headers
# ---------------------------------------
ORDER = ["CA", "CG", "CT", "AT", "AG", "AC"]
HEADERS = [
    "C>A (G>T)",
    "C>G (G>C)",
    "C>T (G>A)",
    "T>A (A>T)",
    "T>C (A>G)",
    "T>G (A>C)"
]

# ---------------------------------------
# Helpers
# ---------------------------------------
def detect_type(filename):
    m = re.search(r'([ACGT]{2})', filename)
    if not m:
        raise ValueError(f"Cannot detect mutation type in: {filename}")
    return m.group(1)

def read_digit(path):
    with open(path, "r") as f:
        return int(f.read().strip())

def plot_bar(values, errors, ylabel, title, output):
    plt.figure(figsize=(10, 6))
    plt.bar(HEADERS, values, yerr=errors, capsize=5, color="orchid")
    plt.grid(True, axis="y", linestyle="--", alpha=0.6)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel(ylabel)
    plt.xlabel("Mutation Type")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output)
    plt.close()

# ---------------------------------------
# Argparse
# ---------------------------------------
parser = argparse.ArgumentParser(description="Mutation Spectrum Plotter")

parser.add_argument("--config", required=True, help="YAML config file")
parser.add_argument("--files", nargs="+", required=True, help="List of spectrum txt files")
parser.add_argument("--mode", choices=["counts", "percentages", "both"], required=True)
parser.add_argument("--output_prefix", required=True, help="Prefix for output PDFs")

args = parser.parse_args()

# ---------------------------------------
# Load YAML
# ---------------------------------------
with open(args.config, "r") as f:
    config = yaml.safe_load(f)

species = config.get("SPECIES")

# ---------------------------------------
# Extract counts in correct order
# ---------------------------------------
counts = []

for mut in ORDER:
    match = [f for f in args.files if mut in f]
    if len(match) != 1:
        raise ValueError(f"Expected exactly one file for {mut}, found {match}")
    counts.append(read_digit(match[0]))

total = sum(counts)
percentages = [c / total for c in counts]

# Confidence intervals
ci_counts = [1.96 * np.sqrt(c) for c in counts]
ci_percent = [1.96 * np.sqrt((p * (1 - p)) / total) for p in percentages]

# ---------------------------------------
# Build DataFrame
# ---------------------------------------
df = pd.DataFrame({
    "Mutation Type": HEADERS,
    "Count": counts,
    "Percentage": percentages
})

print("\nMutation Spectrum Table:")
print(df, "\n")

# ---------------------------------------
# Plot(s)
# ---------------------------------------
title = f"{species}: Mutation Spectrum"

if args.mode in ("counts", "both"):
    plot_bar(
        counts,
        ci_counts,
        ylabel="Count",
        title=title,
        output=f"{args.output_prefix}_counts.pdf"
    )

if args.mode in ("percentages", "both"):
    plot_bar(
        percentages,
        ci_percent,
        ylabel="Percentage",
        title=title,
        output=f"{args.output_prefix}_percentages.pdf"
    )
