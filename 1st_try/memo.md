  # middle.py — before と after の中間段階

```python
  # 1. データの保持と集計だけに専念するクラス（ここは after と同じ）
  class SalesReport:

    def __init__(self, data: list[dict]):
      self.data = data

    def get_total_sales(self) -> int:
      return sum(row["amount"] for row in self.data)

    def get_data(self) -> list[dict]:
      return self.data


  # 2. 出力処理は SalesReport の外に出した。
  #    ただし、まだ共通の親クラス（インターフェース）は無い。
  class CsvReportExporter:

    def export(self, report: SalesReport) -> str:
      lines = ["item,amount"]
      for row in report.get_data():
        lines.append(f"{row['item']},{row['amount']}")
      return "\n".join(lines)


  class PdfReportExporter:

    def export(self, report: SalesReport) -> str:
      total = report.get_total_sales()
      return f"[PDF Data] Total Sales: {total}"


  if __name__ == "__main__":
    data = [
        {"item": "Apple", "amount": 100},
        {"item": "Banana", "amount": 200},
    ]

    report = SalesReport(data)

    print(CsvReportExporter().export(report))
    print(PdfReportExporter().export(report))

```


1. 中間処理を一回挟み、そこで実行する
2. 
3. テストを実行して、
4. さらに、「json追加」というユースケースを挟んで、前者だと「既存のコードを変更しないといけない」afterだと「既存のコードを触らない＆exporterの出力形式が変わらない」ことを言及する