"""
Run the full analysis pipeline for "A Laboratory Test of Flow Trading."

Generates all tables (Tables 1-6, S1-S8) and figures (Figures 4-9, S1-S9)
for the main paper and supplemental appendix.

Robustness specifications (2s, 5s, 10s price intervals) are run automatically.
The default 5s outputs are the main paper results; 2s and 10s generate
supplemental Tables S2-S7.

Usage:
    python run.py

Output is written to output/tables/, output/figures/, and output/intermediate/.
"""

import subprocess
import sys
import os
import re
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.join(BASE_DIR, "code")
CONFIG_FILE = os.path.join(CODE_DIR, "config.py")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def run_interval(interval):
    """Run data.py with a specific price_interval_size."""
    print(f"\n{'='*60}")
    print(f"  Running analysis with price_interval_size = {interval}")
    print(f"{'='*60}\n")

    # Read config.py and set the interval
    with open(CONFIG_FILE, "r") as f:
        config_text = f.read()

    original_text = config_text
    config_text = re.sub(
        r"^price_interval_size\s*=\s*\d+",
        f"price_interval_size = {interval}",
        config_text,
        flags=re.MULTILINE,
    )
    with open(CONFIG_FILE, "w") as f:
        f.write(config_text)

    try:
        result = subprocess.run(
            [sys.executable, os.path.join(CODE_DIR, "data.py")],
            cwd=CODE_DIR,
        )
        if result.returncode != 0:
            print(f"\nERROR: data.py failed for interval {interval}")
            return False
    finally:
        # Always restore original config
        with open(CONFIG_FILE, "w") as f:
            f.write(original_text)

    return True


def copy_robustness_tables(interval):
    """Copy robustness regression/summary tables with supplemental naming."""
    tables_dir = os.path.join(OUTPUT_DIR, "tables")

    # Mapping: source filename (from interval-specific run) -> supplemental table name.
    # S3/S4/S6/S7 are written directly by the interval-specific data.py run.
    if interval == 10:
        renames = {
            "Table2_Summary_Market_T11-T20.tex": "TableS2_Summary_Market_10s.tex",
        }
    elif interval == 2:
        renames = {
            "Table2_Summary_Market_T11-T20.tex": "TableS5_Summary_Market_2s.tex",
        }
    else:
        return

    for src_name, dst_name in renames.items():
        src = os.path.join(tables_dir, src_name)
        dst = os.path.join(tables_dir, dst_name)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  Saved {dst_name}")


