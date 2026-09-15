class SalesReport:

  def __init__(self, data: list[dict]):
    self.data = data

  def generate(self, format_type: str):
    # 1. データの集計・加工ロジック
    total_sales = sum(row["amount"] for row in self.data)
    summary = f"Total Sales: {total_sales}\n"

    # 2. 出力処理
    if format_type == "csv":
      output = "item,amount\n"
      for row in self.data:
        output += f"{row['item']},{row['amount']}\n"
      return output

    elif format_type == "pdf":
      # 架空のPDF描画処理
      print("Drawing PDF layout...")
      return f"[PDF Data] {summary}"


    else:
      raise ValueError(f"Unsupported format: {format_type}")


if __name__ == "__main__":
    # データの準備
    data = [
        {"item": "Apple", "amount": 100},
        {"item": "Banana", "amount": 200},
    ]

    report = SalesReport(data)

    # CSV出力
    csv_result = report.generate("csv")
    print(csv_result)

    # PDF出力
    pdf_result = report.generate("pdf")
    print(pdf_result)

    # もし、json出力を追加したい場合は...? -> SalesReport クラスに generate("json") というメソッドを追加する必要がある。generate()関数を拡張する必要があり、必要のない影響が増えてしまう