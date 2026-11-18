"""Unit tests for the manual-price portfolio tracker."""

import csv
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from main import STOCK_PRICES, calculate_portfolio, run_tracker, save_portfolio_csv


class StockTrackerTests(unittest.TestCase):
    def test_hardcoded_price_list(self):
        self.assertEqual(len(STOCK_PRICES), 5)
        self.assertEqual(STOCK_PRICES["AAPL"], Decimal("180.00"))

    def test_total_investment_calculation(self):
        rows, total = calculate_portfolio({"AAPL": 2, "TSLA": 3})
        self.assertEqual(len(rows), 2)
        self.assertEqual(total, Decimal("1110.00"))

    def test_empty_portfolio(self):
        self.assertEqual(calculate_portfolio({}), ([], Decimal("0.00")))

    def test_invalid_symbol_or_quantity(self):
        for portfolio in ({"FAKE": 1}, {"AAPL": 0}, {"AAPL": -1}, {"AAPL": 1.5}):
            with self.subTest(portfolio=portfolio), self.assertRaises(ValueError):
                calculate_portfolio(portfolio)

    def test_csv_file(self):
        rows, total = calculate_portfolio({"AAPL": 2, "TSLA": 3})
        with TemporaryDirectory() as temp:
            filename = Path(temp) / "report.csv"
            save_portfolio_csv(filename, rows, total)
            with filename.open(newline="", encoding="utf-8") as stream:
                content = list(csv.reader(stream))
            self.assertEqual(content[0][0], "Stock")
            self.assertEqual(content[-1], ["TOTAL", "", "", "1110.00"])

    def test_inputs_accumulate_same_stock(self):
        answers = iter(["aapl", "2", "aapl", "3", "done", "n"])
        logs = []
        rows, total = run_tracker(lambda _: next(answers), logs.append)
        self.assertEqual(total, Decimal("900.00"))
        self.assertEqual(rows[0][1], 5)

    def test_bad_quantity_can_be_retried(self):
        answers = iter(["aapl", "-3", "aapl", "2", "done", "n"])
        logs = []
        _, total = run_tracker(lambda _: next(answers), logs.append)
        self.assertEqual(total, Decimal("360.00"))
        self.assertTrue(any("Invalid quantity" in line for line in logs))


if __name__ == "__main__":
    unittest.main()
