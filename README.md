# Customer Repeat Purchase Analysis

Measuring repeat purchase behaviour and identifying repeat-customer segments using **Python + SQL** on the Online Retail dataset (Dec 2010 - Dec 2011).

## Key Results
| Metric | Value |
|---|---|
| Customers analysed | 4,338 |
| **Repeat rate** (2+ orders) | **65.58%** |
| Revenue from repeat customers | 93.1% |
| Loyal customers (10+ orders) | 9% of customers, 51.3% of revenue |
| AOV one-time vs repeat | £411 vs £486 |
| AOV 1st order vs later orders | £431 vs £497 |
| Median days between orders | 22 |

## Definitions
- **Order** = unique invoice. **Repeat customer** = 2+ distinct orders. **Repeat rate** = repeat customers / total customers.
- **Segments:** One-time (1), Occasional (2-3), Regular (4-9), Loyal (10+).

## Project Structure
```
analysis.py        # cleaning + load into SQLite
run_sql.py         # runs the SQL files, exports results to data/
charts.py          # matplotlib charts
make_pdf.py        # builds the PDF report
sql/               # all SQL queries (views, repeat rate, segments, AOV, cohorts, gaps)
data/              # query outputs (CSV)
charts/            # PNG charts
report/            # PDF report
```

## How to Run
```bash
pip install pandas matplotlib reportlab pillow
# place online_retail_II.csv in the folder and update RAW path in analysis.py
python analysis.py && python run_sql.py && python charts.py && python make_pdf.py
```

## Data Cleaning
Removed rows with missing Customer ID (135,080), cancellations (8,905), zero/negative quantity or price (40) and exact duplicates (5,192). 392,693 rows kept.

## Insights
1. Two out of three customers buy again.
2. Repeat customers produce 93% of revenue.
3. 9% Loyal customers produce 51% of revenue.
4. Customers spend ~15% more on later orders than on their first.
5. Most re-orders happen within 30-60 days: the best window for follow-up campaigns.

## Tools
Python (pandas, matplotlib, reportlab), SQL (SQLite: CTEs, window functions, views).
