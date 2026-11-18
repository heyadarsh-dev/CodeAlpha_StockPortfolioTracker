"""Manual stock portfolio tracker for the CodeAlpha Python internship.

Prices are illustrative hardcoded amounts in USD, not real-time market quotes.
"""

import csv
from decimal import Decimal
from pathlib import Path

STOCK_PRICES = {
    "AAPL": Decimal("180.00"),
    "TSLA": Decimal("250.00"),
    "MSFT": Decimal("410.00"),
    "GOOGL": Decimal("175.00"),
    "NVDA": Decimal("120.00"),
}


def calculate_portfolio(holdings):
    """Return (per-stock rows, total) from {symbol: integer_quantity}."""
    rows = []
    total = Decimal("0.00")
    for symbol, quantity in sorted(holdings.items()):
        if symbol not in STOCK_PRICES:
            raise ValueError(f"Unknown stock symbol: {symbol}")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantities must be positive integers.")
        price = STOCK_PRICES[symbol]
        value = price * quantity
        rows.append((symbol, quantity, price, value))
        total += value
    return rows, total


def display_portfolio(rows, total, output_fn=print):
    output_fn("\nSTOCK PORTFOLIO SUMMARY (USD)")
    output_fn(f"{'Stock':<8} {'Qty':>6} {'Price':>12} {'Value':>14}")
    output_fn("-" * 44)
    for symbol, quantity, price, value in rows:
        output_fn(f"{symbol:<8} {quantity:>6} ${price:>11,.2f} ${value:>13,.2f}")
    output_fn("-" * 44)
    output_fn(f"TOTAL INVESTMENT VALUE: ${total:,.2f} USD")


def save_portfolio_csv(file_path, rows, total):
    """Write a report to a CSV file without introducing external dependencies."""
    with open(file_path, "w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["Stock", "Quantity", "Unit Price USD", "Investment Value USD"])
        for symbol, quantity, price, value in rows:
            writer.writerow([symbol, quantity, f"{price:.2f}", f"{value:.2f}"])
        writer.writerow(["TOTAL", "", "", f"{total:.2f}"])


def run_tracker(input_fn=input, output_fn=print):
    holdings = {}
    output_fn("=== CODEALPHA STOCK PORTFOLIO TRACKER ===")
    output_fn("Illustrative manually defined USD prices (not live market data):")
    for symbol, price in STOCK_PRICES.items():
        output_fn(f"  {symbol}: ${price:.2f}")
    output_fn("Type DONE as the stock symbol to calculate your portfolio.\n")

    while True:
        symbol = input_fn("Stock symbol (or DONE): ").strip().upper()
        if symbol == "DONE":
            break
        if symbol not in STOCK_PRICES:
            output_fn("Unknown symbol. Choose one of: " + ", ".join(STOCK_PRICES))
            continue
        quantity_text = input_fn(f"Quantity of {symbol}: ").strip()
        try:
            quantity = int(quantity_text)
        except ValueError:
            output_fn("Invalid quantity. Enter a positive whole number.")
            continue
        if quantity <= 0 or quantity_text.startswith("+") or not quantity_text.isdecimal():
            output_fn("Invalid quantity. Enter a positive whole number.")
            continue
        holdings[symbol] = holdings.get(symbol, 0) + quantity
        output_fn(f"Added {quantity} share(s) of {symbol}.")

    rows, total = calculate_portfolio(holdings)
    display_portfolio(rows, total, output_fn)
    if not rows:
        output_fn("No holdings entered; nothing to save.")
        return rows, total

    save_choice = input_fn("\nSave portfolio as CSV? (y/n): ").strip().lower()
    if save_choice in {"y", "yes"}:
        path_text = input_fn("Filename [portfolio_report.csv]: ").strip()
        target = Path(path_text or "portfolio_report.csv")
        if target.exists():
            confirm = input_fn(f"'{target}' exists. Overwrite? (y/n): ").strip().lower()
            if confirm not in {"y", "yes"}:
                output_fn("Save cancelled; existing file was not changed.")
                return rows, total
        try:
            save_portfolio_csv(target, rows, total)
        except OSError as exc:
            output_fn(f"Could not save the file: {exc}")
        else:
            output_fn(f"Saved: {target.resolve()}")
    return rows, total


if __name__ == "__main__":
    run_tracker()
