# README for "A Laboratory Test of Flow Trading"

by Daniel Friedman, Yilin Li, and Kristian López Vargas

*American Economic Journal: Microeconomics*, 2026

## Overview

The code in this replication package processes experimental market data from 15 groups of subjects (5 CDA, 5 Flow30, 5 Flow60) and generates all tables and figures reported in the paper. A single command (`python data.py`) runs the entire pipeline. The replicator should expect the code to run in approximately 5 minutes per specification (three specifications total for robustness checks).

## Data Availability and Provenance Statements

### Statement about Rights

- [x] I certify that the author(s) of the manuscript have legitimate access to and permission to use the data used in this manuscript.
- [x] I certify that the author(s) of the manuscript have documented permission to redistribute/publish the data contained within this replication package. Appropriate permissions are documented in the [LICENSE.txt](LICENSE.txt) file.

### License for Data

The data are licensed under a Creative Commons Attribution 4.0 International License (CC-BY 4.0). See [LICENSE.txt](LICENSE.txt) for details.

### Summary of Availability

- [x] All data **are** publicly available.

### Summary of Data Availability

| Data | Files | Location | Provided | Citation |
|------|-------|----------|----------|----------|
| Experimental market data | 660 JSON files | `data/` | Yes | Friedman, Li, and López Vargas (2026) |

### Details on Data Sources

The experimental data were collected by the authors in laboratory sessions at the University of California, Santa Cruz, using the oTree platform. The data consist of second-by-second snapshots of market state and participant state across 15 groups, each completing 22 periods (2 practice + 20 paid periods).

- **Format:** JSON files
- **Total size:** ~317 MB (660 files)
- **Organization:** `data/{treatment}{group}/{period}/1_market.json` and `1_participant.json`
  - `cda1`–`cda5`: Continuous Double Auction treatment (5 groups)
  - `flow1`–`flow5`: Flow30 treatment — max order rate 30 shares/sec (5 groups)
  - `flow6`–`flow10`: Flow60 treatment — max order rate 60 shares/sec (5 groups)

#### JSON File Descriptions

**Market data** (`1_market.json`): Second-by-second snapshots of the market state.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | Integer | Time in seconds from start of period (0–120) |
| `id_in_subsession` | Integer | Unique identifier for the subsession (period) |
| `before_transaction` | Boolean | `true` = state before transaction processing; `false` = after |
| `clearing_price` | Float/Null | Market clearing price (`null` if no clearing occurred) |
| `clearing_rate` | Float/Null | Volume (CDA) or rate (Flow) of clearing |

**Participant data** (`1_participant.json`): Second-by-second snapshots of each participant's state.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | Integer | Time in seconds |
| `id_in_subsession` | Integer | Unique identifier for the subsession |
| `id_in_group` | Integer | Participant ID within the group (1–8) |
| `participant_id` | Integer | Unique database ID for the participant |
| `before_transaction` | Boolean | `true` = state before transaction processing |
| `active_orders` | Array | List of active orders placed by the participant |
| `active_contracts` | Array | List of active contracts held |
| `executed_contracts` | Array | List of contracts executed by the participant |
| `cash` | Float | Current cash balance |
| `inventory` | Float | Current share inventory (positive or negative) |
| `rate` | Float | Current trading rate of the participant |

## Dataset List

| Data file | Source | Notes | Provided |
|-----------|--------|-------|----------|
| `data/cda{1-5}/{1-22}/1_market.json` | Authors | Market snapshots for CDA treatment | Yes |
| `data/cda{1-5}/{1-22}/1_participant.json` | Authors | Participant snapshots for CDA treatment | Yes |
| `data/flow{1-10}/{1-22}/1_market.json` | Authors | Market snapshots for Flow treatments | Yes |
| `data/flow{1-10}/{1-22}/1_participant.json` | Authors | Participant snapshots for Flow treatments | Yes |

## Computational Requirements

### Software Requirements

- Python 3.11 or higher
- A LaTeX distribution (e.g., TeX Live, MacTeX) — required for figure rendering
- The file `requirements.txt` lists all Python package dependencies. Run `pip install -r requirements.txt` to install them.

Python package dependencies:

| Package | Version |
|---------|---------|
| numpy | 2.4.2 |
| pandas | 2.3.3 |
| tabulate | 0.9.0 |
| statsmodels | 0.14.6 |
| matplotlib | 3.10.8 |
| stargazer | 0.0.7 |

### Controlled Randomness

- [x] No pseudo-random number generator is used in the analysis described here.

### Memory, Runtime, Storage Requirements

#### Summary

- Approximate time to reproduce: **< 10 minutes** per specification (three specifications for robustness). Total for all specifications: approximately 15 minutes.
- Approximate storage space required: **< 1 GB** (data: ~317 MB; generated outputs: ~150 MB per specification).

#### Computational Details