def generate_verification_tex():
    """Generate a LaTeX document that compiles all tables and figures."""
    tables_dir = os.path.join(OUTPUT_DIR, "tables")
    figures_dir = os.path.join(OUTPUT_DIR, "figures")
    verif_dir = os.path.join(OUTPUT_DIR, "verification")
    os.makedirs(verif_dir, exist_ok=True)

    # Ordered list of all paper outputs
    main_tables = [
        ("Table 1: Summary Statistics --- Traders' Behavior (T11--T20)", "Table1_Summary_Traders_T11-T20.tex"),
        ("Table 1: Summary Statistics --- Traders' Behavior (T1--T20)", "Table1_Summary_Traders_T1-T20.tex"),
        ("Table 2: Summary Statistics --- Market Performance (T11--T20)", "Table2_Summary_Market_T11-T20.tex"),
        ("Table 2: Summary Statistics --- Market Performance (T1--T20)", "Table2_Summary_Market_T1-T20.tex"),
        ("Table 3: Regression --- Trader Behavior Metrics", "Table3_Regression_Trader_Behavior.tex"),
        ("Table 4: Regression --- Price Volatility and Liquidity", "Table4_Regression_Price_Volatility.tex"),
        ("Table 5: Regression --- Volume", "Table5_Regression_Volume.tex"),
        ("Table 6: Regression --- Efficiency and Buyer-Seller Disparity", "Table6_Regression_Efficiency.tex"),
    ]

    supp_tables = [
        ("Table S1: Spearman Correlations", "TableS1_Spearman_Correlations.tex"),
        ("Table S2: Market Performance (10s intervals)", "TableS2_Summary_Market_10s.tex"),
        ("Table S3: Price Volatility Regression (10s)", "TableS3_Regression_Price_Volatility_10s.tex"),
        ("Table S4: Price Deviation Regression (10s)", "TableS4_Regression_Efficiency_10s.tex"),
        ("Table S5: Market Performance (2s intervals)", "TableS5_Summary_Market_2s.tex"),
        ("Table S6: Price Volatility Regression (2s)", "TableS6_Regression_Price_Volatility_2s.tex"),
        ("Table S7: Price Deviation Regression (2s)", "TableS7_Regression_Efficiency_2s.tex"),
        ("Table S8: Unweighted Price Statistics", "TableS8_Unweighted_Prices.tex"),
    ]

    main_figures = [
        ("Figure 4a: CDA Transaction Prices", "Figure4a_CDA_Prices.pdf"),
        ("Figure 4b: Flow30 Transaction Prices", "Figure4b_Flow30_Prices.pdf"),
        ("Figure 4c: Flow60 Transaction Prices", "Figure4c_Flow60_Prices.pdf"),
        ("Figure 5a: Trade Volume vs.\\ Period", "Figure5a_Volume.pdf"),
        ("Figure 5b: Realized Surplus vs.\\ Period", "Figure5b_Surplus.pdf"),
        ("Figure 6: Profit Distribution (CDF)", "Figure6_Profit_CDF.pdf"),
        ("Figure 7: CDF of $U_{max}$", "Figure7_Umax_CDF.pdf"),
        ("Figure 8: Cumulative Executed Volume", "Figure8_Cumulative_Volume.pdf"),
        ("Figure 9: CDF of Price-Range Width", "Figure9_Price_Range_CDF.pdf"),
    ]

    supp_figures = [
        ("Figure S1a: CDA Prices (All Groups)", "FigureS1a_CDA_Prices_All.pdf"),
        ("Figure S1b: Flow30 Prices (All Groups)", "FigureS1b_Flow30_Prices_All.pdf"),
        ("Figure S1c: Flow60 Prices (All Groups)", "FigureS1c_Flow60_Prices_All.pdf"),
        ("Figure S2a: CDA Trade Volume", "FigureS2a_CDA_Volume.pdf"),
        ("Figure S2b: CDA Realized Surplus", "FigureS2b_CDA_Surplus.pdf"),
        ("Figure S2c: Flow30 Trade Volume", "FigureS2c_Flow30_Volume.pdf"),
        ("Figure S2d: Flow30 Realized Surplus", "FigureS2d_Flow30_Surplus.pdf"),
        ("Figure S2e: Flow60 Trade Volume", "FigureS2e_Flow60_Volume.pdf"),
        ("Figure S2f: Flow60 Realized Surplus", "FigureS2f_Flow60_Surplus.pdf"),
        ("Figure S3: Profit Distribution (Last 10 Periods)", "FigureS3_Profit_CDF_Last10.pdf"),
        ("Figure S4a: CDA Contract Execution", "FigureS4a_CDA_Contract.pdf"),
        ("Figure S4b: Flow30 Contract Execution", "FigureS4b_Flow30_Contract.pdf"),
        ("Figure S4c: Flow60 Contract Execution", "FigureS4c_Flow60_Contract.pdf"),
        ("Figure S5a: CDA Execution Pace", "FigureS5a_CDA_Rate.pdf"),
        ("Figure S5b: Flow30 Execution Pace", "FigureS5b_Flow30_Rate.pdf"),
        ("Figure S5c: Flow60 Execution Pace", "FigureS5c_Flow60_Rate.pdf"),
        ("Figure S6: Price Markup CDF", "FigureS6_Price_Markup_CDF.pdf"),
        ("Figure S7: $U_{max}$ CDF (Early vs.\\ Late)", "FigureS7_Umax_CDF_Periods.pdf"),
        ("Figure S8: Speed Limit Usage vs.\\ Surplus", "FigureS8_Speed_vs_Surplus.pdf"),
        ("Figure S9a: Price-Range vs.\\ Excess Profit", "FigureS9a_PriceRange_vs_Profit.pdf"),
        ("Figure S9b: $U_{max}$ vs.\\ Excess Profit", "FigureS9b_Umax_vs_Profit.pdf"),
        ("Figure S9c: Price Markup vs.\\ Excess Profit", "FigureS9c_Markup_vs_Profit.pdf"),
    ]

    tex = r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{float}
