# CodeAlpha_StockPortfolioTracker

**CodeAlpha Task 2 - Stock Portfolio Tracker**

Console application that accepts stock symbols and positive integer quantities, looks up prices in a **hardcoded Python dictionary**, and calculates the total portfolio investment. An optional `.csv` report is supported.

**Important:** Prices are static examples in USD. This is not real-time financial information or investment advice.

## Run

```bash
python main.py
```

Enter `AAPL` (quantity 2), `TSLA` (quantity 3), then `DONE`:

```text
AAPL       2  x $180.00 = $360.00
TSLA       3  x $250.00 = $750.00
TOTAL INVESTMENT VALUE: $1,110.00 USD
```

Follow the prompts to save a CSV report. Existing files are only overwritten after confirmation.

## Hardcoded stock prices

| Symbol | Price (USD) |
|---|---:|
| AAPL | 180.00 |
| TSLA | 250.00 |
| MSFT | 410.00 |
| GOOGL | 175.00 |
| NVDA | 120.00 |

## Test

```bash
python -m unittest discover -s tests -v
```

**Key concepts:** dictionary, `input()`/`print()`, basic arithmetic, `decimal.Decimal`, CSV file handling.

**Source:** `main.py`.