The code was last run on a MacBook Pro (Apple M1 Pro, 10 cores, 16 GB RAM) running macOS 14.7, with Python 3.11.14. The main analysis (`python data.py`) completes in approximately 5 minutes.

## Description of Programs/Code

The analysis pipeline is orchestrated by `data.py`, which sequentially executes sub-scripts in a shared namespace using `exec(open(...).read())`. The execution order matters.

| Script | Purpose |
|--------|---------|
| `data.py` | Master script — runs all sub-scripts, assembles summary/regression tables |
| `config.py` | Experiment parameters (groups, periods, CE prices/quantities, price interval) |
| `common.py` | Shared imports (numpy, pandas, statsmodels, matplotlib, stargazer) |
| `helpers.py` | DataFrame utilities (`df_explosion`, `replace_nans_with_dict`) |
| `liquidity_cda.py` | PPI liquidity measures for CDA markets |
| `liquidity_flow.py` | PPI liquidity measures for Flow markets |
| `flow_trader_period.py` | Trader-level behavior aggregation for Flow markets |
| `cda.py` | Market-level analysis and time-series figures for CDA |
| `flow.py` | Market-level analysis and time-series figures for Flow |
| `cda_individual.py` | Trader-level analysis for CDA |
| `flow_individual.py` | Trader-level analysis for Flow |
| `new_plots.py` | Cross-treatment comparison visualizations |
| `run_all.py` | Automation script — runs all three robustness specifications |

### License for Code

The code is licensed under a Modified BSD License. See [LICENSE.txt](LICENSE.txt) for details.

## Instructions to Replicators

### Setup

