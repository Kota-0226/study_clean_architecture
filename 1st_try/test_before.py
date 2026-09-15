# test_before.py のイメージ
from before import SalesReport


def test_sales_report_csv():
  report = SalesReport([{"item": "Apple", "amount": 100}])
  result = report.generate("csv")
  assert result == "item,amount\nApple,100"


def test_sales_report_pdf():
  report = SalesReport([{"item": "Apple", "amount": 100}])
  # 課題: PDFのテストを実行すると、内部の print や将来的なファイル保存処理が
  # 自動で走ってしまい、純粋な単体テストが書きにくい。
  result = report.generate("pdf")
  assert "PDF Document" in result