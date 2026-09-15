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

    def export(self, report: SalesReport) -> str: # SalesReport を引数に取るように変更
        lines = ["item,amount"]
        for row in report.get_data(): # self.dataになっていたはずなので、get_data()を新たに定義して、ここではそれを呼ぶようにする。
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

    # CSV出力
    print("=== CSV Export ===")
    csv_exporter  = CsvReportExporter()
    csv_result = csv_exporter.export(report)
    print(csv_result)
    
    # PDF出力
    print("=== PDF Export ===")
    pdf_exporter = PdfReportExporter()
    pdf_result = pdf_exporter.export(report)
    print(pdf_result)