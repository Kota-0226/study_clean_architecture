from abc import ABC, abstractmethod


# 1. データの保持と集計に徹するクラス（SRP）
class SalesReport:

  def __init__(self, data: list[dict]):
    self.data = data

  def get_total_sales(self) -> int:
    return sum(row["amount"] for row in self.data)

  def get_rows(self) -> list[dict]:
    return self.data


# 2. 抽象基底クラス（インターフェース）
class ReportExporter(ABC):

  @abstractmethod
  def export(self, report: SalesReport) -> str:
    pass


# 3. 具象クラス：CSV出力
class CsvReportExporter(ReportExporter):

  def export(self, report: SalesReport) -> str:
    lines = ["item,amount"]
    for row in report.get_rows():
      lines.append(f"{row['item']},{row['amount']}")
    return "\n".join(lines)


# 4. 具象クラス：PDF出力
class PdfReportExporter(ReportExporter):

  def export(self, report: SalesReport) -> str:
    total = report.get_total_sales()
    # PDF生成のロジック...
    return f"--- PDF Document ---\nTotal: {total}"

# 5. 具象クラス：JSON出力
class JsonReportExporter(ReportExporter):

  def export(self, report: SalesReport) -> str:
    import json
    return json.dumps({
      "total_sales": report.get_total_sales(),
      "data": report.get_rows()
    })

if __name__ == "__main__":
    # データの準備
    data = [
        {"item": "Apple", "amount": 100},
        {"item": "Banana", "amount": 200},
    ]
    
    report = SalesReport(data)
    
    # CSV出力
    csv_exporter = CsvReportExporter()
    csv_result = csv_exporter.export(report)
    print(csv_result)
    
    # PDF出力
    pdf_exporter = PdfReportExporter()
    pdf_result = pdf_exporter.export(report)
    print(pdf_result)

    # もし、json出力を追加したい場合は...? -> ReportExporter を継承した JsonReportExporter クラスを追加するだけでOK
    json_exporter = JsonReportExporter()
    json_result = json_exporter.export(report)
    print(json_result)