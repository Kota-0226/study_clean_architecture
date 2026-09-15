import os
import sys
import unittest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from after import CsvReportExporter, PdfReportExporter, SalesReport as AfterSalesReport
from before import SalesReport as BeforeSalesReport


class TestSalesReportBefore(unittest.TestCase):
  """【Before】

  ひとつのクラスにすべての処理（集計、CSV、PDF）が集中しているため、
  実際の出力結果（末尾の改行やフォーマット）に強く依存したテストになります。
  """

  def test_generate_csv(self):
    """CSV出力が仕様どおりの文字列になること"""
    report = BeforeSalesReport([{"item": "Apple", "amount": 100}])
    result = report.generate("csv")
    # Beforeの実装に合わせた期待値（末尾の改行など）
    self.assertEqual(result, "item,amount\nApple,100\n")

  def test_generate_pdf(self):
    """PDF出力に合計金額が含まれること"""
    report = BeforeSalesReport([{"item": "Apple", "amount": 100}])
    result = report.generate("pdf")
    # Beforeの実装で返されるフォーマット（[PDF Data] Total Sales: 100）を検証
    self.assertIn("[PDF Data]", result)
    self.assertIn("Total Sales: 100", result)


class TestSalesReportAfter(unittest.TestCase):
  """【After】

  各クラスの責任が明確に分離されているため、
  計算ロジックや各エクスポーターを独立して純粋な単体テスト（Unit Test）にできます。
  """

  def test_calculate_total_sales(self):
    """売上データの合計金額を正しく計算できること"""
    data = [{"item": "Apple", "amount": 100}, {"item": "Banana", "amount": 200}]
    report = AfterSalesReport(data)

    self.assertEqual(report.get_total_sales(), 300)
    self.assertEqual(report.get_rows(), data)

  def test_csv_report_exporter(self):
    """CSV出力が仕様どおりの文字列になること"""
    mock_report = MagicMock()
    mock_report.get_rows.return_value = [
        {"item": "Apple", "amount": 100},
        {"item": "Orange", "amount": 150},
    ]

    exporter = CsvReportExporter()
    result = exporter.export(mock_report)

    expected = "item,amount\nApple,100\nOrange,150"
    self.assertEqual(result, expected)

  def test_pdf_report_exporter(self):
    """PDF出力に合計金額が含まれること"""
    mock_report = MagicMock()
    mock_report.get_total_sales.return_value = 500

    exporter = PdfReportExporter()
    result = exporter.export(mock_report)

    self.assertIn("--- PDF Document ---", result)
    self.assertIn("Total: 500", result)


if __name__ == "__main__":
  unittest.main()
