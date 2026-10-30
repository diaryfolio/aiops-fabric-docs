"""Render the documentation's synthetic chart with optional Matplotlib (not a build dependency)."""

import argparse
import csv
import json
import os
import tempfile
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/assets/data/reorganisation-performance-example.csv"
OUTPUT = ROOT / "docs/assets/images/reorganisation-performance.svg"
DEPARTMENTS = ("Retail", "Enterprise", "Services")
MONTHS = tuple(range(1, 7))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", type=Path, help="Also write a PNG for visual review")
    args = parser.parse_args()
    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "viewsense-docs-mpl"))
    os.environ.setdefault(
        "XDG_CACHE_HOME", str(Path(tempfile.gettempdir()) / "viewsense-docs-cache"))
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator

    with SOURCE.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    facts = {}
    for row in rows:
        key = int(row["month"]), row["department"]
        if key in facts:
            raise ValueError("Duplicate month/department in the synthetic fixture")
        facts[key] = {field: Decimal(row[field]) for field in (
            "reorganisation_departures", "average_fte", "net_revenue_gbp", "payroll_cost_gbp")}
    if set(facts) != {(month, department) for month in MONTHS for department in DEPARTMENTS}:
        raise ValueError("The example needs all six months for all three departments")
    if any(not value.is_finite() or value < 0 for record in facts.values()
           for value in record.values()):
        raise ValueError("Invalid synthetic value")
    if any(record["average_fte"] <= 0 for record in facts.values()):
        raise ValueError("A positive FTE denominator is required")

    monthly = {month: {field: sum(facts[month, dept][field] for dept in DEPARTMENTS)
                       for field in next(iter(facts.values()))} for month in MONTHS}
    revenue = [monthly[month]["net_revenue_gbp"] for month in MONTHS]
    fte = [monthly[month]["average_fte"] for month in MONTHS]
    per_fte = [value / people for value, people in zip(revenue, fte, strict=True)]

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 12,
        "svg.fonttype": "none", "svg.hashsalt": "viewsense-reorganisation-example-v1",
        "text.color": "#183234", "axes.labelcolor": "#183234",
        "xtick.color": "#526974", "ytick.color": "#526974",
    })
    fig, axes = plt.subplots(3, 1, figsize=(7.2, 8.4), sharex=True)
    fig.patch.set_facecolor("#ffffff")
    fig.subplots_adjust(top=.80, bottom=.16, left=.12, right=.96, hspace=.78)
    fig.suptitle("Reorganisation and financial performance", x=.12, ha="left",
                 y=.97, fontsize=15, fontweight="bold")
    fig.text(.12, .93, "Synthetic example · six complete reporting months", fontsize=11,
             color="#526974")

    bottom = [0.0] * len(MONTHS)
    colors = ("#0f766e", "#287db1", "#a06420")
    for department, color in zip(DEPARTMENTS, colors, strict=True):
        values = [float(facts[month, department]["reorganisation_departures"]) for month in MONTHS]
        axes[0].bar(MONTHS, values, bottom=bottom, width=.6, color=color, label=department)
        bottom = [previous + value for previous, value in zip(bottom, values, strict=True)]
    for month, value in zip(MONTHS, bottom, strict=True):
        axes[0].text(month, value + .35, str(int(value)), ha="center", fontsize=11)
    axes[0].set_ylim(0, max(bottom) * 1.25)
    axes[0].yaxis.set_major_locator(MaxNLocator(integer=True, nbins=4))
    axes[0].set_title("Confirmed reorganisation departures", loc="left", fontsize=12,
                      fontweight="bold", pad=32)
    axes[0].set_ylabel("People")
    axes[0].legend(loc="lower left", bbox_to_anchor=(-.01, 1.01), frameon=False,
                   ncol=3, fontsize=10.5, handlelength=1.2, columnspacing=1)

    axes[1].plot(MONTHS, [float(value / 1_000_000) for value in revenue],
                 marker="o", color="#0f766e", linewidth=2.2)
    axes[1].set_title("Company net revenue", loc="left", fontsize=12, fontweight="bold")
    axes[1].set_ylabel("£ million")
    axes[1].set_ylim(0, 14)
    axes[1].yaxis.set_major_locator(MaxNLocator(nbins=4))

    axes[2].plot(MONTHS, [float(value / 1_000) for value in per_fte],
                 marker="o", color="#287db1", linewidth=2.2)
    axes[2].set_title("Net revenue per average FTE · financial output proxy", loc="left",
                      fontsize=11.5, fontweight="bold")
    axes[2].set_ylabel("£ thousand")
    axes[2].set_ylim(0, 30)
    axes[2].yaxis.set_major_locator(MaxNLocator(nbins=4))

    for axis in axes:
        axis.set_axisbelow(True)
        axis.grid(axis="y", color="#dfe8eb", linewidth=.7)
        axis.spines[["top", "right"]].set_visible(False)
        axis.spines[["bottom", "left"]].set_color("#bdccd1")
        axis.set_xticks(MONTHS, [f"M{month}" for month in MONTHS])
        axis.tick_params(axis="x", labelbottom=True, length=0, pad=7)
        axis.tick_params(axis="y", length=0, pad=7)
    fig.text(.12, .035, "M1 = oldest month · M6 = latest complete month\n"
             "These comparisons do not establish a causal effect of the reorganisation.",
             fontsize=10.5, color="#526974", linespacing=1.6)
    fig.savefig(OUTPUT, format="svg", metadata={
        "Date": None,
        "Title": "Synthetic reorganisation and financial performance comparison",
        "Description": "Monthly departures, company net revenue and revenue per average FTE. "
                       "Illustrative data, not observed company results or a causal estimate.",
    })
    if args.preview:
        fig.savefig(args.preview, dpi=130)
    plt.close(fig)

    def percentage(first, last):
        return str(((last / first - 1) * 100).quantize(Decimal("0.1")))

    summary = {
        "total_departures": int(sum(row["reorganisation_departures"] for row in facts.values())),
        "total_revenue_gbp": str(sum(revenue)),
        "total_payroll_gbp": str(sum(row["payroll_cost_gbp"] for row in facts.values())),
        "revenue_change_pct": percentage(revenue[0], revenue[-1]),
        "fte_change_pct": percentage(fte[0], fte[-1]),
        "revenue_per_fte_change_pct": percentage(per_fte[0], per_fte[-1]),
        "departments": {dept: {field: str(sum(facts[month, dept][field] for month in MONTHS))
                               for field in ("reorganisation_departures", "net_revenue_gbp",
                                             "payroll_cost_gbp")} for dept in DEPARTMENTS},
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