1. Install Python 3.11 or higher.
2. Install a LaTeX distribution (e.g., TeX Live, MacTeX).
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   # or: venv\Scripts\activate  # On Windows
   ```
4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Main Analysis (default specification)

```bash
python data.py
```

This generates all tables in `tables/` (.tex and .csv) and all figures in `figures/` (.png) using the default price interval size of 5 seconds.

### Running All Robustness Specifications

```bash
python run_all.py
```

This runs the analysis three times with `price_interval_size` set to 5, 2, and 10 seconds, saving outputs to `tables_5s/`, `tables_2s/`, `tables_10s/` and `figures_5s/`, `figures_2s/`, `figures_10s/` respectively.

Alternatively, to run a single robustness specification manually:

1. Open `config.py` and change `price_interval_size` to `2` or `10`.
2. Run `python data.py`.
3. Rename the output directories (e.g., `tables/` → `tables_2s/`).

## List of Tables and Programs

The provided code reproduces:

- [x] All tables and figures in the paper (except Figures 1–3 and Figures S10–S16, which are not code-generated).

Figures 1–3 in the main paper are not generated by code: Figure 1 is a screenshot of the experimental interface, Figure 2 is a theoretical diagram, and Figure 3 shows contract configurations. Figures S10–S16 in the Supplemental Appendix are screenshots of experimental instructions.

### Main Paper

| Figure/Table | Program | Output file | Note |
|---|---|---|---|
| Table 1 | `data.py` | `tables/summary_trader_short_table.tex`, `tables/summary_trader_all20_table.tex` | Summary Statistics: Traders' Behavior |
| Table 2 | `data.py` | `tables/summary_market_short_table.tex`, `tables/summary_market_all20_table.tex` | Summary Statistics: Market Performance |
| Table 3 | `data.py` | `tables/trader_behavior_regression_table.tex` | Regression Results: Trader Behavior Metrics |
| Table 4 | `data.py` | `tables/price_regression_table.tex` | Regression Results: Price Volatility and Liquidity |
| Table 5 | `data.py` | `tables/trade_volume_regression_table.tex` | Regression Results: Volume |
| Table 6 | `data.py` | `tables/efficiency_regression_table.tex` | Regression Results: Efficiency and Buyer-Seller Disparity |
| Figure 4a | `cda.py` | `figures/cda_price_single.png` | Transaction prices over time (CDA) |
| Figure 4b | `flow.py` | `figures/flow30_price_single.png` | Transaction prices over time (Flow30) |
| Figure 4c | `flow.py` | `figures/flow60_price_single.png` | Transaction prices over time (Flow60) |
| Figure 5a | `new_plots.py` | `figures/mean_quantity.png` | Trade volume vs. period |
| Figure 5b | `new_plots.py` | `figures/mean_surplus.png` | Realized surplus vs. period |
| Figure 6 | `data.py` | `figures/group_gross_profits_cdf.png` | Profit distribution (CDF of normalized gross profits) |
| Figure 7 | `flow_trader_period.py` | `figures/flow_max_rate_cdf_all20.png` | CDF of U_max |
| Figure 8 | `data.py` | `figures/cumsum_compress_all.png` | Average cumulative executed fraction of contract quantity |
| Figure 9 | `flow_trader_period.py` | `figures/flow_order_price_diff_cdf_all20.png` | CDF of price-range width (p_H - p_L) |

### Supplemental Appendix

| Figure/Table | Program | Output file | Note |
|---|---|---|---|
| Table S1 | `data.py` | (console output) | Spearman Correlations Between Behavioral Variables |
| Table S2 | `run_all.py` | `tables_10s/summary_market_short_table.tex` | Summary Statistics: Market Performance (10s intervals) |
| Table S3 | `run_all.py` | `tables_10s/price_regression_table.tex` | Regression: Price Volatility (10s intervals) |
| Table S4 | `run_all.py` | `tables_10s/efficiency_regression_table.tex` | Regression: Efficiency and Buyer-Seller Disparity (10s intervals) |
| Table S5 | `run_all.py` | `tables_2s/summary_market_short_table.tex` | Summary Statistics: Market Performance (2s intervals) |
| Table S6 | `run_all.py` | `tables_2s/price_regression_table.tex` | Regression: Price Volatility (2s intervals) |
| Table S7 | `run_all.py` | `tables_2s/efficiency_regression_table.tex` | Regression: Efficiency and Buyer-Seller Disparity (2s intervals) |
| Table S8 | `data.py` | (console output) | Summary Statistics with Unweighted Prices |
| Figure S1a | `cda.py` | `figures/cda_price.png` | Transaction prices over time — CDA (all groups) |
| Figure S1b | `flow.py` | `figures/flow30_price.png` | Transaction prices over time — Flow30 (all groups) |
| Figure S1c | `flow.py` | `figures/flow60_price.png` | Transaction prices over time — Flow60 (all groups) |
| Figure S2a | `cda.py` | `figures/cda_quantity.png` | CDA trade volume |
| Figure S2b | `cda.py` | `figures/cda_surplus.png` | CDA realized surplus |
| Figure S2c | `flow.py` | `figures/flow30_quantity.png` | Flow30 trade volume |
| Figure S2d | `flow.py` | `figures/flow30_surplus.png` | Flow30 realized surplus |
| Figure S2e | `flow.py` | `figures/flow60_quantity.png` | Flow60 trade volume |
| Figure S2f | `flow.py` | `figures/flow60_surplus.png` | Flow60 realized surplus |
| Figure S3 | `data.py` | `figures/group_gross_profits_last10_cdf.png` | Profit distribution (last 10 periods) |
| Figure S4a | `cda.py` | `figures/cda_contract.png` | Percentage of contract quantity executed (CDA) |
| Figure S4b | `flow.py` | `figures/flow30_contract.png` | Percentage of contract quantity executed (Flow30) |
| Figure S4c | `flow.py` | `figures/flow60_contract.png` | Percentage of contract quantity executed (Flow60) |
| Figure S5a | `cda.py` | `figures/cda_rate.png` | Mean execution pace (CDA) |
| Figure S5b | `flow.py` | `figures/flow30_rate.png` | Mean execution pace (Flow30) |
| Figure S5c | `flow.py` | `figures/flow60_rate.png` | Mean execution pace (Flow60) |
| Figure S6 | `flow_trader_period.py` | `figures/flow_price_dev_from_contract_cdf_all20.png` | Price Markup Distributions |
| Figure S7 | `flow_trader_period.py` | `figures/flow_max_rate_cdf_all.png` | CDF of U_max (early vs. late periods) |
| Figure S8 | `flow_trader_period.py` | `figures/flow_max_rate_percent_vs_realized_surplus.png` | Speed limit usage vs. realized surplus |
| Figure S9a | `flow_trader_period.py` | `figures/flow_pH-pL_vs_excess_profit.png` | Price-range width vs. excess profit |
| Figure S9b | `flow_trader_period.py` | `figures/flow_max_rate_percent_vs_excess_profit.png` | U_max/U_max^limit vs. excess profit |
| Figure S9c | `flow_trader_period.py` | `figures/flow_price_dev_from_contract_vs_excess_profit.png` | Price markup vs. excess profit |

### Intermediate Data Files

The pipeline produces the following intermediate CSV files in `tables/`, used internally for aggregation and regressions:

| File | Description |
|------|-------------|
| `data_interval.csv` | Interval-level aggregated data |
| `data_period.csv` | Period-level aggregated data |
| `data_second.csv` | Second-by-second aggregated data |
| `data_profits.csv` | Profit data |
| `data_liquidity.csv` | PPI liquidity measures |
| `cda_trader_period.csv` | CDA trader-by-period data |
| `flow_trader_period.csv` | Flow trader-by-period data |
| `regress_data_direction.csv` | Regression data by buy/sell direction |

## References

Friedman, Daniel, Yilin Li, and Kristian López Vargas. 2026. "A Laboratory Test of Flow Trading." *American Economic Journal: Microeconomics*.