\usepackage{amsmath}
\usepackage{threeparttable}
\usepackage[strings]{underscore}
\usepackage[colorlinks=true]{hyperref}

\title{Verification Document\\
\large A Laboratory Test of Flow Trading\\
Friedman, Li, L\'{o}pez Vargas}
\date{\today}

\begin{document}
\maketitle
\tableofcontents
\clearpage

%% ============================================================
\section{Main Paper Tables}
%% ============================================================
"""

    for title, fname in main_tables:
        fpath = os.path.join(tables_dir, fname)
        tex += f"\n\\subsection{{{title}}}\n"
        if os.path.exists(fpath):
            tex += f"\\input{{../tables/{fname}}}\n\\clearpage\n"
        else:
            tex += f"\\textbf{{Missing:}} \\texttt{{{fname}}}\n\\clearpage\n"

    tex += r"""
%% ============================================================
\section{Main Paper Figures}
%% ============================================================
"""

    for title, fname in main_figures:
        fpath = os.path.join(figures_dir, fname)
        tex += f"\n\\subsection{{{title}}}\n"
        if os.path.exists(fpath):
            tex += f"\\begin{{figure}}[H]\n\\centering\n\\includegraphics[width=0.9\\textwidth]{{../figures/{fname}}}\n\\end{{figure}}\n\\clearpage\n"
        else:
            tex += f"\\textbf{{Missing:}} \\texttt{{{fname}}}\n\\clearpage\n"

    tex += r"""
%% ============================================================
\section{Supplemental Appendix Tables}
%% ============================================================
"""

    for title, fname in supp_tables:
        fpath = os.path.join(tables_dir, fname)
        tex += f"\n\\subsection{{{title}}}\n"
        if os.path.exists(fpath):
            tex += f"\\input{{../tables/{fname}}}\n\\clearpage\n"
        else:
            tex += f"\\textbf{{Missing:}} \\texttt{{{fname}}}\n\\clearpage\n"

    tex += r"""
%% ============================================================
\section{Supplemental Appendix Figures}
%% ============================================================
"""

    for title, fname in supp_figures:
        fpath = os.path.join(figures_dir, fname)
        tex += f"\n\\subsection{{{title}}}\n"
        if os.path.exists(fpath):
            tex += f"\\begin{{figure}}[H]\n\\centering\n\\includegraphics[width=0.9\\textwidth]{{../figures/{fname}}}\n\\end{{figure}}\n\\clearpage\n"
        else:
            tex += f"\\textbf{{Missing:}} \\texttt{{{fname}}}\n\\clearpage\n"

    tex += r"""
\end{document}
"""

    verif_path = os.path.join(verif_dir, "all_tables_figures.tex")
    with open(verif_path, 'w') as f:
        f.write(tex)
    print(f"\nVerification document written to {verif_path}")


if __name__ == "__main__":
    # Step 1: Run default specification (5s) — generates main paper outputs
    print("\n" + "="*60)
    print("  STEP 1: Main analysis (5s intervals)")
    print("="*60)
    if not run_interval(5):
        sys.exit(1)

    # Step 2: Run 10s specification — generates Tables S2-S4
    print("\n" + "="*60)
    print("  STEP 2: Robustness check (10s intervals)")
    print("="*60)
    if not run_interval(10):
        sys.exit(1)
    copy_robustness_tables(10)

    # Step 3: Run 2s specification — generates Tables S5-S7
    print("\n" + "="*60)
    print("  STEP 3: Robustness check (2s intervals)")
    print("="*60)
    if not run_interval(2):
        sys.exit(1)
    copy_robustness_tables(2)

    # Step 4: Re-run default 5s to restore main outputs
    print("\n" + "="*60)
    print("  STEP 4: Restoring main (5s) outputs")
    print("="*60)
    if not run_interval(5):
        sys.exit(1)

    # Step 5: Generate verification document
    generate_verification_tex()

    print(f"\n{'='*60}")
    print("  All runs completed successfully.")
    print(f"  Tables:  {os.path.join(OUTPUT_DIR, 'tables')}")
    print(f"  Figures: {os.path.join(OUTPUT_DIR, 'figures')}")
    print(f"  Verify:  {os.path.join(OUTPUT_DIR, 'verification', 'all_tables_figures.tex')}")
    print(f"{'='*60}")
